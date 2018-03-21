import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = sqlite3.connect(db_file)
    return conn


    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    c = conn.cursor()
    c.execute(create_table_sql)

def main():
    database = "/home/walter/Documents/my_git/tao_server/database.db"
    conn = create_connection(database)

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        username text,
                                        password text,
                                        setup text
                                    ); """


    # create a database connection

    if conn is not None:
        # create projects table
        create_table(conn, sql_create_users_table)

    else:
        print("Error! cannot create the database connection.")

if __name__ =="__main__":
    main()