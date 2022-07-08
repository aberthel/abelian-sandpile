#!/usr/bin/#!/usr/bin/env python3

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImagePalette

### VARIABLES ###

sb_height = 100
sb_width = 100

#sandbox
sandbox = np.reshape(np.array([np.array([255, 25, 255])]*sb_height*sb_width, dtype = np.uint8), (sb_height, sb_width, -1))

#drawing palette
#pal = ImagePalette.ImagePalette(palette=[252,251,237,197,245,152,133,191,78,83,133,37,89,64,13], size=15)

#spill_pattern

max_slope = 3
#spill_queue
bucket_size = 1





### MAIN WINDOW KEY BINDS ###

def open_settings(event):
    settings_window = tk.Toplevel(main_window)

    # frame 1

    top_frame = tk.Frame(master=settings_window)

    settings_label = tk.Label(master=top_frame, text="Settings")
    height_label = tk.Label(master=top_frame, text="Sandbox Height")
    height_entry = tk.Entry(master=top_frame, width=10)
    height_entry.insert(0, str(sb_height))
    width_label = tk.Label(master=top_frame, text="Sandbox Width")
    width_entry = tk.Entry(master=top_frame, width=10)
    width_entry.insert(0, str(sb_width))

    settings_label.pack(side=tk.TOP)
    height_label.pack(side=tk.LEFT)
    height_entry.pack(side=tk.LEFT)
    width_entry.pack(side=tk.RIGHT)
    width_label.pack(side=tk.RIGHT)

    # frame 2

    second_frame = tk.Frame(master=settings_window)

    size_note_label = tk.Label(master=second_frame, text="Warning: changing sandbox size will reset the current pattern.")

    size_note_label.pack()

    # frame 3
    bottom_frame = tk.Frame(master=settings_window)

    apply_button = tk.Button(master=bottom_frame, text="Apply New Settings")
    #apply_button.bind("<Button-1>", apply_setting_changes)
    cancel_button = tk.Button(master=bottom_frame, text="Cancel", command=settings_window.destroy)
    #cancel_button.bind("<Button-1>", cancel_setting_changes)

    apply_button.pack(side=tk.LEFT)
    cancel_button.pack(side=tk.RIGHT)
    # pack all frames

    top_frame.pack()
    second_frame.pack()
    bottom_frame.pack()

    settings_window.grab_set()


def open_save(event):
    # TODO: open save window
    print("open save window")










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

main_canvas = tk.Canvas(master=drawing_frame, bg="white", height=100, width=100)
main_canvas.pack()

header_frame.pack()
drawing_frame.pack()

# draw image from sandbox array
# TODO: replace with function later in order to define palette, pixel size, etc.
img = Image.fromarray(sandbox, mode="RGB")
print(img.getpixel((0, 0)))

ph = ImageTk.PhotoImage(img)
main_canvas.create_image(0, 0, image=ph, anchor="nw")

main_window.mainloop()
