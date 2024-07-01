from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

URL = 'https://letterboxd.com/jack/list/official-top-250-films-with-the-most-fans/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Referer": ""
}

def main():
    response = requests.get(URL)
    soap = BeautifulSoup(response.text, 'html.parser')
    movies = soap.find_all('div', class_='film-poster')
    movie_titles = [movie['data-target-link'].split('/')[2].replace('-', ' ').title() for movie in movies]



if __name__ == '__main__':
    main()