from flask import Flask, render_template, url_for, request, redirect

from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # filters_selected = request.form.getlist('filter')
        flats = []
        for i in range(1, 2):
            url = f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={i}&region=1&room1=1&room2=1"
            flats += find_flats_cian(url)

        return render_template("flats_showcase.html", flats=flats)
    else:
        return render_template("index.html")

@app.route('/saved')
def saved():
    return render_template("saved.html")


@app.route('/settings')
def set_filters():
    return render_template("filter_page.html")

@app.route('/dream_flat')
def flat_page():
    return render_template("flat_page.html")

if __name__ == "__main__":
    app.run(debug=True)


def find_flats_cian(url):
    flats = []

    cian_html = requests.get(url).text
    soup = BeautifulSoup(cian_html, features="html.parser")

    offers = soup.select("article[data-name='CardComponent']")

    for offer in offers:
        flat_imgs = set()

        flat_imgs.add(offer.find('img')['src'])
        additional_imgs = offer.select(
            "div[data-name='Gallery']")[0].find_all('img')

        for fa in additional_imgs:
            flat_imgs.add(fa['src'])

        links = offer.find_all('a', {'target': '_blank'})

        flat_name = offer.select(
            "div[data-name='LinkArea']")[0].select("div[data-name='GeneralInfoSectionRowComponent']")[0].text

        flat_price = offer.find("span", {"data-mark" : "MainPrice"}).text

        for a in links:
            if 'https://www.cian.ru/rent/flat/' or 'https://www.cian.ru/sale/flat/' in a['href']:
                if '/cat.php?' not in a['href']:
                    flats.append({"photos": list(flat_imgs), "name": flat_name, "price": flat_price, "link" : a['href']})
                    # flats_dict[a['href']] = flat_phone
                    # flats_dict[a['href']] = flat_description

                    break

    return flats


def find_flats_yandex():
    pass


def find_flats_avito():
    pass


def find_flats_domru():
    pass
