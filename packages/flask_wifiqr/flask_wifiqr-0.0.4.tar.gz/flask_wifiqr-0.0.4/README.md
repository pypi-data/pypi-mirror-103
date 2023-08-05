# wifiqr

WifiQR is a small flask app that embeds my wifi password in the form of a QR code into home assistant

This is a simple 1 page app that returns a QR image that is recognised by most mobile devices (both Android an iPhone). 
Open your camera app, hold your camera in front of the QR image and wait 
until you are prompted to connect to the WIFI ssid given in the QR.


To run:

```
pip install wifiqr


export WIFI_PASSWORD="some_password
export WIFI_SSID="some_ssid"data

python -m wifiqr
```


