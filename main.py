import requests
import selectorlib
from emailing import send_email

URL = "http://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    """Scrape the page source from the url"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    exctractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = exctractor.extract(source)["tours"]
    return value


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read():
    with open("data.txt", "r") as file:
        return file.read()

if __name__ == "__main__":
    scraped = scrape(URL)
    exctracted = extract(scraped)
    content = read()
    print(exctracted)
    if exctracted != "No upcoming tours":
        if exctracted not in content:
            store(exctracted)
            send_email(exctracted)
