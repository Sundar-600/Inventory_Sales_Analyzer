import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from matplotlib import use
import os

# PAGE CONFIG
st.set_page_config(page_title="SALES", page_icon=":heavy_dollar_sign:", layout="wide")

# STYLES
with open("styles/sales.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

month_list = {
    1: "JAN",
    2: "FEB",
    3: "MAR",
    4: "APR",
    5: "MAY",
    6: "JUN",
    7: "JUL",
    8: "AUG",
    9: "SEP",
    10: "OCT",
    11: "NOV",
    12: "DEC",
}

# READING DATA SETS
sal = pd.read_excel("Dataset/Sales.xlsx")
inv = pd.read_excel("Dataset/Inventory.xlsx")

# Sales Year Wise
sal_year = sal.groupby(sal.Date.dt.year)["Selling_Price", "Quandity", "Profit"].sum()
sal_year["Year"] = sal_year.index

# Profit Year Wise
yearly_profit = sal.groupby(sal.Date.dt.year)["Profit_Amount", "Quandity"].sum()

# Cost Year Wise
inv_year = inv.groupby(inv.Date.dt.year)["Total_Cost", "Quandity"].sum()
inv_year["Year"] = inv_year.index
sal_year["Total_Cost"] = inv_year["Total_Cost"]

# Total Sales Cost Profit
total_sales = sal["Selling_Price"].sum()
total_expenditure = inv["Total_Cost"].sum()
total_profit = sal["Profit_Amount"].sum()

# Year Details
years = sal["Date"].dt.year.unique()
num_of_years = len(years)

# Current Year Details
cur_year = years.max()
cur_year_sal = sal[sal["Date"].dt.year == cur_year]
cur_year_exp = inv[inv["Date"].dt.year == cur_year]

# Sales and Cost of Current Year
cur_year_total = cur_year_sal["Selling_Price"].sum()
cur_year_exp = cur_year_exp["Total_Cost"].sum()
cur_year_profit = cur_year_sal["Profit_Amount"].sum()

# Average Sales
avg_year_sales = total_sales // num_of_years
avg_year_expenditure = total_expenditure // num_of_years

# Need to Validate this formula
diff_cur_sal = round(((avg_year_sales - cur_year_total) / avg_year_sales) * 100, 2)
diff_cur_exp = round(
    ((avg_year_expenditure - cur_year_exp) / avg_year_expenditure) * 100, 2
)

st.sidebar.header("OPTIONS")
option = st.sidebar.selectbox("   ", ["Sales", "Profit"])
ycol1, ycol2 = st.columns((3, 1))
years = np.append(0000, years)
st.sidebar.markdown("## FILTERS")
st.sidebar.markdown("## YEAR")
year = st.sidebar.selectbox("", years)
if option == "Sales":
    if year == 0:
        st.session_state["Sal"] = sal
        with ycol1:
            ycol1.markdown("## YEARLY SALES & COSTS")
            fig = px.line()
            fig.add_scatter(
                x=sal_year["Year"], y=sal_year["Selling_Price"], name="Sales"
            )
            fig.update_traces(line_color="lightgreen", selector=dict(name="Sales"))
            fig.add_scatter(
                x=sal_year["Year"], y=sal_year["Total_Cost"], name="Expenditure"
            )
            fig.update_traces(line_color="orange", selector=dict(name="Expenditure"))
            ycol1.plotly_chart(fig, use_container_width=True)
        with ycol2:
            tsal, csal = ycol2.columns((2))
            with tsal:
                tsal.markdown("### Total Sales")
                tsal.metric("", value=f"₹ {total_sales}")
            with csal:
                csal.markdown(f"### {cur_year} Sales")
                csal.metric("", value=f"₹ {cur_year_total}", delta=f"₹ {diff_cur_sal}%")
            texp, cexp = ycol2.columns((2))
            with texp:
                texp.markdown("### Total Costs")
                texp.metric("", value=f"₹ {total_expenditure}")
            with cexp:
                cexp.markdown(f"### {cur_year} Costs")
                cexp.metric(
                    " ",
                    value=f"₹ {cur_year_exp}",
                    delta=f"₹ {diff_cur_exp}%",
                    delta_color="inverse",
                )
    else:
        ycol1.markdown(f"## {year} SALES & COSTS")
        sal2 = sal[(sal["Date"].dt.year) == year]
        inv2 = inv[(inv["Date"].dt.year) == year]
        st.session_state["Sal"] = sal2
        sal_month = sal2.groupby(sal2.Date.dt.month)[
            "Selling_Price", "Quandity", "Profit"
        ].sum()
        sal_month["Month"] = month_list
        inv_month = inv2.groupby(inv2.Date.dt.month)["Total_Cost", "Quandity"].sum()
        inv_month["Month"] = inv_month.index

        sal_month["Total_Cost"] = inv_month["Total_Cost"]

        st.sidebar.subheader("MONTH")
        yearly_sales = sal2["Selling_Price"].sum()
        yearly_expenditure = inv2["Total_Cost"].sum()

        diff_yearly_sales = round(
            ((yearly_sales - avg_year_sales) / avg_year_sales) * 100, 2
        )
        diff_yearly_expenditure = round(
            ((yearly_expenditure - avg_year_expenditure) / avg_year_expenditure) * 100,
            2,
        )

        with ycol1:
            fig = px.line()
            fig.add_scatter(
                x=sal_month["Month"], y=sal_month["Selling_Price"], name="Sales"
            )
            fig.update_traces(line_color="lightgreen", selector=dict(name="Sales"))
            fig.add_scatter(
                x=sal_month["Month"], y=sal_month["Total_Cost"], name="Expenditure"
            )
            fig.update_traces(line_color="orange", selector=dict(name="Expenditure"))
            ycol1.plotly_chart(fig, use_container_width=True)
        with ycol2:
            tsal, csal = ycol2.columns((2))
            with tsal:
                tsal.markdown("### Total Sales")
                tsal.metric("", value=f"₹ {total_sales}")
            with csal:
                csal.markdown(f"### {year} Sales")
                csal.metric(
                    "", value=f"₹ {yearly_sales}", delta=f"₹ {diff_yearly_sales}%"
                )
            texp, cexp = ycol2.columns((2))
            with texp:
                texp.markdown("### Total Costs")
                texp.metric("", value=f"₹ {total_expenditure}")
            with cexp:
                cexp.markdown(f"### {year} Costs")
                cexp.metric(
                    " ",
                    value=f"₹ {yearly_expenditure}",
                    delta=f"₹ {diff_yearly_expenditure}%",
                    delta_color="inverse",
                )

        months = sal2["Date"].dt.month.unique()
        num_of_months = len(months)
        avg_month_sales = yearly_sales // num_of_months
        avg_month_expenditure = yearly_expenditure // num_of_months
        months = np.append(0000, months)
        month = st.sidebar.selectbox(" ", months)
        if month == 0:
            pass
        else:
            this_month = month_list.get(month)
            mcol1, mcol2 = st.columns((3, 1))
            sal3 = sal2[(sal2["Date"].dt.month) == month]
            st.session_state["Sal"] = sal3
            inv3 = inv2[(inv2["Date"].dt.month) == month]
            sal3 = sal3.groupby(by=["Date"], as_index=False)["Selling_Price"].sum()
            inv3 = inv3.groupby(by=["Date"], as_index=False)["Total_Cost"].sum()
            inv3 = inv3.sort_values(by="Date")
            sal3 = sal3.sort_values(by="Date")
            this_month_sales = sal3[sal3["Date"].dt.month == month][
                "Selling_Price"
            ].sum()
            this_month_expenditure = inv3[inv3["Date"].dt.month == month][
                "Total_Cost"
            ].sum()

            diff_month_sales = round(
                ((this_month_sales - avg_month_sales) / avg_month_sales) * 100, 2
            )
            diff_month_expenditure = round(
                (
                    (this_month_expenditure - avg_month_expenditure)
                    / avg_month_expenditure
                )
                * 100,
                2,
            )

            with mcol1:
                mcol1.markdown(f"## {this_month} SALES & COSTS")
                fig = px.line()
                fig.add_scatter(x=sal3["Date"], y=sal3["Selling_Price"], name="Sales")
                fig.update_traces(line_color="green", selector=dict(name="Sales"))
                fig.add_scatter(
                    x=inv3["Date"], y=inv3["Total_Cost"], name="Expenditure"
                )
                fig.update_traces(
                    line_color="orange", selector=dict(name="Expenditure")
                )
                mcol1.plotly_chart(fig, use_container_width=True)
            with mcol2:
                scol1, scol2 = mcol2.columns((2))
                with scol1:
                    scol1.markdown(f"### {year} Sales")
                    scol1.metric("", value=f"₹ {yearly_sales}")
                with scol2:
                    scol2.markdown(f"### {this_month} Sales")
                    scol2.metric(
                        " ", f"₹ {this_month_sales}", delta=f"{diff_month_sales}%"
                    )
                ecol1, ecol2 = mcol2.columns((2))
                with ecol1:
                    ecol1.markdown(f"### {year} Costs")
                    ecol1.metric("", value=f"₹ {yearly_expenditure}")
                with ecol2:
                    ecol2.markdown(f"### {this_month} Costs")
                    ecol2.metric(
                        " ",
                        value=f"₹ {this_month_expenditure}",
                        delta=f"{diff_month_expenditure}%",
                        delta_color="inverse",
                    )

else:
    if year == 0:
        with ycol1:
            ycol1.markdown(f"## YEARLY PROFIT")
            fig = px.line()
            fig.add_scatter(
                x=yearly_profit.index, y=yearly_profit["Profit_Amount"], name="Profit"
            )
            fig.update_traces(line_color="lightgreen")
            ycol1.plotly_chart(fig, use_container_width=True)
        with ycol2:
            pcol1, pcol2 = ycol2.columns((5, 1))
            ccol1, ccol2 = ycol2.columns((5, 1))
            with pcol1:
                pcol1.markdown("## Total Profit")
                pcol1.metric("", value=f"₹ {total_profit}")
            with ccol1:
                ccol1.markdown(f"## {cur_year} Profit")
                ccol1.metric(" ", value=f"₹ {cur_year_profit}")
    else:
        ycol1.markdown(f"## {year} PROFIT")
        prof = sal[(sal["Date"].dt.year) == year]
        profit_month = prof.groupby(prof.Date.dt.month)[
            "Profit_Amount", "Quandity"
        ].sum()
        profit_month["Month"] = month_list
        st.sidebar.subheader("MONTH")
        yearly_profit = prof["Profit_Amount"].sum()
        with ycol1:
            fig = px.line()
            fig.add_scatter(
                x=profit_month.index, y=profit_month["Profit_Amount"], name="Profit"
            )
            fig.update_traces(line_color="green", selector=dict(name="Profit"))
            ycol1.plotly_chart(fig, use_container_width=True)
        with ycol2:
            tpcol1, tpcol2 = ycol2.columns((5, 1))
            mpcol1, mpcol2 = ycol2.columns((5, 1))
            with tpcol1:
                tpcol1.markdown("### Total Profit")
                tpcol1.metric("", value=f"₹ {total_profit}")
            with mpcol1:
                mpcol1.markdown(f"### {year} Profit")
                mpcol1.metric("", value=f"₹ {yearly_profit}")

        months = prof["Date"].dt.month.unique()
        months = np.append(0000, months)
        month = st.sidebar.selectbox(" ", months)
        if month == 0:
            pass
        else:
            this_month = month_list.get(month)
            this_month_profit = prof[(prof["Date"].dt.month == month)][
                "Profit_Amount"
            ].sum()
            mcol1, mcol2 = st.columns((3, 1))
            prof2 = prof[(prof["Date"].dt.month) == month]
            prof2 = prof2.groupby(by=["Date"], as_index=False)["Profit_Amount"].sum()
            prof2 = prof2.sort_values(by="Date")
            with mcol1:
                mcol1.markdown(f"## {this_month} PROFIT")
                fig = px.line()
                fig.add_scatter(x=prof2["Date"], y=prof2["Profit_Amount"])
                fig.update_traces(line_color="green")
                mcol1.plotly_chart(fig, use_container_width=True)
            with mcol2:
                typcol1, typcol2 = mcol2.columns((5, 1))
                tmpcol1, tmpcol2 = mcol2.columns((5, 1))
                with typcol1:
                    typcol1.markdown(f"## {year} PROFIT")
                    typcol1.metric("", value=f"₹ {yearly_profit}")
                with tmpcol1:
                    tmpcol1.markdown(f"## {this_month} PROFIT")
                    tmpcol1.metric(" ", value=f"₹ {this_month_profit}")
