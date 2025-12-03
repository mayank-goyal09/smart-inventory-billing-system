import streamlit as st
import pandas as pd
import sqlite3
from store_manager import StoreManager
import plotly.express as px

# Initialize the Shop
shop = StoreManager()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="🛒 Mayank's Smart Shop",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- CUSTOM THEME / CSS ----------
st.markdown(
    """
<style>
:root {
    --primary: #16a34a;           /* green */
    --primary-dark: #15803d;
    --accent: #f97316;            /* orange */
    --bg-main: #0f172a;
    --bg-surface: #020617;
    --bg-card: #020617;
    --text-main: #e5e7eb;
    --text-muted: #9ca3af;
    --border-subtle: rgba(148, 163, 184, 0.3);
}

/* App background */
.stApp {
    background: radial-gradient(circle at top left, #0f172a 0, #020617 55%, #020617 100%);
    color: var(--text-main);
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f172a 45%, #022c22 100%);
    border-right: 1px solid rgba(15, 118, 110, 0.4);
}
section[data-testid="stSidebar"] * {
    color: var(--text-main) !important;
}

/* Titles */
h1, h2, h3 {
    color: #f9fafb !important;
}

/* Generic card container */
.shop-card {
    background: radial-gradient(circle at top left, rgba(34, 197, 94, 0.12), rgba(15, 23, 42, 0.95));
    border-radius: 18px;
    padding: 20px 22px;
    border: 1px solid rgba(148, 163, 184, 0.45);
    box-shadow:
        0 18px 30px rgba(15, 23, 42, 0.9),
        0 0 0 1px rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(10px);
    transition: transform 0.18s ease-out, box-shadow 0.18s ease-out, border-color 0.18s ease-out;
}
.shop-card:hover {
    transform: translateY(-2px);
    border-color: rgba(34, 197, 94, 0.8);
    box-shadow:
        0 20px 45px rgba(15, 23, 42, 1),
        0 0 22px rgba(34, 197, 94, 0.4);
}

/* KPI metric wrapper */
.kpi-box {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(15, 118, 110, 0.25));
    border-radius: 14px;
    padding: 12px 16px;
    border: 1px solid rgba(45, 212, 191, 0.5);
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(15, 23, 42, 0.9) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(148, 163, 184, 0.7) !important;
    color: var(--text-main) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus,
.stSelectbox div[data-baseweb="select"]:focus-within > div {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 1px var(--primary) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    border-radius: 999px !important;
    color: white !important;
    font-weight: 600;
    border: none;
    padding: 0.5rem 1.3rem;
    box-shadow: 0 0.5rem 1.4rem rgba(34, 197, 94, 0.5);
    transition: transform 0.15s ease-out, box-shadow 0.15s ease-out, filter 0.15s ease-out;
}
.stButton > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
    box-shadow: 0 0.9rem 1.8rem rgba(34, 197, 94, 0.75);
}
.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 0.4rem 1rem rgba(34, 197, 94, 0.4);
}

/* Dataframe */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
}

/* Expander */
.streamlit-expanderHeader {
    font-weight: 500;
    color: var(--text-main);
}

/* Divider */
.shop-divider {
    height: 2px;
    margin: 1.2rem 0 1.6rem 0;
    border-radius: 1px;
    background: linear-gradient(
        90deg,
        rgba(34, 197, 94, 0.0),
        rgba(34, 197, 94, 0.5),
        rgba(249, 115, 22, 0.5),
        rgba(34, 197, 94, 0.0)
    );
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- SIDEBAR ----------
st.sidebar.title("🛒 Smart Inventory")
st.sidebar.caption("Manage sales, stock, and insights in one place.")

menu_choice = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Sell Items", "Restock Inventory", "Payments"],
)

# ---------- 1. DASHBOARD ----------
if menu_choice == "Dashboard":
    st.markdown(
        """
<div class="shop-card">
    <h1 style="margin-bottom: 0.2rem;">📊 Live Sales Dashboard</h1>
    <p style="color: #9ca3af; margin-top: 0.2rem;">
        Monitor revenue, track product performance, and explore detailed sales logs.
    </p>
    <div class="shop-divider"></div>
</div>
""",
        unsafe_allow_html=True,
    )

    conn = sqlite3.connect("smart_inventory.db")
    try:
        df = pd.read_sql_query("SELECT * FROM sales", conn)
    except Exception as e:
        st.error(f"Error reading sales data: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()

    if not df.empty and "total_amount" in df.columns and "quantity" in df.columns:
        total_revenue = df["total_amount"].sum()
        total_items_sold = df["quantity"].sum()
        num_orders = len(df)
        avg_ticket = total_revenue / num_orders if num_orders > 0 else 0

        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        with kpi_col1:
            st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        with kpi_col2:
            st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
            st.metric("Items Sold", int(total_items_sold))
            st.markdown("</div>", unsafe_allow_html=True)
        with kpi_col3:
            st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
            st.metric("Orders", num_orders)
            st.markdown("</div>", unsafe_allow_html=True)
        with kpi_col4:
            st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
            st.metric("Avg Ticket", f"${avg_ticket:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="shop-divider"></div>', unsafe_allow_html=True)

        # Optional simple filter
        products = ["All"] + sorted(df["product_name"].unique().tolist())
        selected_product = st.selectbox("Filter by product", products)

        if selected_product != "All":
            df_plot = df[df["product_name"] == selected_product]
        else:
            df_plot = df

        col_chart, col_side = st.columns([2, 1])

        with col_chart:
            st.subheader("Revenue by Product")
            fig = px.bar(
                df_plot,
                x="product_name",
                y="total_amount",
                color="product_name",
                title="Sales Performance",
                labels={"product_name": "Product", "total_amount": "Revenue"},
            )
            fig.update_layout(
                xaxis_title="Product",
                yaxis_title="Revenue",
                plot_bgcolor="rgba(15,23,42,0.7)",
                paper_bgcolor="rgba(15,23,42,0)",
                font_color="#e5e7eb",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_side:
            # Payment method breakdown (if column exists)
            if "payment_type" in df.columns:
                st.subheader("Payment Methods")
                method_counts = df["payment_type"].value_counts().reset_index()
                method_counts.columns = ["payment_type", "count"]
                pie = px.pie(
                    method_counts,
                    names="payment_type",
                    values="count",
                    hole=0.45,
                    title="Payment Types Used",
                )
                pie.update_layout(
                    plot_bgcolor="rgba(15,23,42,0.7)",
                    paper_bgcolor="rgba(15,23,42,0)",
                    font_color="#e5e7eb",
                )
                st.plotly_chart(pie, use_container_width=True)

            # Payment status breakdown (if column exists)
            if "status" in df.columns:
                st.subheader("Payment Status")
                status_counts = df["status"].value_counts().reset_index()
                status_counts.columns = ["status", "count"]
                bar = px.bar(
                    status_counts,
                    x="status",
                    y="count",
                    color="status",
                    text="count",
                    title="Paid / Pending / Bad Debt",
                )
                bar.update_traces(textposition="outside")
                bar.update_layout(
                    plot_bgcolor="rgba(15,23,42,0.7)",
                    paper_bgcolor="rgba(15,23,42,0)",
                    font_color="#e5e7eb",
                )
                st.plotly_chart(bar, use_container_width=True)

        with st.expander("View Transaction Log", expanded=False):
            st.dataframe(df, use_container_width=True)
    else:
        st.info("No sales data yet. Go to the 'Sell Items' tab to record your first sale.")

# ---------- 2. SELL ITEMS ----------
elif menu_choice == "Sell Items":
    st.markdown(
        """
<div class="shop-card">
    <h1 style="margin-bottom: 0.2rem;">💰 Point of Sale (POS)</h1>
    <p style="color: #9ca3af; margin-top: 0.2rem;">
        Process customer orders quickly and keep inventory in sync with each sale.
    </p>
    <div class="shop-divider"></div>
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/2435/2435281.png",
            width=170,
        )

    with col2:
        st.markdown("#### Select Product to Sell")
        conn = sqlite3.connect("smart_inventory.db")
        try:
            products_df = pd.read_sql_query("SELECT name FROM products", conn)
        except Exception as e:
            st.error(f"Error loading products: {e}")
            products_df = pd.DataFrame(columns=["name"])
        finally:
            conn.close()

        product_list = products_df["name"].tolist()

        if product_list:
            selected_product = st.selectbox("Choose Product", product_list)
            quantity = st.number_input("Quantity", min_value=1, value=1)

            st.markdown("#### Payment Method")
            pay_choice = st.radio(
                "",
                ["Cash", "EMI (30 days)", "Credit (15 days)"],
                horizontal=True,
            )
            pay_map = {
                "Cash": "Cash",
                "EMI (30 days)": "EMI",
                "Credit (15 days)": "Credit",
            }
            payment_type = pay_map[pay_choice]

            if st.button("Confirm Sale ✅"):
                try:
                    # Prefer 3-argument version if StoreManager supports it
                    shop.process_sale(selected_product, int(quantity), payment_type)
                except TypeError:
                    # Fallback to old 2-argument version if payment not yet supported
                    shop.process_sale(selected_product, int(quantity))
                st.success(f"Successfully sold {quantity} × {selected_product} via {payment_type}!")
                st.balloons()
        else:
            st.warning("No products in stock. Go to 'Restock Inventory' to add items first.")

# ---------- 3. RESTOCK INVENTORY ----------
elif menu_choice == "Restock Inventory":
    st.markdown(
        """
<div class="shop-card">
    <h1 style="margin-bottom: 0.2rem;">📦 Inventory Management</h1>
    <p style="color: #9ca3af; margin-top: 0.2rem;">
        Add new products or update stock levels to keep your smart shop always ready.
    </p>
    <div class="shop-divider"></div>
</div>
""",
        unsafe_allow_html=True,
    )

    with st.form("add_stock_form"):
        st.markdown("#### Add New Stock Item")
        new_name = st.text_input("Product Name")
        new_price = st.number_input("Price per Unit ($)", min_value=0.0, format="%.2f")
        new_qty = st.number_input("Stock Quantity", min_value=1, value=10)

        submitted = st.form_submit_button("Add to Inventory 📥")

        if submitted:
            if new_name:
                shop.add_product(new_name, new_price, new_qty)
                st.success(f"Added {new_name} to stock.")
            else:
                st.error("Please enter a product name before submitting.")

    st.markdown("### Current Inventory")
    conn = sqlite3.connect("smart_inventory.db")
    try:
        inv_df = pd.read_sql_query("SELECT * FROM products", conn)
    except Exception as e:
        st.error(f"Error loading inventory: {e}")
        inv_df = pd.DataFrame()
    finally:
        conn.close()

    if not inv_df.empty:
        st.dataframe(inv_df, use_container_width=True)
    else:
        st.info("No products found yet. Add some items above.")

# ---------- 4. PAYMENTS (RECEIVING MONEY ON EMI / CREDIT) ----------
elif menu_choice == "Payments":
    st.markdown(
        """
<div class="shop-card">
    <h1 style="margin-bottom: 0.2rem;">💳 Payments & Pending Dues</h1>
    <p style="color: #9ca3af; margin-top: 0.2rem;">
        View outstanding EMI / credit sales and record payments when customers pay you back.
    </p>
    <div class="shop-divider"></div>
</div>
""",
        unsafe_allow_html=True,
    )

    conn = sqlite3.connect("smart_inventory.db")
    try:
        pending_df = pd.read_sql_query(
            "SELECT sale_id, product_name, total_amount, payment_type, status, due_date, sale_date "
            "FROM sales WHERE status = 'Pending'",
            conn,
        )
    except Exception as e:
        st.error(f"Could not load pending payments. Error: {e}")
        pending_df = pd.DataFrame()
    finally:
        conn.close()

    if pending_df.empty:
        st.info("No pending payments right now. All good.")
    else:
        st.subheader("Pending Sales (Customers Still Owe Money)")
        st.dataframe(pending_df, use_container_width=True)

        st.markdown("#### Record a Payment")

        sale_ids = pending_df["sale_id"].tolist()
        selected_sale_id = st.selectbox("Select Sale ID", sale_ids)

        selected_row = pending_df[pending_df["sale_id"] == selected_sale_id].iloc[0]
        st.write(
            f"- Product: **{selected_row['product_name']}**  \n"
            f"- Total Bill: **${selected_row['total_amount']:.2f}**  \n"
            f"- Payment Type: **{selected_row['payment_type']}**  \n"
            f"- Due Date: **{selected_row['due_date'] or 'N/A'}**"
        )

        amount = st.number_input(
            "Amount received now ($)",
            min_value=0.0,
            step=10.0,
            format="%.2f",
        )

        if st.button("Record Payment ✅"):
            if amount <= 0:
                st.error("Please enter a positive amount.")
            else:
                try:
                    shop.record_payment(int(selected_sale_id), float(amount))
                    st.success(f"Recorded payment of ${amount:.2f} for sale #{selected_sale_id}.")
                except AttributeError:
                    st.error("record_payment() is not defined in StoreManager. Please add it there.")
                except Exception as e:
                    st.error(f"Something went wrong while recording payment: {e}")


# ---------- FOOTER ----------
st.markdown(
        """
<div style="text-align: center; margin-top: 3rem; padding-bottom: 2rem;">
<p style="font-size: 1rem; margin-bottom: 15px; color: var(--text-secondary);">
Made with ❤️ by <span style="color: var(--gold); font-weight: 600;">Mayank</span>
</p>
<div style="display: flex; justify-content: center; gap: 25px;">
<a href="https://github.com/mayank-goyal09" target="_blank" style="text-decoration: none; transition: transform 0.2s;">
<div style="font-size: 1.8rem; filter: grayscale(100%); transition: filter 0.3s;">
🐙 <span style="font-size: 0.9rem; color: var(--text-secondary); display: block;">GitHub</span>
</div>
</a>
<a href="https://www.linkedin.com/in/mayank-goyal-4b8756363/" target="_blank" style="text-decoration: none; transition: transform 0.2s;">
<div style="font-size: 1.8rem; filter: grayscale(100%); transition: filter 0.3s;">
💼 <span style="font-size: 0.9rem; color: var(--text-secondary); display: block;">LinkedIn</span>
</div>
</a>
</div>
<p style="font-size: 0.75rem; margin-top: 20px; opacity: 0.4;">
Maygal Books Vault © 2025
</p>
</div>
""",
        unsafe_allow_html=True,
    )
