# Nanospectrum

## Installation

Nanospectrum has a few non-python dependencies: PulseAudio, SDL2 and SDL2-GFX. On OS X, you can install them using:
`brew install pulseaudio sdl2 sdl2_gfx`.

Install the Python requirements by running `pip install -r requirements.txt`. This project requires Python 3.6 or
greater.

## Setup

Nanospectrum does not yet have any Nanoleaf Aurora detection capabilities. To set Nanospectrum up to control your
Aurora:

* You will need to look at the list of connected devices on your router to determine the Aurora's IP address.
* Press the power button on your Aurora for several seconds, until a white led starts flashing on the controller.
* Run `python aurora_setup.py <ip-address>`.
* This will write the authentication token to the `key` file in the current directory. Keep it there, it will be read
by Nanospectrum to connect to the Aurora.

# Running Nanospectrum

Run `python nanospectrum.py <aurora-ip-address>`. If you don't have an Aurora, or can't connect to it, make up an IP
address and run with the `-i <num-panels>` flag, which will simulate an Aurora with `num-panels panels arranged
linearly.

Run with `-s` to enable SDL output. This is useful for quickly debugging visualizations.

By default, Nanospectrum will listen on the default microphone. Use `-f <filename>` to play a file instead. The file
must be a 16-bit PCM wav file. You can get one from an mp3 (or many other formats) using libav:

`avconv -i file.mp3 file.wav`

(install with `brew install libav` on OS X).

## Creating new visualizations

To create a new visualization, inherit the `visualizations.visualization_base.VisualizationBase` class. You need to
implement the `process_samples(self, samples, n_panels)` method. The samples argument is a numpy array containing
a sequence of int16s representing the samples collected since the last time `process_samples` was called. It needs to
return an `n_panels` by 3 array, containing float values between 0 and 1 that represent the RGB components of each
panel.

# Known issues

* The program will often not halt correctly.
* The power visualization is buggy.
