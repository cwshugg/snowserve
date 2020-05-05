# A python program that works with the other programs in this directory to
# listen in on an IPv4 and IPv6 socket to accept client connections
#
#   Connor Shugg
#   May 2020

# Library inclusions
import sys;             # for command-line arguments
import getopt;          # for command-line argument parsing
import threading;       # for multithreading
from time import sleep; # for testing

# Module inclusions
from sockets import SocketListener;
from clients import ClientThread;


# ============================== Server Class =============================== #
# The main server class
class Server:
    # Constructor: takes in a verbose option and a port to bind to, as well as
    # two integers: the number of accepter threads for IPv4, and the number of
    # accepter threads for IPv6. These are set to 1 by default
    def __init__(self, v, p, na4 = 1, na6 = 1):
        # set up the class fields
        self.verbose = v;
        self.port = p;
        
        # set up variables for the accepter threads
        self.accepters4 = [None] * na4;
        self.accepters6 = [None] * na6;

        # create a new SocketListener for both IPv4 and IPv6 (as long as we
        # have at least 1 listener thread for each)
        self.listener4 = None;
        self.listener6 = None;
        if (na4 > 0):
            self.listener4 = SocketListener(self.verbose, self.port, 4);
        if (na6 > 0):
            self.listener6 = SocketListener(self.verbose, self.port, 6);
        # spawn the accepter threads
        self.accepters_spawn();
    
    
    # --------------------- Accepter Thread Management ---------------------- #
    # Spawns two accepter threads - one that listens in on IPv4, and another
    # that listens in on IPv6
    def accepters_spawn(self):
        # spawn the ipv4 accepters
        for i in range(len(self.accepters4)):
            # initialize the thread object and spin it up
            self.accepters4[i] = ListenerThread(self.verbose, self.listener4, i, 4);
            self.accepters4[i].start();

        # spawn the ipv6 accepters
        for i in range(len(self.accepters6)):
            tid = i + len(self.accepters4);
            # initialize the thread object and spin it up
            self.accepters6[i] = ListenerThread(self.verbose, self.listener6, tid, 6);
            self.accepters6[i].start();
    
    # Toggles all the accepter threads' kill switches and joins them
    def accepters_kill(self):
        # toggle all kill switches
        for i in range(len(self.accepters4)):
            self.accepters4[i].kill = True;
        for i in range(len(self.accepters6)):
            self.accepters6[i].kill = True;

        # join all threads
        for i in range(len(self.accepters4)):
            self.accepters4[i].join();
        for i in range(len(self.accepters6)):
            self.accepters6[i].join();


    # -------------------------- Utility Functions -------------------------- #
    # Prints the string only if self.verbose is True
    def vprint(self, msg):
        if (self.verbose):
            print(msg);




# ========================== Listener Thread Class ========================== #
# A class that defines a thread tasked with listening on a given socket for
# client connections
class ListenerThread (threading.Thread):
    # Constructor: takes in a verbose setting, a socket to listen on, a thread
    # id, and an 'address type' - either 4 or 6
    def __init__(self, v, l, t, at):
        # call parent constructor
        threading.Thread.__init__(self, target=self.listen);

        # set up the class fields
        self.verbose = v;
        self.listener = l;
        self.tid = t;
        self.addrtype = at;
        self.kill = False; 

    # The main function listener threads run
    def listen(self):
        self.vprint("Spawned.");
        # iterate until the kill switch is toggled
        while (not self.kill):
            self.vprint("Waiting for next client...");
            csock = self.listener.accept();

            # spawn a new thread to handle the client connection
            cthread = ClientThread(self.verbose, csock, 5);
            cthread.start();

            
        
        self.vprint("Exiting.");

    
    # -------------------------- Utility Functions -------------------------- #
    # Prints the string only if self.verbose is True
    def vprint(self, msg):
        if (self.verbose):
            print("Accepter [ID %d] (IPv%d) %s" % (self.tid, self.addrtype, msg));




# ======================== Main Invocation/Arguments ======================== #
# Parses command-line arguments and gets everything else going by making a new
# socketListener
def main():
    verbose = False;
    port = 13650;
    n4 = 1;
    n6 = 1;

    # attempt to extract arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvp:a:",
                     ["help", "verbose", "port=", "accepters="]);
    # if it fails, print the usage menu and exit
    except getopt.GetoptError:
        usage();
        sys.exit(0);

    # handle each argument one at a time
    for opt, arg in opts:
        if (opt in ("-h", "--help")):           # -h (--help)
            usage();
            sys.exit(0);
        elif (opt in ("-v", "--verbose")):      # -v (--verbose)
            verbose = True;
        elif (opt in ("-p", "--port")):         # -p (--port)
            port = int(arg);
        elif (opt in ("-a", "--accepters")):    # -a (--accepters)
            try:
                threadCounts = arg.split(",");
                n4 = int(threadCounts[0]);
                n6 = int(threadCounts[1]);
            except:
                usage();
                sys.exit(0);
            
        else:                                   # (default)
            usage();
            sys.exit(0);
    
    # set up the new socketListener object
    s = Server(verbose, port, n4, n6);

    # return the socket listener
    return s;


# Usage/help menu function. Prints out a menu that explains to the user how
# to invoke the program
def usage():
    print("\nInvocation Arguments:");
    print("---------------------------------------------------------------------------------------------");
    print(" -h (--help)                             Prints this help menu");
    print(" -v (--verbose)                          Turns the server's verbose mode on");
    print(" -p <p> (--port=<p>)                     Binds sockets to the given port");
    print(" -a <n4>,<n6> (--accepters=<n4>,<n6>)    Runs the server with <n4> and <n6> accepter threads");
    print("---------------------------------------------------------------------------------------------\n");


# =========== Runner Code =========== #
server = main();
#sleep(10);
#server.accepters_kill();

