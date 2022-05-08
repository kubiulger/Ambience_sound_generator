import scipy
from scipy import io
import pyaudio, struct
import tkinter as Tk   	
import numpy as np
import wave


wavfile_b = './Background/cafe_loud.wav'

wfb = wave.open(wavfile_b, 'rb')

# Read wave file properties
RATE        = wfb.getframerate()     # Frame rate (frames/second)
WIDTH       = wfb.getsampwidth()     # Number of bytes per sample
LEN         = wfb.getnframes()       # Signal length
CHANNELS    = wfb.getnchannels()     # Number of channels

MAXVALUE = 2**(8*WIDTH-1) - 1

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

wavfile_n = './Noise/rain.wav'

wfn = wave.open(wavfile_n, 'rb')

# Read wave file properties
RATE        = wfn.getframerate()     # Frame rate (frames/second)
WIDTH       = wfn.getsampwidth()     # Number of bytes per sample
LEN         = wfn.getnframes()       # Signal length
CHANNELS    = wfn.getnchannels()     # Number of channels

MAXVALUE = 2**(8*WIDTH-1) - 1

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)



left_mat = scipy.io.loadmat('left_filt')
right_mat = scipy.io.loadmat('right_filt')

left_filters = left_mat['h_l']
right_filters = right_mat['h_r']

def get_filter(i):
    return left_filters[i],right_filters[i]

def get_background(i):
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
    if i == 0:
        return 0
    elif i == 1:
        return 1
    elif i == 2:
        return 2
    elif i == 3:
        return 3
    else:
        return -1


DIRECTION = 5

hl,hr = get_filter(DIRECTION)
a = 1

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
  format = pyaudio.paInt16,  
  channels = 2, 
  rate = RATE,
  input = False, 
  output = True,
  frames_per_buffer = 128)            
  # specify low frames_per_buffer to reduce latency



BLOCKLEN = 2048
states1 = np.zeros(199)
states2 = np.zeros(199)

binary_data1 = wfb.readframes(BLOCKLEN)
binary_data2 = wfn.readframes(BLOCKLEN)


while len(binary_data2) == WIDTH * BLOCKLEN:

    
    x1 = struct.unpack('h' * BLOCKLEN, binary_data1)
    x2 = struct.unpack('h' * BLOCKLEN, binary_data2)
    
    x2_l,states1 = scipy.signal.lfilter(hl, a, x2,zi=states1)
    
    x2_r,states2 = scipy.signal.lfilter(hr, a, x2,zi=states2)
    
    y_l = 1*np.array(x1) + 0.2*np.array(x2_l)
    y_r = 1*np.array(x1) + 0.2*np.array(x2_r)
    
    y_l = np.clip(y_l.astype(int),-MAXVALUE,MAXVALUE)
    y_r = np.clip(y_r.astype(int),-MAXVALUE,MAXVALUE)
    

    for i in range(BLOCKLEN):
        yl = y_l[i]
        yr = y_r[i]
        output_bytes1 = struct.pack('h', yl)
        output_bytes2 = struct.pack('h', yr)
        stream.write(output_bytes1+output_bytes2)
    
    binary_data1 = wfb.readframes(BLOCKLEN)
    binary_data2 = wfn.readframes(BLOCKLEN)
    
stream.stop_stream()
stream.close()
p.terminate()