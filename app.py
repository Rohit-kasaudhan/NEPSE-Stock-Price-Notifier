import streamlit as st
import pandas as pd
import requests
import re
from notifier import send_email  # Your email function

# -------------------- Fetch NEPSE Live Prices --------------------
def get_nepse_data():
    try:
        url = "https://www.merolagani.com/LatestMarket.aspx"
        df = pd.read_html(url)[0]
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def get_current_price(symbol):
    df = get_nepse_data()
    match = df[df['Symbol'] == symbol]
    if match.empty:
        return None
    return float(match['LTP'].values[0])  # LTP = Last Traded Price

# -------------------- Email Validation --------------------
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# -------------------- NEPSE Stocks List --------------------
nepse_stocks = {
    
  "Agriculture Development Bank Limited (ADBL)": "ADBL",
  "Api Power Company Ltd. (API)": "API",
  "Arun Kabeli Power Ltd. (AKPL)": "AKPL",
  "Arun Valley Hydropower Development Co. Ltd. (AHPC)": "AHPC",
  "Asian Life Insurance Co. Limited (ALICL)": "ALICL",
  "Bank of Kathmandu Ltd. (BOKL)": "BOKL",
  "Barun Hydropower Co. Ltd. (BARUN)": "BARUN",
  "Best Finance Company Ltd. (BFC)": "BFC",
  "Bottlers Nepal (Balaju) Limited (BNL)": "BNL",
  "Bottlers Nepal (Terai) Limited (BNT)": "BNT",
  "Butwal Power Company Limited (BPCL)": "BPCL",
  "Central Finance Co. Ltd. (CFCL)": "CFCL",
  "Chhimek Laghubitta Bittiya Sanstha Ltd. (CBBL)": "CBBL",
  "Chilime Hydropower Company Limited (CHCL)": "CHCL",
  "Citizen Bank International Limited (CZBIL)": "CZBIL",
  "Citizen Investment Trust (CIT)": "CIT",
  "City Hotel Limited (CITY)": "CITY",
  "Civil Bank Ltd (CBL)": "CBL",
  "Crest Micro Life Insurance Ltd. (CREST)": "CREST",
  "Deva Bikas Bank Limited (DBBL)": "DBBL",
  "Deprosc Laghubitta Bittiya Sanstha Limited (DDBL)": "DDBL",
  "Emerging Nepal Limited (ENL)": "ENL",
  "Everest Bank Limited (EBL)": "EBL",
  "Excel Development Bank Ltd. (EDBL)": "EDBL",
  "First Micro Finance Laghubitta Bittiya Sanstha Limited (FMDBL)": "FMDBL",
  "Garima Bikas Bank Ltd. (GBBL)": "GBBL",
  "Ghorahi Cement Industry Limited (GCIL)": "GCIL",
  "Global IME Bank Limited (GBIME)": "GBIME",
  "Goodwill Finance Co. Ltd. (GFCL)": "GFCL",
  "Guardian Micro-Life Insurance Limited (GMLI)": "GMLI",
  "Guheshowori Merchant Bank & Finance Co. Ltd. (GMFIL)": "GMFIL",
  "Gurkhas Finance Ltd. (GUFL)": "GUFL",
  "Hathway Investment Nepal Limited (HATHY)": "HATHY",
  "Himal Dolakha Hydropower Company Limited (HDHPC)": "HDHPC",
  "Himalayan Bank Limited (HBL)": "HBL",
  "Himalayan Distillery Limited (HDL)": "HDL",
  "Himalayan Life Insurance Limited (HLI)": "HLI",
  "Himalayan Reinsurance Limited (HRL)": "HRL",
  "Himalaya Urja Bikas Company Limited (HURJA)": "HURJA",
  "Hydroelectricity Investment and Development Company Ltd (HIDCL)": "HIDCL",
  "ICFC Finance Limited (ICFC)": "ICFC",
  "IME General Insurance Ltd. (IGI)": "IGI",
  "IME Life Insurance Company Limited (ILI)": "ILI",
  "Janaki Finance Ltd. (JFL)": "JFL",
  "Janata Bank Nepal Ltd. (JBNL)": "JBNL",
  "Jyoti Bikas Bank Limited (JBBL)": "JBBL",
  "Jyoti Life Insurance Ltd (JLI)": "JLI",
  "Kalinchowk Darshan Limited (KDL)": "KDL",
  "Kalika Laghubitta Bittiya Sanstha Limited (KMCDB)": "KMCDB",
  "Kumari Bank Limited (KBL)": "KBL",
  "LIC Nepal Limited (LICN)": "LICN",
  "Machhapuchhre Bank Limited (MBL)": "MBL",
  "Mandakini Hydropower Limited (MHL)": "MHL",
  "Manjushree Finance Ltd. (MFIL)": "MFIL",
  "Miteri Development Bank Limited (MDB)": "MDB",
  "Multipurpose Finance Company Limited (MPFL)": "MPFL",
  "Muktinath Bikas Bank Ltd. (MNBBL)": "MNBBL",
  "Muktinath Krishi Company Limited (MKCL)": "MKCL",
  "Nabil Bank Limited (NABIL)": "NABIL",
  "Neco Insurance Co. Ltd. (NIL)": "NIL",
  "Nepal Bank Limited (NBL)": "NBL",
  "Nepal Credit And Commercial Bank Limited (NCCB)": "NCCB",
  "Nepal Doorsanchar Company Limited (NTC)": "NTC",
  "Nepal Finance Ltd. (NFS)": "NFS",
  "Nepal Hydro Developers Ltd. (NHDL)": "NHDL",
  "Nepal Infrastructure Bank Limited (NIFRA)": "NIFRA",
  "Nepal Insurance Co. Ltd. (NICL)": "NICL",
  "Nepal Investment Bank Limited (NIB)": "NIB",
  "Nepal Khadya Udhyog Limited (NKU)": "NKU",
  "Nepal Life Insurance Company Limited (NLIC)": "NLIC",
  "Nepal Lube Oil Limited (NLO)": "NLO",
  "Nepal Reinsurance Company Limited (NRIC)": "NRIC",
  "Nepal Republic Media Limited (NRM)": "NRM",
  "Nepal SBI Bank Limited (SBI)": "SBI",
  "Nepal Seva Laghubitta Bittiya Sanstha Ltd. (NSEWA)": "NSEWA",
  "Nepal Share Markets Ltd. (NSM)": "NSM",
  "Nepal Trading Limited (NTL)": "NTL",
  "Nepal Vanaspati Ghee Udhyog Limited (NVG)": "NVG",
  "Ngadi Group Power Ltd. (NGPL)": "NGPL",
  "NIC Asia Bank Limited (NICA)": "NICA",
  "NIC Asia Laghubitta Bittiya Sanstha Limited (NICLBSL)": "NICLBSL",
  "Nirdhan Utthan Laghubitta Bittiya Sanstha Limited (NUBL)": "NUBL",
  "NLG Insurance Company Ltd. (NLG)": "NLG",
  "NRN Infrastructure and Development Limited (NRN)": "NRN",
  "NMB Bank Limited (NMB)": "NMB",
  "NMB50 (NMB50)": "NMB50",
  "Om Megashree Pharmaceuticals Limited (OMPL)": "OMPL",
  "Oriental Hotels Limited (OHL)": "OHL",
  "Pokhara Finance Ltd. (PFL)": "PFL",
  "Prabhu Bank Limited (PRVU)": "PRVU",
  "Prabhu Insurance Ltd. (PRIN)": "PRIN",
  "Prabhu Mahalaxmi Life Insurance Limited (PMLI)": "PMLI",
  "Prime Commercial Bank Ltd. (PCBL)": "PCBL",
  "Progressive Finance Limited (PROFL)": "PROFL",
  "Pure Energy Ltd. (PURE)": "PURE",
  "Rastriya Beema Company Limited (RBCL)": "RBCL",
  "Reliable Nepal Life Insurance Limited (RNLI)": "RNLI",
  "Reliance Finance Ltd. (RLFL)": "RLFL",
  "Ridi Hydropower Development Company Ltd. (RIDI)": "RIDI",
  "Sana Kisan Bikas Laghubitta Bittiya sanstha Limited. (SKBBL)": "SKBBL",
  "Sanima Bank Limited (SANIMA)": "SANIMA",
  "Sanima Mai Hydropower Ltd. (SHPC)": "SHPC",
  "Sanima Reliance Life Insurance Limited (SRLI)": "SRLI",
  "Sarbottam Cement Limited (SARBTM)": "SARBTM",
  "Shikhar Insurance Co. Ltd. (SICL)": "SICL",
  "Shivam Cements Limited (SHIVM)": "SHIVM",
  "Shree Investment Finance Co. Ltd. (SIFC)": "SIFC",
  "Soaltee Hotel Limited (SHL)": "SHL",
  "Sonapur Minerals and Oil Limited (SONA)": "SONA",
  "Standard Chartered Bank Nepal Ltd. (SCB)": "SCB",
  "Sun Nepal Life Insurance Company Limited (SNLI)": "SNLI",
  "Sunrise Bank Limited (SRBL)": "SRBL",
  "SuryaJyoti Life Insurance Company Limited (SJLIC)": "SJLIC",
  "Swarojgar Laghubitta Bittiya Sanstha Ltd. (SLBBL)": "SLBBL",
  "Swabhimaan Laghubitta Bittiya Sanstha Ltd. (SWBBL)": "SWBBL",
  "Taragaon Regency Hotel Limited (TRH)": "TRH",
  "Unilever Nepal Limited (UNL)": "UNL",
  "United Finance Ltd. (UFL)": "UFL",
  "United Modi Hydropower Ltd. (UMHL)": "UMHL"


}

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="🇳🇵 NEPSE Stock Price Notifier")
st.title("📈 NEPSE Stock Price Notifier App")
st.caption("Prepared By :- Rohit Kasaudhan ")

# Dropdown for stock selection
selected_stock_name = st.selectbox("Select a NEPSE Stock:", list(nepse_stocks.keys()))
symbol = nepse_stocks[selected_stock_name]

# Show table for current stock info
df = get_nepse_data()
if not df.empty:
    st.subheader("📊 Live NEPSE Market")
    st.dataframe(df[df['Symbol'] == symbol])

# Alert settings
target_price = st.number_input("🎯 Target Price (Rs.):", min_value=1.0)
alert_direction = st.radio("🔔 Alert me when price:", ["Falls below", "Rises above"])
user_email = st.text_input("📧 Enter Your Email:").strip()

# Alert Button
if st.button("🚨 Set Alert"):
    if not symbol or not target_price or not user_email:
        st.error("⚠️ Please fill all the fields.")
    elif not is_valid_email(user_email):
        st.error("❌ Invalid email address.")
    else:
        current_price = get_current_price(symbol)
        if current_price is None:
            st.error("❌ Couldn't fetch NEPSE price. Try again later.")
        else:
            st.info(f"📌 Current Price of {symbol}: Rs. {current_price:.2f}")

            alert_triggered = (
                alert_direction == "Falls below" and current_price <= target_price
            ) or (
                alert_direction == "Rises above" and current_price >= target_price
            )

            if alert_triggered:
                send_email(symbol, current_price, target_price, user_email, alert_direction)
                st.success("✅ Email alert sent successfully!")
            else:
                st.warning("ℹ️ Alert condition not met. No email sent.")
