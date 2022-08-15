# classes for sandbox and imagebuilder
# TODO: add triangle sandbox and hex sandbox

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImagePalette



class Sandbox:
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.bucket = 1
        self.max_slope = 3 #i.e. if cell has a slope of 4, then add it to the spill queue
        self.array = np.zeros((width, height))

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


# TODO: merge with sandbox class? 
class ImageBuilder:
    def __init__(self):
        self.zoom = 5

        #TODO: make sure palette has at least as many options as max_slope + 1 when it's set
        self.palette = [np.array([252,251,237]), np.array([197,245,152]), np.array([133,191,78]), np.array([83,133,37])]
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
        
    def image_to_save(self, sandbox):
        image_array = np.zeros((sandbox.array.shape[0], sandbox.array.shape[1], 3), dtype=np.uint8)

        for x in range(sandbox.array.shape[0]):
            for y in range(sandbox.array.shape[1]):

                if sandbox.array[x, y] <= sandbox.max_slope:
                    image_array[x, y] = self.palette[int(sandbox.array[x, y])]
                else:
                    image_array[x, y] = self.overflow_color


        return Image.fromarray(image_array, mode="RGB").resize((sandbox.array.shape[0] * self.zoom, sandbox.array.shape[1] * self.zoom), resample = Image.NEAREST)


    def im_to_coords(self, x, y):
        return (int(x/self.zoom), int(y/self.zoom))

