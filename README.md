PyHackBar
=========

Simple desktop bar (panel) written using PySide2 (Qt for Python).
A direct replacement for **lemonbar**.

Configuration is done by hacking the code. This is a little bit less dumb than
configuring **lemonbar** with all clickable features. 

C'mon, are you going to write a python script with subprocesses to handle all those
mouse click events and alter the display accordingly? WHY? You can just use a GUI
library to handle this stuff in more idiomatic way. 

Usage
-----

Install with (requires python 3):

```bash
pip install git+https://github.com/pkubik/PyHackBar.git
```

Run through command `pyhackbar`.

Due to the fact that the configuration is done by hacking the code it is probably
a better idea to just clone the repository and install the local copy in
edit/development mode (`-e` option):

```bash
cd PyHackBar
pip install -e .
```

Misc
----

- Tray icon on the right requires `trayer` (from most distros repositories)
- I didn't manage to preserve appropriate padding for the window manager. Use your WM
  config to do so, e.g. `bspc config bottom_padding 36` in BSPWM.
  