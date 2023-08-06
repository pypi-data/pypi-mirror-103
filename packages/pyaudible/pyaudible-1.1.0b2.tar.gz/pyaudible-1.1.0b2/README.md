# PyAudible 1.1.0  

![PyAudible](docs/Graphics/pyaudible.gif)


A Python library for sending and receiving data using audible sound. PyAudible includes a transmitter and a receiver module that could be implemented on multiple devices, enables the transmission of small amounts of data between separated systems in the vicinity.

The library implements a Multi-channel Carrier Modulation protocol, allows a configurable transmitting speed between 5 - 20 bytes/sec. It uses [Cyclic Redundancy Check (CRC)](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) to ensure reliable data delivery.  

The transmitter and the receiver provide simplified Python interface that could be easily integrated in various other projects, possible scenarios includes:

 - Smart Home Appliances (IoT)  
 - Data Broadcasting  
 - Device Pairing  
 - Electronic Key Sharing  


This README file provides a walkthrough of the project, include a quickstart, brief documentation and evaluation.

Other docs can be found at:  
 * [Full Documentation](https://github.com/jasper-zheng/PyAudible/blob/main/docs/Documentation.md)
 * [Protocol Details](https://github.com/jasper-zheng/PyAudible/blob/main/docs/TechnicalDetails.md)
 * [Test & Evaluations](https://github.com/jasper-zheng/PyAudible/blob/main/docs/EvaluationResult.md)  
 

#### Project Roadmap  
 ![Roadmap](docs/Graphics/roadmap.jpg)

## Quickstart  
> Tested on Python 3.8  

#### Requirements

* **Python** 3.8+  
* **PyAudio** 0.2.11+ (speaker access required for the transmitter, microphone access required for the receiver)  
* **Numpy** 1.18.5+  

#### Installation  
With required dependencies installed, use `pip install pyaudible` to download and install PyAudible.  

To validate the installation, run the following code and it should print the version of the transmitter, receiver, PyAudio and PortAudio to the console.  
```
from pyaudible import transmitter, receiver
transmitter.print_transmitter_version()
receiver.print_receiver_version()
```

After the installation, keep following the examples provided below or refer to the full [documentation](https://github.com/jasper-zheng/PyAudible/blob/main/docs/Documentation.md) for more information.  

## Examples and Demos

The following examples will demonstrate the basic transmission protocol of PyAudible. More examples could be find in the full [documentation](https://github.com/jasper-zheng/PyAudible/blob/main/docs/Documentation.md).

#### Example: Modulate and Transmit Data  

In this example we converted a message to electrical signals and generated the modulated audio file.

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
#### Example: Receive and Demodulate Data (Blocking Mode)

In this example we set up a PyAudible Receiver and kept it on standby for 30 seconds. If the transmitted signal was played during the standby time, it would capture and convert the signal back to text.

```python
"""PyAudible Example: Receive and Demodulate Data (Blocking Mode)"""

from pyaudible import receiver

# instantiate the receiver
rx = receiver.Receiver(sensitivity = 'medium',
                        speed = 'auto')

# active the receiver for 30 seconds
retrieved_data = rx.read_block(30)
```

## Protocol Overview  

This section briefly demonstrated the transmission protocol, however, a full detailed explanation could be found in [Protocol Details](https://github.com/jasper-zheng/PyAudible/blob/main/docs/TechnicalDetails.md).  

![Receiver Data Process Flow](https://github.com/jasper-zheng/PyAudible/blob/main/docs/Graphics/infoboard-01.png?raw=true)
*Figure 1: Multi-channel Carrier Modulation*  

The protocol utilises a [Frequency-Shift Keying (FSK)](https://en.wikipedia.org/wiki/Frequency-shift_keying) technique to modulate the raw data into an eight-channel carrier signal `Channel_01` - `Channel_08`. Each carrier channel transmits data by switching the frequency within a range of 16 candidate frequencies <code>F<sub>C</sub>(0)</code> - <code>F<sub>C</sub>(15)</code> (Shown in **Figure 1**). And each candidate frequency represents a 4-bit chunk (`0000`, `0001`...`1111`). Therefore, 8 x 16 = 128 candidate frequencies are equally spaced between `1238 Hz` to `6965 Hz`, divided by `dF = 43.0 kHz`. The original data is converted into binary representations, and then it is encapsulated into packets of 8, 16 or 32 bits per unit time (depending on the transmission rate), then transmitted via 2, 4 or 8 channels.

To handle the transmission signal, the receiver maintains seven Status Flags to signifying the status of the current connection, shown in *Figure 2* below.

![Receiver Handling Behaviours](https://github.com/jasper-zheng/PyAudible/blob/main/docs/Graphics/infoboard-02.png?raw=true)
*Figure 2: Receiver Handling Behaviours*  

The beginning and ending bits of the transmission sequences are the Activating and Terminating Sound Mark. Each part of the sound mark contains essential session descriptors to establish and terminate the connection, shown in *Figure 3* below. These descriptors also maintain important functionalities include flow control and noise resistance mechanism.  

![Sound Mark Structure](https://github.com/jasper-zheng/PyAudible/blob/main/docs/Graphics/infoboard-03.png?raw=true)
*Figure 3: Sound Marks Structure*  


## Documentation  
Full documentation provided in [Documentation](https://github.com/jasper-zheng/PyAudible/blob/main/docs/Documentation.md).  

Alternatively, the documentation can be generated and viewed via `__doc__`, for example `print(receiver.Receiver.read_block.__doc__)`.  


## Test and Evaluation (Overview)  

Full experimentation designs and the evaluation results provided in [Test & Evaluation](https://github.com/jasper-zheng/PyAudible/blob/main/docs/EvaluationResult.md) document.

![Experiment](docs/Graphics/experiment.jpg)

The evaluations of the system were conducted along with the development. [Phase I Evaluation](https://github.com/jasper-zheng/PyAudible/blob/main/docs/EvaluationResult.md#phase-i-evaluation-noise-resistance-mechanism-reliability) assessed the reliability of the noise resistance mechanism in different noise conditions, and verified that the system can achieve at least 90% reliability with a transmission rate at 20 bytes/sec. [Phase II Evaluation](https://github.com/jasper-zheng/PyAudible/blob/main/docs/EvaluationResult.md#phase-ii-evaluation-system-reliability-vs-speed-and-signal-to-noise-ratio) gave a statistical analysis on the reliability with respect to the transmission speed and the signal to noise ratio. The following Speed-Rate-Reliability Lookup Table is taken from the [results of Phase II Evaluation](https://github.com/jasper-zheng/PyAudible/blob/main/docs/EvaluationResult.md#test-21-system-reliability-1), which could help users to decide transmission settings based on noise situations:

<table style="font-size:7px">
    <thead>
        <tr>
            <th>Transmission Speed</th>
            <th>Transmission Success Rate</th>
            <th>Reliability</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=3 align="center">Signal to Noise Ratio = 1.2</td>
        </tr>
        <tr>
            <td>5 bytes/sec (slow)</td>
            <td>0.20</td>
            <td>0.80</td>
        </tr>
        <tr>
            <td>10 bytes/sec (medium)</td>
            <td>0.11</td>
            <td>0.55</td>
        </tr>
        <tr>
            <td>20 bytes/sec (fast)</td>
            <td>0.07</td>
            <td>0.38</td>
        </tr>
        <tr>
            <td colspan=3 align="center">Signal to Noise Ratio = 1.5</td>
        </tr>
        <tr>
            <td>5 bytes/sec (slow)</td>
            <td>0.72</td>
            <td>0.90</td>
        </tr>
        <tr>
            <td>10 bytes/sec (medium)</td>
            <td>0.54</td>
            <td>0.80</td>
        </tr>
        <tr>
            <td>20 bytes/sec (fast)</td>
            <td>0.47</td>
            <td>0.77</td>
        </tr>
        <tr>
            <td colspan=3 align="center">Signal to Noise Ratio = 2</td>
        </tr>
        <tr>
            <td>5 bytes/sec (slow)</td>
            <td>0.99</td>
            <td>1.00</td>
        </tr>
        <tr>
            <td>10 bytes/sec (medium)</td>
            <td>0.73</td>
            <td>0.97</td>
        </tr>
        <tr>
            <td>20 bytes/sec (fast)</td>
            <td>0.66</td>
            <td>0.90</td>
        </tr>
        <tr>
            <td colspan=3 align="center">Signal to Noise Ratio = 2.5</td>
        </tr>
        <tr>
            <td>5 bytes/sec (slow)</td>
            <td>0.99</td>
            <td>1.00</td>
        </tr>
        <tr>
            <td>10 bytes/sec (medium)</td>
            <td>0.95</td>
            <td>1.00</td>
        </tr>
        <tr>
            <td>20 bytes/sec (fast)</td>
            <td>0.90</td>
            <td>0.97</td>
        </tr>
    </tbody>
</table>   

*Speed - Rate - Reliability Lookup Table*


## Latest Updates

**04.01.21 V1.1.0**  
Compatible to any audio backends as long as it provides buffered audio analysis.  

Full update history provided in [Updates](https://github.com/jasper-zheng/PyAudible/blob/main/docs/Updates.md).  


## Acknowledgment

This project is carry out in comply with the guidelines of COMP390 module, as a key element of the Honours Year Project.

## License
[MIT](https://choosealicense.com/licenses/mit/)
