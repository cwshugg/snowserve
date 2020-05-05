# A collection of python classes used to listen in on both an IPv4 and IPv6
# socket.
#
#   Connor Shugg

# Library inclusions
import socket;              # for sockets


# ================================ Main Class =============================== #
# Python class used to spin up sockets on both IPv4 and IPv6 addresses to
# listen in on a port for client connections
class SocketListener:
    # ---------------------------- Class Setup ------------------------------ #
    # Constructor that takes in a verbose option, a port number, and the type
    # of address to bind to (IPv4 = 4, IPv6 = 6)
    def __init__(self, v, p, t):
        self.verbose = v;
        self.port = p;
        self.addrtype = t;
        # set up the listener socket
        self.setup();
   

    # ------------------------ Socket Setup/Teardown ------------------------ #
    # Creates and binds a socket, then sets the socket to be a listener. IPv4
    # OR IPv6 sockets are set up here, depending on self.addrtype
    def setup(self):
        # set up the socket
        if (self.addrtype == 6):
            self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM);
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

        # bind both sockets to the same hostname, and the given port
        self.socket.bind((socket.gethostname(), self.port));    
        # set both sockets to listen
        self.socket.listen(5);
        
        # make some debug prints
        self.vprint("Bound IPv%d socket: %s to port %d"
                    % (self.addrtype, self.socket.getsockname(), self.port));


    # Closes the socket from setup()
    def close(self):
        # close the sockets
        self.socket.close();
        self.vprint("Closed IPv%d socket" % self.addrtype);


    # -------------------------- Client Accepting --------------------------- #
    # Accepts on the listener's socket. This call will block until a client
    # makes contact. The client's socket will be returned
    def accept(self):
        (csock, addr) = self.socket.accept();
        self.vprint("Accepted client (IPv%d) at %s" % (self.addrtype, str(addr)));
        return csock;
    

    # -------------------------- Utility Functions -------------------------- #
    # Prints the string only if 'verbose' is True
    def vprint(self, msg):
        if (self.verbose):
            print(msg);




# =========== Runner Code =========== #
#sl = SocketListener(True, 13650, 6);
#
#print("Accepting on IPv%d..." % sl.addrtype);
#csock = sl.accept();
#print("csock = %s" % str(csock));
#
#sl.close();
