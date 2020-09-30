# The portion of my web server responsible for handling client connections
# accepted by the accepter threads.
#
#   Connor Shugg
#   May 2020

# Library inclusions
import threading        # for multithreaded client-handling

# Modudle inclusions
from sockets import SocketTalker            # for server-client communication
from http_messages import HTTPRequest       # for request message parsing
from http_messages import HTTPParseError    # for request error checking


# ========================= Client Thread Class ============================= #
# A class that defines a thread tasked with handling a single client connection
class ClientThread (threading.Thread):
    # Constructor: takes in a verbose switch, an accepted client socket, and a
    # thread ID
    def __init__(self, v, csock, t):
        # invoke the parent constructor
        threading.Thread.__init__(self, target=self.converse)

        # set up class fields
        self.verbose = v
        self.talker = SocketTalker(self.verbose, csock)
        self.tid = t
    
    # The main function for a client thread that's used to 'converse' with the
    # client through the client socket
    def converse(self):
        self.vprint("Spawned.")
        
        # read data from the client. If nothing was read, we assume the client
        # has closed the socket: end the connection
        data = self.talker.read()
        if (data == None):
            self.exit()

        # otherwise, we can assume SOME sort of data was read from the socket
        self.transact(data)

        # close the connection and have the thread exit
        self.vprint("Exiting.")
        self.exit()
    
    # The function that's run when the thread exits
    def exit(self):
        # close the socket and return
        self.talker.close()
        return
    
    # Takes in the raw text data and attempts to complete a single transaction
    def transact(self, data):
        # create a HTTPRequest object and parse the message contents
        req = HTTPRequest(str(data, "utf-8"))
        parse_error = req.parse()

        self.talker.write("HTTP 200 OK\r\n\r\nParse Error: %d" % int(parse_error))


    # ------------------------- Utility Functions --------------------------- #
    # Prints the string only if self.verbose is True
    def vprint(self, msg):
        if (self.verbose):
            print("Client [ID %d] %s" % (self.tid, msg))


