################### controller.py #######################
#                                                       #
# This module registers all available devices and their #
# functions on this server. function names and number   #
# of arguments are tested to validate the received      #
# requests before execution.                            #
#                                                       #
# Instanciated by: main.py                              #
#                                                       #
#               NAO CHALLENGE 2014-1015                 #
#               Aldebaran Robotics                      #
#               Jonas Lerebours                         #
#########################################################

import SocketServer
import threading
from peripheral import Peripheral
from request import Request

class Controller():
    """ Controller class
    A central unit where all possible actions are registered. 
    It can run a TCP server to receive network request and run specific actions. 
    """
    def __init__(self):
        # init all class members
        self.__available_functions = dict()
        self.__serverThread = threading.Thread()

        # Create the server, binding to localhost on port 9999
        HOST, PORT = "localhost", 9999
        self.__server = SocketServer.TCPServer((HOST, PORT), RemoteCommandsHandler)
        self.__server.allow_reuse_address = True
        self.__server.controller = self
        
    def start_server(self):
        """ start_server 
        Call this function to make the server start listening and processing requests
        """
        print "[CONTROLLER] Starting server..."
        if not self.__serverThread.isAlive():
            # start server with server_forever function never returns, so start as new thread
            self.__serverThread = threading.Thread(target = self.__server.serve_forever)
            self.__serverThread.start()
            print "[CONTROLLER] Server started!"
        else:
            print "[CONTROLLER] [ERROR] Server is already started."
        
    def stop_server(self):
        """ stop_server
        Makes the server stop listening.
        """
        print "[CONTROLLER] Stopping server..."
        if self.__serverThread.isAlive():
            # shutdown is the counterpart of serve_forever
            self.__server.shutdown()
            # wait for the thread to finish (when server has stopped)
            self.__serverThread.join()
            print "[CONTROLLER] Server has correctly stopped!"
        else:
            print "[CONTROLLER] [ERROR] Server is not started."
        
    def register(self, peripheral):
        """ register
        This function uses the introspection capabilities of python 
        to look for all the functions in the given class (device) to register
        them. 
        The instance provided will be used when calls are made to its functions.
        arg: instance of a peripheral
        void return
        """        
        # Check if peripheral inherits from the Peripheral class
        if not isinstance(peripheral, Peripheral):
            print "[CONTROLLER] [ERROR] "+str(peripheral)+" is not a proper action."
        
        # List all function (except names starting with _ that are private)
        new_functions = [function for function in dir(peripheral) if function[0] is not "_"]
        
        # Filter already existing functions and add new ones
        for function in new_functions:
            if function in self.__available_functions:
                print "[CONTROLLER] [ERROR] "+str(function)+" already exists."
            else:
                self.__available_functions.update({function: peripheral})
                print "[CONTROLLER] "+function+ " has been registered"
        
        # Backup in the instance to call its function easily
        try:
            peripheral.registered_peripherals_controller.append(self)
        except AttributeError:
            peripheral.registered_peripherals_controller = [self]
    
    def unregister(self, peripheral):
        """ unregister
        removes all function linked with the provided peripheral instance
        """
        # Check if the peripheral is already registered
        for function in self.__available_functions:
            if self.available_function[function] == peripheral:
                del self.available_function[function]
                print "[CONTROLLER] "+function+ " has been unregistered"

    def get_functions(self):
        """ get_functions
        returns the list of all registered functions 
        """
        return self.__available_functions.keys()
    
    def is_function_valid(self, requested_function, arguments_list):
        # Uses introspection to check if the function exists 
        if not requested_function in self.__available_functions:
            print "[PERIPHCONTROLLER] [ERROR] "+requested_function+" does not seem to exist."
            return False
            
        try:
            the_function = getattr(self.__available_functions[requested_function], requested_function)
        except AttributeError:
            print "[PERIPHCONTROLLER] [ERROR] "+requested_function+" is not in "+str(self.__available_functions[requested_function])
            return False

        # Just a quick double-check, see if it is a real function
        if not callable(the_function):
            print "[PERIPHCONTROLLER] [ERROR] "+requested_function+" does not seem to be an available action."
            return False
            
        # and if the requests presents the right number of args.
        function_argcount  = the_function.func_code.co_argcount - 1 #self should not be counted
        request_argcount = len(arguments_list)
        if function_argcount != request_argcount:
            print "[PERIPHCONTROLLER] [ERROR] Request provides "+str(request_argcount)+" argument(s) for "+ requested_function +", while this action requires "+str(function_argcount)+" argument(s)."
            return False
        
        return the_function

    def execute_function(self, requested_function, arguments_list):
        """ execute_function
        check if function and arguments are valid and execute it.
        """
        fnct = self.is_function_valid(requested_function, arguments_list)
        if(fnct):
            # Request validated: run the function!
            print "[CONTROLLER] starting "+requested_function
            return fnct(*arguments_list)
        else:
            return 
         
    def is_request_valid(self, request):
        """ Test if request contains an existing function, and if the number of arguments is 
        correct. It would be more difficult to do such a function in another language than 
        python!
        When a request has been validated, a specific value is stored in it so it is not tested 
        again by execute_request().
        args: (Request) a request to test
        returns (boolean) request validity
        """
        # A request is supposed to have the right format already (checked at request creation time)
        
        # Validate the function inside the request
        the_function = self.is_function_valid(request.str_command, request.list_str_parameters)
        if( the_function ):
            # all the tests passed!
            request.peripherals_controller_validation_passed = True
            request.peripherals_controller_validation_result = the_function
            return True
        else:
            return False
 
    def execute_request(self, request):
        """ execute_request
        This function directly executes requests. The validation also does the function lookup.
        args: (Request) a request
        returns the result of the function
        void return if invalid function
        """
        # First check is request has been validated already
        to_validate = True
        try:
            if request.peripherals_controller_validation_passed:
                to_validate = False
        except AttributeError:
            pass
        
        # If not, try to validate
        if to_validate and not self.is_request_valid(request):
            print "[CONTROLLER] [ERROR] "+requested_function+" is not valid."
            return         
            
        # Request validated: run the function!
        print "[CONTROLLER] Calling "+request.str_command
        return request.peripherals_controller_validation_result(*request.list_str_parameters)
       

class RemoteCommandsHandler(SocketServer.StreamRequestHandler):
    """ Remote Commands Handler
    A very small class that provides the function to process incoming data
    """
    def handle(self):
        """ This function is automatically called by the python library when new data
        are received. All processing on received data should be placed here. In our 
        case, it parses the request then validate and execute it.
        Coding/Decoding received request is deported in the Request class in order to
        simplify the code.
        """
        # New data received
        print "[CONTROLLER] --- SERVER: NEW REQUEST FROM {}".format(self.client_address[0]) + " ---"
        data = self.rfile.readline().strip()
        print "[CONTROLLER] Request: "+data

        # Create a request parser to correctly read the incoming data
        req = Request()
        if not req.parse(data):
            print "[CONTROLLER] [ERROR] Request parser was unable to parse request."
            return
            
        print "[CONTROLLER] Parser extracted command: "+req.str_command
        print "[CONTROLLER] Parser extracted varargs: "+" | ".join(req.list_str_parameters)
        
        # Ask request parser to validate the request
        if not self.server.controller.is_request_valid(req):
            print "[CONTROLLER] Request is not valid"
            return
        
        # Execute the request
        print "[CONTROLLER] Request is valid! Executing..."
        result = self.server.controller.execute_request(req)
        
        # Send result to the client
        print "[CONTROLLER] Got result: " + str(req.encode(result))
        self.wfile.write(req.encode(result))
    
    def finish(self):
        """ This function is automatically called by the python library after handle. It 
        is not compulsory and can be deleted.
        """
        print "[CONTROLLER] ------ End of request handle ------"
        print ""
    
