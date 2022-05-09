import tkinter as tk
from tkinter import GROOVE, SUNKEN, messagebox
import tkinter.ttk as ttk
from pdb import set_trace as TT
from xml.etree.ElementPath import get_parent_map
from PIL import Image 
from PIL import ImageTk
import pyaudio
import wave
from os.path import exists


window = tk.Tk()
window.title('Ambience Sound Generator')
window.rowconfigure(0, minsize=50)
window.columnconfigure([0, 1, 2, 3], minsize=150)
global background
global top_bottom
global right_left
global noise
global tf_open #True False to check the tf window
global record

#At first it is closed
tf_open = False
background=-1
top_bottom=-1
right_left=-1
noise=-1
record=False


WIDTH       = 2         # Number of bytes per sample
CHANNELS    = 1         # mono
RATE        = 16000     # Sampling rate (frames/second)    
DURATION = 5
BLOCKLEN = 128
K = int( DURATION * RATE / BLOCKLEN )
p = pyaudio.PyAudio()
# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)



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
   if index==1 and right['fg']=='red': #right red
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
   elif index==2 and left['fg']=='green': #left release (it was green)
      right_left=-1
      left['fg']= 'red'

def changeTB(index):
   global top_bottom
   if index==1 and top['fg']=='red': #top red
      top['fg'] = 'green'
      bottom['fg'] = 'red'
      top_bottom =index
   elif index==1 and top['fg']=='green': #top release (it was green)
      top_bottom=-1
      top['fg']='red' 
   elif index==2 and bottom['fg']=='red': #bottom red
      bottom['fg'] = 'green'
      top['fg'] = 'red'
      top_bottom =index
   elif index==2 and bottom['fg']=='green': #bottom release (it was green)
      top_bottom=-1
      bottom['fg']= 'red'
def quit():
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
   global background
   background = index #1:hotel, 2:cafe, 3:nyc
   
def changeSound(index):
   global noise
   noise = index #1:garbage,2:rain, 3:people,4:icemaker

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
frame_a.grid(row =1,column=3)


tf= tk.Button(master=frame_a, text="Show transfer function", command=opentf)
tf.grid(row=0, column=0)


g_l= tk.Label(master=frame_a, text='Volume')
g_l.grid(row=1, column=0)

gain_s= tk.Scale(master=frame_a, from_=0, to=2, length= 200,resolution = 0.01, orient=tk.VERTICAL)
gain_s.grid(rowspan=3, column=0)


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
image=Image.open("./Button_images/nyc.png")
# Resize the image in the given (width, height)
img=image.resize((150, 75))
nyc_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/cafe.png")
# Resize the image in the given (width, height)
img=image.resize((150, 75))
cafe_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/hotel.png")
# Resize the image in the given (width, height)
img=image.resize((150, 75))
hotel_img= ImageTk.PhotoImage(img)

image=Image.open("./Button_images/rain.png")
# Resize the image in the given (width, height)
img=image.resize((100, 50))
rain_img= ImageTk.PhotoImage(img)

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
nyc = tk.Button(master= frame_p, text= "NYC", image=nyc_img, command=lambda:changeLocation(3), relief=tk.SUNKEN)
nyc.grid(row=4, column=0 ,sticky="nsew")
hotel = tk.Button(master= frame_p, text= "Hotel", bg='white', image= hotel_img,command=lambda:changeLocation(1), relief=tk.SUNKEN)
hotel.grid(row=2, column=0 ,sticky="nsew")
cafe = tk.Button(master= frame_p, text= "Cafe", image=cafe_img, command=lambda:changeLocation(2), relief=tk.SUNKEN)
cafe.grid(row=3, column=0 ,sticky="nsew")

#Sounds
garbage = tk.Button(master= frame_s, text= "Garbage", image= garbage_img, command=lambda:changeSound(1), relief=tk.SUNKEN)
garbage.grid(row=1, column=0 ,sticky="nsew")
rain = tk.Button(master= frame_s, text= "Rain", image= rain_img, command=lambda:changeSound(2), relief=tk.SUNKEN)
rain.grid(row=2, column=0 ,sticky="nsew")
people = tk.Button(master= frame_s, text= "People", image= people_img,command=lambda:changeSound(3), relief=tk.SUNKEN)
people.grid(row=3, column=0 ,sticky="nsew")
icem = tk.Button(master= frame_s, text= "Ice Maker",image= icem_img, command=lambda:changeSound(4), relief=tk.SUNKEN)
icem.grid(row=4, column=0 ,sticky="nsew")

#Direction
you = tk.Label(master= frame_d, text= "You", relief=tk.GROOVE)
you.grid(row=3, column=1)
right = tk.Button(master= frame_d, text= "Right", command=lambda:changeRL(1), fg='red')
right.grid(row=3, column=2 ,sticky="nsew")
left = tk.Button(master= frame_d, text= "Left", command=lambda:changeRL(2), fg='red')
left.grid(row=3, column=0 ,sticky="nsew")
top = tk.Button(master= frame_d, text= "Top", command=lambda:changeTB(1),   fg='red')
top.grid(row=2, column=1 ,sticky="nsew")
bottom = tk.Button(master= frame_d, text= "Bottom", command=lambda:changeTB(2),   fg='red')
bottom.grid(row=4, column=1 ,sticky="nsew")


#window.mainloop()

while True:
   window.update_idletasks()
   window.update()
   if record:     
      TT()
      output_wf = wave.open('user_input.wav', 'w')      # wave file
      output_wf.setframerate(RATE)
      output_wf.setsampwidth(WIDTH)
      output_wf.setnchannels(CHANNELS)
      for i in range(K):
         input_bytes = stream.read(BLOCKLEN, exception_on_overflow= False)
         stream.write(input_bytes)
         output_wf.writeframes(input_bytes)
      record=False


stream.stop_stream()
stream.close()
p.terminate()
utput_wf.close()