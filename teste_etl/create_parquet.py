"""
Gera um arquivo Parquet com a coluna coluna_json contendo
o JSON cru que precisa ser explodido via from_json no Spark.
"""

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
import random
from datetime import datetime

def gerar_json_raw(i):
    return json.dumps({
        "level1_A": {
            "level2_A1": {
                "level3_A1": {
                    "level4_A1": [
                        {"level5_A": random.choice(["GEO_OK", "GEO_FAIL", "GEO_UNKNOWN"])}
                    ],
                    "level4_A2": [
                        {
                            "level5_A1": random.choice(["CONNECTED", "DISCONNECTED"]),
                            "level5_A2": random.choice(["WIFI", "4G", "5G"]),
                            "level5_A3": random.choice(["MOBILE", "FIXED"])
                        }
                    ]
                }
            },
            "level2_A2": {
                "level3_A3": {
                    "level4_A3": {
                        "level5_A4": {
                            "level6_A1": round(random.uniform(1.0, 50000.0), 2)
                        }
                    }
                }
            }
        },
        "level1_B": {
            "level2_B1": {
                "level3_B1": f"{random.randint(10000000000, 99999999999)}",
                "level3_B2": f"{random.randint(1000, 9999)}",
                "level3_B3": f"{random.randint(100000, 999999)}",
                "level3_B4": str(random.randint(0, 9)),
                "level3_B5": random.choice(["VAREJO", "PRIME", "PRIVATE"]),
                "level3_B6": random.choice(["V1", "P2", "PR3"])
            },
            "level2_B2": {
                "level3_B7":  f"CIAM-{i:06d}-{random.randint(1000,9999)}",
                "level3_B8":  f"Mozilla/5.0;Mobile;App;Android;version=12;appId=br.com.banco.app/{random.randint(10,15)}.{random.randint(0,9)}.0",
                "level3_B9":  datetime(2024, random.randint(1,12), random.randint(1,28),
                                       random.randint(0,23), random.randint(0,59)).isoformat(),
                "level3_B10": random.choice(["SEG","TER","QUA","QUI","SEX","SAB","DOM"]),
                "level3_B11": {
                    "level4_B1": random.choice(["S", "N"])
                },
                "level3_B12": {
                    "level4_B2": random.choice(["APP_IOS", "APP_ANDROID"])
                }
            },
            "level1_C": {
                "level2_C1": random.choice(["DIGITAL", "PRESENCIAL"])
            }
        }
    })

registros = [
    {
        "id1": f"SESS{i:04d}",
        "id2": random.choice(["PIX", "TED", "DOC", "BOLETO"]),
        "id3": random.choice(["DEBIT", "CREDIT", "TRANSFER"]),
        "data": random.choice([
            datetime(2026, random.randint(1,12), random.randint(1,28)).strftime("%Y-%m-%d"),
            datetime(2026, random.randint(1,12), random.randint(1,28)).strftime("%d/%m/%Y")
        ]),
        "coluna_json": gerar_json_raw(i),
    }
    for i in range(1, 101)
]

df = pd.DataFrame(registros)

schema = pa.schema([
    ("id1", pa.string()),
    ("id2", pa.string()),
    ("id3", pa.string()),
    ("data", pa.string()),
    ("coluna_json", pa.string()),
])

table = pa.Table.from_pandas(df, schema=schema, preserve_index=False)
pq.write_table(table, "python/teste_etl/dados_raw.parquet")

print("Arquivo 'dados_raw.parquet' gerado com sucesso!")
print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")
print()
print("Exemplo do JSON na coluna coluna_json:")
print(json.dumps(json.loads(df['coluna_json'][0]), indent=2))