# Abelian Sandpile model

This project is an interactive implementation of the abelian sandpile model.

In this model, we have a set of spaces laid out in a grid, onto which we can place "grains of sand."
Each space can only accommodate a certain number of grains until they start to spill
over into the adjacent spaces. If those adjacent spaces also exceed their capacity
to hold grains of sand, they will also spill over, and this will continue in a cascade
until the system reaches a steady state.

The scripts here allow you to interact with the abelian sandpile model and explore
how changing the parameters of the model affects the patterns it creates. You can alter
the number of grains of sand placed at a time, the capacity of each space, and the
pattern in which the grains spill: all will produce different results.

This project was created as something of a mathematical toy. Experiment with it,
and see what patterns arise!

## System Requirements

This project was developed in Python version 3.10. It may work on earlier versions
of Python 3, though I make no guarantees.

It requires NumPy and Pillow.

## How To Run

Download the entire project folder.
In the command line, navigate to the project folder.
`python main.py`

A new window should open.

## How To Use

Again, this project was developed as a kind of toy. There is no proper way to
use it, and I encourage you to click around until something interesting happens.

That said, some pointers:

As a default, you deposit one grain of sand every time you click on a space.
This can be changes in Settings under "Bucket Size." I recommend bucket sizes of
no more than 500 or so, as it can take a long time for the system to reach its
steady state. But if you have a long time to spend or just like to watch the cascade,
by all means ignore my suggestions. Extremely large numbers may cause the program
to crash, but I haven't personally tested its upper limit. Set bucket size to
1000000000000000 at your own risk!

The number of grains a space can hold before spilling over can be changed by increasing
or decreasing "Max Slope" in settings. Note that max slope is constrained by the
spill pattern, and not all values are allowed.

The pattern in which grains spill can also be changed in settings. Click on the
pattern grid to toggle individual pixels: black pixels denote where grains of sand
will spill relative to the central point.

Change the color palette by clicking on any of the buttons under "Pixel Colors."
Each color represents a different number of grains of sand in a given space.

## What Do I Do With These Patterns?

The "Save Image" button allows you to save any patterns you create as a PNG image.
From there, you can do whatever you want with it. If you're a creative type,
these patterns might inspire you in your medium of choice. Personally, I think
they'd look great as a patchwork quilt!

## Coming Soon

Future features include improved color palette picking and non-square grids!
