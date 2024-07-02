from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = 'https://letterboxd.com/jack/list/official-top-250-films-with-the-most-fans/'
BASE_URL = 'https://letterboxd.com/'
FILE_NAME_CSV = 'data'


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
        descriptions.append(soap.find('meta', attrs={'name': 'twitter:description'})['content'].replace("\"", ''))
        years_released.append(title_movie_dedicated_web.text.split('(')[1].split(')')[0])
        directors.append(title_movie_dedicated_web.text.split('by')[1].split('•')[0].strip())
    return years_released, directors, descriptions, ratings


def save_to_csv_file(movie_titles: list[str],
                     years_released: list[str],
                     directors: list[str],
                     descriptions: list[str],
                     ratings: list[str]) -> None:
    data_list = []
    for i in range(len(movie_titles)):
        data = {
            'Index': i,
            'Title': movie_titles[i],
            'Release Year': years_released[i],
            'Director': directors[i],
            'Description': descriptions[i],
            'Rating': float(ratings[i])
        }
        data_list.append(data)
    df = pd.DataFrame(data_list)
    df.to_csv(FILE_NAME_CSV + '.csv', index=False)


def main():
    response = requests.get(URL)
    soap = BeautifulSoup(response.text, 'html.parser')
    movies = soap.find_all('div', class_='film-poster')
    movie_titles = [movie['data-target-link'].split('/')[2].replace('-', ' ').title() for movie in movies]
    links = [movie['data-target-link'] for movie in movies]
    years_released, directors, descriptions, ratings = get_years_released_directors_descriptions_ratings(links=links)
    save_to_csv_file(movie_titles, years_released, directors, descriptions, ratings)


if __name__ == '__main__':
    main()
