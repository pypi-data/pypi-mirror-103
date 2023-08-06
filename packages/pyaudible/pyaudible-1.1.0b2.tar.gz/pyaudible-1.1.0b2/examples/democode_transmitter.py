"""PyAudible Example: Modulate and Transmit Data"""

from pyaudible import transmitter

# instantiate the transmitter
tx = transmitter.Transmitter(speed = 'fast', volume = 1.0)

# define the message to be transmitted
message = 'Hello World!'

# define the filename
filename = 'transmitter_sample.wav'

# modulate the message and store the modulated signal to an audio file
tx.modulate_to_file(message, filename)