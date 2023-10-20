import time
from google.cloud import bigquery

client = bigquery.Client()

job_config = bigquery.LoadJobConfig(
    source_format = bigquery.SourceFormat.CSV,
    skip_leading_rows = 1,
    autodetect = True,
)

#Siempre cambiar el nomrbre
tableName = "Sala_1_Servir_resoluciones"
table_id = f"xenon-world-399922.Maycol.{tableName}"

with open(r'primera-sala-Resolution-CSV.csv',"rb") as source_file:
    job = client.load_table_from_file(source_file,table_id,job_config=job_config)

while job.state != 'DONE':
    time.sleep(2)
    job.reload()
    print(job.state)

print(job.result())

table = client.get_table(table_id)
print("Load {} rows and {} columns to {}".format(
    table.num_rows, len(table.schema),table_id
    )
)