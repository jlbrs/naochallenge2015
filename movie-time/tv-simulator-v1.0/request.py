################### Request.py ##########################
#                                                       #
# This module wraps the TCP messages sent/received.     #
# A message is a list of strings. The first cell is a   #
# command string, followed by non-compulsory arguments. #
#                                                       #
# Instanciated by: server.py                            #
#                                                       #
#               NAO CHALLENGE 2014-1015                 #
#               Aldebaran Robotics                      #
#               Jonas Lerebours                         #
#########################################################

import json

class Request():
    """ This class handles message encoding for the TCP server.
    It helps code readability in server.
    """
    def __init__(self):
        self.str_command = ""
        self.list_str_parameters = list()
        
    def parse(self, incoming_request):
        """ This function decodes a request
        arg: (json-encoded data) request coming from client
        returns (boolean) request format is valid
        """
        # Save the original request just in case
        self.original_request = str(incoming_request)
        
        # extract the list from the string
        extracted_list = json.loads(self.original_request)
        
        # the list should contain at least 1 cell
        if len(extracted_list) > 0:
            # first cell is the command
            self.str_command = extracted_list[0].lower()
            # next cells are the args, specific to each command
            self.list_str_parameters = extracted_list[1:]
            return True
            
        else:
            # in case of wrong format, reset and exit
            self.str_command = ""
            self.list_str_parameters = list()
            return False

    def encode(self, data_to_send):
        """ This function encodes a request to send over the network
        arg: (list of strings) request to encode
        returns: (json-encoded data) data to send to client
        """
        return json.dumps(data_to_send)