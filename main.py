import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
from db import create_db,insert_docs,fetch_docs,reports1,reports2

create_db()
# st.write(fetch_docs())

accounts = ["Rajanikant", "Praveena", "Chitrak", "Tushar", "Sweety", "Rajal", "Yatharth", "Monil"]
def data_entry():
    from_account = st.selectbox("From_Account", accounts)
    to_account=st.selectbox("To_Account",accounts)
    amount = st.number_input("Amount:", min_value=0.0, step=0.01)
    txn_date = st.date_input("TxnDate:", datetime.now())
    remarks = st.text_area("Remarks:")


    if st.button("Submit"):
        insert_docs(from_account,to_account,amount,txn_date,remarks)

def report1():
    from_account = st.selectbox("From_Account", accounts)
    to_account=st.selectbox("To_Account",accounts)
    from_date = st.date_input("From Date:", datetime.now())
    to_date = st.date_input("To Date:", datetime.now())

    if st.button("Submit"):
        txns1=reports1(from_account,to_account,from_date,to_date)
        txns2=reports1(to_account,from_account,from_date,to_date)
        df1 = pd.DataFrame(txns1, columns=["TxnId", "From", "To", "Amount", "Date", "Remarks"])
        df2 = pd.DataFrame(txns2, columns=["TxnId", "From", "To", "Amount", "Date", "Remarks"])
        st.table(df1)
        st.table(df2)
        total1=0
        total2=0
        total=0
        payer=""
        receiver=""
        for txn in txns1:
            total1+=txn[3]
        for txn in txns2:
            total2+=txn[3]
        
        color="black"
        if total1-total2>0:
            color="green"
            total=total1-total2
            payer=from_account
            receiver=to_account
        elif total1-total2<0:
            color="red"
            total=total2-total1
            payer=to_account
            receiver=from_account
        st.write(f'<h1 style="font-size: 24px; color:{color}; font-weight: bold;">{payer} Paid {total} to {receiver}</h1>', unsafe_allow_html=True)

def report2():
    from_account = st.selectbox("From_Account", accounts)
    from_date = st.date_input("From Date:", datetime.now())
    to_date = st.date_input("To Date:", datetime.now())

    if st.button("Submit"):
        txns=reports2(from_account,from_date,to_date)
        df = pd.DataFrame(txns, columns=["TxnId", "From", "To", "Amount", "Date", "Remarks"])    
        st.table(df)
            

if "ui_state" not in st.session_state:
    st.session_state.ui_state = "empty"

with st.sidebar:
    service=st.selectbox("Services",["Data Entry","Report1","Ledger"])


# Buttons to switch between UIs
if service=="Data Entry":
    st.session_state.ui_state = "data_entry"

if service=="Report1":
    st.session_state.ui_state = "Report1"

if service=="Ledger":
    st.session_state.ui_state = "Report2"

# Render the appropriate UI based on the session state
if st.session_state.ui_state == "data_entry":
    data_entry()
elif st.session_state.ui_state == "Report1":
    report1()
elif st.session_state.ui_state == "Report2":
    report2()