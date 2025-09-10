#imporing database library
import sqlite3
#Create a database connection to the SQL Server
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('flights.db', check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn
#Create reservations table if it doesn't exist
def create_table(conn):
    try:
        sql_create_reservations_table = """ CREATE TABLE IF NOT EXISTS reservations (
                                            name TEXT NOT NULL,
                                            flight_number TEXT NOT NULL,
                                            departure TEXT NOT NULL,
                                            destination TEXT NOT NULL,
                                            date TEXT NOT NULL,
                                            seat_number TEXT NOT NULL
                                        ); """
        c = conn.cursor()
        c.execute(sql_create_reservations_table)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
#Setting up Database and Table
def setup_database():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")
if __name__ == '__main__':
    setup_database()