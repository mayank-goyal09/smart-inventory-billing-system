# db_setup.py
import sqlite3

DB_NAME = "smart_inventory.db"


def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def create_tables():
    """Create all required tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Products table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL UNIQUE,
            price      REAL    NOT NULL,
            stock      INTEGER NOT NULL
        );
        """
    )

    # Sales table (includes payment info)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT    NOT NULL,
            quantity     INTEGER NOT NULL,
            total_amount REAL    NOT NULL,
            payment_type TEXT    NOT NULL,  -- 'Cash', 'EMI', 'Credit'
            status       TEXT    NOT NULL,  -- 'Paid', 'Pending', 'Bad Debt'
            due_date     TEXT,              -- for EMI/Credit
            sale_date    TEXT    NOT NULL
        );
        """
    )

    # Payments table (money actually received)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS payments (
            payment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id      INTEGER NOT NULL,
            amount_paid  REAL    NOT NULL,
            payment_date TEXT    NOT NULL,
            notes        TEXT,
            FOREIGN KEY (sale_id) REFERENCES sales (sale_id)
        );
        """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables created.")
