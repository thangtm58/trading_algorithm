import zmq  
import math
import time
import random

# A Context object is instantiated. It is the central object for the socket communication.
context = zmq.Context()  
# The socket itself is defined based on the PUB socket type (“communication pattern”).
socket = context.socket(zmq.PUB)  
# The socket gets bound to the local IP address 
socket.bind('tcp://0.0.0.0:5555')  


class InstrumentPrice(object):
    def __init__(self):
        self.symbol = 'SYMBOL'
        self.t = time.time()
        self.value = 100.
        self.sigma = 0.4
        self.r = 0.01

    def simulate_value(self):
        ''' Generates a new, random stock price.
        '''
        t = time.time()
        dt = (t - self.t) / (252 * 8 * 60 * 60)
        dt *= 500
        self.t = t
        self.value *= math.exp((self.r - 0.5 * self.sigma ** 2) * dt +
                               self.sigma * math.sqrt(dt) * random.gauss(0, 1))
        return self.value