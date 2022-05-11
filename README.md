# Ambience_sound_generator

**In this project, we design a graphical user interface (GUI), in which user can select the ambience noise in a selected place from a selected direction. For example, the user can choose to be in a cafe when people are chatting behind the user and we will apply this background noise to the user's input voice according to the direction. We will try to include various different settings.**


The following capture is from our GUI:

<img width="698" alt="Screen Shot 2022-05-11 at 5 55 27 PM" src="https://user-images.githubusercontent.com/23522642/167954271-0d7e888e-7028-4b42-9a27-bd5af9e8c2c4.png">

(LINK EKLEYELIM SOUNDLAR ICIN BEN NERDEN ALDIK TAM BILMIYORUM)

As you can see, our GUI includes choices of places:
 * Hotel
 * Empty Cafe
 * Crowded Cafe
 * Beach

As background sounds, we include
  * Garbage collector
  * Rain on window
  * Outside rain
  * Ice maker
 
 User is able to choice where background noises coming from. There are 8 different selection of directions: right, left, front, right-front etc. Users can adjust the volume by the sliders next to the places and sounds. As it can be seen in the figure, current background sound playing can be seen at the bottom of the page. 
 
  Additionally, users can record their voices via *record my voice* button and play their voices with the preferred background noise via *play my voice with an ambience* button. During play, they can change every setting of the ambient noise as they desire. 
 
 The final simulation can be found in *main.py*. In *gui.py*, there is only GUI implementation and in *ambience_player.py*, there is only filter design. 
 
 
 
  
