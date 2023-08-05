# coding=utf-8
import os

from flask import Flask, render_template, send_file
from flask_qrcode import QRcode

app = Flask(
    import_name=__name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)

qrcode = QRcode(app)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    ssid = os.getenv('WIFI_SSID', 'unknown')
    password = os.getenv('WIFI_PASSWORD', 'notset')

    return send_file(
        qrcode(f"WIFI:S:{ssid};T:WPA;P:{password};;", mode="raw"),
        mimetype="image/png"
    )


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


def main():
    app.run(
        host="0.0.0.0",
        debug=int(os.getenv('DEBUG', 0))
    )


if __name__ == '__main__':
    main()




