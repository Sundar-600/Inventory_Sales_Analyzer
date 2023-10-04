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

output_path = "/Dataset"

#READING DATASET
raw = pd.read_excel("Dataset/Raw_Materials.xlsx",index_col=False)
inv = pd.read_excel("Dataset/Inventory.xlsx",index_col=False)
sal = pd.read_excel("Dataset/Sales.xlsx",index_col=False)

#Original Columns
org_raw_col = list(raw.columns)
org_inv_col = list(inv.columns)
org_sal_col = list(sal.columns)

#End Dates
org_raw_max_date = pd.to_datetime(raw["Date"]).max()
org_inv_max_date = pd.to_datetime(inv["Date"]).max()
org_sal_max_date = pd.to_datetime(sal["Date"]).max()

#Max Order ID 
org_raw_max_id = raw["Order_ID"].max()
org_inv_max_id = inv["Order_ID"].max()
org_sal_max_id = sal["Order_ID"].max()

#UPLOAD SECTION
st.markdown("## UPLOAD :arrow_up:")
up_col1, up_col2, up_col3 = st.columns((3))

#RAW MATERIALS
with up_col1:
    up_col1.markdown("### Raw Materials :thread:")
    up_raw = st.file_uploader("", ["csv", "xls", "xlsx"],accept_multiple_files=False)
    if up_raw is None : 
        st.session_state["RU"] = 1
    elif up_raw is not None and st.session_state["RU"] == 1 :
        st.session_state["RU"] = 0
        progress_bar_raw = up_col1.progress(0)
        for i in range(100):
            time.sleep(0.05)
            progress_bar_raw.progress(i + 1,text="Uploading Please Wait")
        progress_bar_raw.empty()
        try :
            up_raw = pd.read_excel(up_raw)
        except :
            try :
                up_raw = pd.read_csv(up_raw,encoding="ISO-8859-1")
            except : 
                st.warning("Wrong Format or Mismatch in Columns")
        new_raw_col = list(up_raw.columns)
        if org_raw_col == new_raw_col:
            new_raw_min_date = pd.to_datetime(up_raw["Date"]).min()
            new_raw_min_id = up_raw["Order_ID"].min()
            if (org_raw_max_date <= new_raw_min_date):
                if(org_raw_max_id < new_raw_min_id):
                    up_col1.success("File Successfully Uploaded")
                    df = []
                    df.append(raw)
                    df.append(up_raw)
                    new_df = pd.concat(df)
                    writer = pd.ExcelWriter('Dataset/Raw_Materials.xlsx', engine='xlsxwriter')
                    new_df.to_excel(writer,index=False)
                    writer.save()
                else :
                    up_col1.warning("Duplicate or Wrong ID")
            else:
                up_col1.warning("Duplicate or Wrong Date")
        else:
            up_col1.warning("Mismatch Columns or Wrong Excel Sheet")

#INVENTORY
with up_col2:
    up_col2.markdown("### Inventory :package:")
    up_inv = st.file_uploader(" ", ["csv", "xls", "xlsx"],accept_multiple_files=False)
    if up_inv is None :
        st.session_state["IU"] = 1
    elif up_inv is not None and st.session_state["IU"] == 1:
        st.session_state["IU"] = 0
        progress_bar_inv = up_col2.progress(0)
        for i in range(100):
            time.sleep(0.05)
            progress_bar_inv.progress(i + 1,text="Uploading Please Wait")
        progress_bar_inv.empty()
        try :
            up_inv = pd.read_excel(up_inv)
        except :
            try :
                up_inv = pd.read_csv(up_inv,encoding="ISO-8859-1")
            except : 
                st.warning("Wrong Format or Mismatch in Columns")
        new_inv_col = list(up_inv.columns)
        if org_inv_col == new_inv_col:
            new_inv_min_date = up_inv["Date"].min()
            new_inv_min_id = up_inv["Order_ID"].min()
            if (org_inv_max_date <= new_raw_min_date):
                if(org_inv_max_id < new_raw_min_id):
                    up_col2.success("File Successfully Uploaded")
                    df = []
                    df.append(inv)
                    df.append(up_inv)
                    new_df = pd.concat(df)
                    writer = pd.ExcelWriter('Dataset/Inventory.xlsx', engine='xlsxwriter')
                    new_df.to_excel(writer,index=False)
                    writer.save()
                else :
                    up_col2.warning("Duplicate or Wrong ID")
            else:
                up_col2.warning("Duplicate or Wrong Date")
        else:
            up_col2.warning("Mismatch Columns or Wrong Excel Sheet")


#SALES
with up_col3:
    up_col3.markdown("### Sales :moneybag:")
    up_sal = st.file_uploader("  ", ["csv", "xls", "xlsx"],accept_multiple_files=False)
    if up_sal is None : 
        st.session_state["SU"] = 1
    elif up_sal is not None and st.session_state["SU"] == 1:
        st.session_state["SU"] = 0
        progress_bar_sal = up_col3.progress(0)
        for i in range(100):
            time.sleep(0.05)
            progress_bar_sal.progress(i + 1,"Uploading Please Wait")
        progress_bar_sal.empty()
        try :
            up_sal = pd.read_excel(up_sal)
        except :
            try :
                up_sal = pd.read_csv(up_sal,encoding="ISO-8859-1")
            except : 
                st.warning("Wrong Format or Mismatch in Columns")
        new_sal_col = list(up_sal.columns)
        if org_sal_col == new_sal_col:
            new_sal_min_date = pd.to_datetime(up_sal["Date"]).min()
            new_sal_min_id = up_sal["Order_ID"].min()
            if (org_sal_max_date <= new_sal_min_date):
                if(org_sal_max_id < new_sal_min_id):
                    up_col3.success("File Successfully Uploaded")
                    df = []
                    df.append(sal)
                    df.append(up_sal)
                    new_df = pd.concat(df)
                    writer = pd.ExcelWriter('Dataset/Sales.xlsx', engine='xlsxwriter')
                    new_df.to_excel(writer,index=False)
                    writer.save()
                else :
                    up_col3.warning("Duplicate or Wrong ID")
            else:
                up_col3.warning("Duplicate or Wrong Date")
        else:
            up_col3.warning("Mismatch Columns or Wrong Excel Sheet")

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
        data=r_data.to_csv(index = False),
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
        data=i_data.to_csv(index = False),
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
        data=s_data.to_csv(index = False),
        file_name="Sales.csv",
        mime="text/csv/xlxs",
    )
    if sald:
        down_col3.success("Download")
