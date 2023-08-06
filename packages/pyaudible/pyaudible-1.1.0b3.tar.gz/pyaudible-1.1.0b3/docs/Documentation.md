###### PyAudible 1.1.0
# Documentation

PyAudible is a Python library for sending and receiving data using audible sound. PyAudible includes a transmitter and a receiver module that could be implemented on multiple separated devices, enables the transmission of small amounts of data between devices in the vicinity.  

 * The transmitter module `Transmitter` generates encoded audio waveforms.  
 * The receiver module `Receiver` listens and analyses the audio waveforms captured by microphones.  

It allows a configurable transmitting speed between 5 - 20 bytes/sec.  
It uses cyclic redundancy check (CRC) for error detection to improve robustness.

## User Guide

* [Requirements and Installation](#requirements-and-installation)
* [Getting started with PyAudible](#getting-started-with-pyaudible)
  * [Example: Modulate and Transmit Data](#example-modulate-and-transmit-data)
  * [Example: Receive and Demodulate Data (Blocking Mode)](#example-receive-and-demodulate-data-blocking-mode)
  * [Example: Receive and Demodulate Data (Callback Mode)](#example-receive-and-demodulate-data-callback-mode)
* [Class Transmitter](#class-transmitter)
  * [Transmission Speed](#transmission-speed)
  * [Transmission Volume](#transmission-volume)
  * [Class Details](#details)
* [Class Receiver](#class-receiver)
  * [Activation Sensitivity](#activation-sensitivity)
  * [Transmission Speed](#transmission-speed-1)
  * [Listening Modes](#listening-modes)
    * [Blocking Mode](#blocking-mode)
    * [Callback Mode](#callback-mode)
  * [System Logs](#system-logs)
    * [FFT Logs](#fft-logs)
    * [Status Flags](#status-flags)
    * [Received Data](#received-data)

## Requirements and Installation

#### Requirements
PyAudible depends on the following dependencies:  
* **Python** 3.6+  
* **PyAudio** 0.2.11+ (speaker access required for the transmitter, microphone access required for the receiver)  
* **Numpy** 1.18.5+  

#### Installation
PyAudible is currently only available on PyPI.  
With required dependencies installed, use `pip install pyaudible` to download and install PyAudible.


## Getting started with PyAudible
#### Example: Modulate and Transmit Data
```python
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
```
To convert a message to electrical signals and generate the modulated audio file, first instantiate PyAudible by ``transmitter.Transmitter()`` with desired parameters (see [Class Transmitter](#class-transmitter)). It will initialise a transmitter for modulating data.   

Modulate a message by calling ``transmitter.Transmitter.modulate_to_file()`` with input data and the file name, it will modulate the data to audio waveforms and save it to a playable file.

To modulate a message without save it to file, or play the audio right after the modulation, call ``transmitter.Transmitter.modulate()`` or ``transmitter.Transmitter.modulate_and_play()`` (see [Class Transmitter](#class-transmitter)).

#### Example: Receive and Demodulate Data (Blocking Mode)
```python
"""PyAudible Example: Receive and Demodulate Data (Blocking Mode)"""

from pyaudible import receiver

# instantiate the receiver
rx = receiver.Receiver(sensitivity = 'medium',
                        speed = 'auto')

# active the receiver for 30 seconds
retrieved_data = rx.read_block(30)
```
To detect and demodulate data, first instantiate a receiver on the desired device by `receiver.Receiver()` with desired parameters (see [Class Receiver](#class-receiver)). It will initialise a reusable receiver for analysing and demodulating data.

Open the receiver by calling `receiver.Receiver.read_block()`, the receiver will stand-by and continuously detecting audio input. The results will be return in a Python list.

Note that the Blocking Mode will block the thread until all the required time have been recorded, therefore not recommend for frame based application. Alternatively, use Callback Mode to process inputs by frames (see next section).

#### Example: Receive and Demodulate Data (Callback Mode)
```python
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
```

In Callback Mode, after the instantiation, the receiver will be repeatedly called each frame by `receiver.Receiver.read()`.
Whenever new data is ready, the receiver will return the converted data as string immediately, even if the transmission is not finish. If the log mode is on, the receiver will also return a integer representing the current status of the connection, to help interacting with the receiver (see [Class Receiver: Callback Mode](#callback-mode)).  

## Class Transmitter

``class transmitter.Transmitter``  

Python interface to modulate and transmit data. Provides methods to:  
  * Convert text to modulated audio waveform
  * Write a modulated waveform as a uncompressed WAV file
  * Open PyAudio to stream the modulated audio


#### Transmission Speed
The speed of the transmission should be defined when instantiating the transmitter by `speed` parameter in the instantiation function (see [__ init__()](#details)).

Three levels of the speed are specified by ‘slow’, ‘medium’ and ‘fast’. In fast mode, eight channels will be utilised simultaneously for the transmission, and it will provide a speed of 20 bytes per second. Whereas in slow mode, two channels will be utilised for the transmission, and the signal will be copied to the other six channels to improve accuracy.

The following table listed the testing results of the correlation between the transmission speed and the accuracy.



#### Transmission Volume
The volume of the transmission should be defined when instantiating the transmitter by `volume` parameter in the instantiation function (see [__ init__()](#details)).

The volume is specified by a float number ranged from 0 to 1, where 0 represents quiet and 1 represent full amplitude of the waveform.

#### Overview
`text_to_bin(), modulate(), modulate_to_file(), modulate_and_play()`

#### Details  

`__init__(speed, volume)`    
**Parameter**  
speed - Specifies the speed of the transmission, type: string  
*‘slow’, ‘medium’, ‘fast’*  
*Defaults to ‘slow’*  
volume - Specifies the loudness of the transmission, type: float ranged form 0 to 1.  
*Defaults to 1.0*  
**Raise**  
ParameterError - if the parameter `speed` is invalid.

`text_to_bin(text)`  
Convert ASCII text to binary signal.  
**Parameter**  
text - The input text data, type: string

`modulate()`  
Convert text message to a modulated audio waveform.  
**Parameter**  
message - The input text data, type: string  
**Return**  
waveform - Modulated waveform in array form

`modulate_to_file()`  
Convert text message to a modulated audio waveform and save it as .wav format file.  
**Parameter**  
message - The input text data, type: string  
filename - Name of the output wav file, type: string  


## Class Receiver
`class receiver.Receiver`  

Python interface to detect and demodulate broadcasted audio and convert them into text data.

#### Activation Sensitivity
The sensitivity of the receiver should be defined when instantiating the transmitter by `sensitivity` parameter in the instantiation function (see [receiver.Receiver.__ init__()](#)). The options includs ``'low'``, ``'medium'`` and ``'high'``.  

In the activating process, the receiver perform SNR Check to decide whether the current noise condition is competent to perform successful transmission. Activation Sensitivity defines the threshold that activate the receiver. With a higher sensitivity, the receiver will tend to pass the SNR Check easily and be activated for transmission.  

#### Transmission Speed  
By default, the transmission speed of the receiver will be automatically determined by the Flow Control Descriptor defined in the Sound Mark. However, there is still an option to use a fixed receiving speed, and the receiver will ignore the transmissions that don't match this defined speed. Set a fixed receiving speed by defining the `speed` parameter of the receiver to ``'slow'``, ``'medium'`` or ``'fast'`` when instantiating. By default, `speed` parameter is set to `auto`.

#### Listening Modes
The mode of the receiver will be determined by different methods called after the receiver was instantiated. Includes [Blocking Mode](#blocking-mode) and [Callback Mode](#callback-mode).
###### Blocking Mode   
Call `pyaudible.Receiver.read_block()` to use blocking mode. The receiver should be called only once and it will block until all the required time is recorded. After the desired time, call `pyaudible.Receiver.get_received_data()` to retrieve all the received data (see [Example: Receive and Demodulate Data (Blocking Mode)](#example-receive-and-demodulate-data-blocking-mode) for sample code).   

###### Callback Mode  
Call `receiver.Receiver.read_frame()` to use callback mode. The receiver will only analyse audio in the frames that it is called. Therefore, it should be called in the main loop in a frame-based application (see [Example: Receive and Demodulate Data (Callback Mode)](#example-receive-and-demodulate-data-callback-mode) for sample code).   

`receiver.Receiver.read_frame()` will return decoded text once new data is available. If the parameter `log` is `True`, it will also return a integer flag signifying the status to help the system interacting with the receiver (see next section [System Logs and Status Flags](#system-logs)).   

#### System Logs
The receiver will maintain essential data for interaction, includes [FFT Logs](#fft-logs), [Status Flags](#status-flags) and [Received Data](#received-data).  

###### FFT Logs  
FFT Logs maintains the discrete Fourier transform of the current audio input, which are ready to map into a spectrum form. Use `receiver.Receiver.get_fft()` to get FFT Logs.

###### Status Flags  
Status Flag maintains the current status of the connection:  
**0 - Unactivated:** No established connection. The receiver continuously captures audio, looks for the activating signals.  
**1 - Activating:** The receiver detected the start of an activation sound mark, but haven't validated the activation.  
**2 - Preparing:** The activation was validated, and the current condition passed the [SNR Check](https://github.com/jasper-zheng/PyAudible/blob/main/documents/TechnicalDetails.md#signal-to-noise-ratio-check). The receiver is waiting for the first bit of the transmission signal.  
**3 - Activation Failed:** The activation is invalid due to the failure in [SNR Check](https://github.com/jasper-zheng/PyAudible/blob/main/documents/TechnicalDetails.md#signal-to-noise-ratio-check), or it was being detected as an accidental start. The receiver will roll back to **Status 0** in the next frame.  
**4 - Listening:** The connection was established, data is being transmitted.  
**5 - Terminated, transmission succeeded:** The connection was terminated, the received contents passed the [Error Detecting Code Check](https://github.com/jasper-zheng/PyAudible/blob/main/documents/TechnicalDetails.md#error-detecting-code), the transmission was succeeded. The receiver will go back to **Status 0** in the next frame.  
**6 - Terminated, transmission failed:** The connection was terminated, the received contents failed the [Error Detecting Code Check](https://github.com/jasper-zheng/PyAudible/blob/main/documents/TechnicalDetails.md#error-detecting-codee), the transmission was failed. The receiver will go back to **Status 0** in the next frame.   

If the `log` parameter in `receiver.Receiver.read_frame()` is `True`, the status will be returned a integer. Or use `receiver.Receiver.get_status()` to get the current status.

###### Received Data  
Use `receiver.Receiver.get_received_data()` to get all the received transmission stored in a list.

#### Overview
`text_to_bin(), modulate(), modulate_to_file(), modulate_and_play()`

#### Details  

`__init__(actived_channel, sensitivity, speed)`    
**Parameter**  
actived_channel - Specifies the number of channels used, type: integer ranged from 1 to 8, *Defaults to 8*    
sensitivity - Specifies the sensitivity of the receiver, type: string  
*‘low’, ‘medium’, ‘high’*  
*Defaults to ‘medium’*  
speed - Specifies the speed of the receiver, type: string  
*‘auto’, ‘slow’, ‘medium’, ‘fast’*  
*Defaults to ‘auto’*  

**Raises**  
ParameterError - if the parameter `speed` or `sensitivity` is invalid.

`refresh_audio()`  
Reload PyAudio module.  

`read_block(standby_time)`  
Read the input audio in Blocking Mode, standby and listen until all the equested frames have been recorded.  
**Parameter**  
standby_time - The requested time (in second), type: int  
**Returns**  
retrieved_data - Every retrieved data during the standby time, type: 1d-List of string

`read_frame_audio(audio, log)`  
Takes 2048 frames of audio data and perform analysis.  
**Parameter**  
audio - The array version of the audio buffer. Type: np array with a size of (2048,)  
log - If true, it will add a status flag to the returns, accompany with the retrived result. Type: bool  
**Returns**   
retrieved_data - Every retrieved data during the standby time, type: 1d-List of string  

`read_frame(log)`  
Read the input audio in Callback Mode, called each frame to listen to the audio.  
**Parameter**  
log - If true, it will add a status flag to the returns, accompany with the retrived result. Type: bool  
**Returns**   
retrieved_data - Every retrieved data during the standby time, type: 1d-List of string  
status - an integer flag signifying the current status of the connection. Type: int  

`clear_session()`  
Refresh the receiver, abort the current connection and rollback to status 0.  

`bin_to_text(binary)`  
Convert binary signal to ASCII text.  
**Parameter**   
binary - The input binary data, type: string   

`convert_result(received)`   
Convert received binaries from all channels to demodulated text.  
**Parameter**   
received - a list of binary data  
trim - set the trimming point, leave None if do not trim.  
crc - Cyclic Redundancy Check (CRC) checksum code, leave None if skip CRC. type: 3-character string, defaults to None.   
**Raise**  
ASCIIError - If the binary data does not map to ASCII table.  
CRCError - If Cyclic Redundancy Check failed.

`get_fft()`  
Get the discrete Fourier transform result of current audio input.  
**Returns**  
np array with a size of (2048,)  

`get_status()`  
Get the current status of connection.  
**Returns**  
a integer signifying the current status.

`get_received_data()`  
Return all received data  
**Returns**  
1-d list of strings  

`clear()`  
Clear the retrieved data.    
