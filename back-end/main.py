# main.py

from ETSsqLiteDB import initializeDatabase, print_db_tables, create_users, fetch_users

sqLiteDatabase = 'ETSsqLiteDB'


def main():
    # initializeDatabase()
    print_db_tables(sqLiteDatabase)
    # create_users(sqLiteDatabase)
    # fetch_users(sqLiteDatabase)


if __name__ == "__main__":
    main()
