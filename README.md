# 🏪 Smart Inventory and Billing System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A modern retail management application combining **Python OOP**, **SQLite database**, and **Streamlit dashboard** for comprehensive inventory tracking, point-of-sale operations, and flexible payment management.

---

## 📋 Project Overview

This project is a **Smart Inventory and Billing System** designed for retail businesses that need to manage:
- Product inventory with real-time stock tracking
- Multi-payment transactions (Cash, EMI, Credit)
- Payment tracking and debt management
- Interactive business analytics and KPIs

The system features a clean separation of concerns with a Python backend handling all business logic through a `StoreManager` class, SQLite for persistent data storage, and a modern Streamlit interface for user interactions.

---

## ✨ Key Features

### 🎯 Core Functionality
- **Inventory Management**: Add, update, and track product stock levels
- **Point of Sale (POS)**: Process sales transactions with automatic stock deduction
- **Multi-Payment Support**: Handle Cash, EMI, and Credit payments
- **Payment Tracking**: Record partial and full payments for credit/EMI transactions
- **Bad Debt Management**: Automatic tracking of overdue payments
- **Interactive Dashboard**: Real-time KPIs, revenue charts, and payment analytics

### 💳 Payment System
- **Cash**: Immediately marked as Paid with instant settlement
- **EMI**: Scheduled installment payments with due date tracking
- **Credit**: Deferred payment with automatic pending status
- **Payment Recording**: Track payments over time until fully settled

### 📊 Analytics & Reporting
- Revenue tracking with visual charts (Plotly)
- Payment breakdown by type
- Pending payments overview
- Stock status monitoring
- Transaction history

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|----------|
| **Python 3.8+** | Backend logic and OOP implementation |
| **SQLite** | Lightweight database for data persistence |
| **Streamlit** | Modern web dashboard and UI |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive data visualizations |
| **Object-Oriented Programming** | Clean, maintainable code structure |

---

## 🗄️ Database Schema

The SQLite database (`smart_inventory.db`) contains three core tables:

### 📦 Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);
```

### 🧾 Sales Table
```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    total_amount REAL,
    payment_type TEXT,  -- Cash/EMI/Credit
    status TEXT,        -- Paid/Pending
    sale_date TEXT,
    due_date TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### 💰 Payments Table
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER,
    amount_paid REAL,
    payment_date TEXT,
    FOREIGN KEY (sale_id) REFERENCES sales(id)
);
```

---

## 📁 Project Structure

```
smart-inventory-billing-system/
│
├── app.py                      # Main Streamlit application
├── store_manager.py            # StoreManager class (OOP backend)
├── smart_inventory.db          # SQLite database
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
└── pages/
    ├── 01_📊_Dashboard.py      # KPIs and analytics
    ├── 02_🛒_Point_of_Sale.py  # Billing interface
    ├── 03_📦_Inventory.py      # Stock management
    └── 04_💳_Payments.py       # Payment tracking
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/mayank-goyal09/smart-inventory-billing-system.git
cd smart-inventory-billing-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 📖 Usage Guide

### 1️⃣ Dashboard
- View key performance indicators (KPIs)
- Analyze revenue trends with interactive charts
- Monitor payment status breakdown
- Track pending payments and bad debts

### 2️⃣ Point of Sale (POS)
- Select products from inventory
- Enter quantity for purchase
- Choose payment method (Cash/EMI/Credit)
- Process sale with automatic stock deduction
- Generate sale receipt

### 3️⃣ Inventory Management
- View all products with current stock levels
- Add new products to the system
- Restock existing products
- Monitor low-stock items

### 4️⃣ Payment Tracking
- View all pending EMI/Credit sales
- Select a sale to record payment
- Enter payment amount
- System automatically updates status when fully paid
- Track payment history for each sale

---

## 🎨 Features in Detail

### Object-Oriented Design
The `StoreManager` class encapsulates all business logic:
- `add_product()`: Add new products to inventory
- `process_sale()`: Handle sales transactions
- `record_payment()`: Track customer payments
- `get_pending_sales()`: Retrieve unpaid transactions
- `get_sales_summary()`: Generate analytics data

### Payment Flow
1. **Cash Sales**: Immediate payment, marked as "Paid"
2. **EMI/Credit Sales**: 
   - Marked as "Pending" on creation
   - Due date assigned based on payment type
   - Payments recorded incrementally
   - Status auto-updates to "Paid" when fully settled

### Data Visualization
- **Plotly Charts**: Interactive revenue and payment analytics
- **Pandas DataFrames**: Efficient data processing
- **Real-time Updates**: Dashboard reflects latest data

---

## 📊 Sample Use Cases

1. **Retail Store**: Manage daily sales, inventory, and customer credit
2. **Small Business**: Track revenue and pending payments
3. **Learning Project**: Demonstrates OOP, database design, and full-stack development

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Mayank Goyal**
- GitHub: [@mayank-goyal09](https://github.com/mayank-goyal09)
- LinkedIn: [Mayank Goyal](https://www.linkedin.com/in/mayank-goyal-4b8756363/)
- Email: itsmaygal09@gmail.com

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Python Object-Oriented Programming (OOP)
- ✅ SQLite database design and operations
- ✅ Full-stack application development
- ✅ Modern UI/UX with Streamlit
- ✅ Data visualization with Plotly
- ✅ Business logic implementation
- ✅ Git version control

---

## 🌟 Future Enhancements

- [ ] User authentication and role-based access
- [ ] Export reports to PDF/Excel
- [ ] SMS/Email notifications for due payments
- [ ] Barcode scanning for POS
- [ ] Multi-store support
- [ ] Customer management module
- [ ] Inventory forecasting with ML

---

**⭐ If you find this project helpful, please consider giving it a star!**