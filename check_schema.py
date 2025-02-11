import sqlite3

def print_table_schema(table_name):
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema_info = cursor.fetchall()
    print(f"Schema for {table_name}:")
    for column in schema_info:
        print(column)
    conn.close()

def print_foreign_keys(table_name):
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    fk_info = cursor.fetchall()
    print(f"Foreign keys for {table_name}:")
    for fk in fk_info:
        print(fk)
    conn.close()

if __name__ == "__main__":
    print_table_schema("stations")
    print("\n")
    print_table_schema("measurements")
    print("\n")
    print_foreign_keys("measurements")