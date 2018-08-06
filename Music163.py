import requests
from bs4 import BeautifulSoup
import re


def get_music_html():
    urls = "https://music.163.com/#/playlist?id=402924168"
    headers = {
        "Referer":
        "https://music.163.com/",
        "Host":
        "music.163.com",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    music_html = requests.get(urls, headers=headers)
    soup = BeautifulSoup(music_html.text, "lxml")
    #results = soup.find_all('attrs={'id':'song-list-pre-cache'}')#.find_all('li')
    results = soup.find_all('li')
    print(soup)


if __name__ == "__main__":
    get_music_html()