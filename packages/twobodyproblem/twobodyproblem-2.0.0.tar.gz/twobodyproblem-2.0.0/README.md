# Two Body Problem

### a small simulation

**Welcome!**

I wrote a small program in Python to simulate the two body problem.
You type in some parameters, like mass, radius, velocity and distance.
The program will show you a visualization of the simulation.

*This program is command line only. If you want a graphical user interface,
visit [this GitHub page](https://github.com/Two-Body-Problem/twobodyproblem-simulation-python-gui).*

## Table of Contents

[Installation Instructions](#installation-instructions)  
- [via PyPi](#via-pypi)  
- [via GitHub](#via-github)  

[Usage](#usage)
  
## Installation Instructions

*(You may need Microsoft Visual C++ to be able to run the program,
so install it from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools) if needed.)*

### via PyPi

*The Python package manager pip will install the last uploaded version
from the Python Package Index [PyPi](https://pypi.org/project/twobodyproblem).
This will not always be the latest version, so if you want to install all the latest features,
install it from GitHub (see [below](#via-github)).*

1. Make sure [Python](https://www.python.org/downloads) and pip are installed correctly.
1. Run these commands from a command line:
   1. `pip3 install --upgrade pip setuptools wheel`
   1. `pip3 install --upgrade twobodyproblem`
1. Now, the program is runnable with `python -m twobodyproblem` or `python3 -m twobodyproblem`.

### via GitHub

1. Make sure [Python](https://www.python.org/downloads) and pip are installed correctly.
1. Make sure [Git SCM](https://git-scm.com/downloads) is installed correctly.
1. Run these commands from a command line:
    1. `mkdir TwoBody` and `cd TwoBody`
    1. `git clone https://github.com/Two-Body-Problem/twobodyproblem-simulation-python.git`
    1. `pip3 install --upgrade pip setuptools wheel`
    1. `pip3 install twobodyproblem-simulation-python`
1. Now, the program is runnable with `python -m twobodyproblem` or `python3 -m twobodyproblem`.

## Usage

*To learn more about how to run the program with different options,
run `python -m twbodyproblem -h` or `python3 -m twbodyproblem -h` respectively.*

Run the program with `python -m twobodyproblem` or `python3 -m twobodyproblem`.

First, you will have to input *options* and *values*.
The options define the particular behavior of the simulation,
the values define the dimensions (i.e. mass, radius, distance, velocity) of the bodies.

The simulation will start automatically after the last input.

During the simulation, you are able to pause, un-pause and stop the simulation
with the accordingly named buttons below the black rectangle.
The restart button restarts the *whole* program, not just the simulation.

The sliders below the buttons can be used to magnify the bodies in the simulation.
This magnification does not affect the physics, it is only a visual help.

***

*Participation in this README is always welcome!*
