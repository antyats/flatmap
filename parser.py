import requests
from bs4 import BeautifulSoup

def download_image(url):
    try:
        img_data = requests.get(url).content
    except:
        return None

    img_name = url.split('/')[-1]

    file_name = 'bad_images/' + img_name + '.jpg'

    with open(file_name, 'wb') as file:
        file.write(img_data)

def get_images_from_cian():
    for i in range(55):
        print(i)
        url = f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&is_by_homeowner=1&maxprice=1000000&offer_type=flat&p={i}"

        cian_html = requests.get(url).text
        soup = BeautifulSoup(cian_html, features="html.parser")
        offers = soup.select("article[data-name='CardComponent']")

        for offer in offers:
            download_image(offer.find('img')['src'])

get_images_from_cian()