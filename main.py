import requests
import selectorlib
from emailing import send_email
import time
import sqlite3

connection = sqlite3.connect("data.db")
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
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows

while True:
    if __name__ == "__main__":
        scraped = scrape(URL)
        exctracted = extract(scraped)
        print(exctracted)
        if exctracted != "No upcoming tours":
            row = read(exctracted)
            if not row:
                store(exctracted)
                send_email(exctracted)
        time.sleep(3)
