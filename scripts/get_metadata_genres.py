from os import dup, listdir, makedirs
from os.path import isfile, join, sep, getsize, exists

import urllib
import urllib.request
import re
import json
import string
from unidecode import unidecode
from tqdm.std import tqdm
from collections import defaultdict

import config
from imdb import Cinemagoer
ia = Cinemagoer()

META_DIR = join("scripts", "metadata")
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie/%d?api_key=%s&language=en-US"
TMDB_TV_URL = "https://api.themoviedb.org/3/tv/?api_key=%s&language=en-US&query=%s&page=1"
TMDB_SEARCH_MOVIE_URL = "https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=1"
TMDB_SEARCH_TV_URL = "https://api.themoviedb.org/3/search/tv?api_key=%s&language=en-US&query=%s&page=1"
TMDB_DISCOVER_MOVIE = "https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&page=1&with_genre=%s&adult=false"
# TMDB_ID_URL = "https://api.themoviedb.org/3/find/%s?api_key=%s&language=en-US&external_source=imdb_id"
tmdb_api_key = config.tmdb_api_key
# from imdb to tmdb
genres_map = {
    "Sci-Fi" : "Science Fiction"
}
tmdb_genres_map = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

def get_tmdb_from_id(id, type="movie"):
    if type == "movie":
        base_url = TMDB_MOVIE_URL
        date = "release_date"
        title = "title"
    elif type == "tv":
        base_url = TMDB_TV_URL
        date = "first_air_date"
        title = "name"

    url = base_url % (id, tmdb_api_key)
    response = urllib.request.urlopen(url)
    res_data = response.read()
    movie = json.loads(res_data)

    if title in movie and date in movie and "id" in movie and "overview" in movie:
        data = {
            "title": unidecode(movie[title]),
            "release_date": movie[date],
            "id": movie["id"],
        }
        if "overview" in movie :
            data["overview"] = unidecode(movie["overview"]),
        if "genres" in movie:
            data["genres"] = movie["genres"]
        return data
    else:
        print("Field missing in response")
        return {}

def get_tmdb(name, type="movie"):
    if type == "movie":
        base_url = TMDB_SEARCH_MOVIE_URL
        date = "release_date"
        title = "title"
    elif type == "tv":
        base_url = TMDB_SEARCH_TV_URL
        date = "first_air_date"
        title = "name"

    url = base_url % (tmdb_api_key, urllib.parse.quote(name))
    response = urllib.request.urlopen(url)
    res_data = response.read()
    jres = json.loads(res_data)

    if jres['total_results'] > 0:
        movie = jres['results'][0]
        if title in movie and date in movie and "id" in movie and "overview" in movie:
            return {
                "title": unidecode(movie[title]),
                "release_date": movie[date],
                "id": movie["id"],
                "overview": unidecode(movie["overview"]),
                "genres" : movie["genre_ids"]
            }
        else:
            print("Field missing in response")
            return {}
    else:
        return {}

def discover_tmdb(with_genre="") :
    url = TMDB_DISCOVER_MOVIE % (tmdb_api_key, urllib.parse.quote(with_genre))
    response = urllib.request.urlopen(url)
    res_data = response.read()
    jres = json.loads(res_data)
    print(jres.keys)
    return jres["total_pages"]

#print((discover_tmdb("Action")))


def add_info(mdb, movie):
    t = mdb[movie]
    if ("tmdb" in t):
        t = t["tmdb"]
        if "genres" not in t:
            try : 
                infos = get_tmdb_from_id(t["id"])
                if "genres" in infos :
                    t["genres"] = infos["genres"]
            except:
                print("Failed to get: " + t["title"])
                return None
    return mdb

def read_file():
    with open(join(META_DIR, "clean_meta_genres.json"), "r") as f:
        return json.load(f)

def write_file(mdb) :
    with open(join(META_DIR, "clean_meta_genres.json"), "w") as outfile:
        json.dump(mdb, outfile, indent=4)


def count_films_per_genre(json_data, first_only=False):
    genre_count = defaultdict(int)
    for movie_id, movie_info in json_data.items():
        if 'tmdb' in movie_info and 'genres' in movie_info['tmdb']:
            if first_only and len(movie_info['tmdb']['genres']) > 0:
                genre_count[movie_info['tmdb']['genres'][0]['name']] += 1
            else :
                for genre in movie_info['tmdb']['genres']:
                    genre_count[genre['name']] += 1
    return dict(genre_count)

def count_frommeta():
    with open(join(META_DIR, "clean_meta_genres.json"), "r") as f:
            j = json.load(f)
            c = count_films_per_genre(j)
            print(c)
            c = count_films_per_genre(j, True)
            print(c)


### Get downloaded id
def get_downloaded_id():
    ids = []
    missing = []
    with open(join(META_DIR, "clean_meta_genres.json"), "r") as f:
        movies = json.load(f)
        for movie in movies :
            movie = movies[movie]
            if 'tmdb' in movie :
                ids.append(movie["tmdb"]["id"])
            else:
                missing.append(movie)
    return ids, missing

def get_imdb(name):
    try :
        movies = ia.search_movie(name)
        if len(movies) > 0 :
            id = (movies[0].getID())
            data = ia.get_movie(id)
            d = {"title": data["title"], "id":id}
            if "year" in data:
                d["year"] = data["year"]
            if "genres" in data :
                d["genres"] = data["genres"]
            if "plot" in data:
                d["overview"] = data["plot"]
            if "synopsis" in data :
                d["synopsis"] = data["synopsis"]
            return d
    except:
        return None

def add_dets(mdb = read_file()):
    for movie in tqdm(mdb):
        #add_info(movie)
        if "imdb" not in movie :
            title = mdb[movie]["files"][0]["name"]
            # print(title)
            try :
                mdb[movie]["imdb"] = get_imdb(title) 
            except:
                print("Could't get data for " + title)
    write_file(mdb)

# print(get_tmdb("The Matrix", "movie"))
# print(ia.get_movie(1228705))
