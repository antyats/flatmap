from flask import Flask, render_template, url_for, request, redirect
from constants import CITIES
from parsers import find_flats_cian

app = Flask(__name__)

CITIESMAIN = {}

for city, num in CITIES:
    CITIESMAIN[city] = num


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
            flats += find_flats_cian(url_cian)

        flats.sort(key=lambda x: x['model_prediction'], reverse=True)

        return render_template("flats_showcase.html", flats=flats)

    else:
        return render_template("filter_page.html")


@app.route('/saved')
def saved():
    return render_template("saved.html")


@app.route('/dreamflat', methods=['POST'])
def flatpage():
    name = request.form['name']
    price = request.form['price']
    photos = request.form.getlist('photos[]')
    description = request.form['description']
    return render_template('flat_page.html', name=name, price=price, description=description, photos=photos)


if __name__ == "__main__":
    app.run(debug=True)
