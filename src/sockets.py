# A collection of python classes used to listen in on both an IPv4 and IPv6
# socket.
#
# Helpful documentation: https://docs.python.org/3/library/socket.html
#
#   Connor Shugg
#   May 2020

# Library inclusions
import socket;              # for sockets

# ============================= Listener Class ============================== #
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
        
        # use getaddrinfo() to find an IPv4/6 address to bind to (only TCP)
        # NOTE: on Azure VMs, I can't seem to be able to bind to an IPv6 socket
        # in this way. It must be something to do with how I set it up.
        for addrinfo in socket.getaddrinfo(socket.gethostname(), self.port,
                                           family=self.socket.family,
                                           proto=socket.IPPROTO_TCP):
            # take the first address found that has the protocol and family
            # we specified, and bind the socket to it. Then, exit the loop
            chosen_address = addrinfo[4]
            self.socket.bind(chosen_address)
            break

        # set the socket to listen
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




# ============================== Talker Class =============================== #
# A class used by client threads to read from and write to a client socket.
class SocketTalker:
    # Constructor: takes in a verbose setting and a client socket
    def __init__(self, v, csock):
        # set up class fields
        self.verbose = v;
        self.socket = csock;
   
    # Closes the client socket
    def close(self):
        self.socket.close();


    # ---------------------- Socket Reading/Writing ------------------------- #
    # Calls recv() on the client socket, and returns the read-in data. If the
    # socket has been closed, None is returned
    def read(self, limit = 1024):
        data = self.socket.recv(limit);
        # if the socket is closed, return None
        if (not data):
            return None;
        # otherwise, return the data
        return data;
    
    # Takes a given message and writes it to the client socket
    def write(self, msg):
        self.socket.sendall(bytes(msg, encoding="utf8"));


    # ------------------------- Utility Functions --------------------------- #
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
