from pandas.core.arrays import categorical
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
from unicodedata import category
from PIL.Image import new
from numpy import remainder
import os

st.set_page_config(page_title="Storage", page_icon=":package:", layout="wide")

with open("styles/storage.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Importing Datasets
raw = pd.read_excel("Dataset/Raw_Materials.xlsx")
inv = pd.read_excel("Dataset/Inventory.xlsx")
sal = pd.read_excel("Dataset/Sales.xlsx")

# Total Raw Materials
total_raw_material = raw.groupby(by=["R_Material"], as_index=False)["R_Qty (kgs)"].sum()
total_raw_material_colour = raw.groupby(by=["R_Material", "R_Colour"], as_index=False)[
    "R_Qty (kgs)"
].sum()

# Total Inventory Products
total_inv_material = inv.groupby(by=["Material"], as_index=False)[
    "Materials_Used(Kgs)"
].sum()
total_inv_product_material = inv.groupby(by=["Product", "Material"], as_index=False)[
    "Quandity"
].sum()
total_inv_material_colour = inv.groupby(by=["Material", "Colour"], as_index=False)[
    "Materials_Used(Kgs)"
].sum()

total_inv_product = inv.groupby(by=["Product"], as_index=False)["Quandity"].sum()
total_inv_product_size = inv.groupby(by=["Product", "Size"], as_index=False)[
    "Quandity"
].sum()
total_inv_product_colour = inv.groupby(by=["Product", "Colour"], as_index=False)[
    "Quandity"
].sum()


# Total Sales Report
total_sal_product = sal.groupby(by=["Product"], as_index=False)["Quandity"].sum()
total_sal_product_size = sal.groupby(by=["Product", "Size"], as_index=False)[
    "Quandity"
].sum()
total_sal_product_colour = sal.groupby(by=["Product", "Colour"], as_index=False)[
    "Quandity"
].sum()
total_sal_product_material = sal.groupby(by=["Product", "Material"], as_index=False)[
    "Quandity"
].sum()

# Remaining Raw Material
remaining_raw_material = total_raw_material.copy()
remaining_raw_material["R_Qty (kgs)"] = (
    total_raw_material["R_Qty (kgs)"] - total_inv_material["Materials_Used(Kgs)"]
)

# Remaining Raw Material Colour
remaining_raw_material_colour = total_raw_material_colour.copy()
remaining_raw_material_colour["R_Qty (kgs)"] = (
    total_raw_material_colour["R_Qty (kgs)"]
    - total_inv_material_colour["Materials_Used(Kgs)"]
)

# Remaining Inventory Product
remaining_inv_product = total_inv_product.copy()
remaining_inv_product["Quandity"] = (
    total_inv_product["Quandity"] - total_sal_product["Quandity"]
)

# Remaining Inventory Product Size
remaining_inv_product_size = total_inv_product_size.copy()
remaining_inv_product_size["Quandity"] = (
    total_inv_product_size["Quandity"] - total_sal_product_size["Quandity"]
)

# Remaining Inventory Product Colour
remaining_inv_product_colour = total_inv_product_colour.copy()
remaining_inv_product_colour["Quandity"] = (
    total_inv_product_colour["Quandity"] - total_sal_product_colour["Quandity"]
)

# Remaining Inventory Product Material
remaining_inv_product_material = total_inv_product_material.copy()
remaining_inv_product_material["Quandity"] = (
    total_inv_product_material["Quandity"] - total_sal_product_material["Quandity"]
)

# Colour

colour_order = [
    ("black", 1),
    ("blue", 2),
    ("brown", 3),
    ("grey", 4),
    ("pink", 5),
    ("purple", 6),
    ("white", 7),
    ("yellow", 8),
    ("orange", 9),
]

colour_unique = raw["R_Colour"].unique()
fabric_colour = sorted(colour_unique)

st.markdown("# REMAINING STOCKS :package: ")
st.markdown("## RAW MATERIALS :thread:")
st.markdown("<br>", unsafe_allow_html=True)
rem_raw_col1, rem_raw_col2 = st.columns((2))

with rem_raw_col1:
    rem_raw_col1.markdown("## Material Wise Details")
    fig = px.pie(
        remaining_raw_material, values="R_Qty (kgs)", names="R_Material", hole=0.35
    )
    fig.update_traces(
        text=remaining_raw_material["R_Material"],
        textposition="inside",
        textinfo="value",
    )
    rem_raw_col1.plotly_chart(fig, use_container_width=True)


with rem_raw_col2:
    rem_raw_col2.markdown("## Colour Wise Details")
    colour_unique = raw["R_Colour"].unique()
    fabric_colour = sorted(colour_unique)
    fig = px.bar(
        remaining_raw_material_colour,
        x="R_Material",
        y="R_Qty (kgs)",
        text=[
            "{:,.0f}".format(x) for x in remaining_raw_material_colour["R_Qty (kgs)"]
        ],
        template="seaborn",
        color_discrete_sequence=fabric_colour,
        color="R_Colour",
    )
    rem_raw_col2.plotly_chart(fig, use_container_width=True)


st.markdown("## FINISHED PRODUCTS :shirt:")
st.markdown("<br>", unsafe_allow_html=True)
rem_inv_col1, rem_inv_col2 = st.columns((2))

with rem_inv_col1:
    rem_inv_col1.markdown("## Product Wise Details")
    fig = px.pie(remaining_inv_product, values="Quandity", names="Product", hole=0.35)
    fig.update_traces(
        text=remaining_inv_product["Product"],
        textposition="inside",
        textinfo="value",
    )
    rem_inv_col1.plotly_chart(fig, use_container_width=True)

with rem_inv_col2:
    rem_inv_col2.markdown("## Size Wise Details")
    fig = px.bar(
        remaining_inv_product_size,
        x="Product",
        y="Quandity",
        text=["{:,.0f}".format(x) for x in remaining_inv_product_size["Quandity"]],
        template="seaborn",
        color_discrete_sequence=["yellow", "green", "red", "white"],
        color="Size",
    )
    rem_inv_col2.plotly_chart(fig, use_container_width=True)

with st.expander("MORE DETAILS "):
    rem_inv_col3, rem_inv_col4 = st.columns((2))
    with rem_inv_col3:
        rem_inv_col3.markdown("## Colour Wise Details")
        fig = px.bar(
            remaining_inv_product_colour,
            x="Product",
            y="Quandity",
            text=[
                "{:,.0f}".format(x) for x in remaining_inv_product_colour["Quandity"]
            ],
            template="seaborn",
            color_discrete_sequence=fabric_colour,
            color="Colour",
        )
        rem_inv_col3.plotly_chart(fig, use_container_width=True)

    with rem_inv_col4:
        rem_inv_col4.markdown("## Material Wise Details")
        fig = px.bar(
            remaining_inv_product_material,
            x="Material",
            y="Quandity",
            text=[
                "{:,.0f}".format(x) for x in remaining_inv_product_material["Quandity"]
            ],
            template="seaborn",
            color_discrete_sequence=fabric_colour,
            color="Product",
        )
        rem_inv_col4.plotly_chart(fig, use_container_width=True)
