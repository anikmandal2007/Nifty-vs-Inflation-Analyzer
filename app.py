# Cell 1: Install market data scraper
!pip install yfinance plotly pandas -q

# Cell 2: Data retrieval and analysis pipeline
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. Fetch Nifty 50 historical monthly close data
nifty = yf.download("^NSEI", start="2019-01-01", end="2024-01-01", interval="1mo")
nifty_monthly = nifty['Close'].resample('MS').first()
nifty_df = pd.DataFrame(nifty_monthly)
nifty_df.columns = ['Nifty_Close']
nifty_df.index = nifty_df.index.tz_localize(None)

# 2. Historical CPI (Combined) base index (2012=100) benchmark
# Published by MoSPI / Reserve Bank of India
cpi_raw = {
    '2019': [139.7, 139.9, 140.4, 141.1, 142.0, 142.9, 144.2, 145.0, 145.8, 147.2, 148.6, 150.4],
    '2020': [150.2, 149.9, 149.8, 151.0, 151.8, 152.6, 154.7, 156.2, 157.9, 159.3, 158.9, 157.3],
    '2021': [156.3, 156.6, 156.8, 157.8, 160.4, 161.3, 162.5, 162.9, 163.2, 165.5, 166.7, 166.2],
    '2022': [165.7, 166.1, 167.7, 170.1, 171.7, 172.6, 174.3, 175.3, 176.7, 178.0, 177.5, 176.4],
    '2023': [176.5, 176.8, 177.2, 178.6, 179.6, 181.3, 186.5, 186.0, 184.1, 185.2, 186.3, 185.7]
}

# Transform dictionary to monthly time series
records = []
for year, values in cpi_raw.items():
    for month_idx, val in enumerate(values, start=1):
        date_str = f"{year}-{month_idx:02d}-01"
        records.append({'Date': pd.to_datetime(date_str), 'CPI': val})

cpi_df = pd.DataFrame(records).set_index('Date')

# 3. Align datasets and calculate growth
df = nifty_df.join(cpi_df, how='inner').dropna()

# Normalize base investment to 100 at start
df['Nominal_Wealth'] = (df['Nifty_Close'] / df['Nifty_Close'].iloc[0]) * 100
df['CPI_Base_Growth'] = (df['CPI'] / df['CPI'].iloc[0]) * 100

# Exact Fisher Real Wealth Calculation
df['Real_Wealth'] = (df['Nominal_Wealth'] / df['CPI_Base_Growth']) * 100

# 4. Interactive Plotly Visualization
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.index, y=df['Nominal_Wealth'],
    mode='lines', name='Nominal Wealth (Nifty 50)',
    line=dict(color='#0052cc', width=2.5)
))

fig.add_trace(go.Scatter(
    x=df.index, y=df['CPI_Base_Growth'],
    mode='lines', name='Inflation Baseline (CPI)',
    line=dict(color='#ff5630', dash='dot', width=2)
))

fig.add_trace(go.Scatter(
    x=df.index, y=df['Real_Wealth'],
    mode='lines', name='Real Purchasing Power (Adjusted)',
    line=dict(color='#36b37e', width=2.5)
))

fig.update_layout(
    title='Nifty 50 Nominal vs. Real Purchasing Power Return (2019-2023)',
    xaxis_title='Year',
    yaxis_title='Indexed Portfolio Value (Base = 100)',
    template='plotly_white',
    hovermode='x unified',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

fig.show()
