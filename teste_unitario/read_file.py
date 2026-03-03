from pyspark.sql import SparkSession

def conn_spark():
    return SparkSession.builder.getOrCreate()

def read_file(path, spark):
    return spark.read.csv(path)


spark = conn_spark()
path = 'file.csv'
df = read_file(path, spark)
# df.show()
