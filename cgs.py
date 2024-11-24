import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("Stock Spread Analysis")

# Tickers List
tickers = ['TOSK.JK', 'MPIX.JK', 'ALII.JK', 'MKAP.JK', 'MEJA.JK', 'LIVE.JK', 'HYGN.JK', 'BAIK.JK', 'VISI.JK', 'AREA.JK', 'MHKI.JK', 'ATLA.JK', 'DATA.JK', 'SOLA.JK', 'BATR.JK', 'SPRE.JK', 'PART.JK', 'GOLF.JK', 'ISEA.JK', 'BLES.JK', 'GUNA.JK', 'LABS.JK', 'DOSS.JK', 'NEST.JK', 'PTMR.JK', 'VERN.JK', 'DAAZ.JK', 'BOAT.JK', 'OASA.JK', 'POWR.JK', 'INCF.JK', 'WSBP.JK', 'PBSA.JK', 'IPOL.JK', 'ISAT.JK', 'ISSP.JK', 'ITMA.JK', 'ITMG.JK', 'JAWA.JK', 'JECC.JK', 'NAIK.JK']


# Remove duplicates
tickers = list(set(tickers))

# Tick rules
def calculate_tick(price):
    if price < 200:
        return 1
    elif 200 <= price < 500:
        return 2
    elif 500 <= price < 2000:
        return 5
    elif 2000 <= price < 5000:
        return 10
    else:
        return 25

# Fetch data
def fetch_data():
    spread_data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data = stock.info
        bid, ask = data.get("bid"), data.get("ask")

        if bid and ask:
            spread = ask - bid
            tick = calculate_tick(bid)
            real_spread = spread - (tick * 2)
            spread_percent = (real_spread / bid) * 100 if bid > 0 else 0
            gain_trade = (real_spread / bid) * 100 if bid > 0 else 0

            spread_data.append({
                "Ticker": ticker, 
                "Bid": bid, 
                "Ask": ask, 
                "Spread": spread, 
                "Real Spread": real_spread, 
                "Spread (%)": spread_percent,
                "Gain/Trade (%)": gain_trade
            })
    return pd.DataFrame(spread_data)

# Fetch data initially
df = fetch_data()

# Display data
st.write("### Spread Data with Gain/Trade (%)")
st.dataframe(df)

# Top 3 by Gain/Trade (%)
st.write("### Top 3 Stocks by Gain/Trade (%)")
st.table(df.nlargest(5, "Gain/Trade (%)"))

# Visualization
if not df.empty:
    st.write("### Gain/Trade (%) Visualization")
    fig, ax = plt.subplots()
    df.dropna().plot.bar(x="Ticker", y="Gain/Trade (%)", ax=ax, color="blue", legend=False)
    plt.title("Gain/Trade (%) per Ticker")
    plt.xlabel("Ticker")
    plt.ylabel("Gain/Trade (%)")
    st.pyplot(fig)

# Refresh button
if st.button("Refresh Data"):
    df = fetch_data()
    st.dataframe(df)
