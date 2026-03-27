# python -m test -v
import pytest
from unittest.mock import patch
from pyspark.sql import SparkSession
from etl import (
    read_file,
    transform_data,
    save_data
)

@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder.master("local[1]").appName("TesteETL").getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def mock_data():
    data=[{'id1': 'SESS0001', 'id2': 'PIX', 'id3': 'CREDIT', 'data': '2026-10-19', 'coluna_json': '{"level1_A": {"level2_A1": {"level3_A1": {"level4_A1": [{"level5_A": "GEO_OK"}], "level4_A2": [{"level5_A1": "DISCONNECTED", "level5_A2": "5G", "level5_A3": "MOBILE"}]}}, "level2_A2": {"level3_A3": {"level4_A3": {"level5_A4": {"level6_A1": 9049.68}}}}}, "level1_B": {"level2_B1": {"level3_B1": "49737731047", "level3_B2": "1978", "level3_B3": "359952", "level3_B4": "3", "level3_B5": "PRIVATE", "level3_B6": "PR3"}, "level2_B2": {"level3_B7": "CIAM-000001-4786", "level3_B8": "Mozilla/5.0;Mobile;App;Android;version=12;appId=br.com.banco.app/10.7.0", "level3_B9": "2024-02-08T18:12:00", "level3_B10": "SEG", "level3_B11": {"level4_B1": "S"}, "level3_B12": {"level4_B2": "APP_ANDROID"}}, "level1_C": {"level2_C1": "PRESENCIAL"}}}'}]
    return spark.createDataFrame(data, schema="id1 STRING, id2 STRING, id3 STRING, data STRING, coluna_json STRUCT<level1_A:STRUCT<level2_A1:STRUCT<level3_A1:STRUCT<level4_A1:ARRAY<STRUCT<level5_A:STRING>>>>>>")


def test_etl_process(mock_data):
    with patch('etl.spark.read.parquet', return_value=mock_data):
        df = read_file()
        assert df.count() == 1
        transformed_df = transform_data(df)
        assert transformed_df.count() == 1
        assert 'level5_A3' in transformed_df.columns
        save_data(transformed_df)
        print('fim do teste')