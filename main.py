import scipy
from scipy import io
import pyaudio, struct
import tkinter as Tk   	
import numpy as np
import wave


def get_filter(i):
    '''
        Given a direction index (0 to 7) returns the HRTF filters
        corresponding to that direction (0 is directly infront 
        circles 45 degrees clock wise with increasing index)
    '''
    if i == 8:
        return -1 # No filter button 
    return left_filters[i],right_filters[i]

def get_background(i):
    '''
        Given an index 0 to 3 returns the name of the background file
        to be loaded
    '''
    if i == 0:
        return './Background/cafe_loud.wav'
    elif i == 1:
        return './Background/cafe_quiet.wav'
    elif i == 2:
        return './Background/beach.wav'
    elif i == 3:
        return './Background/hotel_lobby.wav'
    else:
        return -1
    
    
def get_noise(i):
    '''
        Given an index 0 to 3 returns the name of the noise file
        to be loaded
    '''
    if i == 0:
        return './Noise/rain.wav'
    elif i == 1:
        return './Noise/rain.wav'
    elif i == 2:
        return './Noise/rain.wav'
    elif i == 3:
        return './Noise/rain.wav'
    else:
        return -1

'''
Initialization of wav file parameters (same for all of our files)
'''
RATE        = 44100                  # Frame rate (frames/second)
WIDTH       = 2                      # Number of bytes per sample
CHANNELS    = 1                      # Number of channels
MAXVALUE = 2**(8*WIDTH-1) - 1


'''
Load the filter matrices
'''
left_mat = scipy.io.loadmat('left_filt')
right_mat = scipy.io.loadmat('right_filt')

left_filters = left_mat['h_l']
right_filters = right_mat['h_r']


'''
Flags indicating a button is just pressed
Triggers loading of new wav files and filters
'''
load_background_flag = 1
load_noise_flag = 1
load_filter_flag = 1

'''
Initial parameters
'''
DIRECTION = 2
BACKGROUND = 1
NOISE = 1

'''
Create pyaudio object for streaming audio
'''
p = pyaudio.PyAudio()
stream = p.open(
  format = pyaudio.paInt16,  
  channels = 2, 
  rate = RATE,
  input = False, 
  output = True,
  frames_per_buffer = 128)            
  # specify low frames_per_buffer to reduce latency


'''
Block processing stuff
'''
BLOCKLEN = 2048
states1 = np.zeros(199)
states2 = np.zeros(199)

'''
Connect to quit button to exit while loop
'''
CONTINUE = True

while CONTINUE:
    if load_background_flag == 1:
        wavfile_b = get_background(BACKGROUND)
        wfb = wave.open(wavfile_b, 'rb')
        binary_background = wfb.readframes(BLOCKLEN)
        
        load_background_flag = 0
    
    if load_noise_flag == 1:
        wavfile_n = get_background(NOISE)
        wfn = wave.open(wavfile_n, 'rb')
        binary_noise = wfn.readframes(BLOCKLEN)
        
        load_noise_flag = 0
    
    if load_filter_flag == 1:
        hl,hr = get_filter(DIRECTION)
        
        load_filter_flag = 0
    
    #Unpack the background and noise
    x1 = struct.unpack('h' * BLOCKLEN, binary_background)
    x2 = struct.unpack('h' * BLOCKLEN, binary_noise)
    
    #Filter the noise for each ear
    x2_l,states1 = scipy.signal.lfilter(hl, 1, x2,zi=states1)
    x2_r,states2 = scipy.signal.lfilter(hr, 1, x2,zi=states2)
    
    #Add background and noise to each ear
    '''
    Gains will be added
    '''
    y_l = 1*np.array(x1) + 0.2*np.array(x2_l)
    y_r = 1*np.array(x1) + 0.2*np.array(x2_r)
    
    #Clip and convert to integer
    y_l = np.clip(y_l.astype(int),-MAXVALUE,MAXVALUE)
    y_r = np.clip(y_r.astype(int),-MAXVALUE,MAXVALUE)
    
    '''
    Combines left and right ear
    Might need to find a better way to do this
    '''
    for i in range(BLOCKLEN):
        yl = y_l[i]
        yr = y_r[i]
        output_bytes1 = struct.pack('h', yl)
        output_bytes2 = struct.pack('h', yr)
        stream.write(output_bytes1+output_bytes2)
    
    binary_background = wfb.readframes(BLOCKLEN)
    if len(binary_background) < WIDTH * BLOCKLEN:
        wfb.rewind()
        binary_background = wfb.readframes(BLOCKLEN)
        
    binary_noise = wfn.readframes(BLOCKLEN)
    if len(binary_noise) < WIDTH * BLOCKLEN:
        wfn.rewind()
        binary_noise = wfn.readframes(BLOCKLEN)
    
stream.stop_stream()
stream.close()
p.terminate()