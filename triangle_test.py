import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw, ImageTk, ImagePalette
import math

# test file to figure out triangular tiling

height = 10
width = 10
scale = 100
h = math.sin(math.pi/3)

temp = np.array([0, 1])
a = np.swapaxes(np.tile(temp, (height, int(width/2))), 0, 1)


im = Image.new("RGB", size=(1500, 1500), color="black")

draw = ImageDraw.Draw(im)

# draw triangles

for x in range(height):
    for y in range(width):
        if y % 2 == 0:
            x_fixed = int((x+1)/2)
            if x % 2 == 0:
                coords = [(x_fixed*scale, y*h*scale), ((x_fixed+1)*scale, y*h*scale), ((x_fixed+0.5)*scale, (y+1)*h*scale)]
            else:
                coords = [((x_fixed)*scale, y*h*scale), ((x_fixed-0.5)*scale, (y+1)*h*scale), ((x_fixed+.5)*scale, (y+1)*h*scale)]
        else:
            x_fixed = int(x/2)
            if x % 2 == 0:
                coords = [((x_fixed+0.5)*scale, y*h*scale), ((x_fixed+1)*scale, (y+1)*h*scale), (x_fixed*scale, (y+1)*h*scale)]
            else:
                coords = [((x_fixed+0.5)*scale, y*h*scale), ((x_fixed+1.5)*scale, y*h*scale), ((x_fixed+1)*scale, (y+1)*h*scale)]
        
        
        
        if a[x, y] == 0:
            color = "red"
        else:
            color = "blue"
        
        
        draw.polygon(coords, fill=color)


im.save("test.png")



def place_sand(event):
    # this might be the strangest possible way to accomplish this
    # but it works
    # and you know, that's the important part
    
    x = event.x/scale
    y=event.y/scale
    
    y_real = int(y/h)
    
    y = y - y_real*h
    
    if y_real % 2 == 1:
        x = x+.5
        x_fixed=int(y/(2*h) + x)
        x_half=int(y/(2*h) - x) * -1
        x_real = x_half + x_fixed - 1
    else:
        x_fixed=int(y/(2*h) + x)
        x_half=int(y/(2*h) - x) * -1
        x_real = x_half + x_fixed
    
    
    
    
    
    print(str(x_real) + ", " + str(y_real))

main_window = tk.Tk()
drawing_frame = tk.Frame()

main_canvas = tk.Canvas(master=drawing_frame, bg="grey", height=800, width=800)
main_canvas.bind("<Button-1>", place_sand)
main_canvas.pack()

current_image = ImageTk.PhotoImage(im)
image_container = main_canvas.create_image(0, 0, image=current_image, anchor="nw")
drawing_frame.pack()

main_window.mainloop()