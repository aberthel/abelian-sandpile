#!/usr/bin/#!/usr/bin/env python3

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImagePalette
from tkinter.filedialog import asksaveasfilename
import settings
import sandboxes

# TODO: interchange triangular and hexagonal sandboxes
sandbox = sandboxes.Sandbox(100, 100)
sw = ""

### MAIN WINDOW KEY BINDS ###

# opens settings window
def open_settings(event):
    global sw
    sw = settings.Window(main_canvas, sandbox)


#def update_spill_image():
#    global spill_image
#    spill_image = spe.to_image()
#    spill_canvas.itemconfig(spill_container, image=spill_image)

# opens save dialog box
def open_save(event):

    # only PNG images are supported at the moment    
    supported_filetypes = [('PNG Image', '*.png')]
    
    filename = asksaveasfilename(filetypes=supported_filetypes, defaultextension=supported_filetypes)
    sandbox.image.save(filename, "PNG")

# update image displayed on main canvas
def update_image():
    global current_image # image has to be saved in a global variable or gc removes it
    current_image = sandbox.to_image()
    main_canvas.itemconfig(image_container, image=current_image)
    main_window.update()

# handles button press event on main canvas
def place_sand(event):
    # TODO: can be streamlined - im_to_coords called within place_sand
    sandbox.place_sand(sandbox.im_to_coords(event.x, event.y))

# called whenever settings window is closed so that zoom and color palette automatically change
def return_focus(event):
    main_canvas.configure(height=sandbox.zoom*sandbox.height, width=sandbox.zoom*sandbox.width)
    update_image()
    
### MAIN WINDOW SETUP ###

main_window = tk.Tk()

header_frame = tk.Frame()
drawing_frame = tk.Frame()

# buttons at top of window - settings, save, etc.
title_label = tk.Label(master=header_frame, text="Abelian Sandpile Model")
settings_button = tk.Button(master=header_frame, text="Settings")
settings_button.bind("<Button-1>", open_settings)
save_button = tk.Button(master=header_frame, text="Save Image")
save_button.bind("<Button-1>", open_save)

title_label.pack(side=tk.TOP)
settings_button.pack(side=tk.LEFT)
save_button.pack(side=tk.RIGHT)

# canvas holds the sandpile image and is interactive by clicking with left mouse button
main_canvas = tk.Canvas(master=drawing_frame, bg="grey", height=sandbox.zoom*sandbox.height, width=sandbox.zoom*sandbox.width)
main_canvas.bind("<Button-1>", place_sand)
main_canvas.pack()

header_frame.pack()
drawing_frame.pack()

# draw image from sandbox array
current_image = sandbox.to_image()
image_container = main_canvas.create_image(0, 0, image=current_image, anchor="nw")

spill_image = "" #TODO: remove???
main_window.bind("<FocusIn>", return_focus)
main_window.mainloop()
