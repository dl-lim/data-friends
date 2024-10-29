import sqlite3

con = sqlite3.connect("rag.db")

cursor = con.cursor()


def create_tables() -> None:
    """
    Initialise all sql tables.
    :return: None.
    """
    tables = [
        "CREATE TABLE IF NOT EXISTS docs(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255) NOT NULL, contents VARCHAR(255) NOT NULL)",
        "CREATE TABLE IF NOT EXISTS terms(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255) NOT NULL, idf DECIMAL NOT NULL)",
        "CREATE TABLE IF NOT EXISTS term_frequencies(id INTEGER PRIMARY KEY AUTOINCREMENT, term INT NOT NULL, doc INT NOT NULL, tf INT NOT NULL)",
    ]
    for table in tables:
        cursor.execute(table)
    return