import requests
from bs4 import BeautifulSoup
import smtplib
import os

PERSONAL_EMAIL = os.environ.get("PERSONAL_EMAIL")
MY_YAHOO = os.environ.get("MY_YAHOO")
YAHOO_SMTP = "smtp.mail.yahoo.com"
YAHOO_PASS = os.environ.get("YAHOO_PASS")


surf_forecast_nazare = "https://www.surf-forecast.com/breaks/Nazare/forecasts/latest/six_day"

# Get response from surf-forecast.com for Nazare
response = requests.get(surf_forecast_nazare)
nazare_page = response.text

# Convert text data to beautiful soup
soup = BeautifulSoup(nazare_page, "html.parser")

# Find forecast table
forecast_table = soup.find(class_="forecast-table")
# Find swell height and direction data
wave_data = forecast_table.find_all(class_="swell-icon")
# Separate height (m) from direction data, create list of all wave heights
wave_heights = []
for wave in wave_data:
    all = wave.text
    height = float(all.translate({ord(i): None for i in 'NSEW'}))
    wave_heights.append(height)

# big_swell function to state whether there's big_swell incoming (6m or more?)
def big_swell():
    if max(wave_heights) >= 6:
        pumping = True
    else:
        pumping = False
    return pumping

# Send email function, sends notification if big_swell is true
if big_swell():
    with smtplib.SMTP(YAHOO_SMTP) as connection:
        connection.starttls()
        connection.login(user=MY_YAHOO, password=YAHOO_PASS)
        connection.sendmail(
            from_addr=MY_YAHOO,
            to_addrs=PERSONAL_EMAIL,
            msg=f"Subject:Big Swell Coming to Nazare!\n\nNazare has some swell coming in the next 12 days.\n{max(wave_heights)}m waves expected.\nMore details here: https://www.surf-forecast.com/breaks/Nazare/forecasts/latest/six_day"
        )
    print("Email sent")
else:
    print(f"Email not sent, waves only {max(wave_heights)}m")
    pass
