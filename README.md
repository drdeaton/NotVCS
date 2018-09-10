# Not VCS

Not VCS is a python script that allows you to unpack and repack .vex files. 

# Requirements
Not VCS requires Python 3
# Unpacking
To unpack a .vex file, move the script into the directory with your .vex file.
Open a command prompt, powershell window, or terminal, and type the following command:

`python notvcs.py --mode unpack --file <.vex file name>`

Your .vex file should be extracted to a folder named `unpacked`, which will contain a json file and a source directory, which will in turn have all of your source files.

# Repacking
To repack a .vex file, simply have the script in the same directory as your `unpacked` directory. Run the following command:

`python notvcs.py --mode repack`

To repack with preprocessor (if you have multiple files), use:

`python notvcs.py --mode preprocess`

Please note that the preprocessor is pretty sketchy. Don't rely too much on it.
