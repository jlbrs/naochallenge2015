################ user_database.py #######################
#                                                       #
# This module represents a database containing users'   #
# personal data (here names and tastes only). It could  #
# be online in the cloud, and be based on all social    #
# networks profiling data, so NAO can guess these types #
# automatically!                                        #
#                                                       #
# Instanciated by: main.py                              #
#                                                       #
#               NAO CHALLENGE 2014-1015                 #
#               Aldebaran Robotics                      #
#               Jonas Lerebours                         #
#########################################################


from database import Database
import random

class UserDatabase(Database):
    """ This database contains:
    keys:   (string) username
    values: (list of strings) movie types
    """
    def __init__(self):
        Database.__init__(self)
        
    """
    functions to get details about a user
    """
    def get_user_actors(self, user):
        return self._get_item_detail(user, "actors")
        
    def get_user_language(self, user):
        return self._get_item_detail(user, "language")
        
        
    def _generate_random_tastes_db(self):
        """ This function is meant to be called at initialization, in order to 
        randomize the database. Each user will be randomly assigned one or two 
        movie type(s) to like!
        no arg, void return
        """
        # names are fixed here (from the rules)
        userlist = ["user1", "user2", "user3", "user4", "user5"]
        
        # get existing actors and languages lists from film library
        try:
            for controller in self.registered_peripherals_controller:
                actorslist = controller.execute_function("get_all_actors", [])
                languageslist = controller.execute_function("get_all_languages", [])
        except AttributeError:
            print "[USER DB] [ERROR] Could not generate DB, please register me first to a controller that includes a film library."
            return
        
        # choose random favourite actors list for each user
        for user in userlist:
            # a user can like one or two actors
            nr_actors = int(round(1+random.random()))
            # user a set to have unique elements inside
            choices = set()
            for i in range(nr_actors):
                # select a random item from the tastes list
                random_index = int(round(float(len(actorslist)-1)*random.random()))
                choices.add(actorslist[random_index])
            # store the new user
            self._storage[user] = {'name':user, 'actors':list(choices), 'language':languageslist[int(round(float(len(languageslist)-1)*random.random()))]}     
            # print self._storage[user]