from flask import Flask, render_template, url_for, request, redirect, session, abort
from authlib.integrations.flask_client import OAuth
from bs4 import BeautifulSoup
import requests
from constants import CITIES
from parsers import find_flats_cian

app = Flask(__name__)

TOKEN = '9c44622b22e82c8fff6a2661c09cdb0b'


CITIESMAIN = {}

for city, num in CITIES:
    CITIESMAIN[city] = num

appConf = {
    "OAUTH2_CLIENT_ID": "1006174737288-392dr3qihp0l067sielgm0afbdi3iejm.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET": "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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "ef2f1148-c3fb-44d9-ac15-8e168782e497",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)

oauth.register(
    "FlatMap",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email"},
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',

)

@app.route("/google-login")
def googleLogin():
    if "user" in session:
        abort(404)
    return oauth.FlatMap.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))


@app.route("/signin-google")
def googleCallback():
    token = oauth.FlatMap.authorize_access_token()
    session["user"] = token
    return redirect(url_for("registration"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("registration"))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return render_template("filter_page.html")
    else:
        return render_template("index.html")


@app.route('/filters', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        one_room = 1 if request.form.get("one_room") == "on" else 0
        two_rooms = 1 if request.form.get("two_room") == "on" else 0
        three_rooms = 1 if request.form.get("three_room") == "on" else 0
        four_rooms = 1 if request.form.get("four_room") == "on" else 0
        min_price = int(request.form.get("min_price")
                        ) if request.form.get("min_price") != "" else 0
        max_price = int(request.form.get("max_price")) if request.form.get(
            "max_price") != "" else "inf"

        city = CITIESMAIN[request.form.get("location")] if request.form.get(
            "location") != "" else ""

        flats = []
        for i in range(1):
            url_cian = f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={i}&region=1&room1={one_room}&room2={two_rooms}&room3={three_rooms}&room4={four_rooms}&maxprice={max_price}&minprice={min_price}&region={city}"
            url_other = f"https://ads-api.ru/main/api?user=x545275@gmail.com&token={TOKEN}&city={request.form.get('location')}&price1={min_price}&price2={max_price}&&category_id=2&param[2019]={max([one_room, two_rooms, three_rooms, four_rooms])}"
            flats += find_flats_cian(url_cian)

        flats.sort(key=lambda x: x['model_prediction'], reverse=True)

        return render_template("flats_showcase.html", flats=flats)

    else:
        return render_template("filter_page.html")


@app.route('/saved')
def saved():
    return render_template("saved.html")

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

@app.route('/login')
def registration():
    return render_template("registration.html", session=session.get("user"))

@app.route('/dreamflat', methods=['POST'])
def flatpage():
    name = request.form['name']
    price = request.form['price']
    photos = request.form.getlist('photos[]')
    description = request.form['description']
    return render_template('flat_page.html', name=name, price=price, description=description, photos=photos)


if __name__ == "__main__":
    app.run(debug=True)
