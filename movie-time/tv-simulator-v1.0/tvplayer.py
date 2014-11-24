################### tvplayer.py #########################
#                                                       #
# This module represents the connected screen (TV). It  #
# is able to play files from a movie database.          #
#                                                       #
# Instanciated by: main.py                              #
#                                                       #
#               NAO CHALLENGE 2014-1015                 #
#               Aldebaran Robotics                      #
#               Jonas Lerebours                         #
#########################################################

from peripheral import Peripheral

class TVPlayer(Peripheral):
    def _start_player(self, file):
        """ This function opens the movie player.
        args:    (string) path to the movie file
        void return
        """
        pass
        
    def _find_file(self, movie):
        """ ask controller for the filename for the movie """
        # trying to find a film library
        try:
            for controller in self.registered_peripherals_controller:
                filename = controller.execute_function("get_movie_filename", [movie])
                if filename:
                    return filename
        except AttributeError:
            print "[TVPlayer] [ERROR] Could not find film, please register me first to a controller that includes a film library."
        return
        
    def play_movie(self, movie, language=False):
        """ This function finds a movie in the DB and plays it.
        args:    (string) movie
        returns: (boolean) playing
        """
        # ask the movie database for the file path
        file = self._find_file(movie)
        if file:
            # play it!
            print "[TVPlayer] Playing movie from "+file
            if language:
                print "[TVPlayer] Adding subtitles in "+language
            self._start_player(file)
            return True
        else:
            print "[TVPlayer] [ERROR] "+movie+" is not available"
            return False

