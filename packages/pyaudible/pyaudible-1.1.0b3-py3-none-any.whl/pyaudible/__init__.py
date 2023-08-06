# PyAudible : Sending and Receiving Data using Audible Sound

#

'''
A Python library for sending and receiving data using audible sound. 
PyAudible includes a transmitter and a receiver module that could be 
implemented on multiple devices, enables the transmission of small 
amounts of data between separated systems in the vicinity.

The library implements a Multi-channel Carrier Modulation protocol, allows 
a configurable transmitting speed between 5 - 20 bytes/sec. It uses Cyclic 
Redundancy Check (CRC) to ensure reliable delivery of data.

Overview
--------

**Classes**
  :py:class:`Transmitter`, :py:class:`Receiver`
  

'''
__version__ = "1.1.0"
__author__ = "Jasper Zheng (Shuoyang)"

def get_version():
    return [__version__]
    
def print_version():
    print('PyAudible version {}'.format(__version__))
    
    
    