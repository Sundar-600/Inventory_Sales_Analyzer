import streamlit as st
import pandas as pd
import plotly_express as px
from streamlit.elements import progress
import time
import os
import numpy as np
from tables import file

st.set_page_config(page_title="DataSet", page_icon=":chart:", layout="wide")

with open("styles/dataset.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#READING DATASET
raw = pd.read_excel("Dataset/Raw_Materials.xlsx")
inv = pd.read_excel("Dataset/Inventory.xlsx")
sal = pd.read_excel("Dataset/Sales.xlsx")

#Original Columns
org_raw_col = list(raw.columns)
org_inv_col = list(inv.columns)
org_sal_col = list(sal.columns)

#End Dates
org_raw_max_date = raw["Date"].max()
org_inv_max_date = inv["Date"].max()
org_sal_max_date = sal["Date"].max()

#Max Order ID 
org_raw_max_id = raw["Order_ID"]
org_inv_max_id = inv["Order_ID"]
org_sal_max_id = sal["Order_ID"]

#UPLOAD SECTION
st.markdown("## UPLOAD :arrow_up:")
up_col1, up_col2, up_col3 = st.columns((3))

#RAW MATERIALS
with up_col1:
    up_col1.markdown("### Raw Materials :thread:")
    up_raw = st.file_uploader("", ["csv", "xls", "xlsx"])
    up_col1.write(org_raw_col)
    if up_raw is not None:
        progress_bar = up_col1.progress(0)
        file_raw = up_raw
        for i in range(100):
            time.sleep(0.05)
            progress_bar.progress(i + 1)
        up_raw = pd.read_csv(file_raw)
        new_raw_col = list(up_raw.column)
        if org_raw_col == new_raw_col:
            new_raw_min_date = up_raw["Date"].min()
            new_raw_min_id = up_raw["Order_ID"].min()
            if (org_raw_max_date <= new_raw_min_date) and (
                org_raw_max_id < new_raw_min_id
            ):
                up_col1.success("File Successfully Uploaded")
            else:
                up_col1.warning("Duplicate or Wrong Date or Order ID")
        else:
            up_col1.warning("Mismatch Columns or Wrong Excel Sheet")

#INVENTORY
with up_col2:
    up_col2.markdown("### Inventory :package:")
    up_inv = st.file_uploader(" ", ["csv", "xls", "xlsx"])
    if up_inv is not None:
        progress_bar = up_col2.progress(0)
        for i in range(100):
            time.sleep(0.05)
            progress_bar.progress(i + 1)
        up_col2.success("File Successfully Uploaded")

#SALES
with up_col3:
    up_col3.markdown("### Sales :moneybag:")
    up_sal = st.file_uploader("  ", ["csv", "xls", "xlsx"])
    if up_sal is not None:
        progress_bar = up_col3.progress(0)
        for i in range(100):
            time.sleep(0.05)
            progress_bar.progress(i + 1)
        up_col3.success("File Successfully Uploaded")

st.markdown("<br><br>", unsafe_allow_html=True)

#DOWNLOAD SECTION
st.markdown("## DOWNLOAD :arrow_down:")

down_col1, down_col2, down_col3 = st.columns((3))

#RAW MATERIALS
with down_col1:
    down_col1.markdown("### Raw Materials :thread:")
    down_col1.markdown("<br>", unsafe_allow_html=True)
    if "Raw" in st.session_state:
        r_data = st.session_state["Raw"]
    else:
        r_data = raw
    with down_col1.expander("Selected Data Set"):
        st.table(r_data)
    rawd = down_col1.download_button(
        label="Download ",
        data=r_data.to_csv(),
        file_name="RawMaterials.csv",
        mime="text/csv/xlxs",
    )
    if rawd:
        down_col1.success("Downloded")

#INVENTORY
with down_col2:
    down_col2.markdown("### Inventory :package:")
    down_col2.markdown("<br>", unsafe_allow_html=True)
    if "Inv" in st.session_state:
        i_data = st.session_state["Inv"]
    else:
        i_data = inv
    with down_col2.expander("Selected Data Set"):
        st.table(i_data)
    invd = down_col2.download_button(
        label="Download ",
        data=i_data.to_csv(),
        file_name="Inventory.csv",
        mime="text/csv/xlxs",
    )
    if invd:
        down_col2.success("Download")

#SALES
with down_col3:
    down_col3.markdown("### Sales :moneybag:")
    down_col3.markdown("<br>", unsafe_allow_html=True)
    if "Sal" in st.session_state:
        s_data = st.session_state["Sal"]
    else:
        s_data = sal
    with down_col3.expander("Selected Data Set"):
        st.table(s_data)
    sald = down_col3.download_button(
        label="Download ",
        data=s_data.to_csv(),
        file_name="Sales.csv",
        mime="text/csv/xlxs",
    )
    if sald:
        down_col3.success("Download")
