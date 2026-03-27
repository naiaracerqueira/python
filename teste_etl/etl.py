from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructType, StructField, ArrayType, DoubleType
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ReadParquet").getOrCreate()

def read_file():
    try:
        df = spark.read.parquet("python/teste_etl/dados_raw.parquet")
        return df
    except Exception as e:
        print(f"Erro durante a leitura do arquivo: {e}")
        raise

def transform_data(df):
    try:
        schema = StructType([
            StructField("level1_A", StructType([
                StructField("level2_A1", StructType([
                    StructField("level3_A1", StructType([
                        StructField("level4_A1", ArrayType(
                            StructType([
                                StructField("level5_A", StringType())
                            ])
                        )),
                        StructField("level4_A2", ArrayType(
                            StructType([
                                StructField("level5_A1", StringType()),
                                StructField("level5_A2", StringType()),
                                StructField("level5_A3", StringType())
                            ])
                        ))
                    ]))
                ])),
                StructField("level2_A2", StructType([
                    StructField("level3_A3", StructType([
                        StructField("level4_A3", StructType([
                            StructField("level5_A4", StructType([
                                StructField("level6_A1", DoubleType())
                            ]))
                        ]))
                    ]))
                ]))
            ])),
            StructField("level1_B", StructType([
                StructField("level2_B1", StructType([
                    StructField("level3_B1", StringType()),
                    StructField("level3_B2", StringType()),
                    StructField("level3_B3", StringType()),
                    StructField("level3_B4", StringType()),
                    StructField("level3_B5", StringType()),
                    StructField("level3_B6", StringType())
                ])),
                StructField("level2_B2", StructType([
                    StructField("level3_B7", StringType()),
                    StructField("level3_B8", StringType()),
                    StructField("level3_B9", StringType()),
                    StructField("level3_B10", StringType()),
                    StructField("level3_B11", StructType([
                        StructField("level4_B1", StringType())
                    ])),
                    StructField("level3_B12", StructType([
                        StructField("level4_B2", StringType())
                    ]))
                ])),
                StructField("level1_C", StructType([
                    StructField("level2_C1", StringType())
                ]))
            ]))
        ])
        df = df.withColumn(
                "parsed_json", F.from_json(F.col("coluna_json"), schema)
            ).drop("coluna_json"
            ).select(
                F.col("id1"),
                F.col("id2"),
                F.col("id3"),
                F.col("parsed_json.level1_A.level2_A1.level3_A1.level4_A1")[0]["level5_A"].alias("level4_A1"),
                F.col("parsed_json.level1_A.level2_A1.level3_A1.level4_A2")[0]["level5_A1"].alias("level5_A1"),
                F.col("parsed_json.level1_A.level2_A1.level3_A1.level4_A2")[0]["level5_A2"].alias("level5_A2"),
                F.col("parsed_json.level1_A.level2_A1.level3_A1.level4_A2")[0]["level5_A3"].alias("level5_A3"),
                F.col("parsed_json.level1_A.level2_A2.level3_A3.level4_A3.level5_A4.level6_A1").alias("level6_A1"),
                F.col("parsed_json.level1_B.level2_B1.level3_B1").alias("level3_B1"),
                F.col("parsed_json.level1_B.level2_B1.level3_B2").alias("level3_B2"),
                F.col("parsed_json.level1_B.level2_B1.level3_B3").alias("level3_B3"),
                F.col("parsed_json.level1_B.level2_B1.level3_B4").alias("level3_B4"),
                F.col("parsed_json.level1_B.level2_B1.level3_B5").alias("level3_B5"),
                F.col("parsed_json.level1_B.level2_B1.level3_B6").alias("level3_B6"),
                F.col("parsed_json.level1_B.level2_B2.level3_B7").alias("level3_B7"),
                F.split(F.split(F.col("parsed_json.level1_B.level2_B2.level3_B8"), ";").getItem(5), "=").getItem(1).alias("level3_B8"),
                F.to_timestamp(F.col("parsed_json.level1_B.level2_B2.level3_B9")).alias("level3_B9"),
                F.col("parsed_json.level1_B.level2_B2.level3_B10").alias("level3_B10"),
                F.col("parsed_json.level1_B.level2_B2.level3_B11.level4_B1").alias("level4_B1"),
                F.col("parsed_json.level1_B.level2_B2.level3_B12.level4_B2").alias("level4_B2"),
                F.col("parsed_json.level1_B.level1_C.level2_C1").alias("level2_C1"),
                F.col('data')
            ).dropDuplicates(
            )
        df.show(1, truncate=False)
        return df
    except Exception as e:
        print(f"Erro durante a transformação: {e}")
        raise

def parse_date(col):
    try:
        formats = ['yyyy-MM-dd', 'dd-MM-yyyy']
        parsed_date = F.coalesce(*[F.to_date(col, fmt) for fmt in formats])
        return parsed_date
    except Exception as e:
        print(f"Erro durante o parse da data: {e}")
        raise

def save_data(df):
    try:
        df.write.parquet("python/teste_etl/silver", mode="overwrite")
    except Exception as e:
        print(f"Erro durante a escrita: {e}")
        raise

if __name__ == "__main__":
    df = read_file()
    df = transform_data(df)
    save_data(df)