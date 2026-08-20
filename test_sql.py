# File used to ensure that SAS token can successfully connect to SQL server and retrieve data

import pyodbc

SYNAPSE_SERVER = "" # YOUR_WORKSPACE_NAME-ondemand.sql.azuresynapse.net
DATABASE = "" # YOUR_DATABASE_NAME
SQL_USER = "" # YOUR_SQL_USERNAME
SQL_PASS = "" # YOUR_SQL_PASSWORD

print("[*] Testing SQL Authentication and SAS Token Credential...")
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    f"Server=tcp:{SYNAPSE_SERVER},1433;"
    f"Database={DATABASE};"
    f"Uid={SQL_USER};"
    f"Pwd={SQL_PASS};"
    "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

try:
    # Test login
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("Successfully logged into Synapse Serverless SQL.")
    
    # Test the SAS token binding and View execution
    print("Querying the view to verify Storage Account access...")
    cursor.execute("SELECT TOP 5 * FROM vw_NetworkTraffic")
    
    rows = cursor.fetchall()
    
    print(f"Success - the SAS token works. Retrieved {len(rows)} records:\n")
    for row in rows:
        print(row)
        
    conn.close()
    
except Exception as e:
    print(f"\nERROR ENCOUNTERED:\n{e}")