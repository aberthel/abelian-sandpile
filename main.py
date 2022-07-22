#!/usr/bin/#!/usr/bin/env python3

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImagePalette
import settings

class Sandbox:
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.bucket = 1
        self.max_slope = 3 #i.e. if cell has a slope of 4, then add it to the spill queue
        self.array = np.zeros((height, width))

        self.spill_pattern = np.array([[0,1,0], [1,0,1], [0,1,0]])

        self.spill_queue = [] #starts out empty


    def place_sand(self, tup):

        self.array[tup[1], tup[0]] += self.bucket
        update_image()
        if self.array[tup[1], tup[0]] > self.max_slope:

            if not tup in self.spill_queue:
                self.spill_queue.append(tup)
                self.spill()

    def spill(self):
        # TODO: lock place_sand input?
        while self.spill_queue:
            tup = self.spill_queue.pop(0)
            grains_spilled = int(self.array[tup[1], tup[0]]/np.sum(self.spill_pattern))
            self.array[tup[1], tup[0]] = self.array[tup[1], tup[0]] % np.sum(self.spill_pattern)

            mid_i = int(self.spill_pattern.shape[1]/2)
            mid_j = int(self.spill_pattern.shape[0]/2)

            for i in range(self.spill_pattern.shape[1]):
                for j in range(self.spill_pattern.shape[0]):
                    if self.spill_pattern[i, j] == 1:
                        self.array[tup[1] - mid_i + i, tup[0] - mid_j + j] += grains_spilled
                        #NOTE: animation of spilling doesn't happen. Force computer to wait?
                        update_image()
                        if self.array[tup[1] - mid_i + i, tup[0] - mid_j + j] > self.max_slope:
                            if not ((tup[0] - mid_j + j, tup[1] - mid_i + i)) in self.spill_queue:
                                self.spill_queue.append((tup[0] - mid_j + j, tup[1] - mid_i + i))





# converts sandbox array into an image
class ImageBuilder:
    def __init__(self):
        self.zoom = 5

        #TODO: make sure palette has at least as many options as max_slope + 1 when it's set
        self.palette = [np.array([252,251,237]), np.array([197,245,152]), np.array([133,191,78]), np.array([83,133,37]), np.array([89,64,13])]
        self.overflow_color = np.array([201, 30, 18])


    def to_image(self, sandbox):

        image_array = np.zeros((sandbox.array.shape[0], sandbox.array.shape[1], 3), dtype=np.uint8)

        #TODO: better way to do this?
        for x in range(sandbox.array.shape[0]):
            for y in range(sandbox.array.shape[1]):

                if sandbox.array[x, y] <= sandbox.max_slope:
                    image_array[x, y] = self.palette[int(sandbox.array[x, y])]
                else:
                    image_array[x, y] = self.overflow_color


        img1 = Image.fromarray(image_array, mode="RGB").resize((sandbox.array.shape[0] * self.zoom, sandbox.array.shape[1] * self.zoom), resample = Image.NEAREST)

        #TODO: zoom?

        img2 = ImageTk.PhotoImage(img1)

        return img2

    def im_to_coords(self, x, y):
        return (int(x/self.zoom), int(y/self.zoom))






sandbox = Sandbox(100, 100)
ib = ImageBuilder()
sw = ""

### MAIN WINDOW KEY BINDS ###

def open_settings(event):
    global sw
    sw = settings.Window(main_canvas, sandbox, ib)


def update_spill_image():
    global spill_image
    spill_image = spe.to_image()
    spill_canvas.itemconfig(spill_container, image=spill_image)

def open_save(event):
    # TODO: open save window
    print("open save window")

def update_image():
    global current_image
    current_image = ib.to_image(sandbox)
    main_canvas.itemconfig(image_container, image=current_image)
    main_window.update()

def place_sand(event):
    sandbox.place_sand(ib.im_to_coords(event.x, event.y))


### MAIN WINDOW SETUP ###

main_window = tk.Tk()

header_frame = tk.Frame()
drawing_frame = tk.Frame()

title_label = tk.Label(master=header_frame, text="Abelian Sandpile Model")
settings_button = tk.Button(master=header_frame, text="Settings")
settings_button.bind("<Button-1>", open_settings)
save_button = tk.Button(master=header_frame, text="Save Image")
save_button.bind("<Button-1>", open_save)

title_label.pack(side=tk.TOP)
settings_button.pack(side=tk.LEFT)
save_button.pack(side=tk.RIGHT)

## TODO: size of drawing frame needs to be dynamic in the future
main_canvas = tk.Canvas(master=drawing_frame, bg="grey", height=ib.zoom*sandbox.height, width=ib.zoom*sandbox.width)
main_canvas.bind("<Button-1>", place_sand)
main_canvas.pack()

header_frame.pack()
drawing_frame.pack()

# draw image from sandbox array
# TODO: replace with function later in order to define palette, pixel size, etc.
current_image = ib.to_image(sandbox)
image_container = main_canvas.create_image(0, 0, image=current_image, anchor="nw")

spill_image = ""

main_window.mainloop()
