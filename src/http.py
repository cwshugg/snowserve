# The portion of my web server responsible for parsing HTTP Request messages
# and forming HTTP Response messages
#
#   Connor Shugg
#   May 2020


# ============================== HTTP Parsing =============================== #
# A class that represents an HTTP Request message. The varios properties of the
# connection are broken down into class fields
class HTTPRequest:
    # Constructor: takes in a request string (a string that contains the entire
    # request message in a string)
    def __init__(self, reqstr):
        self.requestString = reqstr;

        # set up default class fields
        self.method = None;
        self.uri = None;
        self.version = 1.0;
        self.headers = [];

        # invoke the parsing function
        self.parse();

    # The main parsing function that uses the request string to read each value
    # of the request message
    def parse(self):
        # wrap the entire parse attemp in a try-catch. Hopefully, some
        # malicious/malformed requests will get caught this way
        try:
            # replace the "\r" with " " to make string parsing easier
            string = self.requestString.replace("\r", " ");
            # split the first line (there should be three strings on the first
            # line, separated by whitespace)
            pieces = string.split(" ", 3);
            # ensure the length is 4 - the three pieces of the top line, and
            # the remaining string of the message
            print(str(pieces));
            if (len(pieces) != 4):
                raise Exception("HTTP top-line parsing error.");

            # set the various information gotten from the top line
            self.method = pieces[0];
            self.uri = pieces[1];
            if ("1.1" in pieces[2]):
                self.version = 1.1;

        except:
            return;
        
        # Creates and returns a string containing all of the request's info
        def toString(self):
            string = "HTTP Request:\n";
            string += "Method:\t" + self.method;
            string += "Target:\t" + self.uri;
            string += "Version:\t" + str(self.version);


req = HTTPRequest("GET / HTTP/1.1\r\nUser-Agent: curl/7.29.0\r\nHost: cedar.rlogin:13650\r\nAccept: */*\r\n\r\n");
