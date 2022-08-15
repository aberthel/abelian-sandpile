# classes for sandbox and imagebuilder
# TODO: add triangle sandbox and hex sandbox

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImagePalette


# sandbox class holds the main sandbox array and handles the "spill" event
class Sandbox:

    # height and width are the only required parameters
    # everything else is initiated to a default value
    def __init__(self, height, width, canvas, window):
        # dimensions of sandbox array
        self.height = height
        self.width = width
        self.array = np.zeros((width, height))

        # bucket settings
        self.bucket = 1
        self.max_slope = 3 #i.e. if cell has a slope of 4, then add it to the spill queue

        # spill event settings
        self.spill_pattern = np.array([[0,1,0], [1,0,1], [0,1,0]])
        self.spill_queue = [] #starts out empty

        # image display settings
        self.zoom = 5
        self.palette = [np.array([252,251,237]), np.array([197,245,152]), np.array([133,191,78]), np.array([83,133,37])]
        self.overflow_color = np.array([201, 30, 18])
        self.image = ""
        self.photoimage = ""
        self.canvas = canvas
        self.image_container = ""
        self.window = window

    # called when user clicks a cell on the GUI
    # tup is the cell the user clicked
    def place_sand(self, tup):

        # increment cell's value by bucket size
        self.array[tup[1], tup[0]] += self.bucket

        # update image
        self.update_canvas()

        # if cell now has a higher value than max allowed slope, then initiate spill event
        if self.array[tup[1], tup[0]] > self.max_slope:
            # edge case: a cell should only be represented in the spill queue once at any given point in time
            if not tup in self.spill_queue:
                self.spill_queue.append(tup)
                self.spill()

    # spill event
    def spill(self):
        # TODO: lock place_sand input? - not strictly necessary, program still works with multiple inputs
        # loop repeats until there are no cells left in the spill queue
        while self.spill_queue:

            # take grains from the selected cell and distribute them evenly among cells
            # indicated in spill_pattern
            # the remainder is left in the selected cell - parameters like max_slope and
            # spill_pattern should be confined so that the remainder is always
            # less than max_slope
            tup = self.spill_queue.pop(0)
            grains_spilled = int(self.array[tup[1], tup[0]]/np.sum(self.spill_pattern))
            self.array[tup[1], tup[0]] = self.array[tup[1], tup[0]] % np.sum(self.spill_pattern)

            mid_i = int(self.spill_pattern.shape[1]/2)
            mid_j = int(self.spill_pattern.shape[0]/2)

            for i in range(self.spill_pattern.shape[1]):
                for j in range(self.spill_pattern.shape[0]):
                    if self.spill_pattern[i, j] == 1:
                        self.array[tup[1] - mid_i + i, tup[0] - mid_j + j] += grains_spilled

                        self.update_canvas()
                        if self.array[tup[1] - mid_i + i, tup[0] - mid_j + j] > self.max_slope:
                            if not ((tup[0] - mid_j + j, tup[1] - mid_i + i)) in self.spill_queue:
                                self.spill_queue.append((tup[0] - mid_j + j, tup[1] - mid_i + i))

    # generate image from array using image settings
    # stores Image in variable self.image for later to save as png
    # returns PhotoImage for use in canvas
    def to_image(self):
        image_array = np.zeros((self.array.shape[0], self.array.shape[1], 3), dtype=np.uint8)

        #TODO: better way to do this?
        for x in range(self.array.shape[0]):
            for y in range(self.array.shape[1]):

                if self.array[x, y] <= self.max_slope:
                    image_array[x, y] = self.palette[int(self.array[x, y])]
                else:
                    image_array[x, y] = self.overflow_color


        self.image = Image.fromarray(image_array, mode="RGB").resize((self.array.shape[0] * self.zoom, self.array.shape[1] * self.zoom), resample = Image.NEAREST)

        self.photoimage = ImageTk.PhotoImage(self.image)

    def update_canvas(self):
        self.to_image()
        self.canvas.itemconfig(self.image_container, image=self.photoimage)
        self.window.update()


    # converts canvas coordinates to array coordinates
    def im_to_coords(self, x, y):
        return (int(x/self.zoom), int(y/self.zoom))
