################### movie_library.py ####################
#                                                       #
# This module reprensents the user's films library.     #
# All the movies are registered here (and stored as a   #
# csv file, see below), with their metadata such as the #
# type of movie. The TV Player can ask the movie db for #
# the file to play for a given movie.                   #
#                                                       #
# Instanciated by: main.py, user_database.py            #
#                                                       #
#               NAO CHALLENGE 2014-1015                 #
#               Aldebaran Robotics                      #
#               Jonas Lerebours                         #
#########################################################

from database import Database
import csv

class MovieLibrary(Database):
    """ Library (CSV file) contains:
    (1)name ; (*)genres ; (1)filename ; (*)actors ; (1)language
    """
    def __init__(self):
        Database.__init__(self)
        self._generate_movie_db()


    def _generate_movie_db(self):
        """ allows to read movie database from csv file once only """
        filename = "movies.csv"
        # decode movies.csv
        self._storage = dict()
        with open(filename, 'r') as f:
            csv_db = csv.DictReader(f)
            for row in csv_db:
                row['genres'] = row['genres'].split(',')
                row['actors'] = row['actors'].split(',')
                # print row
                title = row['name']
                self._storage[title] = row
    
   
    """
    functions to get a list of movies with a specific criteria
    """
    def get_movies_by_genre(self, genre):
        return self._get_items_by_detail('genres', genre)
        
    def get_movies_by_actor(self, actor):
        return self._get_items_by_detail('actors', actor)
        
    def get_movies_by_language(self, language):
        return self._get_items_by_detail('language', language)
        
        
    """
    functions to get movies details
    """
    def get_movie_filename(self, movie):
        return self._get_item_detail(movie, 'filename')
            
    def get_movie_language(self, movie):
        return self._get_item_detail(movie, 'language')
        
    def get_movie_genres(self, movie):
        return self._get_item_detail(movie, 'genres')
            
    def get_movie_actors(self, movie):
        return self._get_item_detail(movie, 'actors')   
        

    """
    functions to list all existing values
    """
    def get_all_languages(self):
        return self._get_list_details("language")
        
    def get_all_names(self):
        return self._get_list_details("name")
        
    def get_all_actors(self):
        return self._get_list_details("actors")
        
    def get_all_genres(self):
        return self._get_list_details("genres")

        


