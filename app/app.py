
import os
import pickle
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_data():
    fp = pd.read_csv(os.path.join(BASE, "data/processed/city_fingerprint.csv"))
    sim = pd.read_csv(os.path.join(BASE, "data/processed/city_similarity.csv"), index_col=0)
    cities = pd.read_csv(os.path.join(BASE, "outputs/city_cluster.csv"))
    summary = pd.read_csv(os.path.join(BASE, "outputs/cluster_summary.csv"))
    return fp, sim, cities, summary

st.set_page_config(page_title="Pollution Fingerprint Explorer", layout="wide")

st.title("🌍 Pollution Fingerprint Explorer")
st.caption("Explore city-level air-pollution profiles, clusters and similar cities.")

fp, sim, cities, summary = load_data()

city = st.selectbox("Select city", sorted(fp["city"].unique()))
row = fp[fp["city"] == city].iloc[0]
cluster = int(row["cluster"])

c1, c2, c3 = st.columns(3)
c1.metric("City", city)
c2.metric("Cluster", cluster)
c3.metric("Cities in cluster", int((fp["cluster"] == cluster).sum()))

pollutants = ["pm25", "pm10", "no2", "so2", "o3", "co"]
zcols = [f"{p}_z" for p in pollutants]

left, right = st.columns(2)

with left:
    values = [row[c] for c in zcols]
    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=[p.upper() for p in pollutants] + [pollutants[0].upper()],
        fill="toself",
        name=city
    ))
    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title="Pollution Fingerprint"
    )
    st.plotly_chart(radar, use_container_width=True)

with right:
    profile = row[zcols].sort_values(ascending=False)
    chart = pd.DataFrame({
        "pollutant": [x.replace("_z", "").upper() for x in profile.index],
        "z_score": profile.values
    })
    fig = px.bar(
        chart,
        x="z_score",
        y="pollutant",
        orientation="h",
        title="Standardized pollutant levels"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("🔎 Similar Cities")
similar = sim[city].drop(city).sort_values(ascending=False).head(10)
sim_table = similar.rename("similarity").reset_index()
sim_table.columns = ["city", "similarity"]
sim_table["similarity"] = (sim_table["similarity"] * 100).round(1)
st.dataframe(sim_table, use_container_width=True, hide_index=True)

st.subheader("🌍 Global Cluster Map")
fig_map = px.scatter_geo(
    cities,
    lat="latitude",
    lon="longitude",
    color="cluster",
    hover_name="city",
    hover_data=["country", "cluster"],
    title="Global Pollution Profile Clusters"
)
fig_map.update_layout(geo=dict(showland=True))
st.plotly_chart(fig_map, use_container_width=True)

st.subheader("Cluster Profile")
st.dataframe(
    summary[summary["cluster"] == cluster],
    use_container_width=True,
    hide_index=True
)
