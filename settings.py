#!/usr/bin/#!/usr/bin/env python3
"""
Author: Ana Berthel
Date Last Modified: Aug 19, 2022

Defines the settings window class as well as the auxilliary spill pattern editor
class. Used to change parameters of the model and adjust how it is converted into
an image.
"""

import tkinter as tk
from tkinter.colorchooser import askcolor
import numpy as np
from PIL import Image, ImageTk, ImagePalette
from functools import partial
import platform

class SpillPatternEditor:
    """
    Contains an array that defines a new spill pattern to be used by the Sandbox.
    Also converts that array to an image for display by settings window.
    """

    def __init__(self, pattern):
        self.pattern = pattern.copy()
        self.zoom = 50

    def to_image(self):
        """ Convert array to PhotoImage for display """

        image_array = np.zeros((self.pattern.shape[0], self.pattern.shape[1], 3), dtype=np.uint8)

        #TODO: better way to do this? More pythonic?
        for x in range(self.pattern.shape[0]):
            for y in range(self.pattern.shape[1]):

                if self.pattern[x, y] == 0:
                    image_array[x, y] = np.array([255, 255, 255])
                else:
                    image_array[x, y] = np.array([0, 0, 0])

        img1 = Image.fromarray(image_array, mode="RGB").resize((self.pattern.shape[0] * self.zoom, self.pattern.shape[1] * self.zoom), resample = Image.NEAREST)

        img2 = ImageTk.PhotoImage(img1)

        return img2

    def toggle_pixel(self, event):
        """ toggles pixel value between 0 and 1 based on mouse click event """

        x = int(event.x/self.zoom)
        y = int(event.y/self.zoom)

        if self.pattern[y, x] == 0:
            self.pattern[y, x] = 1
        else:
            self.pattern[y, x] = 0



# Builds and handles events for the settings window
class Window:
    """
    Builds the settings window and handles events.
    Used to change Sandbox parameters.
    """

    def __init__(self, main_window, sandbox):
        self.sandbox = sandbox
        self.window = tk.Toplevel(main_window)

        self.isMac = False
        if platform.system() == "Darwin":
            self.isMac = True

        ## Set up frames ##

        # Frame 1: height and width fields

        self.frame1 = tk.Frame(master=self.window)

        self.settings_label = tk.Label(master=self.frame1, text="Settings")

        self.height_label = tk.Label(master=self.frame1, text="Sandbox Height")
        self.height_entry = tk.Entry(master=self.frame1, width=10)
        self.height_entry.insert(0, str(sandbox.height))

        self.width_label = tk.Label(master=self.frame1, text="Sandbox Width")
        self.width_entry = tk.Entry(master=self.frame1, width=10)
        self.width_entry.insert(0, str(sandbox.width))

        self.settings_label.pack(side=tk.TOP)
        self.height_label.pack(side=tk.LEFT)
        self.height_entry.pack(side=tk.LEFT)
        self.width_entry.pack(side=tk.RIGHT)
        self.width_label.pack(side=tk.RIGHT)

        # Frame 2: warning note about changing size and zoom

        self.frame2 = tk.Frame(master=self.window)

        self.size_note_label = tk.Label(master=self.frame2, text="Warning: changing sandbox size will reset the current pattern.")
        self.zoom_label = tk.Label(master=self.frame2, text="Sandbox Zoom")
        self.zoom_entry = tk.Entry(master=self.frame2, width=10)
        self.zoom_entry.insert(0, str(sandbox.zoom))

        self.size_note_label.pack(side=tk.TOP)
        self.zoom_label.pack()
        self.zoom_entry.pack()

        # Frame 3: max slope before grains spill

        self.frame3 = tk.Frame(master=self.window)

        self.slope_label = tk.Label(master=self.frame3, text="Max Slope")
        self.less_slope_button = tk.Button(master=self.frame3, text="-")
        self.slope_indicator_label = tk.Label(master=self.frame3, text=str(sandbox.max_slope))
        self.more_slope_button = tk.Button(master=self.frame3, text="+")

        self.slope_label.pack(side=tk.LEFT)
        self.more_slope_button.pack(side=tk.RIGHT)
        self.more_slope_button.bind("<Button-1>", self.add_slope)
        self.slope_indicator_label.pack(side=tk.RIGHT)
        self.less_slope_button.pack(side=tk.RIGHT)
        self.less_slope_button.bind("<Button-1>", self.subtract_slope)

        # Frame 4: sand bucket size

        self.frame4 = tk.Frame(master=self.window)

        self.bucket_label = tk.Label(master=self.frame4, text="Bucket Size")
        self.bucket_entry = tk.Entry(master=self.frame4, width=20)
        self.bucket_entry.insert(0, str(sandbox.bucket))

        self.bucket_label.pack(side=tk.LEFT)
        self.bucket_entry.pack(side=tk.RIGHT)

        # Frame 5: spill pattern

        self.frame5 = tk.Frame(master=self.window)

        self.spe = SpillPatternEditor(sandbox.spill_pattern)
        self.spill_pattern_label = tk.Label(master=self.frame5, text="Spill Pattern (click to edit)")
        self.spill_canvas = tk.Canvas(master=self.frame5, bg="grey", height=self.spe.pattern.shape[0]*self.spe.zoom, width=self.spe.pattern.shape[1]*self.spe.zoom)
        self.spill_canvas.bind("<Button-1>", self.toggle_pixel)
        self.inc_spill_button = tk.Button(master=self.frame5, text="Increase Pattern Size")
        self.dec_spill_button = tk.Button(master=self.frame5, text="Decrease Pattern Size")
        self.inc_spill_button.bind("<Button-1>", self.inc_pattern_size)
        self.dec_spill_button.bind("<Button-1>", self.dec_pattern_size)

        self.spill_pattern_label.pack()
        self.spill_canvas.pack()
        self.inc_spill_button.pack(side=tk.LEFT)
        self.dec_spill_button.pack(side=tk.RIGHT)

        self.spill_image = self.spe.to_image()
        self.spill_container = self.spill_canvas.create_image(0, 0, image=self.spill_image, anchor="nw")

        # Frame 6: Color picker selection

        # Frame 6a: Label and overflow

        self.frame6a = tk.Frame(master=self.window)

        self.frame6 = tk.Frame(master=self.window)

        #TODO: button bg color doesn't work right on macs, do version handling for that
        # maybe just replace buttons with labels? they don't *have* to be buttons
        self.color_picker_label = tk.Label(master=self.frame6a, text="Pixel Colors (click to edit)")
        if self.isMac:
            self.overflow_color_button = tk.Button(master=self.frame6a, text="overflow", highlightbackground=self.rgb_to_hex(sandbox.overflow_color))
        else:
            self.overflow_color_button = tk.Button(master=self.frame6a, text="overflow", bg=self.rgb_to_hex(sandbox.overflow_color))
        self.overflow_color_button.bind("<Button-1>", lambda event, x=-1: self.choose_color(x))

        self.color_buttons = []
        for x in range(len(sandbox.palette)):
            if self.isMac:
                self.color_buttons.append(tk.Button(master=self.frame6, text=str(x), highlightbackground=self.rgb_to_hex(sandbox.palette[x])))
            else:
                self.color_buttons.append(tk.Button(master=self.frame6, text=str(x), bg=self.rgb_to_hex(sandbox.palette[x])))
            self.color_buttons[x].bind("<Button-1>", lambda event, x=x: self.choose_color(x))

        self.color_picker_label.pack()
        self.overflow_color_button.pack()
        for x in range(len(sandbox.palette)):
            self.color_buttons[x].grid(column=x+1, row=1)

        # Frame 7: apply and cancel buttons

        self.frame7 = tk.Frame(master=self.window)

        self.apply_button = tk.Button(master=self.frame7, text="Apply New Settings")
        self.apply_button.bind("<Button-1>", self.apply_setting_changes)
        self.cancel_button = tk.Button(master=self.frame7, text="Cancel", command=self.window.destroy)

        self.apply_button.pack(side=tk.LEFT)
        self.cancel_button.pack(side=tk.RIGHT)

        # Now we pack all frames from top to bottom

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()
        self.frame5.pack()
        self.frame6a.pack()
        self.frame6.pack()
        self.frame7.pack()

        # And finally for init, grab set

        self.window.grab_set()

    def choose_color(self, x):
        """ Opens color picker and sets button x to selected color """

        new_color = askcolor(title="Pick New Color")

        if x < 0:
            if self.isMac:
                self.overflow_color_button.configure(highlightbackground=new_color[1])
            else:
                self.overflow_color_button.configure(bg=new_color[1])
        else:
            if self.isMac:
                self.color_buttons[x].configure(highlightbackground=new_color[1])
            else:
                self.color_buttons[x].configure(bg=new_color[1])

    def rgb_to_hex(self, a):
        """ converts rgb tuple to hex string """
        return '#%02x%02x%02x' % (a[0], a[1], a[2])

    def hex_to_rgb(self, a):
        """ converts hex string to rgb numpy array """
        hex = a.lstrip("#")
        return np.asarray(tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)))

    def add_slope(self, event):
        """ increases max slope label by 1 """
        new_slope = int(self.slope_indicator_label["text"]) + 1
        self.slope_indicator_label.configure(text=str(new_slope))
        self.add_color()

    def subtract_slope(self, event):
        """ decreases max slope label by 1 if constraints allow it """
        # check that max slope is at least as many as full pixels
        min_max = self.spe.pattern.sum() - 1
        if int(self.slope_indicator_label["text"]) > min_max:
            new_slope = int(self.slope_indicator_label["text"]) - 1
            self.slope_indicator_label.configure(text=str(new_slope))
            self.subtract_color()

    def inc_pattern_size(self, event):
        """ Increases the size of the spill pattern by 1 on every side """
        v = np.zeros((self.spe.pattern.shape[0], 1), dtype=np.uint8)
        h = np.zeros((1, self.spe.pattern.shape[1]+2), dtype=np.uint8)

        a = np.concatenate((v, self.spe.pattern, v), axis=1)
        self.spe.pattern = np.concatenate((h, a, h), axis=0)
        self.spill_canvas.configure(height=self.spe.pattern.shape[0]*self.spe.zoom, width=self.spe.pattern.shape[1]*self.spe.zoom)
        self.spill_image = self.spe.to_image()
        self.spill_canvas.itemconfig(self.spill_container, image=self.spill_image)

    def dec_pattern_size(self, event):
        """ Decreases the size of the spill pattern by 1 on every side """
        # we don't want a pattern smaller than three pixels per side!
        if self.spe.pattern.shape[0] > 3:
            self.spe.pattern = self.spe.pattern[1:-1, 1:-1]

            self.spill_canvas.configure(height=self.spe.pattern.shape[0]*self.spe.zoom, width=self.spe.pattern.shape[1]*self.spe.zoom)
            self.spill_image = self.spe.to_image()
            self.spill_canvas.itemconfig(self.spill_container, image=self.spill_image)

        pass

    def add_color(self):
        """ Add a color button to the window """
        x = int(self.slope_indicator_label["text"])

        if x >= len(self.color_buttons):
            if self.isMac:
                self.color_buttons.append(tk.Button(master=self.frame6, text=str(x), highlightbackground="#ffffff"))
            else:
                self.color_buttons.append(tk.Button(master=self.frame6, text=str(x), bg="#ffffff"))
            self.color_buttons[x].bind("<Button-1>", lambda event, x=x: self.choose_color(x))
            self.color_buttons[x].grid(column=x+1, row=1)
        else:
            self.color_buttons[x].grid(column=x+1, row=1)


    def subtract_color(self):
        """ Remove a color button from the window """
        x = int(self.slope_indicator_label["text"])

        self.color_buttons[x+1].grid_forget()

    def apply_setting_changes(self, event):
        """ Apply setting changes to the parameters in Sandbox and close window """
        # height and width
        if not int(self.height_entry.get()) == self.sandbox.height or not int(self.width_entry.get()) == self.sandbox.width:
            self.sandbox.height = int(self.height_entry.get())
            self.sandbox.width = int(self.width_entry.get())
            self.sandbox.array = self.array = np.zeros((self.sandbox.width, self.sandbox.height))
        # zoom
        self.sandbox.zoom = int(self.zoom_entry.get())
        # max slope
        self.sandbox.max_slope = int(self.slope_indicator_label["text"])
        #bucket size
        self.sandbox.bucket = int(self.bucket_entry.get())
        #spill pattern
        self.sandbox.spill_pattern = self.spe.pattern.copy()
        #pixel colors
        if self.isMac:
            self.sandbox.overflow_color = self.hex_to_rgb(self.overflow_color_button["highlightbackground"])
        else:
            self.sandbox.overflow_color = self.hex_to_rgb(self.overflow_color_button["bg"])
        palette = []
        for x in range(self.sandbox.max_slope+1):
            if self.isMac:
                palette.append(self.hex_to_rgb(self.color_buttons[x]["highlightbackground"]))
            else:
                palette.append(self.hex_to_rgb(self.color_buttons[x]["bg"]))
        self.sandbox.palette = palette


        self.window.destroy()

    def toggle_pixel(self, event):
        """ Handles click events on the spill pattern canvas """
        self.spe.toggle_pixel(event)
        self.spill_image = self.spe.to_image()
        self.spill_canvas.itemconfig(self.spill_container, image=self.spill_image)

        # check that max slope is at least as many as full pixels
        min_max = self.spe.pattern.sum() - 1
        if int(self.slope_indicator_label["text"]) < min_max:
            self.slope_indicator_label.configure(text=min_max)
            self.add_color()
