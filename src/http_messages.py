# The portion of my web server responsible for parsing HTTP request messages
# and putting together HTTP response messages
#
#   Connor Shugg
#   June 2020

# Library inclusions
from enum import IntEnum

# ========================= HTTP Request Error Enum ========================= #
# Stores various values corresponding to parse errors
class HTTPParseError (IntEnum):
    PARSE_ERROR = 1             # generic parsing error
    BAD_METHOD = 2              # bad request method
    BAD_TARGET = 3              # bad target URI
    BAD_VERSION = 4             # bad HTTP/X.X version
    REQUEST_TOO_LONG = 5        # the request was too long


# =========================== HTTP Request Class ============================ #
# A class that defines a single HTTP request message
class HTTPRequest:
    # Constructor: takes in the string making up the request message
    def __init__(self, text):
        self.text = text
        # initialize start line fields
        self.method = None
        self.target = None
        self.version = None
        # initialize headers
        self.headers = {}
        # initialize message body
        self.body = None
        # initialize a new enforcer object
        self.enforcer = HTTPEnforcer()

    # Takes the raw text and parses out the various HTTP fields. Returns 0 on
    # success and a nonzero value on error
    def parse(self):
            # split text by "\r\n" as a delimeter
            lines = self.text.split("\r\n")
    
            # take the first line and parse out the three fields
            start_fields = lines[0].split(" ")
            # request method
            self.method = start_fields[0].strip()
            err = self.enforcer.validate_method(self.method)   # error check
            if (err):
                return err

            # request target
            self.target = start_fields[1].strip()
            err = self.enforcer.validate_target(self.target)   # error check
            if (err):
                return err
            
            # request version
            self.version = start_fields[2].strip()
            self.version = self.version.replace("HTTP/", "")
            # validate the remaining string before parsing as a float
            err = self.enforcer.validate_version(self.version)  # error check
            if (err):
                return err
            # parse version as a float
            self.version = float(self.version)
            
            # iterate through the remaining lines to pick out headers
            lines = lines[1:]
            index = 0
            while (index < len(lines)):
                # check to see if we've exceeded the header limit
                if (index >= self.enforcer.header_limit):
                    return HTTPParseError.REQUEST_TOO_LONG
                
                # if the current line empty, we've gone past the headers
                if (lines[index] == ""):
                    break
                
                # split the line by ": " - if there aren't TWO resulting
                # strings, skip this header
                header = lines[index].split(": ")
                if (len(header) < 2):
                    continue
                # otherwise, add this header to the header dictionary
                else:
                    header[0] = header[0].strip()
                    header[1] = header[1].strip()
                    self.headers[header[0]] = header[1]
                
                index += 1
            
            # at this point, 'index' should be set to the index of the first
            # blank line. If the index is currently at (or before) the second
            # to last position, we can check for a message body
            if (index < len(lines) - 1):
                index += 1      # skip past the "\r\n" line
                self.body = ""  # set the body to be an empty string
                # iterate through the remaining lines and append them all to
                # the message body as one big string
                while (index < len(lines)):
                    self.body += lines[index]
                    index += 1
            
            # if, in the end, the body is still empty, set it back to 'None'
            if (self.body == ""):
                self.body = None
            
            # the parsing was a success - return 0
            return 0



# ========================== HTTP Enforcer Class ============================ #
# A class used to define and enforce rules HTTP requests into the server must
# follow, such as specific methods, specific URLs, etc.
class HTTPEnforcer:
    # Constructor: creates a HTTP enforcer with default rules
    def __init__(self):
        self.header_limit = 64      # the maximum number of allowed headers
        # TODO: Instead of using hardcoded arrays, add in config files
        self.allowed_methods = ["GET", "POST"]
        self.allowed_targets = ["/", "/ifttt"]
        self.allowed_versions = [1.1]
    
    # Takes in a HTTP method and checks to see if it's allowed. Returns a 0
    # on success, and a HTTPParseError on error
    def validate_method(self, method):
        if (method in self.allowed_methods):
            return 0
        else:
            return HTTPParseError.BAD_METHOD
    
    # Takes in a HTTP target URI and checks to see if it's allowed. Returns a
    # 0 on success, and a HTTPParseError on error
    def validate_target(self, target):
        if (target in self.allowed_targets):
            return 0
        else:
            return HTTPParseError.BAD_TARGET
    
    # Takes in a halfway-parsed HTTP version number (should look like "1.1")
    # and determines 1) if it can be parsed, and 2) if the version is accepted
    # by the web server. Returns a 0 on success, and a HTTPParseError on error
    def validate_version(self, version):
        # attempt to convert to an integer
        try:
            version = float(version)
        except:
            return HTTPParseError.BAD_VERSION
        # if the above worked, ensure the version is allowed
        if (version in self.allowed_versions):
            return 0
        else:
            return HTTPParseError.BAD_VERSION

