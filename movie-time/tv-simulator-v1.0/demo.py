import socket
import sys
import json

HOST, PORT = "localhost", 9999

def send_receive(data):
    try:        
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to server and send data
        sock.connect((HOST, PORT))
        
        # send data
        sock.sendall(json.dumps(data)+"\n")

        # Receive data from the server and shut down
        result = json.loads(sock.recv(1024))
        return result
        
    finally:
        sock.close()   
     
# get a single result
data = ["get_user_language", "user1"]
language = send_receive(data)
print "** Single value returned: " + language
print ""
     
# get a list returned
data = ["get_movie_actors", "film1"]
actors = send_receive(data)
print "** List returned: "+" | ".join(actors)
print ""

# get a boolean returned
data = ["play_movie", "film1"]
result = send_receive(data)
print "** Boolean returned: " + ("True" if result else "False")
print ""

# get an exception (ValueError)
print "** Error: "
data = ["playmovie"]
result = send_receive(data)
print result