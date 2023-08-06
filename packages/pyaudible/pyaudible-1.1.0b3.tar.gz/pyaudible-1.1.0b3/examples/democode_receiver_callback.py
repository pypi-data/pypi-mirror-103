"""PyAudible Example: Receive and Demodulate Data (Callback Mode)"""

from pyaudible import receiver
import time

# instantiate the receiver
rx = receiver.Receiver(sensitivity = 'medium',
                        speed = 'auto')

# create a empty variable to store the received data
retrieved_data = ''

# create a while loop for 30 seconds
start_time = time.time()
while (time.time() - start_time < 30):
    
    # call the receiver on each frames
    # the receiver will return received data on the fly
    data = rx.read_frame(log = False)
    
    # if received data is not empty, add then to the predefined variable
    if data:
        retrieved_data += data

# Received data will also be stored in a list, 
# it contains messages demodulated from each singal during the standby time
message_list = rx.received_data()
