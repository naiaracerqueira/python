from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StringType, StructType
from pyspark.sql import functions as F

spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

data = [('James', '45'), ('Naiara', '36'), ('Pedro', '30')]
schema = StructType([
    StructField('_c0', StringType(), True),
    StructField('_c1', StringType(), True)
])
df = spark.createDataFrame(data, schema)
df.show()
