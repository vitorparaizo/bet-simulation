import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")


df = pd.read_csv("dataset-bets-nsx-full-rows.csv")
df["bet_date"] = pd.to_datetime(df["bet_date"])
df = df.sort_values("bet_date")

df["Month"] = df["bet_date"].apply(lambda x: str(x.year) + "-" + str(x.month).zfill(2))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="bet_date", y="payout", color="category", title="Payout por dia")
col1.plotly_chart(fig_date, use_container_width=True)

fig_vertical = px.histogram(df_filtered, x="vertical", y="stake_value", color="category",
                            title="Volume de apostas por tipo de vertical", barmode="group")
col2.plotly_chart(fig_vertical, use_container_width=True)

category_total = df_filtered.groupby("category")[["payout"]].sum().reset_index()
fig_category = px.bar(category_total, x="category", y="payout", title="Faturamento por categoria")
col3.plotly_chart(fig_category, use_container_width=True)

fig_result = px.pie(df_filtered, values="stake_value", names="result", title="Distribuição de resultados (stake)")
col4.plotly_chart(fig_result, use_container_width=True)

segment_rating = df_filtered.groupby("segment")[["payout"]].mean().reset_index()
fig_segment = px.bar(segment_rating, x="segment", y="payout", title="Média de payout por segmento")
col5.plotly_chart(fig_segment, use_container_width=True)

# st.markdown("Turnover Por Vertical")

# turnover_df = df_filtered.groupby("vertical").agg(
#     total_stake=pd.NamedAgg(column="stake_value", aggfunc="sum"),
#     total_bets=pd.NamedAgg(column="stake_value", aggfunc="count")
# ).reset_index

# turnover_df["turnover"] = turnover_df["stake_value"] / turnover_df["total_bets"]

# fig_turnover = px.bar(
#     turnover_df,
#     x="turnover",
#     y="turnover",
#     text_auto=".2s",
#     title="Turnover Médio por Vertical",
#     labels={"turnover":"Turnover Médio"},
#     color="vertical"
# )
# st.plotly_chart(fig_turnover, user_container_width=True)
