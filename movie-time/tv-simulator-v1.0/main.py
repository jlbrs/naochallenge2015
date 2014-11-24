# NAO Challenge 2014-2015 
# version 1.0
# main file: starts all devices and register everything together!
# Server starts when everything is ready. To stop it, press CTRL+C
# see each module for their description

""" STEP 1
Create the device controller
"""
# Start the general controller
print "[MAIN] Starting controller"
from controller import Controller
controller = Controller()

""" STEP 2
Register all devices (film library, user db and tvplayer) to the controller
"""

# Create the film library - must be done first because userdb and tvplayer need it
print "[MAIN] Creating a new film library"
from movie_library import MovieLibrary
movie_db = MovieLibrary()

print "[MAIN] Registering the film library"
controller.register(movie_db)

# Create the users database
print "[MAIN] Creating a new users database"
from user_database import UserDatabase
user_db = UserDatabase()

print "[MAIN] Registering the users database"
controller.register(user_db)

print "[MAIN] Randomize the database"
user_db._generate_random_tastes_db()

# Create a TV player
print "[MAIN] Creating the TV player"
from tvplayer import TVPlayer
tv = TVPlayer()

print "[MAIN] Registering the TV player"
controller.register(tv)

""" STEP 3
Start the server: open controller to the world!
"""
# Final test
# print "[MAIN] Final list of available actions:"
# print " \t ".join(controller.get_functions())
# print ""

# run the controller!
print "[MAIN] Starting controller"
controller.start_server()

""" STEP 4
Wait for an exception to stop the server and exit
CTRL+C make a KeyboardInterrupt interruption 
"""
try:
    import time
    while(True):
        time.sleep(1)
except:
    controller.stop_server()
