#!/usr/bin/#!/usr/bin/env python3
"""
Author: Ana Berthel
Date Last Modified: Aug 19, 2022

Contains the Sandbox class, which implements the actual mathematical model. It
also converts the numerical array to an image based on user-defined parameters.
"""

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImagePalette, ImageDraw
import math


class Sandbox:
    """ Sandbox class holds the main sandbox array and handles the spill event """

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

    def place_sand(self, tup):
        """ Called when user clicks a cell on the GUI, places sand on the array """
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

    def spill(self):
        """ Spill event - called when a cell's value exceeds the maximum allowed """
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

    def to_image(self):
        """
        Generates image from array
        stores Image in variable for later to save as png
        returns PhotoImage for use in Canvas
        """

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
        """ Updates canvas with new image from array """
        self.to_image()
        self.canvas.itemconfig(self.image_container, image=self.photoimage)
        self.window.update()

    def im_to_coords(self, x, y):
        """ Converts canvas coordinates to array coordinates """
        return (int(x/self.zoom), int(y/self.zoom))


class TriangleSandbox:
    """ Sandbox class holds the main sandbox array and handles the spill event.
    Grid is a triangular grid instead of a square grid. """

    def __init__(self, height, width, canvas, window):
        # dimensions of sandbox array
        self.height = height
        self.width = width
        self.array = np.zeros((width, height))

        # bucket settings
        self.bucket = 1
        self.max_slope = 3 #i.e. if cell has a slope of 4, then add it to the spill queue

        # spill event settings
        # TODO: need separate spill patterns for upward and downward facing triangles
        self.spill_pattern = np.array([[0,1,0], [1,0,1], [0,1,0]])
        self.spill_queue = [] #starts out empty

        # image display settings
        self.zoom = 10
        self.palette = ["#fcfbed", "#c5f598", "#85bf4e", "#538525"]
        self.overflow_color = "#c91e12"
        self.image = ""
        self.photoimage = ""
        self.canvas = canvas
        self.image_container = ""
        self.window = window

    def place_sand(self, tup):
        """ Called when user clicks a cell on the GUI, places sand on the array """
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

    def spill(self):
        """ Spill event - called when a cell's value exceeds the maximum allowed """
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

    def to_image(self):
        """
        Generates image from array
        stores Image in variable for later to save as png
        returns PhotoImage for use in Canvas
        """

        h = math.sin(math.pi/3)
        self.image = im = Image.new("RGB", size=(self.height * self.zoom, self.width * self.zoom), color="black")
        draw = ImageDraw.Draw(self.image)

        #TODO: better way to do this?
        for x in range(self.height):
            for y in range(self.width):
                if y % 2 == 0:
                    x_fixed = int((x+1)/2)
                    if x % 2 == 0:
                        coords = [(x_fixed*self.zoom, y*h*self.zoom), ((x_fixed+1)*self.zoom, y*h*self.zoom), ((x_fixed+0.5)*self.zoom, (y+1)*h*self.zoom)]
                    else:
                        coords = [((x_fixed)*self.zoom, y*h*self.zoom), ((x_fixed-0.5)*self.zoom, (y+1)*h*self.zoom), ((x_fixed+.5)*self.zoom, (y+1)*h*self.zoom)]
                else:
                    x_fixed = int(x/2)
                    if x % 2 == 0:
                        coords = [((x_fixed+0.5)*self.zoom, y*h*self.zoom), ((x_fixed+1)*self.zoom, (y+1)*h*self.zoom), (x_fixed*self.zoom, (y+1)*h*self.zoom)]
                    else:
                        coords = [((x_fixed+0.5)*self.zoom, y*h*self.zoom), ((x_fixed+1.5)*self.zoom, y*h*self.zoom), ((x_fixed+1)*self.zoom, (y+1)*h*self.zoom)]

                if self.array[y, x] <= self.max_slope:
                    color = self.palette[int(self.array[y, x])]
                else:
                    color = self.overflow_color

                draw.polygon(coords, fill=color)

        self.photoimage = ImageTk.PhotoImage(self.image)

    def update_canvas(self):
        """ Updates canvas with new image from array """
        self.to_image()
        self.canvas.itemconfig(self.image_container, image=self.photoimage)
        self.window.update()

    def im_to_coords(self, x_coords, y_coords):
        """ Converts canvas coordinates to array coordinates """

        h = math.sin(math.pi/3)
        x=x_coords/self.zoom
        y=y_coords/self.zoom

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

        return (int(x_real), int(y_real))
