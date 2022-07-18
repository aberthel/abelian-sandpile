#!/usr/bin/#!/usr/bin/env python3

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImagePalette
import time

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
        # NOTE: will this work when multiple scripts are used???
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
                            self.spill_queue.append((tup[0] - mid_j + j, tup[1] - mid_i + i))





# converts sandbox array into an image
class ImageBuilder:
    def __init__(self):
        self.zoom = 10

        self.spill_pattern_zoom = 50
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

    def spill_pattern_to_image(self, sandbox):
        image_array = np.zeros((sandbox.spill_pattern.shape[0], sandbox.spill_pattern.shape[1], 3), dtype=np.uint8)

        #TODO: better way to do this?
        for x in range(sandbox.spill_pattern.shape[0]):
            for y in range(sandbox.spill_pattern.shape[1]):

                if sandbox.spill_pattern[x, y] == 0:
                    image_array[x, y] = np.array([255, 255, 255])
                else:
                    image_array[x, y] = np.array([0, 0, 0])

        img1 = Image.fromarray(image_array, mode="RGB").resize((sandbox.spill_pattern.shape[0] * self.spill_pattern_zoom, sandbox.spill_pattern.shape[1] * self.spill_pattern_zoom), resample = Image.NEAREST)

        img2 = ImageTk.PhotoImage(img1)

        return img2


sandbox = Sandbox(100, 100)
ib = ImageBuilder()

### MAIN WINDOW KEY BINDS ###

def open_settings(event):
    global spill_image

    settings_window = tk.Toplevel(main_window)

    # frame 1

    top_frame = tk.Frame(master=settings_window)

    settings_label = tk.Label(master=top_frame, text="Settings")
    height_label = tk.Label(master=top_frame, text="Sandbox Height")
    height_entry = tk.Entry(master=top_frame, width=10)
    height_entry.insert(0, str(sandbox.height))
    width_label = tk.Label(master=top_frame, text="Sandbox Width")
    width_entry = tk.Entry(master=top_frame, width=10)
    width_entry.insert(0, str(sandbox.width))

    settings_label.pack(side=tk.TOP)
    height_label.pack(side=tk.LEFT)
    height_entry.pack(side=tk.LEFT)
    width_entry.pack(side=tk.RIGHT)
    width_label.pack(side=tk.RIGHT)

    # frame 2

    second_frame = tk.Frame(master=settings_window)

    size_note_label = tk.Label(master=second_frame, text="Warning: changing sandbox size will reset the current pattern.")

    size_note_label.pack()

    # frame 3 : slope
    third_frame = tk.Frame(master=settings_window)

    slope_label = tk.Label(master=third_frame, text="Max Slope")
    less_slope_button = tk.Button(master=third_frame, text="-")
    slope_indicator_label = tk.Label(master=third_frame, text=str(sandbox.max_slope))
    more_slope_button = tk.Button(master=third_frame, text="+")

    slope_label.pack(side=tk.LEFT)
    more_slope_button.pack(side=tk.RIGHT)
    slope_indicator_label.pack(side=tk.RIGHT)
    less_slope_button.pack(side=tk.RIGHT)


    #frame 4: bucket size
    fourth_frame = tk.Frame(master=settings_window)
    bucket_label = tk.Label(master=fourth_frame, text = "Bucket Size")
    bucket_entry = tk.Entry(master=fourth_frame, width=20)
    bucket_entry.insert(0, str(sandbox.bucket))

    bucket_label.pack(side=tk.LEFT)
    bucket_entry.pack(side=tk.RIGHT)

    # frame 5: spill pattern
    fifth_frame = tk.Frame(master=settings_window)
    spill_pattern_label = tk.Label(master=fifth_frame, text="Spill Pattern (click to edit)")
    # TODO: for some reason, small amount of background visible in right and bottom edges
    spill_canvas = tk.Canvas(master=fifth_frame, bg="grey", height=sandbox.spill_pattern.shape[0] * ib.spill_pattern_zoom, width=sandbox.spill_pattern.shape[1] * ib.spill_pattern_zoom)

    spill_pattern_label.pack()
    spill_canvas.pack()

    # TODO: this isn't going to work because we only want to edit sandbox if user applies settings
    spill_image = ib.spill_pattern_to_image(sandbox)
    print(spill_image)
    spill_container = spill_canvas.create_image(0, 0, image=spill_image, anchor="nw")

    # bottom frame
    bottom_frame = tk.Frame(master=settings_window)

    apply_button = tk.Button(master=bottom_frame, text="Apply New Settings")
    #apply_button.bind("<Button-1>", apply_setting_changes)
    cancel_button = tk.Button(master=bottom_frame, text="Cancel", command=settings_window.destroy)

    apply_button.pack(side=tk.LEFT)
    cancel_button.pack(side=tk.RIGHT)
    # pack all frames

    top_frame.pack()
    second_frame.pack()
    third_frame.pack()
    fourth_frame.pack()
    fifth_frame.pack()
    bottom_frame.pack()



    settings_window.grab_set()


def open_save(event):
    # TODO: open save window
    print("open save window")

def update_image():
    global current_image
    current_image = ib.to_image(sandbox)
    main_canvas.itemconfig(image_container, image=current_image)

def place_sand(event):
    sandbox.place_sand(ib.im_to_coords(event.x, event.y))

    #update_image()










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
main_canvas = tk.Canvas(master=drawing_frame, bg="grey", height=1000, width=1000)
main_canvas.bind("<Button-1>", place_sand)
main_canvas.pack()

header_frame.pack()
drawing_frame.pack()

# draw image from sandbox array
# TODO: replace with function later in order to define palette, pixel size, etc.
current_image = ib.to_image(sandbox)
image_container = main_canvas.create_image(0, 0, image=current_image, anchor="nw")

spill_image = ib.spill_pattern_to_image(sandbox)

main_window.mainloop()
