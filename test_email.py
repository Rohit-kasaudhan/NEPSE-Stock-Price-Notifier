from notifier import send_email

subject = "📈  NEPSE Stock Price Alert Test"
body = "Hello \n\nThis is a  test email  checking if our alert system is working or not? 🔥"
to_email = "ksdrohit28@gmail.com"  # Apna hi email daal test ke liye

send_email(subject, body, to_email)