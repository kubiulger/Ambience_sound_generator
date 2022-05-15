import scipy
from scipy import io
from scipy import signal
import pyaudio, struct
import tkinter as Tk   	
import numpy as np
import wave



global CONTINUE
global DIRECTION,BACKGROUND,NOISE
global load_background_flag,load_noise_flag,load_filter_flag
global RECORDING


'''
TODO: 
    Add linear change in gain for sliders
    Add more noise files
    Add "No Direction" button and filter
    Make button parameters global
    Connect parameters to buttons
    Test and debug
    Add recording functionality
'''
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
        return './Noise/rain_inside.wav'
    elif i == 1:
        return './Noise/rain_outside.wav'
    elif i == 2:
        return './Noise/icemaker.wav'
    elif i == 3:
        return './Noise/garbage.wav'
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
DIRECTION = 1
BACKGROUND = 0
NOISE = 0
RECORDING = 0

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
BLOCKLEN = 256
states1 = np.zeros(199)
states2 = np.zeros(199)
g1_prev = 0.0
g2_prev = 0.0
g1_now = 0.6
g2_now = 0.3

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
        wavfile_n = get_noise(NOISE)
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
    
    g1_lin = (g1_now*g1_prev)*np.array(range(BLOCKLEN))/BLOCKLEN+g1_prev
    g2_lin = (g2_now*g2_prev)*np.array(range(BLOCKLEN))/BLOCKLEN+g2_prev
    
    y_l = g1_lin*np.array(x1) + g2_lin*np.array(x2_l)
    y_r = g1_lin*np.array(x1) + g2_lin*np.array(x2_r)
    
    
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
        
    g1_prev = g1_now
    g2_prev = g2_now
        
    '''
    Need to figure out how to do this
    '''
    if RECORDING == 1:
        wf = wave.open('recording.wav', 'w')
        wf.setnchannels(CHANNELS)         
        wf.setsampwidth(WIDTH)          
        wf.setframerate(RATE)
        wf.writeframes()
    
stream.stop_stream()
stream.close()
p.terminate()