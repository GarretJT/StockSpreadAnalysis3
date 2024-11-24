import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("Stock Spread Analysis")

# Tickers List
tickers = ['MTPS.JK', 'CPRI.JK', 'HRME.JK', 'POSA.JK', 'JAST.JK', 'FITT.JK', 'BOLA.JK', 'CCSI.JK', 'SFAN.JK', 'POLU.JK', 'KJEN.JK', 'KAYU.JK', 'ITIC.JK', 'PAMG.JK', 'IPTV.JK', 'BLUE.JK', 'ENVY.JK', 'EAST.JK', 'LIFE.JK', 'FUJI.JK', 'KOTA.JK', 'INOV.JK', 'ARKA.JK', 'SMKL.JK', 'HDIT.JK', 'KEEN.JK', 'BAPI.JK', 'TFAS.JK', 'GGRP.JK', 'OPMS.JK', 'NZIA.JK', 'SLIS.JK', 'PURE.JK', 'IRRA.JK', 'DMMX.JK', 'SINI.JK', 'WOWS.JK', 'ESIP.JK', 'TEBE.JK', 'KEJU.JK', 'PSGO.JK', 'AGAR.JK', 'IFSH.JK', 'REAL.JK', 'IFII.JK', 'PMJS.JK', 'UCID.JK', 'GLVA.JK', 'PGJO.JK', 'AMAR.JK', 'CSRA.JK', 'INDO.JK', 'AMOR.JK', 'TRIN.JK', 'DMND.JK', 'PURA.JK', 'PTPW.JK', 'TAMA.JK', 'IKAN.JK', 'AYLS.JK', 'DADA.JK', 'ASPI.JK', 'ESTA.JK', 'BESS.JK', 'AMAN.JK', 'CARE.JK', 'SAMF.JK', 'SBAT.JK', 'KBAG.JK', 'CBMF.JK', 'RONY.JK', 'CSMI.JK', 'BBSS.JK', 'BHAT.JK', 'CASH.JK', 'TECH.JK', 'EPAC.JK', 'UANG.JK', 'PGUN.JK', 'SOFA.JK', 'PPGL.JK', 'TOYS.JK', 'SGER.JK', 'TRJA.JK', 'PNGO.JK', 'SCNP.JK', 'BBSI.JK', 'KMDS.JK', 'PURI.JK', 'SOHO.JK', 'HOMI.JK', 'ROCK.JK', 'ENZO.JK', 'PLAN.JK', 'PTDU.JK', 'ATAP.JK', 'VICI.JK', 'PMMP.JK', 'WIFI.JK', 'FAPA.JK', 'DCII.JK', 'KETR.JK', 'DGNS.JK', 'UFOE.JK', 'BANK.JK', 'WMUU.JK', 'EDGE.JK', 'UNIQ.JK', 'BEBS.JK', 'SNLK.JK', 'ZYRX.JK', 'LFLO.JK', 'FIMP.JK', 'TAPG.JK', 'NPGF.JK', 'LUCY.JK', 'ADCP.JK', 'HOPE.JK', 'MGLV.JK', 'TRUE.JK', 'LABA.JK', 'ARCI.JK', 'IPAC.JK', 'MASB.JK', 'BMHS.JK', 'FLMC.JK', 'NICL.JK', 'UVCR.JK', 'BUKA.JK', 'HAIS.JK', 'OILS.JK', 'GPSO.JK', 'MCOL.JK', 'RSGK.JK', 'RUNS.JK', 'SBMA.JK', 'CMNT.JK', 'GTSI.JK', 'IDEA.JK', 'KUAS.JK', 'BOBA.JK', 'MTEL.JK', 'DEPO.JK', 'BINO.JK', 'CMRY.JK', 'WGSH.JK', 'TAYS.JK', 'WMPP.JK', 'RMKE.JK', 'OBMD.JK', 'AVIA.JK', 'IPPE.JK', 'NASI.JK', 'BSML.JK', 'DRMA.JK', 'ADMR.JK', 'SEMA.JK', 'ASLC.JK', 'NETV.JK', 'BAUT.JK', 'ENAK.JK', 'NTBK.JK', 'SMKM.JK', 'STAA.JK', 'NANO.JK', 'BIKE.JK', 'WIRG.JK', 'SICO.JK', 'GOTO.JK', 'TLDN.JK', 'MTMH.JK', 'WINR.JK', 'IBOS.JK', 'OLIV.JK', 'ASHA.JK', 'SWID.JK', 'TRGU.JK', 'ARKO.JK', 'CHEM.JK', 'DEWI.JK', 'AXIO.JK', 'KRYA.JK', 'HATM.JK', 'RCCC.JK', 'GULA.JK', 'JARR.JK', 'AMMS.JK', 'RAFI.JK', 'KKES.JK', 'ELPI.JK', 'EURO.JK', 'KLIN.JK', 'TOOL.JK', 'BUAH.JK', 'CRAB.JK', 'MEDS.JK', 'COAL.JK', 'PRAY.JK', 'CBUT.JK', 'BELI.JK']


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
