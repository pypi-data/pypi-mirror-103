"""PyAudible Example: Receive and Demodulate Data (Blocking Mode)"""

from pyaudible import receiver

# instantiate the receiver
rx = receiver.Receiver(sensitivity = 'medium', 
                        speed = 'auto')

# active the receiver for 30 seconds
retrieved_data = rx.read_block(30)