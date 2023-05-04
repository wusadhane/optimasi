import requests
import sqlite3
from bs4 import BeautifulSoup


# mendapatkan data dari web trading view bs4
def getAllContent():
    url = (
        "https://id.tradingview.com/markets/stocks-indonesia/sectorandindustry-sector/"
    )
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return [
        target["href"].split("/")[4].replace("-", " ")
        for target in soup.select(".tv-screener__symbol")
    ]


def spesificContent(target):
    url = (
        "https://id.tradingview.com/markets/stocks-indonesia/sectorandindustry-sector/"
        + target.replace(" ", "-")
    )
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return [target.text for target in soup.select(".tv-screener__symbol")]


# Input ke database

conn = sqlite3.connect("database.db")
c = conn.cursor()


def getSektor():
    url = (
        "https://id.tradingview.com/markets/stocks-indonesia/sectorandindustry-sector/"
    )
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return [
        target["href"].split("/")[4].replace("-", " ")
        for target in soup.select(".tv-screener__symbol")
    ]


def getSubSektor(sektor):
    url = (
        "https://id.tradingview.com/markets/stocks-indonesia/sectorandindustry-sector/"
        + sektor.replace(" ", "-")
        + "/industries/"
    )
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return [
        target["href"].split("/")[4].replace("-", " ")
        for target in soup.select(".tv-screener__symbol")
    ]


def getEmiten(subsektor):
    url = (
        "https://id.tradingview.com/markets/stocks-indonesia/sectorandindustry-industry/"
        + subsektor.replace(" ", "-")
    )
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return [target.text for target in soup.select(".tv-screener__symbol")]


# fungsi sqlite3
# for sektor in getSektor():
#     for subSektor in getSubSektor(sektor):
#         for emiten in getEmiten(subSektor):
#             c.executescript(
#                 f"INSERT INTO sektor VALUES(null,'{sektor}','{subSektor}','{emiten}');"
#             )

# sektors = getSektor()

# for sektor in sektors:
#     subSektors = getSubSektor(sektor)
#     for subSektor in subSektors:
#         emitens = getEmiten(subSektor)
#         for emiten in emitens:
#             c.executescript(
#                 f"INSERT INTO sektor VALUES(null,'{sektor}','{subSektor}','{emiten}');"
#             )

# import time

# sektors = getSektor()

# for sektor in sektors:
#     subSektors = getSubSektor(sektor)
#     for subSektor in subSektors:
#         emitens = getEmiten(subSektor)
#         for emiten in emitens:
#             c.executescript(
#                 f"INSERT INTO data VALUES(null,'{sektor}','{subSektor}','{emiten}');"
#             )
#     time.sleep(100)
