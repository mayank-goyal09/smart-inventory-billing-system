# store_manager.py
import sqlite3
from datetime import datetime, timedelta


class StoreManager:
    """Business logic layer for inventory, sales, and payments."""

    def __init__(self, db_name="smart_inventory.db"):
        self.db_name = db_name

    # ---------- INTERNAL UTILS ----------

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    # ---------- INVENTORY ----------

    def add_product(self, name: str, price: float, stock: int) -> None:
        """
        Add a new product or increase stock if it already exists.
        """
        name = name.strip()
        if not name:
            print("Product name cannot be empty.")
            return

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Check if product exists
            cursor.execute("SELECT stock FROM products WHERE name = ?", (name,))
            row = cursor.fetchone()

            if row:
                # Update existing stock
                new_stock = row[0] + stock
                cursor.execute(
                    "UPDATE products SET price = ?, stock = ? WHERE name = ?",
                    (price, new_stock, name),
                )
                print(f"Updated product '{name}': price={price}, stock={new_stock}")
            else:
                # Insert new product
                cursor.execute(
                    "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                    (name, price, stock),
                )
                print(f"Added new product '{name}': price={price}, stock={stock}")

            conn.commit()

    # ---------- SALES ----------

    def process_sale(self, product_name: str, quantity: int, payment_type: str = "Cash") -> int | None:
        """
        Process a sale, update stock, and create a sales record.
        payment_type: 'Cash', 'EMI', or 'Credit'
        Returns the sale_id if successful, otherwise None.
        """
        product_name = product_name.strip()

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Get product details
            cursor.execute(
                "SELECT stock, price FROM products WHERE name = ?",
                (product_name,),
            )
            row = cursor.fetchone()

            if not row:
                print(f"Product '{product_name}' not found.")
                return None

            current_stock, price = row

            if quantity <= 0:
                print("Quantity must be positive.")
                return None

            if current_stock < quantity:
                print(
                    f"Not enough stock for '{product_name}'. "
                    f"Requested={quantity}, Available={current_stock}"
                )
                return None

            total_bill = price * quantity
            new_stock = current_stock - quantity

            # Payment details
            payment_type = payment_type.capitalize()
            if payment_type not in ("Cash", "Emi", "Credit"):
                payment_type = "Cash"

            # Normalize payment_type to consistent values
            if payment_type == "Emi":
                payment_type = "EMI"

            status = "Paid" if payment_type == "Cash" else "Pending"
            due_date = None

            if payment_type == "EMI":
                due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            elif payment_type == "Credit":
                due_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")

            sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 1. Update stock
            cursor.execute(
                "UPDATE products SET stock = ? WHERE name = ?",
                (new_stock, product_name),
            )

            # 2. Insert sale row
            cursor.execute(
                """
                INSERT INTO sales (
                    product_name, quantity, total_amount,
                    payment_type, status, due_date, sale_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    product_name,
                    quantity,
                    total_bill,
                    payment_type,
                    status,
                    due_date,
                    sale_date,
                ),
            )
            sale_id = cursor.lastrowid

            # 3. If cash, record immediate payment
            if payment_type == "Cash":
                cursor.execute(
                    """
                    INSERT INTO payments (sale_id, amount_paid, payment_date, notes)
                    VALUES (?, ?, ?, ?)
                    """,
                    (sale_id, total_bill, sale_date, "Cash payment"),
                )

            conn.commit()

            print(
                f"Sale recorded: id={sale_id}, {quantity}x '{product_name}', "
                f"type={payment_type}, status={status}, total={total_bill}"
            )

            return sale_id

    # ---------- PAYMENTS ----------

    def record_payment(self, sale_id: int, amount_paid: float) -> None:
        """
        Record a payment against an existing sale (for EMI or Credit).
        Updates the sale status to 'Paid' if fully settled.
        """
        if amount_paid <= 0:
            print("Payment amount must be positive.")
            return

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Get sale info
            cursor.execute(
                "SELECT total_amount, status FROM sales WHERE sale_id = ?",
                (sale_id,),
            )
            sale_row = cursor.fetchone()
            if not sale_row:
                print(f"Sale id {sale_id} not found.")
                return

            total_amount, current_status = sale_row

            # Sum of previous payments
            cursor.execute(
                "SELECT COALESCE(SUM(amount_paid), 0) FROM payments WHERE sale_id = ?",
                (sale_id,),
            )
            already_paid = cursor.fetchone()[0] or 0.0

            new_total_paid = already_paid + amount_paid
            remaining = total_amount - new_total_paid

            # Insert payment record
            payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                INSERT INTO payments (sale_id, amount_paid, payment_date, notes)
                VALUES (?, ?, ?, ?)
                """,
                (sale_id, amount_paid, payment_date, "EMI/Credit payment"),
            )

            # Update sale status if fully paid
            new_status = "Paid" if remaining <= 0.0001 else "Pending"
            cursor.execute(
                "UPDATE sales SET status = ? WHERE sale_id = ?",
                (new_status, sale_id),
            )

            conn.commit()

            print(
                f"Payment recorded for sale {sale_id}: +{amount_paid}, "
                f"paid={new_total_paid}, remaining={max(0, remaining)}, status={new_status}"
            )

    def mark_bad_debt(self, sale_id: int) -> None:
        """
        Mark a sale as bad debt (unrecoverable).
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sales SET status = 'Bad Debt' WHERE sale_id = ?",
                (sale_id,),
            )
            conn.commit()
            print(f"Sale {sale_id} marked as Bad Debt.")
