import pandas as pd 
import os 
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
   filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s-%(levelname)s-%(message)s",
    filemode="a"
    
)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df,table_name,engine):
    '''this function will ingest the dataframe into database table'''
    df.to_sql(table_name,con=engine, if_exists = 'replace' , index = False)

def load_raw_data():
    '''this function load the csv as a dataframe and ingestion into db '''
    start = time.time()
    for file in os.listdir(r"C:\PROJECT_2025\powerbi2025\Vendor Performance Data Analytics\dataset\data\data"):
         if '.csv' in file:
           df = pd.read_csv(r'C:\PROJECT_2025\powerbi2025\Vendor Performance Data Analytics\dataset\data\data/'+file)
           print(df.shape)
           logging.info(f'ingesting{file} in db')
           ingest_db(df,file[:-4],engine)
    end = time.time()
    total_time = (end-start)/60
    
    logging.info('-----------------------ingestion complete-------------------------------')
    logging.info('ingestion complete')
    logging.info(f'Total time taken :{total_time} minutes')

if __name__ == "__main__":
    load_raw_data()