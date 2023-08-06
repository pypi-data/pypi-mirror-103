# PyAudible - Receiver
#

'''

Overview
--------

**Classes**
  :py:class:`Receiver`
  

'''
__version__ = "1.1.0"

import pyaudio
import numpy as np
import time

from scipy.fftpack import fft

#%%

class Receiver(object):
    '''
    PyAudio Receiver. Use `receiver.Receiver()` to create an instantiation.
    
    '''
    
    CHUNK               = 1024 * 2
    FORMAT              = pyaudio.paInt16
    CHANNELS            = 1
    RATE                = 44100
    
    FRAMES_PER_FFT      = 16 # FFT takes average across how many frames
    SAMPLES_PER_FFT     = CHUNK * FRAMES_PER_FFT
    FREQ_STEP           = float(RATE)/SAMPLES_PER_FFT
    
    CHANNEL_NUMBER      = 8
    SHARED_CHANNEL      = 8
    TRACK_NUM           = 1
    
    FRAME_TIME          = 0.2
    
    active_freq_bin     = [55,193,323]
    #ending_freq_bin     = [56,196,323]
    #ending_channel_num  = [0,4,7]
    ending_freq_bin     = [56,323]
    ending_channel_num  = [0,7]

    d_channel_1 = [[53,57,58],[59,60],[61,62],[63,64],[65,66],[67,68],[69,70],[71,72],[73,74],[75,76],[77,78],[79,80],[81,82],[83,84],[85,86],[87,88]]
    d_channel_2 = [[91,92],[93,94],[95,96],[97,98],[99,100],[101,102],[103,104],[105,106],[107,108],[109,110],[111,112],[113,114],[115,116],[117,118],[119,120],[121,122]]
    d_channel_3 = [[125,126],[127,128],[129,130],[131,132],[133,134],[135,136],[137,138],[139,140],[141,142],[143,144],[145,146],[147,148],[149,150],[151,152],[153,154],[155,156]]
    d_channel_4 = [[159,160],[161,162],[163,164],[165,166],[167,168],[169,170],[171,172],[173,174],[175,176],[177,178],[179,180],[181,182],[183,184],[185,186],[187,188],[189,190]]
    d_channel_5 = [[191,192],[193,194],[195,196],[197,198],[199,200],[201,202],[203,204],[205,206],[207,208],[209,210],[211,212],[213,214],[215,216],[217,218],[219,220],[221,222]]
    d_channel_6 = [[223,224],[225,226],[227,228],[229,230],[231,232],[233,234],[235,236],[237,238],[239,240],[241,242],[243,244],[245,246],[247,248],[249,250],[251,252],[253,254]]
    d_channel_7 = [[257,258],[259,260],[261,262],[263,264],[265,266],[267,268],[269,270],[271,272],[273,274],[275,276],[277,278],[279,280],[281,282],[283,284],[285,286],[287,288]]
    d_channel_8 = [[291,292],[293,294],[295,296],[297,298],[299,300],[301,302],[303,304],[305,306],[307,308],[309,310],[311,312],[313,314],[315,316],[317,318],[319,320],[321,322,323]]
    d_channel_9 = [[324]]
    
    d_channel = []    
    chunk_list = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
    

    activation_info = [[],[],[],[],[]]
    received_info   = [] #i0: Estimated length
    ending_info     = [[],[],[],[],[],[],[],[]]
    ending_mark     = [0,0,0,0,0] #i0: ending pointer, i1: Estimated length, i2-4: crc
    
    status = 0
    #speed_info = [[0,0],[0,2],[1,3]]
    speed_info = [[0,0],[4,0],[7,0]]
    
    def __init__(self, actived_channel = 8, sensitivity = 'medium', speed = 'auto'):
        '''
        Initialise a PyAudible Receiver.

        Parameters
        ----------
        actived_channel : int, optional
            Number of actived channel. The default is 8.
        sensitivity : string, 'low', 'medium' or 'high', optional
            sensitivity defines the threshold that 
            activate the receiver. With a higher sensitivity, the 
            receiver will tend to pass the SNR Check easily and be 
            activated for transmission. The default is 'medium'.
        speed : string, 'slow', 'medium' or 'fast' , optional
            By default, the transmission speed of the receiver will
            be automatically determined by the Flow Control 
            Descriptor defined in the Sound Mark. However, there is 
            still an option to use a fixed receiving speed, and the 
            receiver will ignore the transmissions that don't match 
            this defined speed. The default is 'auto'.

        Raises
        ------
        ParameterError
            if the parameter `speed` or `sensitivity` is invalid.

        Returns
        -------
        None.

        '''
        self.d_channel.append(self.d_channel_1)
        self.d_channel.append(self.d_channel_2)
        self.d_channel.append(self.d_channel_3)
        self.d_channel.append(self.d_channel_4)
        self.d_channel.append(self.d_channel_5)
        self.d_channel.append(self.d_channel_6)
        self.d_channel.append(self.d_channel_7)
        self.d_channel.append(self.d_channel_8)
        self.d_channel.append(self.d_channel_9)
        
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format = self.FORMAT,
            channels = self.CHANNELS,
            rate = self.RATE,
            input = True,
            output = True,
            frames_per_buffer = self.CHUNK
            )
        
        self.current_bins = []
        self.pointers = []
        self.recieved_bins = []
        self.fft = []
        self.scheduled_pointer = 0
        self.retrieved_data = []
        if sensitivity == 'medium':
            self.sensitivity = 2
        elif sensitivity == 'low':
            self.sensitivity = 3
        elif sensitivity == 'high':
            self.sensitivity = 1
        else:
            raise ParameterError(message = 'sensitivity could only be low, medium, or high')
            
        for i in range(self.SHARED_CHANNEL):
            self.pointers.append(0)
            self.current_bins.append([0,0,0,0,0,0,0])
            self.recieved_bins.append([])
        
    def refresh_audio(self):
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format = self.FORMAT,
            channels = self.CHANNELS,
            rate = self.RATE,
            input = True,
            output = True,
            frames_per_buffer = self.CHUNK
            )
        
    def update_speed_info(self):
        if (self.SHARED_CHANNEL == 8):
            self.speed_info = [[0,0],[4,0],[7,0]]
        elif (self.SHARED_CHANNEL == 2):
            self.speed_info = [[0,0],[0,2],[1,3]]
        else:
            self.speed_info = [[0,0],[0,1],[3,1]]
    
    def callback(self, input_data, frame_count, time_info, flags):
    
        return (input_data, pyaudio.paContinue)

    def read_block(self, standby_time):
        '''
        Read the input audio (Blocking Mode):
            Standby and listen until all the equested frames have been recorded.

        Parameters
        ----------
        standby_time : int
            The requested time (in second).

        Returns
        -------
        retrieved_data: list
            Every retrieved data during the standby time

        '''
        frame_count = 0
        start_time = time.time()
        
        self.scheduled_pointer = 0
        while (time.time() - start_time < standby_time):
            bit = self.read_frame()
            print(bit, end=(''))
            frame_count += 1
        
        return self.retrieved_data
    
    def read_frame_audio(self, audio, log = False):
        '''
        Takes 2048 frames of audio data and perform analysis.

        Parameters
        ----------
        audio : np array with a size of (2048,)
            The array version of the audio buffer.
        log : bool, optional
            If true, it will add a status flag to the returns, 
            accompany with the retrived result. 
            The default is False.

        Returns
        -------
        retrieved_data: String
            The retrieved and demodulated data, empty if the 
            receiver have not detected anything yet.
        
        status: int
            0: Unactivated
            1: Activating
            2: Activated, preparing
            3: Activation Failed, rollback to unactivated
            4: Listening
            5: Terminated, received auccessfully
            6: Terminated, received failed

        '''
        try:
            if (audio.shape[0]==2048):
                self.fft = fft(audio)
                #######################
                
                
                freq_bins = []
                for i in range(self.SHARED_CHANNEL):
                    candidate_freq = []
                    for j in range(int(self.CHANNEL_NUMBER/self.SHARED_CHANNEL)):
                        freq_bin = np.abs(self.fft[ self.d_channel[j*self.SHARED_CHANNEL+i][0][0]  : self.d_channel[j*self.SHARED_CHANNEL+i][15][-1]+1 ]).argmax() + self.d_channel[j*self.SHARED_CHANNEL+i][0][0]
                        candidate_freq.append(freq_bin)
                    freq_bins.append(candidate_freq)
                #print(freq_bins)
                try:
                    self.status = self.update_statue(freq_bins,self.status)
                except ActivationError as ae:
                    print(ae)
                bit = ''
                if self.status==4 and len(self.recieved_bins[0]) != self.scheduled_pointer:
                    length = True
                    for i in range(self.SHARED_CHANNEL-1):
                        if len(self.recieved_bins[i])==len(self.recieved_bins[i+1]):
                            continue
                        else:
                            length = False
                            break
                    if length:
                        bit = self.convert_result([[item[-1]] for item in self.recieved_bins])
                        self.scheduled_pointer = len(self.recieved_bins[0])
                if log:
                    if self.status == 3:
                        self.status = 0
                        return bit, 3
                    elif self.status == 5:
                        self.status = 0
                        return self.retrieved_data[-1], 5
                    elif self.status == 6:
                        self.status = 0
                        return bit, 6
                    else:
                        return bit, self.status
                else:
                    if self.status == 3:
                        self.status = 0
                        return ''
                    elif self.status == 5:
                        self.status = 0
                        return self.retrieved_data[-1]
                    elif self.status == 6:
                        self.status = 0
                        return ''
                    else:
                        return bit
            else:
                raise AttributeError
                
                
                
                #######################
        except AttributeError:
                print('The number of frames need to be 2048')
    
    
    def read_frame(self, log = False):
        '''
        Read the input audio (Callback Mode):
            Called each frame to listen to the audio.

        Parameters
        ----------
        log : bool, optional
            If true, it will add a status flag to the returns, 
            accompany with the retrived result. 
            The default is False.

        Returns
        -------
        retrieved_data: String
            The retrieved and demodulated data, empty if the 
            receiver have not detected anything yet.
        
        status: int
            0: Unactivated
            1: Activating
            2: Activated, preparing
            3: Activation Failed, rollback to unactivated
            4: Listening
            5: Terminated, received auccessfully
            6: Terminated, received failed

        '''
        data = self.stream.read(self.CHUNK, exception_on_overflow = False)
        data_int = np.frombuffer(data, dtype = np.int16)
        self.fft = fft(data_int)
        
        #######################
        
        
        freq_bins = []
        for i in range(self.SHARED_CHANNEL):
            candidate_freq = []
            for j in range(int(self.CHANNEL_NUMBER/self.SHARED_CHANNEL)):
                freq_bin = np.abs(self.fft[ self.d_channel[j*self.SHARED_CHANNEL+i][0][0]  : self.d_channel[j*self.SHARED_CHANNEL+i][15][-1]+1 ]).argmax() + self.d_channel[j*self.SHARED_CHANNEL+i][0][0]
                candidate_freq.append(freq_bin)
            freq_bins.append(candidate_freq)
        #print(freq_bins)
        try:
            self.status = self.update_statue(freq_bins,self.status)
        except ActivationError as ae:
            print(ae)
        bit = ''
        if self.status==4 and len(self.recieved_bins[0]) != self.scheduled_pointer:
            length = True
            for i in range(self.SHARED_CHANNEL-1):
                if len(self.recieved_bins[i])==len(self.recieved_bins[i+1]):
                    continue
                else:
                    length = False
                    break
            if length:
                try:
                    bit = self.convert_result([[item[-1]] for item in self.recieved_bins])
                    self.scheduled_pointer = len(self.recieved_bins[0])
                except:
                    print('transmission interrupted')
                    self.status = 6
                    self.clear_session()
                
        if log:
            if self.status == 3:
                self.status = 0
                return bit, 3
            elif self.status == 5:
                self.status = 0
                return self.retrieved_data[-1], 5
            elif self.status == 6:
                self.status = 0
                return bit, 6
            else:
                return bit, self.status
        else:
            if self.status == 3:
                self.status = 0
                return ''
            elif self.status == 5:
                self.status = 0
                return self.retrieved_data[-1]
            elif self.status == 6:
                self.status = 0
                return ''
            else:
                return bit
            
        #######################

    def most_frequent(self, List): 
        counter = 0
        num = List[0]
        for i in List: 
            curr_frequency = List.count(i) 
            if(curr_frequency> counter): 
                counter = curr_frequency 
                num = i 
        return num
    def get_bin_num(self, freq_bin,n):
        for i in range(16):
            if freq_bin in self.d_channel[n][i]:
                return i
        print('request {} in number {} channel'.format(freq_bin,n))
        return 99
    
    

    def update_statue(self, freq_bins,status):
        '''
        Status:
            0: Unactivated
            1: Activating
            2: Activated, Preparing
            3: Activation Failed, rollback to unactivated
            4: Listening
                4.5 (Hide): Terminating
            5: Terminated, Received Successfully
            6: Terminated, Received Failed
        '''
         # if the activation frequency is been detected three times, 
        if (status == 0):
            if (freq_bins[self.speed_info[0][0]][self.speed_info[0][1]] == self.active_freq_bin[0] and freq_bins[self.speed_info[1][0]][self.speed_info[1][1]] == self.active_freq_bin[1] and freq_bins[self.speed_info[2][0]][self.speed_info[2][1]] == self.active_freq_bin[2]):
                self.activation_info = [[],[],[],[],[]]
                self.received_info = []
                self.pointers[0] = 1
                status = 1
                print('activating...')
                ########## TODO ##########
                self.activation_info[0].append(freq_bins[1][0])
                self.activation_info[1].append(freq_bins[2][0])
                self.activation_info[2].append(freq_bins[3][0])
                self.activation_info[3].append(self.get_bin_num(freq_bins[5][0],5))
                self.activation_info[4].append(self.get_bin_num(freq_bins[6][0],6))
                
        elif (status == 1):
            if (freq_bins[self.speed_info[0][0]][self.speed_info[0][1]] == self.active_freq_bin[0] and freq_bins[self.speed_info[1][0]][self.speed_info[1][1]] == self.active_freq_bin[1] and freq_bins[self.speed_info[2][0]][self.speed_info[2][1]] == self.active_freq_bin[2]):
                self.pointers[0] += 1
                ########## TODO ##########
                self.activation_info[0].append(freq_bins[1][0])
                self.activation_info[1].append(freq_bins[2][0])
                self.activation_info[2].append(freq_bins[3][0])
                self.activation_info[3].append(self.get_bin_num(freq_bins[5][0],5))
                self.activation_info[4].append(self.get_bin_num(freq_bins[6][0],6))
                
                if (self.pointers[0] == self.sensitivity):
                    self.SHARED_CHANNEL = self.most_frequent(self.activation_info[3]+self.activation_info[4])
                    if self.SHARED_CHANNEL!=4 and self.SHARED_CHANNEL!=8 and self.SHARED_CHANNEL!=2:
                        self.clear_session()
                        status = 3
                        raise ActivationError
                        
                    self.TRACK_NUM = int(self.CHANNEL_NUMBER / self.SHARED_CHANNEL)
                    self.update_speed_info()
                    self.current_bins = []
                    self.recieved_bins = []
                    self.pointers = []
                    for i in range(self.SHARED_CHANNEL):
                        self.current_bins.append([0,0,0,0,0,0,0])
                        self.recieved_bins.append([])
                        self.pointers.append(0)
                    status = 2
                    #self.pointers[0] = 0
                    print("Activated, on preparing")
                    
                    
            else:
                self.clear_session()
                status = 3
                
                
                print('activation failed')
        elif (status == 2):
            if (freq_bins[self.speed_info[0][0]][self.speed_info[0][1]] != self.active_freq_bin[0] and freq_bins[self.speed_info[2][0]][self.speed_info[2][1]] != self.active_freq_bin[2]):
                #print(self.activation_info)
                self.received_info.append(100*self.get_bin_num(self.most_frequent(self.activation_info[0]),1) + 10*self.get_bin_num(self.most_frequent(self.activation_info[1]),2) + self.get_bin_num(self.most_frequent(self.activation_info[2]),3))
                
                
                print('Estimated length: {}'.format(self.received_info[0]))
                print('On recieving...')
                self.d_channel[0][0] = [57,58]
                #self.d_channel[7][15] = [311,312]
                status = self.check_channels(freq_bins)
            else:
                ########## TODO ##########
                if self.SHARED_CHANNEL == 8:
                    self.activation_info[0].append(freq_bins[1][0])
                    self.activation_info[1].append(freq_bins[2][0])
                    self.activation_info[2].append(freq_bins[3][0])
                elif self.SHARED_CHANNEL == 2:
                    self.activation_info[0].append(freq_bins[1][0])
                    self.activation_info[1].append(freq_bins[0][1])
                    self.activation_info[2].append(freq_bins[1][1])
                else:
                    self.activation_info[0].append(freq_bins[1][0])
                    self.activation_info[1].append(freq_bins[2][0])
                    self.activation_info[2].append(freq_bins[3][0])
                       
        elif (status == 4):
            status = self.check_channels(freq_bins)
            
            if (self.ending_mark[0]>=1):
                self.ending_mark[0] += 1
                ########## TODO ##########
                if self.SHARED_CHANNEL == 8:
                    self.ending_info[0].append(freq_bins[0][0])
                    self.ending_info[1].append(freq_bins[1][0])
                    self.ending_info[2].append(freq_bins[2][0])
                    self.ending_info[3].append(freq_bins[3][0])
                    self.ending_info[4].append(freq_bins[4][0])
                    self.ending_info[5].append(freq_bins[5][0])
                    self.ending_info[6].append(freq_bins[6][0])
                    self.ending_info[7].append(freq_bins[7][0])
                elif self.SHARED_CHANNEL == 2:
                    self.ending_info[0].append(freq_bins[0][0])
                    self.ending_info[1].append(freq_bins[1][0])
                    self.ending_info[2].append(freq_bins[0][1])
                    self.ending_info[3].append(freq_bins[1][1])
                    self.ending_info[4].append(freq_bins[0][2])
                    self.ending_info[5].append(freq_bins[1][2])
                    self.ending_info[6].append(freq_bins[0][3])
                    self.ending_info[7].append(freq_bins[1][3])
                else:
                    self.ending_info[0].append(freq_bins[0][0])
                    self.ending_info[1].append(freq_bins[1][0])
                    self.ending_info[2].append(freq_bins[2][0])
                    self.ending_info[3].append(freq_bins[3][0])
                    self.ending_info[4].append(freq_bins[0][1])
                    self.ending_info[5].append(freq_bins[1][1])
                    self.ending_info[6].append(freq_bins[2][1])
                    self.ending_info[7].append(freq_bins[3][1])
                
                if self.ending_mark[0] >= 5:
                    
                    validated = 0
                    for i in range(2):
                        count = 0
                        for info in self.ending_info[self.ending_channel_num[i]]:
                            if info == self.ending_freq_bin[i]:
                                count += 1
                                if count == 2:
                                    validated += 1
                                    break
                    if validated == 2:
                        #if validated ended
                        print('')
                        self.d_channel[0][0] = [53,57,58]
                        self.ending_mark[0] = 0
                        self.ending_mark[1]=100*self.get_bin_num(self.most_frequent(self.ending_info[1]),1) + 10*self.get_bin_num(self.most_frequent(self.ending_info[2]),2) + self.get_bin_num(self.most_frequent(self.ending_info[3]),3)
                        print('Ending marks estimated length: {}'.format(self.ending_mark[1]))
                        
                        crc_bin = [0,0,0]
                        crc_bin[0] = self.get_bin_num(self.most_frequent(self.ending_info[4]),4)
                        crc_bin[1] = self.get_bin_num(self.most_frequent(self.ending_info[5]),5)
                        crc_bin[2] = self.get_bin_num(self.most_frequent(self.ending_info[6]),6)
                        crc = ''
                        print(crc_bin)
                        for i in range(3):
                            if ( crc_bin[i] == 2):
                                crc += '0'
                            elif ( crc_bin[i] == 5):
                                crc += '1'
                            else:
                                crc = None
                                print('escaped from crc test')
                                break
                        
                        if(self.check_result(self.received_info[0], self.ending_mark[1], self.copy_recieved_bins) == 1):
                            try: 
                                result = self.convert_result(self.copy_recieved_bins, self.trim, crc)
                            except UnicodeDecodeError:
                                print('UnicodeDecodeError')
                                self.clear_session()
                                return 6
                            except CRCError:
                                print('CRCError')
                                self.clear_session()
                                return 6
                            self.retrieved_data.append(result)
                            #print(result)
                            
                            self.clear_session()
                            
                            return 5
                        else:
                            self.clear_session()
                            return 6
                    else:
                        #if not ended
                        self.d_channel[0][0] = [57,58]
                        self.ending_mark[0] = 0
                
            elif (freq_bins[self.speed_info[2][0]][self.speed_info[2][1]] == self.ending_freq_bin[1]):
                #if one of the ending bit appears, expande the fft scope, start monitoring for 5 frames
                #create copy of recieved_bin
                #undo the pointer
                self.ending_mark[0] = 1
                self.d_channel[0][0] = [56,57,58]
                self.ending_info = [[],[],[],[],[],[],[],[]]
                
                self.copy_recieved_bins = []
                for bins in self.recieved_bins:
                    copy_bins = bins.copy()
                    self.copy_recieved_bins.append(copy_bins)
                for pointer, current_bin, recieved_bin in zip(self.pointers, self.current_bins, self.copy_recieved_bins):
                    if pointer >= 3:
                        recieved_bin.append(current_bin[pointer-1])
        return status
    
    def clear_session(self):
        self.activation_info = [[],[],[],[],[]]
        self.received_info = []
        self.SHARED_CHANNEL = 8
        self.scheduled_pointer = 0
        self.trim = 0
        self.update_speed_info()
        self.d_channel[0][0] = [53,57,58]
        self.ending_mark = [0,0,0,0,0]
        self.refresh_audio()
        #self.TRACK_NUM = int(self.CHANNEL_NUMBER / self.SHARED_CHANNEL)
    
    def check_channels(self, freq_bins):
        frame_result = []
        for freq_bin, current_bin, recieved_bin,i in zip(freq_bins,self.current_bins,self.recieved_bins,range(self.SHARED_CHANNEL)):
            freq_bin_nums = []
            for j in range(self.TRACK_NUM):
                freq_bin_nums.append(self.get_bin_num(freq_bin[j],j*self.SHARED_CHANNEL+i))
            frame_result.append(freq_bin_nums)
            freq_bin_num = self.most_frequent(freq_bin_nums)
            if (self.pointers[i]==0):
                current_bin[self.pointers[i]] = freq_bin_num
                self.pointers[i] += 1
            elif ( freq_bin_num == current_bin[self.pointers[i]-1]) or (self.pointers[i] < 3):
                #if this bit is the same as the last bit
                current_bin[self.pointers[i]] = freq_bin_num
                self.pointers[i] += 1
                if (self.pointers[i] == 7):
                    recieved_bin.append(current_bin[self.pointers[i]-1])
                    current_bin[0] = freq_bin_num
                    self.pointers[i] = 3
            else:
                #if new bit appears,
                number = self.most_frequent(current_bin[0:self.pointers[i]-1])
                recieved_bin.append(number)
                current_bin[0] = freq_bin_num
                self.pointers[i] = 1
        #print(frame_result)
        
        return 4
        
    def bin_to_text(self,bin_data):
        st = ''
        for i in range(len(bin_data)):
            st += str(int(bin_data[i]))
        st = st[:1]+'b'+st[1:]
        n = int(st, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    
    def check_result(self, a, e, received):
        minimum_block_length = self.SHARED_CHANNEL * 4
        full_length_a = (int((a-1) / minimum_block_length) + 1)
        full_length_e = (int((e-1) / minimum_block_length) + 1)
        
        for i in range(self.SHARED_CHANNEL):
            if len(received[i]) == full_length_a:
                self.trim = a
                continue
            elif len(received[i]) == full_length_e:
                self.trim = e
                continue
            else:
                print('recieve failed')
                return 0
        return 1
        
    def convert_result(self, received, trim = -1, crc = None):
        '''
        Convert received binaries from all channels to demodulated text

        Parameters
        ----------
        received : ndarray (binaries)
            received binaries from all channels.
        trim : int (optional)
            set the trimming point.
        crc : 

        Returns
        -------
        result : string
            converted message.

        '''
        binary = ''
        
        for i in range(len(received[0])):
            for j in range(self.SHARED_CHANNEL):
                binary += self.chunk_list[received[j][i]]
                
        if crc:
            if self.crc_check(binary,'1011',crc):
                i = 0
                print('crc {} passed'.format(crc))
            else:    
                raise CRCError 
        if trim == -1:
            trim = len(binary)
        #print(binary)
        return self.bin_to_text(binary[0:trim])
    
    def crc_check(self, input_bitstring, polynomial_bitstring = '1011', check_value = '000'):
        """Calculate the CRC check of a string of bits using a chosen polynomial."""
        polynomial_bitstring = polynomial_bitstring.lstrip('0')
        len_input = len(input_bitstring)
        initial_padding = check_value
        input_padded_array = list(input_bitstring + initial_padding)
        while '1' in input_padded_array[:len_input]:
            cur_shift = input_padded_array.index('1')
            for i in range(len(polynomial_bitstring)):
                input_padded_array[cur_shift + i] \
                = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
        return ('1' not in ''.join(input_padded_array)[len_input:])

    def get_fft(self):
        '''
        Get the discrete Fourier transform result of current audio input

        Returns
        -------
        np array with a size of (2048,)
            FFT result.

        '''
        return self.fft
        
    def get_status(self):
        '''
        Get the current status of connection.

        Returns
        -------
        int
            a integer signifying the current status.

        '''
        return self.status
        
    def clear(self):
        '''
        Clear the retrieved data

        Returns
        -------
        None.

        '''
        self.status = 0
        self.current_bins = []
        self.pointers = []
        self.recieved_bins = []
        self.fft = []
        self.retrieved_data = []
        for i in range(self.SHARED_CHANNEL):
            self.pointers.append(0)
            self.current_bins.append([0,0,0,0,0,0,0])
            self.recieved_bins.append([])
            
    def get_received_data(self):
        '''
        Return all received data

        Returns
        -------
        retrieved_data: list
            All retrieved data during the standby time

        '''
        return self.retrieved_data
    
#%%
    
class Error(Exception):
    """Base class for exceptions in this module."""
pass

class ParameterError(Error):
    
    def __init__(self, message = 'speed could only be slow, medium or fast'):
        self.message = message
        super().__init__(self.message)

class ActivationError(Error):
    
    def __init__(self, message = 'Activation failed, increase volume'):
        self.message = message
        super().__init__(self.message)
        
class ASCIIError(Error):
    def __init___(self, message = 'Invalid data received'):
        super().__init__(self.message)
        
class CRCError(Error):
    def __init___(self, message = 'crc test failed'):
        super().__init__(self.message)

#%%

def get_receiver_version():
    return [__version__, pyaudio.__version__, pyaudio.get_portaudio_version()]
    
def print_receiver_version():
    print('PyAudible receiver version {} \nPyAudio version {} \nPortAudio verision {} '.format(__version__,pyaudio.__version__,pyaudio.get_portaudio_version()))
    
    
    