# Personal Python Webserver
Evidently, I decided that learning how to use pre-existing web servers isn't fun enough, because here we are! I decided to write one in Python instead.

## Threading
This server takes a multithreaded approach. At runtime, the number of "accepter" threads can be specified, both for an IPv4 and IPv6 address. These threads are responsible only for listening in on a socket for connections and spawning client threads.

Client threads are spawned whenever a new request comes in. This thread handles all communication between the client and the server. Once the connection closes, so does the thread.

(**NOTE**: for the moment, I have gone with the somewhat dangerous "spawn a client thread for every connection" approach. I understand this is dangerous in terms of thread-bombing, so I hope to explore other ideas: either imposing a limit on the number of client threads at one time, or taking a new approach entirely.)
