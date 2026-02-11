import streamlit as st
import pandas as pd
from datetime import date

# -------- SESSION CART --------
if "cart" not in st.session_state:
    st.session_state.cart = []

# -------- ADD TO CART --------
def add_to_cart(get_db):
    st.header("Billing Section")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()

    df = pd.DataFrame(data, columns=["ID","Name","Price","Stock"])

    col1, col2 = st.columns(2)

    with col1:
        pid = st.selectbox("Product", df["ID"])
        qty = st.number_input("Quantity", min_value=1)

    with col2:
        st.dataframe(df)

    if st.button("Add To Cart"):
        product = df[df["ID"]==pid].iloc[0]

        st.session_state.cart.append({
            "id": pid,
            "name": product["Name"],
            "price": product["Price"],
            "qty": qty,
            "total": product["Price"]*qty
        })

    show_cart(get_db)

# -------- SHOW CART --------
def show_cart(get_db):

    st.subheader("Cart")

    cart = st.session_state.cart
    df = pd.DataFrame(cart)

    if not df.empty:
        st.dataframe(df)

        total = df["total"].sum()
        st.metric("Total Amount", total)

        if st.button("Generate Bill"):
            generate_bill(get_db, total)

# -------- GENERATE BILL --------
def generate_bill(get_db, total):

    db = get_db()
    cur = db.cursor()

    # insert bill
    cur.execute("INSERT INTO bills(bill_date,total_amount) VALUES(%s,%s)",
                (date.today(), total))
    bill_id = cur.lastrowid

    # insert items + update stock
    for i in st.session_state.cart:

        cur.execute("""INSERT INTO bill_items
                    (bill_id,product_id,quantity)
                    VALUES(%s,%s,%s)""",
                    (bill_id,i["id"],i["qty"]))

        cur.execute("""UPDATE products
                    SET stock = stock - %s
                    WHERE id=%s""",
                    (i["qty"],i["id"]))

    db.commit()

    # download bill
    bill_text = f"Bill No:{bill_id}\nTotal:{total}"
    st.download_button("Download Bill",
                       bill_text,
                       file_name="bill.txt")

    st.success("Bill Generated!")
    st.session_state.cart = []

# -------- VIEW SALES --------
def view_sales(get_db):

    st.header("Daily Sales")

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT bill_date, SUM(total_amount) FROM bills GROUP BY bill_date")
    data = cur.fetchall()

    df = pd.DataFrame(data, columns=["Date","Total"])

    st.dataframe(df)

    if not df.empty:
        st.metric("Today Sales",
                  df[df["Date"]==date.today()]["Total"].sum())
