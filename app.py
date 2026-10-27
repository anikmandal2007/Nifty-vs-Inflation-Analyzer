import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Nifty 50 vs. Inflation Analyzer", layout="wide")

st.title("🇮🇳 Real Wealth & Inflation Analyzer")
st.markdown("Evaluating real purchasing power returns of Indian equities against CPI inflation using the Fisher Equation.")

# Sidebar controls
st.sidebar.header("Parameters")
start_year = st.sidebar.selectbox("Start Year", [2019, 2020, 2021, 2022], index=0)
initial_investment = st.sidebar.number_input("Initial Investment (₹)", min_value=1000, value=100000, step=5000)

@st.cache_data
def load_data():
    # 1. Fetch Nifty 50 monthly close
    nifty = yf.download("^NSEI", start="2019-01-01", end="2024-01-01", interval="1mo", progress=False)
    
    if isinstance(nifty.columns, pd.MultiIndex):
        close_series = nifty['Close']['^NSEI']
    else:
        close_series = nifty['Close']
        
    nifty_df = pd.DataFrame(close_series.resample('MS').first())
    nifty_df.columns = ['Nifty_Close']
    nifty_df.index = nifty_df.index.tz_localize(None)

    # 2. Historical All-India CPI (Combined) index (2012=100)
    cpi_raw = {
        '2019': [139.7, 139.9, 140.4, 141.1, 142.0, 142.9, 144.2, 145.0, 145.8, 147.2, 148.6, 150.4],
        '2020': [150.2, 149.9, 149.8, 151.0, 151.8, 152.6, 154.7, 156.2, 157.9, 159.3, 158.9, 157.3],
        '2021': [156.3, 156.6, 156.8, 157.8, 160.4, 161.3, 162.5, 162.9, 163.2, 165.5, 166.7, 166.2],
        '2022': [165.7, 166.1, 167.7, 170.1, 171.7, 172.6, 174.3, 175.3, 176.7, 178.0, 177.5, 176.4],
        '2023': [176.5, 176.8, 177.2, 178.6, 179.6, 181.3, 186.5, 186.0, 184.1, 185.2, 186.3, 185.7]
    }

    records = []
    for year, values in cpi_raw.items():
        for month_idx, val in enumerate(values, start=1):
            date_str = f"{year}-{month_idx:02d}-01"
            records.append({'Date': pd.to_datetime(date_str), 'CPI': val})

    cpi_df = pd.DataFrame(records).set_index('Date')
    df_combined = nifty_df.join(cpi_df, how='inner').dropna()
    return df_combined

df_raw = load_data()

filter_date = pd.to_datetime(f"{start_year}-01-01")
df = df_raw[df_raw.index >= filter_date].copy()

base_nifty = df['Nifty_Close'].iloc[0]
base_cpi = df['CPI'].iloc[0]

df['Nominal_Wealth'] = (df['Nifty_Close'] / base_nifty) * initial_investment
df['CPI_Inflation_Factor'] = (df['CPI'] / base_cpi)
df['Real_Wealth'] = df['Nominal_Wealth'] / df['CPI_Inflation_Factor']

# Metrics
final_nominal = df['Nominal_Wealth'].iloc[-1]
final_real = df['Real_Wealth'].iloc[-1]
inflation_loss = final_nominal - final_real

col1, col2, col3 = st.columns(3)
col1.metric("Final Nominal Value", f"₹{final_nominal:,.0f}")
col2.metric("Real Purchasing Power", f"₹{final_real:,.0f}")
col3.metric("Inflation Haircut", f"-₹{inflation_loss:,.0f}", delta_color="inverse")

# Interactive Chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.index, y=df['Nominal_Wealth'],
    mode='lines', name='Nominal Wealth (Nifty 50)',
    line=dict(color='#0052cc', width=2.5)
))

fig.add_trace(go.Scatter(
    x=df.index, y=df['Real_Wealth'],
    mode='lines', name='Real Purchasing Power (Adjusted)',
    line=dict(color='#36b37e', width=2.5)
))

fig.add_trace(go.Scatter(
    x=df.index, y=initial_investment * df['CPI_Inflation_Factor'],
    mode='lines', name='CPI Baseline (Cost of Living)',
    line=dict(color='#ff5630', dash='dot', width=1.5)
))

fig.update_layout(
    title=f"Nominal vs. Real Wealth Progression (Starting {start_year})",
    xaxis_title="Date",
    yaxis_title="Portfolio Value (INR)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

st.plotly_chart(fig, use_container_width=True)
