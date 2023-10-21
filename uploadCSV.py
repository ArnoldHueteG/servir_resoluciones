import time
from google.cloud import bigquery

def uploadCsv(fileNameCsv,table_id,tableName):
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        source_format = bigquery.SourceFormat.CSV,
        skip_leading_rows = 1,
        autodetect = True,
    )
    with open(fileNameCsv, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    table = client.get_table(table_id)
    print("Load {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema),table_id
        )
    )

csvName = 'Nombre.csv'
tableName = "NombreTablaDeEjemplo"
table_id = f"xenon-world-399922.Maycol.{tableName}"

uploadCsv(csvName,tableName,table_id)

