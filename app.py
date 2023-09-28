from pandas.core.arrays import categorical
from pandas.io.pytables import _ensure_encoding
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import os

st.set_page_config(page_title="Analytics", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Details")

# Styles
with open("styles/app.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# READ FROM EXCEL
raw = pd.read_excel("Dataset/Raw_Materials.xlsx")
inv = pd.read_excel("Dataset/Inventory.xlsx")
sal = pd.read_excel("Dataset/Sales.xlsx")

# Raw Date
raw_start = pd.to_datetime(raw["Date"]).min()
raw_end = pd.to_datetime(raw["Date"]).max()


# Inventory Date
inv_start = pd.to_datetime(inv["Date"]).min()
inv_end = pd.to_datetime(inv["Date"]).max()

# Sales Date
sal_start = pd.to_datetime(sal["Date"]).min()
sal_end = pd.to_datetime(sal["Date"]).max()

# Options
option = ["None", "Raw Materials", "Products", "Sales"]


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

colour_unique = inv["Colour"].unique()
fabric_colour = sorted(colour_unique)

dcol1, dcol2, dcol3 = st.columns((3))
with dcol1:
    dcol1.markdown("## Raw Materials")
    dcol1.markdown("<br>", unsafe_allow_html=True)
    dcol1.markdown("### START DATE :calendar:")
    r_start = dcol1.date_input("", raw_start, raw_start, raw_end, format="DD/MM/YYYY")
    r_start = datetime.combine(r_start, datetime.min.time())

    dcol1.markdown("### END DATE :calendar:")
    r_end = dcol1.date_input(" ", raw_end, raw_start, raw_end, format="DD/MM/YYYY")
    r_end = datetime.combine(r_end, datetime.min.time())

with dcol2:
    dcol2.markdown("## FINISHED PRODUCTS")
    dcol2.markdown("<br>", unsafe_allow_html=True)
    dcol2.markdown("### START")
    i_start = dcol2.date_input("  ", inv_start, inv_start, inv_end, format="DD/MM/YYYY")
    i_start = datetime.combine(i_start, datetime.min.time())

    dcol2.markdown("### END DATE :calendar:")
    i_end = dcol2.date_input("   ", inv_end, inv_start, inv_end, format="DD/MM/YYYY")
    i_end = datetime.combine(i_end, datetime.min.time())

with dcol3:
    dcol3.markdown("## SOLD PRODUCTS")
    dcol3.markdown("<br>", unsafe_allow_html=True)
    dcol3.markdown("### START DATE :calendar:")
    s_start = dcol3.date_input("  ", sal_start, sal_start, sal_end, format="DD/MM/YYYY")
    s_start = datetime.combine(s_start, datetime.min.time())

    dcol3.markdown("### END DATE :calendar:")
    s_end = dcol3.date_input("   ", sal_end, sal_start, sal_end, format="DD/MM/YYYY")
    s_end = datetime.combine(s_end, datetime.min.time())

st.markdown("<br><br>", unsafe_allow_html=True)

date_raw = raw[(raw["Date"] >= r_start) & (raw["Date"] <= r_end)].copy()
date_inv = inv[(inv["Date"] >= i_start) & (raw["Date"] <= i_end)].copy()
date_sal = sal[(sal["Date"] >= s_start) & (raw["Date"] <= s_end)].copy()

st.session_state["Raw"] = date_raw
st.session_state["Inv"] = date_inv
st.session_state["Sal"] = date_sal

st.sidebar.markdown("## Options: ")
selected = st.sidebar.selectbox("", options=option)

if selected == "Raw Materials":
    fcol1, fcol2 = st.columns((2))
    st.sidebar.markdown("## Raw Material :thread:")
    material = st.sidebar.multiselect("", date_raw["R_Material"].unique())
    st.sidebar.markdown("## Raw Material Colour :lower_left_paintbrush:")
    if not material:
        raw2 = date_raw.copy()
        check = 0
    else:
        raw2 = date_raw[date_raw["R_Material"].isin(material)]
        check = 1

    colour = st.sidebar.multiselect(" ", raw2["R_Colour"].unique())

    if not colour:
        raw2 = raw2.copy()
    else:
        raw2 = raw2[raw2["R_Colour"].isin(colour)]

    if not material and not colour:
        raw2 = date_raw.copy()

    st.session_state["Raw"] = raw2

    colour_unique = raw2["R_Colour"].unique()
    fabric_colour = sorted(colour_unique)

    category_fabric = raw2.groupby(by=["R_Material"], as_index=False)[
        "R_Qty (kgs)"
    ].sum()
    category_colour = raw2.groupby(by=["R_Material", "R_Colour"], as_index=False)[
        "R_Qty (kgs)"
    ].sum()

    with fcol1:
        fcol1.markdown("## Raw Materials Details")
        fig = px.pie(
            category_fabric, values="R_Qty (kgs)", names="R_Material", hole=0.35
        )
        fig.update_traces(
            text=raw2["R_Material"], textposition="inside", textinfo="value"
        )
        fcol1.plotly_chart(fig, use_container_width=True)

    with fcol2:
        fcol2.markdown("## Colour wise Details")
        if check:
            fig = px.bar(
                category_colour,
                x="R_Material",
                y="R_Qty (kgs)",
                text=["{:,.0f}".format(x) for x in category_colour["R_Qty (kgs)"]],
                template="seaborn",
                color_discrete_sequence=fabric_colour,
                color="R_Colour",
            )
            fcol2.plotly_chart(fig, use_container_width=True)
        else:
            fcol2.plotly_chart(px.bar(), use_container_width=True)
elif selected == "Products":
    fcol1, fcol2 = st.columns((2))
    st.sidebar.markdown("## Products :shirt:")
    product = st.sidebar.multiselect("", date_inv["Product"].unique())
    if not product:
        inv2 = date_inv.copy()
        check = 0
    else:
        inv2 = date_inv[date_inv["Product"].isin(product)]
        check = 1
    st.sidebar.markdown("## Fabric Material :thread:")
    material = st.sidebar.multiselect(" ", inv2["Material"].unique())
    if not material:
        inv3 = inv2.copy()
    else:
        inv3 = inv2[inv2["Material"].isin(material)]
    st.sidebar.markdown("## Size 📏")
    size = st.sidebar.multiselect("  ", inv2["Size"].unique())
    if not size:
        inv4 = inv3.copy()
    else:
        inv4 = inv3[inv3["Size"].isin(size)]
    if not product and not material and not size:
        final_inv = date_inv.copy()
    elif product and not material and not size:
        final_inv = inv3.copy()
    elif product and material and not size:
        final_inv = inv4.copy()
    else:
        final_inv = inv4.copy()
    st.session_state["Inv"] = final_inv
    colour_unique = final_inv["Colour"].unique()
    fabric_colour = sorted(colour_unique)
    category_product = final_inv.groupby(by=["Product"], as_index=False)[
        "Quandity"
    ].sum()
    category_material = final_inv.groupby(by=["Product", "Material"], as_index=False)[
        "Quandity"
    ].sum()
    category_size = final_inv.groupby(by=["Product", "Size"], as_index=False)[
        "Quandity"
    ].sum()
    category_colour = final_inv.groupby(by=["Product", "Colour"], as_index=False)[
        "Quandity"
    ].sum()

    with fcol1:
        fcol1.markdown("## Prouct Details")
        fig = px.pie(category_product, values="Quandity", names="Product", hole=0.35)
        fig.update_traces(
            text=final_inv["Product"], textposition="inside", textinfo="value"
        )
        fcol1.plotly_chart(fig, use_container_width=True)

    with fcol2:
        fcol2.markdown("## Size Wise Details")
        fig = px.bar(
            category_size,
            x="Product",
            y="Quandity",
            text=["{:,.0f}".format(x) for x in category_size["Quandity"]],
            template="seaborn",
            color_discrete_sequence=["yellow", "green", "red", "white"],
            color="Size",
        )
        fcol2.plotly_chart(fig, use_container_width=True)

    with st.expander("MORE DETAILS"):
        fcol3, fcol4 = st.columns((2))
        with fcol3:
            fcol3.markdown("## Material Wise Details")
            fig = px.bar(
                category_material,
                x="Product",
                y="Quandity",
                text=["{:,.0f}".format(x) for x in category_material["Quandity"]],
                template="seaborn",
                color_discrete_sequence=[
                    "white",
                    "green",
                    "yellow",
                    "orange",
                    "lightblue",
                ],
                color="Material",
            )
            fcol3.plotly_chart(fig, use_container_width=True)

        with fcol4:
            fcol4.markdown("## Colour Wise Details")
            fig = px.bar(
                category_colour,
                x="Product",
                y="Quandity",
                text=["{:,.0f}".format(x) for x in category_colour["Quandity"]],
                template="seaborn",
                color_discrete_sequence=fabric_colour,
                color="Colour",
            )
            fcol4.plotly_chart(fig, use_container_width=True)

elif selected == "Sales":
    fcol1, fcol2 = st.columns((3, 1))
    category_product = date_sal.groupby(by=["Product"], as_index=False)[
        "Selling_Price"
    ].sum()
    best_selling_product = (
        date_sal.groupby(by=["Product", "Size"], as_index=False)["Profit_Amount"].sum()
    ).max()
    best_product_profit = str(int(best_selling_product["Profit_Amount"]))
    worst_selling_product = (
        date_sal.groupby(by=["Product", "Size"], as_index=False)["Profit_Amount"].sum()
    ).min()
    worst_product_profit = str(int(worst_selling_product["Profit_Amount"]))
    with fcol1:
        product_colour = ["lightgreen"]
        fig = px.bar(
            category_product,
            x="Product",
            y="Selling_Price",
            text=["₹{:,.0f}".format(x) for x in category_product["Selling_Price"]],
            template="seaborn",
            color_discrete_sequence=product_colour,
            color="Product",
        )
        fcol1.plotly_chart(fig, use_container_width=True)

    with fcol2:
        best, b2 = fcol2.columns((5, 1))
        worst, w2 = fcol2.columns((5, 1))
        with best:
            best.markdown("#### BEST SELLING PRODUCT DETAILS")
            best.markdown(
                "#### Product Name   : " + best_selling_product["Product"].upper()
            )
            best.markdown(
                "#### Product Size   : " + best_selling_product["Size"].upper()
            )
            best.markdown("#### Profit Amount  : ₹" + best_product_profit)
        fcol2.markdown("<br>", unsafe_allow_html=True)
        with worst:
            worst.markdown("#### WORST SELLING PRODUCT DETAILS")
            worst.markdown(
                "#### Product Name  : " + worst_selling_product["Product"].upper()
            )
            worst.markdown(
                "#### Product Size  : " + worst_selling_product["Size"].upper()
            )
            worst.markdown("#### Profit Amount : ₹" + worst_product_profit)
