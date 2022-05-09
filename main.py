import tkinter as tk
from tkinter import GROOVE, SUNKEN, messagebox
import tkinter.ttk as ttk
from pdb import set_trace as TT
from xml.etree.ElementPath import get_parent_map
from PIL import Image 
from PIL import ImageTk

import pyaudio, struct, wave
from os.path import exists

import scipy
from scipy import io, signal
import numpy as np



global CONTINUE
global DIRECTION,BACKGROUND,NOISE
global load_background_flag,load_noise_flag,load_filter_flag
global RECORDING
global front_back
global right_left


'''
TODO: 
    Add "No Direction" button and filter
    Connect parameters to buttons
    Test and debug
    Add recording functionality
'''
window = tk.Tk()
window.title('Ambience Sound Generator')
window.rowconfigure(0, minsize=50)
window.columnconfigure([0, 1, 2, 3], minsize=150)

'''
Initialization of wav file parameters (same for all of our files)
'''
RATE        = 44100                  # Frame rate (frames/second)
WIDTH       = 2                      # Number of bytes per sample
CHANNELS    = 1                      # Number of channels
MAXVALUE = 2**(8*WIDTH-1) - 1
BLOCKLEN = 1024
DURATION = 5
K = int( DURATION * RATE / BLOCKLEN )

'''
GUI
'''
#label_r = tk.Label() 
def play():
   #messagebox.showinfo( "Hello Python", "Hello World")
   if exists('user_input.wav'):
      f =  wave.open('user_input.wav','rb')  
      for i in range(K):
         data = f.readframes(BLOCKLEN)  
         stream.write(data)
   else:
      label2 = tk.Label(text="No voice record found")
      label2.grid(row=3, column=1)
      window.after(2000, destroy_widget, label2) # label as argument for destroy_widget
      

def destroy_widget(widget):
   #widget.destroy()
   widget['text']='' 

    

def changeRL(index):
    global right_left
    global load_filter_flag
    if index==1 and right['fg']=='red': #right red
      load_filter_flag = 1
      right['fg'] = 'green'
      left['fg'] = 'red'
      right_left =index
    elif index==1 and right['fg']=='green': #right release (it was green)
      right_left=-1
      right['fg']='red' 
    elif index==2 and left['fg']=='red': #left red
      left['fg'] = 'green'
      right['fg'] = 'red'
      right_left =index
      load_filter_flag = 1
    elif index==2 and left['fg']=='green': #left release (it was green)
      right_left=-1
      left['fg']= 'red'

def changeTB(index):
    global front_back
    if index==1 and top['fg']=='red': #top red
      top['fg'] = 'green'
      bottom['fg'] = 'red'
      front_back =index
    elif index==1 and top['fg']=='green': #top release (it was green)
      front_back=-1
      top['fg']='red' 
    elif index==2 and bottom['fg']=='red': #bottom red
      bottom['fg'] = 'green'
      top['fg'] = 'red'
      front_back =index
    elif index==2 and bottom['fg']=='green': #bottom release (it was green)
      front_back=-1
      bottom['fg']= 'red'
      
      
def quit():
    global CONTINUE
    CONTINUE = False
    window.destroy() 

label_r = tk.Label() 
def recordorStop():
   global record
   my_text= r['text']
   if my_text== "Stop":
      label_r['text'] ="Done!"
      label_r.grid(row=3, column=0) 
      window.after(2000, destroy_widget, label_r) # label as argument for destroy_widget
      r['text'] = "Record my voice" 
      # TO DO Save the recording
      record= False
   else:
      label_r['text'] ="Recording..."
      label_r.grid(row=3, column=0) 
      r['text'] = "Stop"
      # TO DO Start recording
      
      record= True
      
def change_ambient():
   label2 = tk.Label(text="Recording...")
   label2.pack()

def changeLocation(index):
    global BACKGROUND
    global load_background_flag
    #1:hotel, 2:cafe, 3:beach
    if index == 1 and hotel['text'] == 'off':
        load_background_flag = 1
        BACKGROUND = 1 
        hotel['text'] == 'on'
        cafe['text'] == 'off'
        beach['text'] == 'off'
    elif index == 1 and hotel['text'] == 'on':
        BACKGROUND = 1
        load_background_flag = 2
        hotel['text'] == 'off'
    elif index == 2 and cafe['text'] == 'off':
        load_background_flag = 1
        BACKGROUND = 1 
        hotel['text'] == 'off'
        cafe['text'] == 'on'
        beach['text'] == 'off'
    elif index == 2 and cafe['text'] == 'on':
        BACKGROUND = 1
        load_background_flag = 2
        cafe['text'] == 'off'
    elif index == 1 and beach['text'] == 'off':
        load_background_flag = 1
        BACKGROUND = 3 
        hotel['text'] == 'off'
        cafe['text'] == 'off'
        beach['text'] == 'on'
    elif index == 1 and beach['text'] == 'on':
        BACKGROUND = 3
        load_background_flag = 2
        beach['text'] == 'off'
   
   
def changeSound(index):
    global NOISE
    global load_noise_flag
    NOISE = index #1:garbage,2:rain, 3:people,4:icemaker
    load_noise_flag = 1
    if index == 1 and garbage['text'] == 'off':
        load_noise_flag = 1
        NOISE = 1 
        garbage['text'] == 'on'
        rain_in['text'] == 'off'
        people['text'] == 'off'
        icem['text'] == 'off'
    elif index == 1 and garbage['text'] == 'on':
        NOISE = 1
        load_noise_flag = 2
        garbage['text'] == 'off'
        
    if index == 2 and rain_in['text'] == 'off':
        load_noise_flag = 1
        NOISE = 2 
        garbage['text'] == 'off'
        rain_in['text'] == 'on'
        people['text'] == 'off'
        icem['text'] == 'off'
    elif index == 2 and rain_in['text'] == 'on':
        NOISE = 2
        load_noise_flag = 2
        rain_in['text'] == 'off'

    if index == 3 and people['text'] == 'off':
        load_noise_flag = 1
        NOISE = 3 
        garbage['text'] == 'off'
        rain_in['text'] == 'off'
        people['text'] == 'on'
        icem['text'] == 'off'
    elif index == 3 and people['text'] == 'on':
        NOISE = 3
        load_noise_flag = 2
        people['text'] == 'off'
    
    if index == 4 and icem['text'] == 'off':
        load_noise_flag = 1
        NOISE = 4 
        garbage['text'] == 'off'
        rain_in['text'] == 'off'
        people['text'] == 'off'
        icem['text'] == 'on'
    elif index == 4 and icem['text'] == 'on':
        NOISE = 4
        load_noise_flag = 2
        icem['text'] == 'off'
    

def opentf():
   tf= tk.Tk()
   tf.title("Tranfer Function")
   global tf_open
   tf_open= True


frame_header = tk.Frame(master=window, bg="black")
frame_header.grid(row=0,columnspan=5, padx=5, pady=5, sticky="nsew")
#frame_header.pack(side=tk.TOP, fill= tk.X)

frame_p = tk.Frame(master= window, relief= SUNKEN)
frame_p.grid(row=1, column=0)
#frame_p.pack(side=tk.LEFT)

frame_s = tk.Frame(master= window, relief=SUNKEN)
frame_s.grid(row=1, column=1)

frame_d = tk.Frame(master= window, relief=SUNKEN)
frame_d.grid(row=1, column=2)
#frame_d.pack(side=tk.RIGHT)

frame_0 = tk.Frame(master= window, relief= GROOVE)
frame_0.grid(row=2, column=0)
#frame_1.pack(side=tk.BOTTOM)

frame_1 = tk.Frame(master= window, relief= GROOVE)
frame_1.grid(row=2, column=1)
#frame_1.pack(side=tk.BOTTOM)

frame_2 = tk.Frame(master= window, relief= tk.RAISED)
frame_2.grid(row=2,column=2)
#frame_2.pack(side=tk.BOTTOM)

frame_a =tk.Frame(master= window, relief= tk.RAISED)
frame_a.grid(row =4,columnspan=3, column=1)

label_update=tk.Frame(master= frame_a, relief= tk.RAISED) 
label_update.grid(row=0, column=0)

#tf= tk.Button(master=frame_a, text="Show transfer function", command=opentf)
#tf.grid(row=0, column=0)


#g_l= tk.Label(master=frame_p, text='Volume')
#g_l.grid(row=2, column=1)

gain_back= tk.Scale(master=frame_p, from_=0, to=2, length= 200,resolution = 0.01, orient=tk.VERTICAL)
gain_back.grid(rowspan=3, row=2, column=1)

gain_noise= tk.Scale(master=frame_s, from_=0, to=2, length= 200,resolution = 0.01, orient=tk.VERTICAL)
gain_noise.grid(rowspan=3, row=2, column=1)

# Frame border effects
border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

label = tk.Label(
   master= frame_header,
   text = "Ambience Sound Generator",
   fg= "white",
   bg = "black",
   #width=30,
   height=3
   )
label.grid(row=0, columnspan=5, padx= 300, sticky="nsew")


label_p = tk.Label(
  master= frame_p,
   text = "Places", 
   font=18,
   fg='white',
   bg='darkblue'
)

label_p.grid(row=0, column=0, sticky="nsew")

label_s = tk.Label(
  master= frame_s,
   text = "Sound ",   
   font=18,
   fg='white',
   bg='purple'
)

label_s.grid(row=0, column=0, sticky="nsew")

label_d = tk.Label(
  master= frame_d,
   text = "Direction ",   
   font=18,
   fg='white',
   bg='red'
)

label_d.grid(row=0, column=1, sticky="nsew")

#text_box = tk.Text()
#text_box.pack()

r = tk.Button(master= frame_0, text ="Record my voice", command = recordorStop)
r.grid(row=0, column=0, padx=40,sticky="nsew")
B = tk.Button(master= frame_1, text ="Play my voice with an ambience", command = play)
B.grid(row=0, column=0, padx= 20, sticky="nsew")
q = tk.Button(master= frame_2, text ="Quit", command = quit)
q.grid(row=0, column=1,padx=70, sticky="nsew")


# Load the image
image=Image.open("./Button_images/beach.png")
# Resize the image in the given (width, height)
img=image.resize((150, 75))
beach_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/cafe.png")
# Resize the image in the given (width, height)
img=image.resize((150, 75))
cafe_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/hotel.png")
# Resize the image in the given (width, height)
img=image.resize((150, 75))
hotel_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/rain_out.png")
# Resize the image in the given (width, height)
img=image.resize((100, 50))
rain_out_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/rain_in.png")
# Resize the image in the given (width, height)
img=image.resize((100, 50))
rain_in_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/icem.png")
# Resize the image in the given (width, height)
img=image.resize((100, 50))
icem_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/garbage.png")
# Resize the image in the given (width, height)
img=image.resize((100, 50))
garbage_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/people.png")
# Resize the image in the given (width, height)
img=image.resize((100, 50))
people_img= ImageTk.PhotoImage(img)


#places
beach = tk.Button(master= frame_p, text= "off", image=beach_img, command=lambda:changeLocation(3), relief=tk.SUNKEN)
beach.grid(row=4, column=0 ,sticky="nsew")
hotel = tk.Button(master= frame_p, text= "off", bg='white', image= hotel_img,command=lambda:changeLocation(1), relief=tk.SUNKEN)
hotel.grid(row=2, column=0 ,sticky="nsew")
cafe = tk.Button(master= frame_p, text= "off", image=cafe_img, command=lambda:changeLocation(2), relief=tk.SUNKEN)
cafe.grid(row=3, column=0 ,sticky="nsew")

#Sounds
garbage = tk.Button(master= frame_s, text= "off", image= garbage_img, command=lambda:changeSound(1), relief=tk.SUNKEN)
garbage.grid(row=1, column=0 ,sticky="nsew")
rain_in = tk.Button(master= frame_s, text= "off", image= rain_in_img, command=lambda:changeSound(2), relief=tk.SUNKEN)
rain_in.grid(row=2, column=0 ,sticky="nsew")
rain_out = tk.Button(master= frame_s, text= "off", image= rain_out_img, command=lambda:changeSound(3), relief=tk.SUNKEN)
rain_out.grid(row=3, column=0 ,sticky="nsew")
people = tk.Button(master= frame_s, text= "off", image= people_img,command=lambda:changeSound(4), relief=tk.SUNKEN)
people.grid(row=4, column=0 ,sticky="nsew")
icem = tk.Button(master= frame_s, text= "off",image= icem_img, command=lambda:changeSound(5), relief=tk.SUNKEN)
icem.grid(row=5, column=0 ,sticky="nsew")

#Direction
you = tk.Label(master= frame_d, text= "You", relief=tk.GROOVE)
you.grid(row=3, column=1)
right = tk.Button(master= frame_d, text= "Right", command=lambda:changeRL(1), fg='red')
right.grid(row=3, column=2 ,sticky="nsew")
left = tk.Button(master= frame_d, text= "Left", command=lambda:changeRL(2), fg='red')
left.grid(row=3, column=0 ,sticky="nsew")
top = tk.Button(master= frame_d, text= "Front", command=lambda:changeTB(1),   fg='red')
top.grid(row=2, column=1 ,sticky="nsew")
bottom = tk.Button(master= frame_d, text= "Back", command=lambda:changeTB(2),   fg='red')
bottom.grid(row=4, column=1 ,sticky="nsew")



'''
Filters
'''


def get_filter(i):
    '''
        Given a direction index (0 to 7) returns the HRTF filters
        corresponding to that direction (0 is directly infront 
        circles 45 degrees clock wise with increasing index)
    '''
    TT()
    if i == -1:
        l_f = np.zeros(200)
        l_f[0] = 1
        r_f = np.zeros(200)
        r_f[0] = 1
        return  l_f,r_f# No filter button 
    return left_filters[i-1],right_filters[i-1]

def get_index():
    #front:0, front_right:1, right:2..
    global DIRECTION
    global front_back
    global right_left
    TT()
    if front_back==1 and right_left==-1:
        DIRECTION=0
    elif front_back==1 and right_left==1:
        DIRECTION=1
    elif front_back==-1 and right_left==1:
        DIRECTION=2 
    elif front_back==2 and right_left==1:
        DIRECTION=3
    elif front_back==2 and right_left==-1:
        DIRECTION=4
    elif front_back==2 and right_left==2:
        DIRECTION=5
    elif front_back==-1 and right_left==2:
        DIRECTION=6
    elif front_back==1 and right_left==2:
        DIRECTION=7
    else:
        DIRECTION=-1    


def get_background(i):
    '''
        Given an index 0 to 3 returns the name of the background file
        to be loaded
    '''
    if i == 1:
        return './Background/cafe_loud.wav'
    elif i == 2:
        return './Background/cafe_quiet.wav'
    elif i == 3:
        return './Background/beach.wav'
    elif i == 4:
        return './Background/hotel_lobby.wav'
    else:
        return -1
    
    
def get_noise(i):
    '''
        Given an index 0 to 3 returns the name of the noise file
        to be loaded
    '''
    if i == 1:
        return './Noise/rain_inside.wav'
    elif i == 2:
        return './Noise/rain_outside.wav'
    elif i == 3:
        return './Noise/icemaker.wav'
    elif i == 4:
        return './Noise/garbage.wav'
    else:
        return -1


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
load_noise_flag = 2
load_filter_flag = 2

'''
Initial parameters
'''
DIRECTION = 5
BACKGROUND = 1
NOISE = 1
RECORDING = 0
right_left=-1
front_back=-1



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
Initial stuff
'''
states1 = np.zeros(199)
states2 = np.zeros(199)
g1_prev = 0.0
g2_prev = 0.0
g1_now = 0.6
g2_now = 0.4
bg = 0.0
nos = 0.0


binary_background = [0]*BLOCKLEN
binary_noise = [0]*BLOCKLEN

'''
Connect to quit button to exit while loop
'''
CONTINUE = True



while CONTINUE:
    window.update_idletasks()
    window.update()
    
    if load_background_flag == 1:
        #label_update['text']=
        wavfile_b = get_background(BACKGROUND)
        TT()
        wfb = wave.open(wavfile_b, 'rb')

        binary_background = wfb.readframes(BLOCKLEN)
        load_noise_flag = 0
        bg = 1.0
    elif load_background_flag == 2:
        bg = 0.0
        load_noise_flag = 0
    
    if load_noise_flag == 1:
        
        wavfile_n = get_noise(NOISE)
        
        wfn = wave.open(wavfile_n, 'rb')
        binary_noise = wfn.readframes(BLOCKLEN)
        load_noise_flag = 0
        nos = 1.0
    elif load_noise_flag == 2:
        nos = 0.0
        load_noise_flag = 0
    
    if load_filter_flag == 1:
        get_index()
        TT()
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
    
    y_l = bg*g1_lin*np.array(x1) + nos*g2_lin*np.array(x2_l)
    y_r = bg*g1_lin*np.array(x1) + nos*g2_lin*np.array(x2_r)
    
    
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