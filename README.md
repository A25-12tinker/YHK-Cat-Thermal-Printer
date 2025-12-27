YHK Cat Thermal Printer - a GUI fork
====================================

> The Android and iOS app named **WalkPrint** is compatible with (...) [the] printer. (...)

All technical work was done by [user abhigkar](https://github.com/abhigkar). This is merely a copy-paste to and from chatgpt to make working with the printer seamless thanks to graphical interface.

How to use the script?
----------------------

1. connet with a printer\*;
2. obtain MAC address like xx:xx:xx:xx:xx:xx\*;
3. run `sdptool add --channel=N SP`, where **"N"** is the channel;
4. run `sudo rfcomm bind **N** xx:xx:xx:xx:xx:xx`
5. run `python main.py`

\* Your basic bluetooths software should be enough for those tasks.

Original instruction with `bluetoothctl`:

1. Scan the MAC address of your printer using Bluetoothctl
2. Run scan on if printer found run pair xx:xx:xx:xx:xx:xx ADDR and trust xx:xx:xx:xx:xx:xx
3. Exit bluetoothctl
4.  I have selected 2 in my case.
5. Run sudo rfcomm bind **N** xx:xx:xx:xx:xx:xx, N  = channel = port
6. Run cat-printer.py

References
----------

Other reference projects:

* original repository: [abhigkar/YHK-Cat-Thermal-Printer](https://github.com/abhigkar/YHK-Cat-Thermal-Printer)
* [repositories](https://github.com/JJJollyjim/catprinter)
* [bitbank2/Thermal_Printer](https://github.com/bitbank2/Thermal_Printer)
* [WerWolv/PythonCatPrinter](https://github.com/WerWolv/PythonCatPrinter)
* [amber-sixel/PythonCatPrinter](https://github.com/amber-sixel/PythonCatPrinter)
* [the6p4c/catteprinter](https://github.com/the6p4c/catteprinter)
* [JJJollyjim/PyCatte](https://github.com/JJJollyjim/PyCatte)
* [xssfox](https://gist.github.com/xssfox/b911e0781a763d258d21262c5fdd2dec)
