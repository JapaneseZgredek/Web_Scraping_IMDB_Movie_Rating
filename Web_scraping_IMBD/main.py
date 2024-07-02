from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

URL = 'https://letterboxd.com/jack/list/official-top-250-films-with-the-most-fans/'
BASE_URL = 'https://letterboxd.com/'


def get_years_released_directors_descriptions_ratings(links: list[str]) -> tuple[list[str], list[str], list[str], list[str]]:
    years_released = []
    directors = []
    descriptions = []
    ratings = []
    for link in links:
        response = requests.get(BASE_URL + link)
        soap = BeautifulSoup(response.text, 'html.parser')
        title_movie_dedicated_web = soap.find('title')
        ratings.append(soap.find('meta', attrs={'name': 'twitter:data2'})['content'][:4])
        descriptions.append(soap.find('meta', attrs={'name': 'twitter:description'})['content'])
        years_released.append(title_movie_dedicated_web.text.split('(')[1].split(')')[0])
        directors.append(title_movie_dedicated_web.text.split('by')[1].split('•')[0].strip())
    return years_released, directors, descriptions, ratings


def main():
    response = requests.get(URL)
    soap = BeautifulSoup(response.text, 'html.parser')
    movies = soap.find_all('div', class_='film-poster')
    movie_titles = [movie['data-target-link'].split('/')[2].replace('-', ' ').title() for movie in movies]
    links = [movie['data-target-link'] for movie in movies]
    years_released, directors, descriptions, ratings = get_years_released_directors_descriptions_ratings(links=links)
    print(ratings)
    print(descriptions)

if __name__ == '__main__':
    main()