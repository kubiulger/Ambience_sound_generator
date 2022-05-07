import scipy
import numpy as np

left_mat = scipy.io.loadmat('left_filt')
right_mat = scipy.io.loadmat('right_filt')

left_filters = left_mat['h_l']
right_filters = right_mat['h_r']

def get_filter(i):
    return left_filters[i],right_filters[i]

import wave

file_name = './Background/hotel_lobby.wav'

wf = wave.open(file_name)

print('file name:', file_name ) 
print('number of channels:', wf.getnchannels() ) 
print('number of frames per second:', wf.getframerate() )
print('signal length:', wf.getnframes() )
print('number of bytes per sample:', wf.getsampwidth() )

wf.close()