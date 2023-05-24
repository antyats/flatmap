from flask import Flask, render_template, url_for, request, redirect
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

CITIES = [['Абакан', '4628'], ['Анадырь', '4634'], ['Анапа', '5129'], ['Архангельск', '4557'], ['Астрахань', '4558'], ['Барнаул', '4555'], ['Белгород', '4561'], ['Биробиджан', '4569'], ['Благовещенск', '4556'], ['Бронницы', '4690'], ['Брянск', '4562'], ['Видный', '5922'], ['Владивосток', '4604'], ['Владикавказ', '4613'], ['Владимир', '4564'], ['Волгоград', '4565'], ['Вологда', '4566'], ['Волоколамск', '5379'], ['Воронеж', '4567'], ['Воскресенск', '5388'], ['Геленджик', '4717'], ['Горно-Алтайск', '4554'], ['Грозный', '4631'], ['Дзержинский', '4734'], ['Дмитров', '5482'], ['Долгопрудный', '4738'], ['Дубна', '4741'], ['Екатеринбург', '4612'], ['Жуковский', '4750'], ['Звенигород', '4756'], ['Иванов', '4570'], ['Ижевск', '4624'], ['Иркутск', '4572'], ['Йошкар-Ола', '4591'], ['Казань', '4618'], ['Калининград', '4574'], ['Калуга', '4576'], ['Кемерово', '4580'], ['Киров', '4581'], ['Коломна', '4809'], ['Королёв', '4813'], ['Кострома', '4583'], ['Красноармейск', '4817'], ['Краснодар', '4584'], ['Краснознаменск', '4822'], ['Красноярск', '4585'], ['Курган', '4586'], ['Курск', '4587'], ['Кызыл', '4622'], ['Липецк', '4589'], ['Лобня', '4848'], ['Лыткарино', '4851'], ['Магадан', '4590'], ['Майкоп', '4553'], ['Махачкала', '4568'], ['Москва', '1'],
          ['Мурманск', '4594'], ['Назрань', '4571'], ['Нальчик', '4573'], ['Нарьян-Мар', '4595'], ['Новгород', '4596'], ['Новороссийск', '4896'], ['Новосибирск', '4598'], ['Омск', '4599'], ['Оренбург', '4600'], ['Орехово-Зуево', '4916'], ['Орёл', '4601'], ['Пенза', '4602'], ['Пермь', '4603'], ['Петрозаводск', '4579'], ['Петропавловск-Камчатский', '4577'], ['Подольск', '4935'], ['Протвино', '4945'], ['Псков', '4605'], ['Пущино', '4949'], ['Реутов', '4958'], ['Ростов-На-Дону', '4606'], ['Рошаль', '4960'], ['Рязань', '4607'], ['Салехард', '4635'], ['Самара', '4608'], ['Санкт-Петербург', '2'], ['Саранск', '4592'], ['Саратов', '4609'], ['Серпухов', '4983'], ['Смоленск', '4614'], ['Сочи', '4998'], ['Ставрополь', '4615'], ['Сургут', '5003'], ['Сыктывкар', '4582'], ['Тамбов', '4617'], ['Тверь', '4619'], ['Тольятти', '5015'], ['Томск', '4620'], ['Тула', '4621'], ['Тюмень', '4623'], ['Улан-Удэ', '4563'], ['Ульяновск', '4625'], ['Уфа', '4560'], ['Фрязино', '5038'], ['Хабаровск', '4627'], ['Ханты-Мансийск', '4629'], ['Химки', '5044'], ['Чебоксары', '4633'], ['Челябинск', '4630'], ['Череповец', '5050'], ['Черкесск', '4578'], ['Чита', '4720'], ['Электросталь', '5064'], ['Элиста', '4575'], ['Южно-Сахалинск', '4611'], ['Якутск', '4610'], ['Ярославль', '4636']]

CITIESMAIN = {}

for city, num in CITIES:
    CITIESMAIN[city] = num


def find_substring(string, substring):
    index = string.find(substring)
    if index != -1:
        words = string[:index].split()
        return words[-1]
    else:
        return str(None)


def find_first_digit(string):
    match = re.search(r'\d+', string)
    if match:
        return match.group()
    else:
        return None


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
        for i in range(1, 2):
            url_cian = f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={i}&region=1&room1={one_room}&room2={two_rooms}&room3={three_rooms}&room4={four_rooms}&maxprice={max_price}&minprice={min_price}&region={city}"
            flats += find_flats_cian(url_cian)

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

        title = offer.select(
            "div[data-name='GeneralInfoSectionRowComponent']")[0].text
        description = offer.select("div[data-name='Description']")[0].text

        flat_rooms = "Хорошая"

        if "1-к" in description or "1-комн." in description or "1-комн" in description or "1-к" in title or "1-комн." in title or "1-комн" in title:
            flat_rooms = "1 комнатная"
        if "2-к" in description or "2-комн." in description or "2-комн" in description or "2-к" in title or "2-комн." in title or "2-комн" in title:
            flat_rooms = "2 комнатная"
        if "3-к" in description or "3-комн." in description or "3-комн" in description or "3-к" in title or "3-комн." in title or "3-комн" in title:
            flat_rooms = "3 комнатная"
        if "4-к" in description or "4-комн." in description or "4-комн" in description or "4-к" in title or "4-комн." in title or "4-комн" in title:
            flat_rooms = "4 комнатная"

        flat_floor = "самом тихом"

        floor_text = find_substring(description, "этаж") + " " + find_substring(
            description, "этаже") + " " + find_substring(title, "этаж") + " " + find_substring(title, "этаже")
        find_floor = find_first_digit(floor_text)

        if find_floor:
            flat_floor = find_floor

        flat_space = "самого удобного размера в"
        space_text = find_substring(description, "м²") + " " + find_substring(
            description, "м²") + " " + find_substring(title, "м²") + " " + find_substring(title, "м²")
        find_space = find_first_digit(space_text)

        if find_space:
            flat_space = find_space

        flat_name = f"{flat_rooms} квартира на {flat_floor} этаже с площадью {flat_space} м²"

        flat_price = offer.find("span", {"data-mark": "MainPrice"}).text

        for a in links:
            if 'https://www.cian.ru/rent/flat/' or 'https://www.cian.ru/sale/flat/' in a['href']:
                if '/cat.php?' not in a['href']:
                    flats.append(
                        {
                            "photos": list(flat_imgs),
                            "name": flat_name,
                            "price": flat_price,
                            "link": a['href'],
                            "description": description,
                            "floor": flat_floor,
                            "space": flat_space,
                            "rooms": flat_rooms,
                        })
                    break

        for i in range(len(flats)):
            flats[i]['index'] = i

    return flats


def find_flats_yandex():
    pass


def find_flats_avito():
    pass


def find_flats_domru():
    pass


if __name__ == "__main__":
    app.run(debug=True)
