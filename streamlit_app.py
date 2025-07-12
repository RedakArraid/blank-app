import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# === CONFIGURATION DE L'APPLICATION ===
st.set_page_config(page_title="📊 Rapport des Clics", layout="centered")
st.title("📈 Rapport Visuel des Redirections")
# === URLS DES API ===
API_LINKEDIN = "http://168.231.86.179:8888/api_linkedin.php"
API_GITHUB = "http://168.231.86.179:8888/clicks-api.php"

# === FONCTION DE RÉCUPÉRATION DES DONNÉES ===
@st.cache_data
def fetch_data(url):
    try:
        response = requests.get(url)
        if response.ok:
            return response.json()
        else:
            st.error(f"Erreur HTTP depuis {url}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de l'appel API : {e}")
        return None

# === FORMATAGE DES DONNÉES EN DATAFRAME ===
def format_data(data, destination):
    if not data or "by_day" not in data:
        return pd.DataFrame()

    records = []
    for day, sources in data["by_day"].items():
        for canal, count in sources.items():
            records.append({
                "date": pd.to_datetime(day, format="%Y-%m-%d"),
                "canal": canal,
                "clics": count,
                "destination": destination
            })
    return pd.DataFrame(records)

# === CHARGEMENT DES DONNÉES ===
data_linkedin = fetch_data(API_LINKEDIN)
data_github = fetch_data(API_GITHUB)

df_linkedin = format_data(data_linkedin, "LinkedIn")
df_github = format_data(data_github, "GitHub")
df_all = pd.concat([df_linkedin, df_github]).sort_values("date")

# === SECTION 1 : TOTAUX DES CLICS ===
st.markdown("## 🔢 Totaux des clics")
col1, col2 = st.columns(2)
col1.metric("Vers LinkedIn", f"{df_linkedin['clics'].sum()} clics")
col2.metric("Vers GitHub", f"{df_github['clics'].sum()} clics")

# === SECTION 2 : DIAGRAMMES EN SECTEURS ===
st.markdown("## 📁 Répartition des clics par canal")

col3, col4 = st.columns(2)

with col3:
    if not df_linkedin.empty:
        pie_data = df_linkedin.groupby("canal")["clics"].sum().reset_index()
        fig = px.pie(pie_data, names="canal", values="clics", title="LinkedIn")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Pas de données LinkedIn.")

with col4:
    if not df_github.empty:
        pie_data = df_github.groupby("canal")["clics"].sum().reset_index()
        fig = px.pie(pie_data, names="canal", values="clics", title="GitHub")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Pas de données GitHub.")

# === SECTION 3 : HISTOGRAMMES EMPILÉS ===
st.markdown("## 📅 Histogrammes empilés des clics par jour")

# Choix des destinations à afficher
selected_dest = st.multiselect(
    "Choisir les destinations à afficher :",
    options=["LinkedIn", "GitHub"],
    default=["LinkedIn", "GitHub"]
)

df_filtered = df_all[df_all["destination"].isin(selected_dest)]

if df_filtered.empty:
    st.warning("Aucune donnée disponible.")
else:
    grouped = (
        df_filtered
        .groupby(["date", "destination", "canal"])["clics"]
        .sum()
        .reset_index()
        .sort_values("date")
    )

    fig = px.bar(
        grouped,
        x="date",
        y="clics",
        color="canal",
        facet_row="destination",
        barmode="stack",
        title="Clics empilés par jour, par destination et par canal"
    )
    fig.update_layout(bargap=0.3)

    st.plotly_chart(fig, use_container_width=True)
