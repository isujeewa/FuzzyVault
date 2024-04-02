import psycopg2

def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname="SnapSecure",
            user="pgadmin",
            password="Uow@1234",
            host="snapsecure.postgres.database.azure.com",
            port="5432"
        )
        print("Connected to database.")
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None

# Test the connection
conn = connect_to_database()
if conn is not None:
    conn.close()
    print("Connection closed.")
