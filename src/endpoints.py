# The portion of my web server responsible for handling URL endpoints. An
# endpoint could be a static file or a script execution
#
#   Connor Shugg
#   September 2020

# Library inclusions
import abc              # "Abstract Base Classes"


# ======================== Endpoint 'Template' Class ======================== #
# This class represents a 'template' for an Endpoint. Endpoints must implement
# this function:
#       assign()        This is what the client thread calls to perform the
#                       endpoint's task. Takes in a HTTPRequest object
#       get_target()    This is used to retrieve the Endpoint's target URL
# Endpoints must also have the following property(s):
#       target          This is the target URL the endpoint is responsible for
#
# Endpoints may have child Endpoints. If a parent Endpoint is assigned a
# request whose target has a child's endpoint at the end of the URL, the parent
# can assign its child the request.
#
# This class is defined as an abstract class. See below for documentation:
# https://docs.python.org/3/library/abc.html
class Endpoint(abc.ABC):
    # Constructor: takes in an optional 'verbose' switch
    def __init__(self, verbose):
        self.verbose = verbose
        self.target = "/"
        self.children = None
    
    # Abstract method whose sole purpose is to return a string: the endpoint's
    # target URL
    @abc.abstractmethod
    def get_target(self):
        return self.target
    
    # An abstract method that takes in an HTTP request, handles it, and returns
    # a HTTPResponse object. This function is used by client threads to "assign"
    # a request to an endpoint.
    @abc.abstractmethod
    def assign(self, request):
        return
    

    # ------------------------- Utility Functions --------------------------- #
    # Prints the string only if self.verbose is True
    def vprint(self, msg):
        if (self.verbose):
            print("Endpoint [%d] %s" % (self.target, msg))


# ======================= Static File Serving Endpoint ====================== #
# A simple static-file-serving endpoint. Defines a server root and serves
def FileEndpoint(Endpoint):
    def __init__(self, verbose):
        # call the parent constructor
        super().__init__(verbose)
        # modify the target
        self.target = "/gimme"
