import tkinter as tk
from tkinter import GROOVE, SUNKEN, messagebox
import tkinter.ttk as ttk


window = tk.Tk()
window.rowconfigure(0, minsize=50)
window.columnconfigure([0, 1, 2, 3], minsize=150)

label_r = tk.Label() 

def play():
   #messagebox.showinfo( "Hello Python", "Hello World")
   label2 = tk.Label(text="No voice record found")
   label2.grid(row=3, column=1)
   window.after(2000, destroy_widget, label2) # label as argument for destroy_widget

def destroy_widget(widget):
   widget.destroy()

def quit():
   window.destroy() 

def recordorStop():
   my_text= r['text']
   
   if my_text== "Stop":
      label_r['text'] ="Done!"
      label_r.grid(row=3, column=0) 
      window.after(2000, destroy_widget, label_r) # label as argument for destroy_widget
      # TO DO Save the recording
   else:
      label_r['text'] ="Recording..."
      label_r.grid(row=3, column=0) 
      r['text'] = "Stop"
      # TO DO Start recording

def change_ambient():
   label2 = tk.Label(text="Recording...")
   label2.pack()


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
   text = "Place "
)

label_p.grid(row=0, column=0, sticky="nsew")

label_s = tk.Label(
  master= frame_s,
   text = "Sound "
)

label_s.grid(row=0, column=0, sticky="nsew")

label_d = tk.Label(
  master= frame_d,
   text = "Direction "
)

label_d.grid(row=0, column=0, sticky="nsew")

#text_box = tk.Text()
#text_box.pack()

r = tk.Button(master= frame_0, text ="Record my voice", command = recordorStop)
r.grid(row=0, column=0, padx=40,sticky="nsew")
B = tk.Button(master= frame_1, text ="Play my voice with an ambience", command = play)
B.grid(row=0, column=0, padx= 20, sticky="nsew")
q = tk.Button(master= frame_2, text ="Quit", command = quit)
q.grid(row=0, column=0,padx=70, sticky="nsew")




window.mainloop()