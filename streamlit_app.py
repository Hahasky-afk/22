
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="US Macro Dashboard", layout="wide")
st.title("🇺🇸 美国宏观经济仪表盘")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "dashboard_dataset.csv")
if not os.path.exists(DATA_PATH):
    st.error("请先运行 fetch_fred_data_enhanced.py 和 process_data.py 抓取并整理数据。")
    st.stop()

df = pd.read_csv(DATA_PATH, parse_dates=["date"], index_col="date")

MODULES = {
    "🏦 利率": ["FEDFUNDS", "GS2", "GS5", "GS10", "GS30", "SOFR", "IORB", "EFFR", "RRPONTSYD"],
    "📈 通胀": ["CPIAUCSL", "CPILFESL", "PPIACO", "WPSFD49207", "PCE", "PCEPILFE"],
    "👷 就业": ["PAYEMS", "UNRATE", "ICSA", "JTSJOL", "CIVPART"],
    "💰 货币": ["M1SL", "M2SL", "WTREGEN", "EXCSRESNS", "RRPONTSYD"],
    "🏛️ 财政": ["GFDEBTN", "FYFSD", "A091RC1Q027SBEA"],
    "🛍️ 消费": ["RSAFS", "PSAVERT", "UMCSENT", "CCLACBW027SBOG"],
    "🏠 房地产": ["USSTHPI", "MORTGAGE30US", "HOUST"],
    "🌐 美元与海外": ["DTWEXBGS"],
    "🏭 制造与贸易": ["NAPM", "IEABC", "IRABC", "INDPRO", "NETEXP"]
}

st.sidebar.header("选择模块")
selected_module = st.sidebar.selectbox("📊 请选择要查看的模块", list(MODULES.keys()))

st.subheader(selected_module)

for code in MODULES[selected_module]:
    if code in df.columns:
        fig = px.line(df, x=df.index, y=code, title=code)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"❗ 数据中缺失：{code}")
