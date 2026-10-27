# 🇮🇳 Real Wealth & Inflation Analyzer (India)

An interactive financial economics application tracking the **Nominal vs. Real Purchasing Power Return** of the Nifty 50 Index adjusted for All-India CPI (Combined) inflation.

## 📌 Overview
Headline nominal stock market returns often mask true wealth growth. This tool applies the **Fisher Equation** to empirically decouple real economic purchasing power expansion from monetary inflation.

## 🧮 Mathematical Framework
Real returns are calculated using the discrete Fisher relationship:
$$1 + r_{\text{real}} = \frac{1 + r_{\text{nominal}}}{1 + i}$$

Where:
- $r_{\text{nominal}}$: Nominal price return of the Nifty 50 Index
- $i$: CPI (Combined) cumulative rate of inflation
- $r_{\text{real}}$: Effective purchasing power return

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Streamlit, Pandas, Plotly, yfinance
- **Data Sources:** Yahoo Finance API (`^NSEI`), Reserve Bank of India / MoSPI CPI Index

## 🚀 Live Demo
Access the interactive dashboard here: [Live Streamlit App](YOUR_STREAMLIT_APP_URL_HERE)
