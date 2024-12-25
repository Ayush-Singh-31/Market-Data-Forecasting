import dask.dataframe as dd

def loadID() -> dd.DataFrame:
    filePaths = ["Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=0/part-0.parquet",
                  "Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=1/part-0.parquet",
                  "Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=2/part-0.parquet",
                  "Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=3/part-0.parquet",
                  "Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=4/part-0.parquet",
                  "Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=5/part-0.parquet",
                  "Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=6/part-0.parquet",
                  "Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=7/part-0.parquet",
                  "Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=8/part-0.parquet",
                  "Data/jane-street-real-time-market-data-forecasting/train.parquet/partition_id=9/part-0.parquet"
                  ]
    return dd.read_parquet(filePaths)

def clean(df: dd.DataFrame) -> dd.DataFrame:
    # Drop rows with NaN values of Columns with NAN values less than 3%
    columns = ['feature_08', 'feature_15', 'feature_16', 'feature_17', 'feature_18', 'feature_19', 
               'feature_32', 'feature_33', 'feature_37', 'feature_40', 'feature_41', 'feature_44', 
               'feature_45', 'feature_46', 'feature_47', 'feature_51', 'feature_52', 'feature_54', 
               'feature_55', 'feature_56', 'feature_57', 'feature_58', 'feature_62', 'feature_63', 
               'feature_64', 'feature_66', 'feature_73', 'feature_74', 'feature_75', 'feature_76', 
               'feature_77', 'feature_78']
    df = df.dropna(subset=columns)
    return df

def NaNCorrelation(df: dd.DataFrame) -> dd.DataFrame:
    # Finding Correlation between features with NaN values greater than 3%
    columns = ['feature_00','feature_01','feature_02','feature_03','feature_04','feature_21','feature_26','feature_27','feature_31','feature_39','feature_42','feature_50','feature_53']
    print(df[columns].corr().compute())

    # 0-2, 0-3, 2-3, 21-31 are highly correlated and 39-50, 42-53 are Moderately correlated
    df['feature_0_2_3'] = (df['feature_00'] + df['feature_02'] + df['feature_03']) / 3
    df['feature_21_31'] = (df['feature_21'] + df['feature_31']) / 2
    df = df.drop(['feature_00','feature_02','feature_03','feature_21','feature_31'], axis=1)

    columns = ['feature_0_2_3','feature_21_31']
    df = df.dropna(subset=columns)

    return df

def correlationMatrix(df: dd.DataFrame) -> dd.DataFrame:
    print(df.corr().compute())


if __name__ == "__main__":
    id = loadID()
    id = clean(id)
    id = NaNCorrelation(id)
    correlationMatrix(id)

