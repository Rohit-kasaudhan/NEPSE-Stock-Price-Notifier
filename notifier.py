import smtplib
from email.message import EmailMessage

def send_email(symbol, current_price, target_price, to_email, direction="Falls below"):
    msg = EmailMessage()

    condition_text = (
        " The share which you were looking for has dropped down" if direction == "Falls below"
        else "The share which you were looking for has risen up"
    )

    subject = f" !! 🔔 {symbol} !! {condition_text} Rs. {target_price}!"
    body = (
        f"Namaste!\n\n"
        f"{symbol}  current price is Rs. {current_price:.2f}, "
        f" {condition_text}.\n\n"
        f"🎯 Target Price: Rs. {target_price}\n"
        f"📊 Current Price: Rs. {current_price:.2f}\n\n"
        f"Have a view of your stocks , These Stocks are not Stable and Fluctuating! 📉📈\n\n"
        f"- NEPSE Alert System"
    )

    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = "ksdrohit28@gmail.com"

    password = "amesbgeriqwjdolh"  # Your Gmail App Password

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login("ksdrohit28@gmail.com", password)
            smtp.send_message(msg)
            print("✅ Email alert sent!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

