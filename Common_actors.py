import sys
from imdb import IMDb


def imdb_search(movie):
    # create an instance of the IMDb class
    ia = IMDb()
    movie_list = ia.search_movie(movie)
    if movie_list:  # check if we found a result
        id_movie = movie_list[0].movieID
        cast_movie_id = ia.get_movie(id_movie).get("cast")
        cast_movie_name = [ids.get("name") for ids in cast_movie_id]
        cast_movie_name_line = ", ".join([str(i) for i in cast_movie_name])
        return "Movie found", cast_movie_name_line, cast_movie_name
    else:
        return "Not found", "No cast", ["None"]
