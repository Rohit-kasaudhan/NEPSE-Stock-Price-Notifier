import pandas as pd
import time
from notifier import send_email

# -------------------- NEPSE Price Fetcher --------------------
def get_nepse_current_price(symbol):
    try:
        url = "https://www.merolagani.com/LatestMarket.aspx"
        df = pd.read_html(url)[0]
        match = df[df['Symbol'] == symbol]
        if match.empty:
            print(f"No data found for {symbol}")
            return None
        return float(match['LTP'].values[0])  # Last Traded Price
    except Exception as e:
        print(f"Error fetching NEPSE data: {e}")
        return None

# -------------------- Check and Notify --------------------
def check_and_notify(symbol, target_price, user_email):
    current_price = get_nepse_current_price(symbol)
    if current_price is None:
        return

    print(f"{symbol} current price: Rs. {current_price:.2f}")
    if current_price <= target_price:
        subject = f"🔔 {symbol} dropped to Rs. {current_price:.2f}!"
        body = (
            f"Hey bhai,\n\n{symbol} ka price ab Rs. {current_price:.2f} hai, "
            f"jo tumhare target Rs. {target_price} se kam ya barabar hai.\n\n"
            "Jaldi check kar market ka scene! 🚀📉"
        )
        send_email(subject, body, user_email)
        print("🚨 Email alert sent!")
    else:
        print("✅ Price above target. No alert.")

# -------------------- Main Loop --------------------
if __name__ == "__main__":
    # Example inputs
    symbol = "NABIL"
    target_price = 300.00
    user_email = "ksdrohit28@gmail.com"

    while True:
        check_and_notify(symbol, target_price, user_email)
        print("⏳ Waiting 5 minutes for next check...\n")
        time.sleep(300)  # 5 minutes
