import pandas as pd
import sqlite3
import logging
from ingestion_db import ingest_db

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s-%(levelname)s-%(message)s",
    filemode="a"
)

def create_vendor_summary(conn):
    """This function merges different tables to get the overall vendor summary."""
    vendor_sales_summary = pd.read_sql_query("""
    WITH freight_summary AS (
        SELECT 
            VendorNumber,
            SUM(freight) AS freight_cost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),

    purchase_summary AS (
        SELECT 
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            SUM(p.Quantity) AS total_purchase_quantity,
            SUM(p.Dollars) AS total_purchase_dollars,
            pp.PurchasePrice,
            pp.volume,
            pp.price AS actual_price
        FROM purchases AS p
        JOIN purchase_prices AS pp 
            ON p.Brand = pp.Brand
        GROUP BY p.VendorNumber, p.VendorName, p.Brand
    ),

    sales_summary AS (
        SELECT 
            VendorNo,
            Brand,
            SUM(salesDollars) AS total_sales_dollars,
            SUM(SalesPrice) AS total_sale_price,
            SUM(SalesQuantity) AS total_sales_quantity,
            SUM(ExciseTax) AS total_excise_tax
        FROM sales
        GROUP BY VendorNo, Brand
    )

    SELECT 
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.total_purchase_quantity,
        ps.total_purchase_dollars,
        ps.PurchasePrice,
        ps.volume,
        ps.actual_price,
        ss.total_sales_dollars,
        ss.total_sale_price,
        ss.total_sales_quantity,
        ss.total_excise_tax,
        fs.freight_cost
    FROM purchase_summary ps
    LEFT JOIN sales_summary ss 
        ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
    LEFT JOIN freight_summary fs 
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.total_purchase_dollars DESC;
    """, conn)
    return vendor_sales_summary

def clean_data(df):
    """This function cleans the data and adds new columns for analysis."""
    # Ensure required columns exist
    required_columns = ['volume', 'VendorName', 'Description', 'total_sales_dollars', 
                       'total_purchase_dollars', 'total_sales_quantity', 'total_purchase_quantity']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing required columns: {missing_columns}")
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Change datatype to float
    df['volume'] = df['volume'].astype('float64')

    # Fill missing values with 0
    df.fillna(0, inplace=True)

    # Remove white spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # Create new columns
    df['GrossProfit'] = df['total_sales_dollars'] - df['total_purchase_dollars']
    
    # Calculate ProfitMargin, avoiding division by zero
    df['ProfitMargin'] = (df['GrossProfit'] / df['total_sales_dollars'] * 100).where(
        df['total_sales_dollars'] != 0, 0)
    
    # Calculate StockTurnover, avoiding division by zero
    df['StockTurnover'] = (df['total_sales_quantity'] / df['total_purchase_quantity']).where(
        df['total_purchase_quantity'] != 0, 0)
    
    # Calculate SalesPurchaseRatio, avoiding division by zero
    df['SalesPurchaseRatio'] = (df['total_sales_dollars'] / df['total_purchase_dollars']).where(
        df['total_purchase_dollars'] != 0, 0)

    return df

if __name__ == '__main__':
    # Create database connection
    conn = sqlite3.connect('inventory.db')

    logging.info('Creating vendor summary table')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning the data...')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting data...')
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    logging.info('Ingestion complete')

    # Close the connection
    conn.close()