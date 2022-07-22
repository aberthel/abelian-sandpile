### settings window class
### requires tkinter as tk
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImagePalette

class SpillPatternEditor:
    def __init__(self, pattern):
        self.pattern = pattern.copy()
        self.zoom = 50

    def to_image(self):
        image_array = np.zeros((self.pattern.shape[0], self.pattern.shape[1], 3), dtype=np.uint8)

        #TODO: better way to do this?
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
        x = int(event.x/self.zoom)
        y = int(event.y/self.zoom)

        if self.pattern[y, x] == 0:
            self.pattern[y, x] = 1
        else:
            self.pattern[y, x] = 0



# Builds and handles events for the settings window
class Window:
    def __init__(self, main_window, sandbox, ib):
        self.sandbox = sandbox
        self.ib = ib
        self.window = tk.Toplevel(main_window)

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

        # Frame 2: warning note about changing size

        self.frame2 = tk.Frame(master=self.window)

        self.size_note_label = tk.Label(master=self.frame2, text="Warning: changing sandbox size will reset the current pattern.")

        self.size_note_label.pack()

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

        self.spill_pattern_label.pack()
        self.spill_canvas.pack()

        self.spill_image = self.spe.to_image()
        self.spill_container = self.spill_canvas.create_image(0, 0, image=self.spill_image, anchor="nw")

        # Frame 6: Color picker selection

        self.frame6 = tk.Frame(master=self.window)

        self.color_picker_label = tk.Label(master=self.frame6, text="Pixel Colors (click to edit)")
        self.overflow_color_button = tk.Button(master=self.frame6, text="overflow", bg=self.rgb_to_hex(ib.overflow_color))

        # TODO: list full of buttons for each allowed color

        self.color_picker_label.pack()
        self.overflow_color_button.pack()

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
        self.frame6.pack()
        self.frame7.pack()

        # And finally for init, grab set

        self.window.grab_set()

    def rgb_to_hex(self, a):
        return '#%02x%02x%02x' % (a[0], a[1], a[2])

    def add_slope(self, event):
        new_slope = int(self.slope_indicator_label["text"]) + 1
        self.slope_indicator_label.configure(text=str(new_slope))

    def subtract_slope(self, event):
        # TODO: need to make sure max slope and spill pattern are compatible
        # check that max slope is at least as many as full pixels
        min_max = self.spe.pattern.sum() - 1
        if int(self.slope_indicator_label["text"]) > min_max:
            new_slope = int(self.slope_indicator_label["text"]) - 1
            self.slope_indicator_label.configure(text=str(new_slope))

    def apply_setting_changes(self, event):
        #TODO: height and width changes
        # max slope
        self.sandbox.max_slope = int(self.slope_indicator_label["text"])
        #bucket size
        self.sandbox.bucket = int(self.bucket_entry.get())
        #spill pattern
        self.sandbox.spill_pattern = self.spe.pattern.copy()

        self.window.destroy()

    def toggle_pixel(self, event):
        self.spe.toggle_pixel(event)
        self.spill_image = self.spe.to_image()
        self.spill_canvas.itemconfig(self.spill_container, image=self.spill_image)

        # check that max slope is at least as many as full pixels
        min_max = self.spe.pattern.sum() - 1
        if int(self.slope_indicator_label["text"]) < min_max:
            self.slope_indicator_label.configure(text=min_max)

    def reset_spill_pattern(self, pattern):
        self.spe.pattern = pattern
        self.spill_image = self.spe.to_image()
        self.spill_canvas.itemconfig(self.spill_container, image=self.spill_image)
