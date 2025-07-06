from sqlalchemy import create_engine
import pandas as pd

#Source: MySQL connection (replace with your own password if needed)
mysql_engine = create_engine('mysql+pymysql://root:pakistan%40321%24@localhost/project_manager')

# Destination: SQLite file
sqlite_engine = create_engine('sqlite:///project_manager.db')

# Table names from your models (use lowercase)
tables = ['project_user', 'project', 'task', 'user', 'role']

for table in tables:
    print(f"🔄 Migrating table: {table}")
    try:
        df = pd.read_sql_table(table, mysql_engine)
        df.to_sql(table, sqlite_engine, if_exists='replace', index=False)
        print(f"Migrated {table} to SQLite")
    except Exception as e:
        print(f"Error migrating {table}: {e}")
