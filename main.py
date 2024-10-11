from datetime import datetime
import smtplib
import requests

#Enter my Lat and Long
MY_LAT=52.517224
MY_LONG=13.471778

#email sender login
my_email = "testyt439@gmail.com"
password = "tvywvibqttdrqajr"


#Get ISS Lat and long
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

def check_overhead():
    if abs(iss_latitude-MY_LAT)<5 and abs(iss_longitude-MY_LONG)<5:
        return True

def check_sundown():
    #Get sunrise and sunset for my location
    parameters = {
        "lat":MY_LAT,
        "lng":MY_LONG,
        "formatted":0
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)
    response.raise_for_status()
    data=response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if (time_now.hour > sunset) or (time_now.hour < sunrise):
        return True

#Send email
def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="colin.rods@gmail.com",
                            msg=f"Subject:ISS notifier!\n\nLook up!"
                            )


if check_overhead() and check_sundown():
    send_email()
