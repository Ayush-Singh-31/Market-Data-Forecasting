import os
import pandas as pd
import pyarrow.parquet as pq

def getParquet(path:str)->pd.DataFrame:
    table = pq.read_table(path)
    return table.to_pandas()

def loadID()->pd.DataFrame:
    id0 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=0/part-0.parquet")
    id1 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=1/part-0.parquet")
    id2 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=2/part-0.parquet")
    id3 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=3/part-0.parquet")
    id4 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=4/part-0.parquet")
    id5 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=5/part-0.parquet")
    id6 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=6/part-0.parquet")
    id7 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=7/part-0.parquet")
    id8 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=8/part-0.parquet")
    id9 = getParquet("Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=9/part-0.parquet")
    df = pd.concat([id0, id1, id2, id3, id4, id5, id6, id7, id8, id9], axis=0, ignore_index=True)
    return df

def saveID(df:pd.DataFrame)->None:
    df.to_csv("Data/id.csv")
    return

if __name__ == "__main__":
    if not os.path.exists("Data/id.csv"):
        id = loadID()
        saveID(id)