#System Modules
import os
import sys
#sys.path.append(os.path.abspath(os.path.join("../..")))
sys.path.append(".")
#sys.path.append(os.path.abspath(os.path.join('..')))
#sys.path.insert(0, './pages')
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error

def DBConnect(dbName=None):
    conn = mysql.connect(host='localhost', user='root', password='mommissedu',
                         database=dbName, buffered=True)
    cur = conn.cursor()
    return conn, cur

def emojiDB(dbName: str) -> None:
    conn, cur = DBConnect(dbName)
    dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
    cur.execute(dbQuery)
    conn.commit()

def createDB(dbName: str) -> None:
    conn, cur = DBConnect()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};") # creating database
    conn.commit()
    cur.close()

def createTables(dbName: str) -> None:
    conn, cur = DBConnect(dbName)
    sqlFile = 'schema.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')

    for command in sqlCommands:
        try:
            res = cur.execute(command)
        except Exception as ex:
            print("Command skipped: ", command)
            print(ex)
    conn.commit()
    cur.close()

    return

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    #cols_2_drop = ['original_text']
    try:
        #df = df.drop(columns=cols_2_drop, axis=1)
        for col in df.columns:
            if(df[col].isnull().sum()):
                df[col] = df[col].fillna(df[col].mode()[0])
    except KeyError as e:
        print("Error:", e)

    return df


def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
    conn, cur = DBConnect(dbName)

    df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO Telecom_db.TelecomDataTable (Bearer Id, Dur. (ms), IMSI, MSISDN/Number, IMEI, Last Location Name, Avg RTT DL (ms), Avg RTT UL (ms), Avg Bearer TP DL (kbps), Avg Bearer TP UL (kbps), TCP DL Retrans. Vol (Bytes), TCP UL Retrans. Vol (Bytes), HTTP DL (Bytes), HTTP UL (Bytes), Activity Duration DL (ms), Activity Duration UL (ms), Dur. (ms).1, Handset Manufacturer, Handset Type, Social Media DL (Bytes), Social Media UL (Bytes), Google DL (Bytes), Google UL (Bytes), Email DL (Bytes), Email UL (Bytes), Youtube DL (Bytes), Youtube UL (Bytes), Netflix DL (Bytes), Netflix UL (Bytes), Gaming DL (Bytes), Gaming UL (Bytes), Other DL (Bytes), Other UL (Bytes), Total UL (Bytes), Total DL (Bytes)) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
             %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        #print("sucessfully")
        data = (row[0], row[1], row[2], row[3], row[4], (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                row[12], row[13], row[14], row[15], row[16], (row[17]), (row[18]), row[19], row[20], row[21], row[22],
                row[23], row[24],row[25], row[26], row[27], row[28], row[29], row[30],
                row[31], row[32], row[33], row[34])

        try:
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            # Commit your changes in the database
            print ("error ha")
            conn.commit()
            #print("Data Inserted Successfully")
        except Exception as e:
            conn.rollback()
            print("Error: ", e)
    return

def db_execute_fetch(*args, many=False, tablename='', rdf=True, **kwargs) -> pd.DataFrame:

    connection, cursor1 = DBConnect(**kwargs)
    if many:
        cursor1.executemany(*args)
    else:
        cursor1.execute(*args)

    # get column names
    field_names = [i[0] for i in cursor1.description]

    # get column values
    res = cursor1.fetchall()

    # get row count and show info
    nrow = cursor1.rowcount
    if tablename:
        print(f"{nrow} recrods fetched from {tablename} table")

    cursor1.close()
    connection.close()

    # return result
    if rdf:
        return pd.DataFrame(res, columns=field_names)
    else:
        return res
if __name__ == "__main__":
    #print("sucessfully")
    dbName='Tele_db'
    createDB(dbName)
    emojiDB(dbName='Tele_db')
    createTables(dbName)
    #file_name = 'tele-data.csv'
    df = pd.read_csv('telecom.csv')
    insert_to_tweet_table(dbName='Tele_db', df=df, table_name='TeleTable')
    #print("sucessfully")
