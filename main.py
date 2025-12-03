# main.py (Updated for EMI & Bad Debt Support)
import db_setup
from store_manager import StoreManager
import dashboard  # Make sure this file still exists or remove this line if using Streamlit only
import sys
import sqlite3
import pandas as pd

# 1. Setup
db_setup.create_tables()
my_shop = StoreManager()

def print_menu():
    print("\n--- 🏦 MAYANK'S ENTERPRISE STORE SYSTEM ---")
    print("1. 📦 Add New Product (Stock)")
    print("2. 💰 Sell Product (Cash/EMI/Credit)")
    print("3. 💳 Manage Payments & Debts")
    print("4. 📊 Show Sales Report")
    print("5. ❌ Exit")

def manage_payments_menu():
    print("\n--- 💳 FINANCE MANAGER ---")
    print("1. View Pending Payments")
    print("2. Record a Payment (Customer Paying EMI)")
    print("3. Report Bad Debt (Customer Defaulted)")
    print("4. Back to Main Menu")
    
    choice = input("👉 Select Option: ")
    
    if choice == '1':
        conn = sqlite3.connect('smart_inventory.db')
        df = pd.read_sql_query("SELECT * FROM sales WHERE status='Pending'", conn)
        conn.close()
        if df.empty:
            print("✅ No pending payments!")
        else:
            print(df[['sale_id', 'product_name', 'total_amount', 'due_date']])

    elif choice == '2':
        sale_id = input("Enter Sale ID to Pay: ")
        amount = float(input("Enter Amount Paid ($): "))
        my_shop.record_payment(int(sale_id), amount)

    elif choice == '3':
        sale_id = input("Enter Sale ID to Mark as BAD DEBT: ")
        confirm = input(f"⚠️ Are you sure you want to write off Sale #{sale_id}? (y/n): ")
        if confirm.lower() == 'y':
            my_shop.mark_bad_debt(int(sale_id))

# 2. The Main Loop
while True:
    print_menu()
    choice = input("👉 Enter choice (1-5): ")

    if choice == '1':
        # ADD STOCK
        p_name = input("Enter Product Name: ")
        try:
            p_price = float(input("Enter Price ($): "))
            p_qty = int(input("Enter Quantity: "))
            my_shop.add_product(p_name, p_price, p_qty)
        except ValueError:
            print("⚠️ Error: Please enter valid numbers.")

    elif choice == '2':
        # ADVANCED SELLING
        p_name = input("Enter Product Name: ")
        try:
            p_qty = int(input("Quantity: "))
            
            print("\nSelect Payment Type:")
            print("1. Cash (Paid Now)")
            print("2. EMI (Due in 30 Days)")
            print("3. Credit (Due in 15 Days)")
            pay_choice = input("👉 Choice (1-3): ")
            
            p_type = "Cash"
            if pay_choice == '2': p_type = "EMI"
            elif pay_choice == '3': p_type = "Credit"
            
            my_shop.process_sale(p_name, p_qty, p_type)
            
        except ValueError:
            print("⚠️ Error: Quantity must be a number.")

    elif choice == '3':
        # NEW: FINANCE MENU
        manage_payments_menu()


    elif choice == '4':
        # DASHBOARD
        print("📊 Generating Report...")
        dashboard.show_sales_chart()

    elif choice == '5':
        print("👋 Shop Closed.")
        sys.exit()
    
    else:
        print("⚠️ Invalid choice.")
