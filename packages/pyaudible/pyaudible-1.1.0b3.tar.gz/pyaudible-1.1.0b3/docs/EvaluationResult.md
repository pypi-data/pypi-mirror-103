###### PyAudible 1.1.0
# Test & Evaluation

### Key Takeaway  

The evaluations of the system were conducted along with the development. [Phase I Evaluation](#phase-i-evaluation-noise-resistance-mechanism-reliability) assessed the reliability of the noise resistance mechanism in different noise conditions, and verified that the system can achieve at least 90% reliability with a transmission rate at 20 bytes/sec. [Phase II Evaluation](#phase-ii-evaluation-system-reliability-vs-speed-and-signal-to-noise-ratio) gave a statistical analysis on the reliability with respect to the transmission speed and the signal to noise ratio. The following [Speed-Rate-Reliability Lookup Table](#key-takeaway) is taken from the [results of Phase II Evaluation](#test-21-system-reliability-1), which could help users to decide transmission settings based on noise situations:

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


### Contents  

 * [Phase I Evaluation: Noise Resistance Mechanism Reliability](#phase-i-evaluation-noise-resistance-mechanism-reliability)
   * [Experiment Design](#experiment-design)
     * [Test 1.1: Flatter Continuous Noise](#test-11-flatter-continuous-noise)
     * [Test 1.2: Sudden Disruptive Noise](#test-12-sudden-disruptive-noise)
   * [Result and Analysis](#experiment-results)  
     * [Test 1.1 Results: Flatter Continuous Noise](#test-11-results-flatter-continuous-noise)
     * [Test 1.2 Results: Sudden Disruptive Noise](#test-12-results-sudden-disruptive-noise)  


 * [Phase II Evaluation: System Reliability vs. Speed and Noise Conditions](#phase-ii-evaluation-system-reliability-vs-speed-and-signal-to-noise-ratio)
   * [Experiment Design](#experiment-design-1)
     * [Test 2.1: System Reliability](#test-21-system-reliability)
   * [Result and Analysis](#experiment-results-1)  
     * [Test 2.1 Results: System Reliability](#test-21-system-reliability-1)

## Phase I Evaluation: Noise Resistance Mechanism Reliability  
The goal of Phase I evaluation is to assess the reliability of the noise resistance mechanism, including Sound Mark Integrity Check and Error Detecting Code. As a part of the transmission protocol, the noise resistance mechanism should be able to tolerate unpredictable background noise.   

To detect and recover from the noise, the receiver assesses the sound marks to decide whether the current noise condition is competent for successful transmission, and then use error detecting codes to perform Cyclic Redundancy Check (CRC), and therefore verify transmission integrity. Therefore, to assess the reliability of this mechanism, the following criteria were included:    
 * The probability that the receiver staying inactive when the power of the background noise is strong enough to disturb the transmission.  
 * The probability that the receiver successfully detect the fault caused by the noise and abort the transmission.  

#### Experiment Design

The test consists of two parts, aims at assessing the noise resistance mechanism under two noise conditions: Flatter Continuous Noise and Sudden Disruptive Noise.  

![Experiment](Graphics/experiment.jpg)

##### Test 1.1: Flatter Continuous Noise  

This is the situation where the noise remains constant and stable over the transmission periods, such as ambient noise in the office, city traffic, or white noise in a plane. Continuous noise can affect the signal to noise ratio ![equation](https://latex.codecogs.com/svg.image?SNR) between the power of modulated signal ![equation](https://latex.codecogs.com/svg.image?P_{signal}) and the background noise ![equation](https://latex.codecogs.com/svg.image?P_{noise}) .  

The test was conducted in a transmission system between a MacBook and an iPhone, where the MacBook acted as the receiver and the iPhone acted as the transmitter, with a distance of 2 meters. To control the noise in the environment, the system was implemented in a silent room with acoustic control, a separated speaker was used to produce recorded ambient noise at desired levels.  

The test includes three rounds, where the activation sensitivity was set to different levels. In each round, data were transmitted in the same system in turns, but with different settings (with and without noise resistance mechanism implemented).  

Besides, a special handling in the test is that whether the receiver decides to stay inactive or be activated, the system will activate the receiver anyway, to verify whether the receiver is making the correct decision on staying inactive.  

Following data were recorded:  
  * **Total Transmission:** Count the total number of transmission.  
  * **Succeed Activation:** Number of times that the receiver was activated.  
  * **Invalid Aborting:** Number of times that the activation was decided abort, however, the receiver still got correct data from the transmission.  
  * **Incorrect Transmission:** Number of times that the receiver got incorrect data, regardless the error report.  
  * **Fault was Detected:** Number of times that the receiver got incorrect data, but the fault was successfully detected and the transmission aborted.
  * **Fault Detection:** Number of times that the data was successfully transmitted, but an error was mistakenly reported.

To improve the generality of the test, each round of test will repeat until 100 incorrect transmissions were made. The reliability `R` of the noise resistance mechanism represents the probability that the receiver aborts the transmission or detects the fault, given that the transmission is not successful. Therefore, let `A` denotes the event that an activation was aborted, `D` denotes the event that a fault was detected, `F` denotes the event that a transmission was failed. According to the axioms of probability theory, the reliability  `R` could be calculated by:  

![equation](https://latex.codecogs.com/svg.image?R&space;=&space;P((A&space;\cup&space;D)|F)=\frac{P(A\cup&space;D&space;\cap&space;F)}{P(F)})   

##### Test 1.2: Sudden Disruptive Noise  
In this situation, the noise refers to sudden bursts of sounds that happen after the transmission started, such as a cough or sneeze, sudden talks and handclaps, or a falling object hits the floor. Disruptive noise may have a destructive effect on the transmission, since the amplitude and frequency of noise may fully cover the transmission channels. Therefore, the error detecting code should be able to identify the fragmentary in the received data.   

The basic set up of the test was the same as **Test 1.1**, however, in addition to the continuous background noise, another sudden bursting noise was triggered after the receiver was activated, the type of bursting noise include random played hand claps, shouts, laughter and clanks.  

Following data was recorded:  

 * **Succeed Transmission:** Number of times that the data was successfully transmitted to the receiver, with no error reported.
 * **Failed Transmission:** Number of times that the receiver got incorrect data, with no error detected.  
 * **Fault was Detected:** Number of times that the receiver got incorrect data, but the fault was successfully detected and the transmission aborted.  

The reliability `R` was be represented as the probability that the receiver detected the fault, given that the transmission was not successful.  

![equation](https://latex.codecogs.com/svg.image?R&space;=&space;P(FaultDetected|TransmissionFailed)&space;=&space;\frac{P(TransmissionFailed\cap&space;FaultDetected)}{P(TransmissionFailed)})  


#### Experiment Results
##### Test 1.1 Results: Flatter Continuous Noise
<table style="font-size:7px">
    <thead>
        <tr>
            <th></th>
            <th>Total Transmission</th>
            <th>Succeed Activation</th>
            <th>Invalid Aborting</th>
            <th>Incorrect Transmission</th>
            <th>Fault was Detected</th>
            <th>Fault Detection</th>
            <th>Reliability</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=8 align="center">Activation Sensitivity = 3 (Low Sensitivity)</td>
        </tr>
        <tr>
            <td>With Noise Resistance</td>
            <td>129</td>
            <td>50</td>
            <td>12</td>
            <td>100</td>
            <td>31</td>
            <td>1</td>
            <td>0.98</td>
        </tr>
        <tr>
            <td>w/ Noise Resistance</td>
            <td>125</td>
            <td>116</td>
            <td>N/A</td>
            <td>100</td>
            <td>N/A</td>
            <td>N/A</td>
            <td>0.09</td>
        </tr>
        <tr>
            <td colspan=8 align="center">Activation Sensitivity = 2 (Medium Sensitivity)</td>
        </tr>
        <tr>
            <td>With Noise Resistance</td>
            <td>139</td>
            <td>85</td>
            <td>10</td>
            <td>100</td>
            <td>51</td>
            <td>2</td>
            <td>0.95</td>
        </tr>
        <tr>
            <td>w/ Noise Resistance</td>
            <td>125</td>
            <td>111</td>
            <td>N/A</td>
            <td>100</td>
            <td>N/A</td>
            <td>N/A</td>
            <td>0.14</td>
        </tr>
        <tr>
            <td colspan=8 align="center">Activation Sensitivity = 1 (High Sensitivity)</td>
        </tr>
        <tr>
            <td>With Noise Resistance</td>
            <td>123</td>
            <td>99</td>
            <td>5</td>
            <td>100</td>
            <td>71</td>
            <td>1</td>
            <td>0.90</td>
        </tr>
        <tr>
            <td>w/ Noise Resistance</td>
            <td>141</td>
            <td>122</td>
            <td>N/A</td>
            <td>100</td>
            <td>N/A</td>
            <td>N/A</td>
            <td>0.19</td>
        </tr>
    </tbody>
</table>  

*Table 1.1.1: Recorded data for Test1.1*

The testing results were recored in **Table 1.1.1** and **Table 1.2.1**, relevant data was calculated. **Figure 1.1.1** shows significant increase in reliability with respect to the noise resistance mechanism, and a modest decrease when raised the activation sensitivity from medium to high. However in **Figure 1.1.2**, it is shown that when the activation sensitivity was low, 75% of failed transmission were prevented in respect of the SNR check, whereas when the activation sensitivity was high, a majority of failed transmission were prevented by the error detecting code. Overall, the system can achieve approximately 90% reliability in a continuous disruptive noise condition.

<img src="https://github.com/jasper-zheng/PyAudible/blob/main/tests/Figures/F_1.1.1.png?raw=true" width="400">

*Figure 1.1.1 noise resistance mechanism Reliability*  

<img src="https://github.com/jasper-zheng/PyAudible/blob/main/tests/Figures/F_1.1.2.png?raw=true" width="400">

*Figure 1.1.2 Number of failed transmission prevented by each technique*

##### Test 1.2 Results: Sudden Disruptive Noise
<table style="font-size:7px">
    <thead>
        <tr>
            <th></th>
            <th>Total Transmission</th>
            <th>Failed Transmission</th>
            <th>Fault was Detected</th>
            <th>Fault Detection</th>
            <th>Reliability</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=6 align="center">Transmission Rate = 20</td>
        </tr>
        <tr>
            <td>With Noise Resistance</td>
            <td>100</td>
            <td>56</td>
            <td>54</td>
            <td>2</td>
            <td>0.96</td>
        </tr>
        <tr>
            <td>w/ Noise Resistance</td>
            <td>100</td>
            <td>70</td>
            <td>N/A</td>
            <td>N/A</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td colspan=6 align="center">Transmission Rate = 10</td>
        </tr>
        <tr>
            <td>With Noise Resistance</td>
            <td>100</td>
            <td>67</td>
            <td>63</td>
            <td>2</td>
            <td>0.94</td>
        </tr>
        <tr>
            <td>w/ Noise Resistance</td>
            <td>100</td>
            <td>60</td>
            <td>N/A</td>
            <td>N/A</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td colspan=6 align="center">Transmission Rate = 5</td>
        </tr>
        <tr>
            <td>With Noise Resistance</td>
            <td>100</td>
            <td>70</td>
            <td>67</td>
            <td>4</td>
            <td>0.95</td>
        </tr>
        <tr>
            <td>w/ Noise Resistance</td>
            <td>100</td>
            <td>67</td>
            <td>N/A</td>
            <td>N/A</td>
            <td>N/A</td>
        </tr>
    </tbody>
</table>   

*Table 1.2.1: Recorded data for Test1.2*  

Since the control group did not implement the error detecting code, once the transmission was failed, there was no way to recover from the fault. However, **Figure 1.2.1** shows that we could expect the system reliability to be above 0.9 over all the transmission rates. And the transmission rate did not have an evident affect on the reliability when confronting disruptive noise.  

Although CRC can promise a high-efficiency error detection, a few errors still occurred during the test. By locating the incorrect transmissions, it turned out that the checksum codes in these transmissions were broken due to the noise. In the error detecting process design, if a checksum code is broken, the system will skip the CRC to reduce the number of False Positives. Therefore, those errors were escaped from the error detection. However, these errors could be prevented if changing the design of the error detecting process from skipping the broken checksum codes to request a honest CRC strictly.  

<img src="https://github.com/jasper-zheng/PyAudible/blob/main/tests/Figures/F_1.2.1.png?raw=true" width="400">

*Figure 1.2.1 noise resistance mechanism Reliability (Disruptive Noise)*  

## Phase II Evaluation: System Reliability vs. Speed and Signal to Noise Ratio  

Since the protocol only provide limited number of channels, the system is assumed that it could either sacrifice speed to improve accuracy, or improve speed and expect occasionally failed transmission or incorrect receipt that might decrease reliability. Therefore, the main purpose of Phase III Evaluation is to assess the transmission success rate and reliability of the system under different speed settings and noise conditions.

#### Experiment Design  
##### Test 2.1: System Reliability  

![SNR](Graphics/snr.jpg)  

The testing system includes a MacBook as receiver, and an iPhone as transmitter. Two devices were implemented in a silent room with acoustic control, distanced two meters. A separated speaker and a decibel noise meter were used to produce pre-recored noise and precisely control the signal to noise ratio in the system.   

The test includes 12 rounds, in the first three rounds, the signal to noise ratio was maintained at 1.2, the speed was set to 5, 10, 20 bytes / sec respectively. In the second and the third round, the signal to noise ratio was maintained at 1.5, 2 and 2.5. In each round, 100 pieces random generated data with random length were transmitted through the system, following data was collected:  

 * **Received Transmission:** Number of times that the transmission reached and accepted by the receiver, regardless the correctness.
 * **Correct Transmission:** Number of times that the transmission reached and accepted by the receiver, and the receiving was correct.   

The transmission success rate `S` defines the ratio between total number of correct received data and total number of transmission. The reliability `R` defines the ratio between total number of correct received data and total number of received data.  

![equation](https://latex.codecogs.com/svg.image?S&space;=&space;\frac{CorrectTransmission}{TotalTransmission})  

![equation](https://latex.codecogs.com/svg.image?R&space;=&space;\frac{CorrectTransmission}{ReceivedTransmission})  


#### Experiment Results
##### Test 2.1: System Reliability
<table style="font-size:7px">
    <thead>
        <tr>
            <th>Transmission Speed</th>
            <th>Total Transmission</th>
            <th>Received Transmission</th>
            <th>Correct Transmission</th>
            <th>Transmission Success Rate</th>
            <th>Reliability</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=6 align="center">SNR = 1.2</td>
        </tr>
        <tr>
            <td>5</td>
            <td>100</td>
            <td>23</td>
            <td>20</td>
            <td>0.20</td>
            <td>0.86</td>
        </tr>
        <tr>
            <td>10</td>
            <td>100</td>
            <td>15</td>
            <td>11</td>
            <td>0.11</td>
            <td>0.73</td>
        </tr>
        <tr>
            <td>20</td>
            <td>100</td>
            <td>16</td>
            <td>9</td>
            <td>0.07</td>
            <td>0.56</td>
        </tr>
        <tr>
            <td colspan=6 align="center">SNR = 1.5</td>
        </tr>
        <tr>
            <td>5</td>
            <td>100</td>
            <td>78</td>
            <td>72</td>
            <td>0.72</td>
            <td>0.92</td>
        </tr>
        <tr>
            <td>10</td>
            <td>100</td>
            <td>64</td>
            <td>54</td>
            <td>0.54</td>
            <td>0.84</td>
        </tr>
        <tr>
            <td>20</td>
            <td>100</td>
            <td>58</td>
            <td>47</td>
            <td>0.47</td>
            <td>0.81</td>
        </tr>
        <tr>
            <td colspan=6 align="center">SNR = 2</td>
        </tr>
        <tr>
            <td>5</td>
            <td>100</td>
            <td>99</td>
            <td>99</td>
            <td>0.99</td>
            <td>1.00</td>
        </tr>
        <tr>
            <td>10</td>
            <td>100</td>
            <td>75</td>
            <td>73</td>
            <td>0.73</td>
            <td>0.97</td>
        </tr>
        <tr>
            <td>20</td>
            <td>100</td>
            <td>79</td>
            <td>66</td>
            <td>0.66</td>
            <td>0.96</td>
        </tr>
        <tr>
            <td colspan=6 align="center">SNR = 2.5</td>
        </tr>
        <tr>
            <td>5</td>
            <td>100</td>
            <td>99</td>
            <td>99</td>
            <td>0.99</td>
            <td>1.00</td>
        </tr>
        <tr>
            <td>10</td>
            <td>100</td>
            <td>95</td>
            <td>95</td>
            <td>0.95</td>
            <td>1.00</td>
        </tr>
        <tr>
            <td>20</td>
            <td>100</td>
            <td>91</td>
            <td>90</td>
            <td>0.90</td>
            <td>0.99</td>
        </tr>
    </tbody>
</table>   

*Table 2.1: Recorded data for test2.1*  

After 100 pieces of data were transmitted, the transmission success rate `S` was calculated as the ratio between total number of correct received data and total number of transmission. **Figure 2.1.1** shows an exponential increase in the success rate with respect to signal to noise ratio. When SNR is greater than 2, the success rate for the slow transmission setting almost reach 1, and when increase SNR to 2.5, we could approximately expect a success rate over 0.9.  

The reliability `R` was defined as the ratio between total number of correct received data and total number of received data. **Figure 2.1.2** illustrates how the reliability was affected by the transmission rate and the signal to noise ratio. Since the reliability represents the correctness of the transmission, it was expected to have a higher value than transmission success rate. The figure shows that to achieve at least 0.9 reliability, `SNR` should be maintain above 1.5 for the slow transmission setting, and above 2 for the medium and fast transmission settings.  

<img src="https://github.com/jasper-zheng/PyAudible/blob/main/tests/Figures/F_2.1.1.png?raw=true" width="400">

*Figure 2.1.1: Transmission Success Rate vs. Speed and Signal to Noise Ratio*  

<img src="https://github.com/jasper-zheng/PyAudible/blob/main/tests/Figures/F_2.1.2.png?raw=true" width="400">

*Figure 2.1.2: System Reliability vs. Speed and Signal to Noise Ratio*  
