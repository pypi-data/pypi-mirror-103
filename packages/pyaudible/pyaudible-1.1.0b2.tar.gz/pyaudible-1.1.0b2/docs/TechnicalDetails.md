###### PyAudible 1.1.0
# Transmission Protocol Design
This document gives an overview of the technical details in the transmission protocol. It refers the protocol design to a stripped OSI (Open Systems Interconnection) model and analyses the physical and data link layers.  

#### Contents
 * [Physical Layer: Multi-channel Carrier Modulation](#physical-layer-multi-channel-carrier-modulation)
 * [Data Link Layer: Sound Marks](#data-link-layer-sound-marks)
   * [Activating and Terminating Sound Mark](#activating-and-terminating-sound-mark)
   * [Noise Resistance Mechanism](#noise-resistance-mechanism)
     * [Signal to Noise Ratio Check](#signal-to-noise-ratio-check)
     * [Error Detecting Code](#error-detecting-code)
 * [Protocol Handling (Receiver Status)](#protocol-handling-receiver-status)  


## Physical Layer: Multi-channel Carrier Modulation

<img src="Graphics/multi-channel_carrier.png" width="600">  

*Figure 1: Multi-channel Carrier Modulation*  

The protocol utilises a [Frequency-Shift Keying (FSK)](https://en.wikipedia.org/wiki/Frequency-shift_keying) technique to modulate the raw data into an eight-channel carrier signal `Channel_01` - `Channel_08`. Each carrier channel transmits data by switching the frequency within a range of 16 candidate frequencies <code>F<sub>C</sub>(0)</code> - <code>F<sub>C</sub>(15)</code> (Shown in **Figure 1**). And each candidate frequency represents a 4-bit chunk `ck_0` - `ck_15`, shown in **Table 1**. Therefore, 8 x 16 = 128 candidate frequencies are equally spaced between `1238 Hz` to `6965 Hz`, divided by `dF = 43.0 kHz`. The original data is converted into binary representations, and then it is encapsulated into packets of 8, 16 or 32 bits per unit time (depended on the transmission rate), then transmitted via 2, 4 or 8 channels.
<table style="font-size:7px">
    <thead>
        <tr>
            <th>Chunk ID</th>
            <th>Binary Representation</th>
            <th>Frequency</th>
            <th>...</th>
            <th>Chunk ID</th>
            <th>Binary Representation</th>
            <th>Frequency</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>ck_00</td>
            <td>0000</td>
            <td>1238 + 0 * 43 Hz</td>
            <td>...</td>
            <td>ck_00</td>
            <td>0000</td>
            <td>6277 + 0 * 43 Hz</td>
        </tr>
        <tr>
            <td>ck_01</td>
            <td>0001</td>
            <td>1238 + 1 * 43 Hz</td>
            <td>...</td>
            <td>ck_01</td>
            <td>0001</td>
            <td>6277 + 1 * 43 Hz</td>
        </tr>
        <tr>
            <td>ck_02</td>
            <td>0010</td>
            <td>1238 + 2 * 43 Hz</td>
            <td>...</td>
            <td>ck_02</td>
            <td>0010</td>
            <td>6277 + 2 * 43 Hz</td>
        </tr>
        <tr>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
        </tr>
        <tr>
            <td>ck_15</td>
            <td>1111</td>
            <td>1238 + 15 * 43 Hz</td>
            <td>...</td>
            <td>ck_15</td>
            <td>1111</td>
            <td>6277 + 15 * 43 Hz</td>
        </tr>
    </tbody>
</table>    

*Table 1: Chunk - Binary - Frequency*  

If each channel transmits different data simultaneously, it allows a maximum transmission speed of 32 bits per unit. And if the unit time is 0.2 second, the transmission speed can be up to 20 bytes per sec.   

However, a portion of the communication channels could be used as repeat requests for error control to improve robustness. Depending on the setting, the system utilises 0, 4 or 6 carriers to repeat the transmission signal. Error correction is based on the original signal and the repeated signal.   

![image](Graphics/infoboard-01.png)   
*Figure 2: Receiver Data Process Flow*  

For example, in **Figure 2**, the transmission speed set to `slow`, therefore, the original binary data will be divided into two splits, the first split will be transmitted through channel 01, 03, 05 and 07, the second split will be transmitted through channel 02, 04, 06 and 08. After demodulating the signal, the receiver will analyse each split of data respectively. Then perform error correction based on the repeated signals. And finally, the receiver will recover the binary data and convert it into text format.    

## Data Link Layer: Sound Marks  
The data link layer specifies the link between the transmitter and the receiver, includes the protocol to establish and terminate the connection, flow control and noise resistance mechanism.   
#### Activating and Terminating Sound Mark
The beginning and ending bits of the transmission sequences are the Activating and Terminating Sound Mark. Each part of the sound mark contains essential session descriptors to establish and terminate the connection.  

![Sound Mark Frequency Usage](Graphics/infoboard-03.png)  
*Figure 3: Sound Mark Frequency Usage*  

The current approach utilised the 1st, 5th and 8th channels as the activating and terminating descriptor. The transmitter broadcasts the marker contains the activating descriptor to activate the transmission. Three channels are taken to prevent the ambient noise from accidentally produce an activating mark.   

Meanwhile, the 2nd, 3rd, 4th channels are error-detecting descriptor, and technical details will be discussed in the next section ([Error Detecting Code](#error-detecting-code)).  


The 6th, 7th channels are the flow control descriptor, signifying the upcoming transmission rate. Since the transmission system only establishes an asynchronous link between the Tx and the Rx, the transmission rate must be defined ahead of the establishment to ensure the receiver knows the coming of a new byte. The receiver will configure the clock according to the flow control signal.  

#### Noise Resistance Mechanism  
The noise resistance mechanism provides error control methods to achieve reliable data transmission over an environment with inconvenient noise. The methods include Signal to Noise Check (SNR Check) and Error Detecting Code.  

Both measures aim at improving the reliability of the transmission, in other words, reduce the number of [False Negatives](http://methods.sagepub.com/reference/the-sage-encyclopedia-of-communication-research-methods/i5497.xml). The effectiveness of the mechanisms was evaluated after the development, and the results were included in the [evaluation document](#).  

###### Signal to Noise Ratio Check
The main purpose of the [Signal to Noise Ratio (SNR)](https://en.wikipedia.org/wiki/Signal-to-noise_ratio) Check is to assess whether the current noise condition is competent to perform successful transmission. During the activating of the transmission, the receiver estimates the integrity `K` of the activating sound mark. If `K` exceeds the defined threshold `θ`, the noise condition will be decided as competent, and the receiver will establish the connection. The threshold `θ` is defined as the `sensitivity` of the receiver (Details written in the [PyAudible documentation](#)).  

The setting of the threshold might differ between different noise condition. The rise of the threshold will reduce the number of [False Negatives](http://methods.sagepub.com/reference/the-sage-encyclopedia-of-communication-research-methods/i5497.xml), however, it might introduce the increase in [False Positives](https://methods.sagepub.com/Reference//the-sage-encyclopedia-of-communication-research-methods/i5517.xml).   

![SNR](Graphics/snr.jpg)  
*Figure 4: Power spectrum of received signal under different background noises*  

###### Error Detecting Code  
The Error Detecting Code aims to validate the received data using [Cyclic Redundancy Check (CRC)](https://en.wikipedia.org/wiki/Cyclic_redundancy_check). The transmitter produces a hashed fixed-length code (checksum) before the transmission, then attaches it to the error-detecting descriptor in the sound marks. The receiver evaluates the checksum and the transmitted contents. If the contents match the checksum, the transmission will be considered valid. Otherwise, it will be reported as failed transmission, and the system will request another repetition.   

## Protocol Handling (Receiver Status)
To create interactive and controllable responses, the protocol includes the handling behaviours of the receiver. The receiver maintains seven Status Flags to signifying the status of the current connection.   

![Receiver Status Design](Graphics/infoboard-02.png)
*Figure 5: Receiver Status*  

![Receiver Status Design](Graphics/infoboard-04.png)
*Figure 6: Receiver Status*  

**Status 0** - Unactivated  
No established connection. The receiver continuously captures audio, looks for the activating signals.  

**Status 1** - Activating  
The receiver detected the start of an activation sound mark, but haven't validated the activation.  

**Status 2** - Preparing  
The activation was validated, and the current condition passed the [SNR Check](#signal-to-noise-ratio-check). The receiver is waiting for the first bit of the transmission signal.  

**Status 3** - Activation Failed  
The activation is invalid due to the failure in [SNR Check](#signal-to-noise-ratio-check), or it was being detected as an accidental start. The receiver will roll back to **Status 0** in the next frame.  

**Status 4** - Listening  
The connection was established, data is being transmitted.  

**Status 5** - Terminated, transmission succeeded  
The connection was terminated, the received contents passed the [Error Detecting Code Check](#error-detecting-code), the transmission was succeeded. The receiver will go back to **Status 0** in the next frame.  

**Status 6** - Terminated, transmission failed  
The connection was terminated, the received contents failed the [Error Detecting Code Check](#error-detecting-code), the transmission was failed. The receiver will go back to **Status 0** in the next frame.  
