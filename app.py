import streamlit as st
import mysql.connector
from billing import add_to_cart, generate_bill, view_sales

# ---------------- SESSION STATE INIT ----------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "total" not in st.session_state:
    st.session_state.total = 0

# ---------------- DB Connection ----------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="shop_db"
    )

st.title("Inventory & Billing Management")

menu = st.sidebar.selectbox("Menu",
        ["Add Product","Billing","Sales Summary"])

# ---------------- ADD PRODUCT ----------------
if menu == "Add Product":
    st.header("Add Products")

    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=1)
    stock = st.number_input("Stock", min_value=1)

    if st.button("Add"):
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO products(name,price,stock) VALUES(%s,%s,%s)",
                    (name,price,stock))
        db.commit()
        st.success("Product Added!")

# ---------------- BILLING ----------------
elif menu == "Billing":
    add_to_cart(get_db)

# ---------------- SALES ----------------
elif menu == "Sales Summary":
    view_sales(get_db)
