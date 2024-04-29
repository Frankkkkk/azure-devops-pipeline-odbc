import struct
import pyodbc
import os

server = "MY-SERVER.database.windows.net"
database = "MY-DATABASE"
DRIVER = '{ODBC Driver 17 for SQL Server}'
CONNECTION_STRING = f"Driver={DRIVER};Server={server};Database={database}"


# is there a better way in 2023?
def pyodbc_attrs(access_token: str) -> dict:
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    token_bytes = bytes(access_token, 'utf-8')
    exp_token = b''
    for i in token_bytes:
        exp_token += bytes({i}) + bytes(1)
    return {SQL_COPT_SS_ACCESS_TOKEN: struct.pack("=i", len(exp_token)) + exp_token}


def get_conn() -> pyodbc.Connection:
    access_token = os.environ['AZURE_DB_TOKEN']
    return pyodbc.connect(CONNECTION_STRING, attrs_before=pyodbc_attrs(access_token))

conn = get_conn()

cursor = conn.cursor()
cursor.execute("SELECT @@version")
print(cursor.fetchall())
1/0
