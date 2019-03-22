# WITH THE RELEASE OF VEXCODE, THIS PROJECT IS OFFICIALLY DEAD
# VEXCODE IS FAR SUPERIOR TO VCS+NOTVCS, USE THAT INSTEAD

# VCS4CMD

VCS4CMD, formerly known as NotVCS, is a program aimed at making VCS better. VCS4CMD in currently in beta, so, as of the time of writing, it requires both Vex Coding Studio and ProsV5 to be installed.

# Why VCS4CMD?

VCS4CMD has a few key advantages that complement other programs. It is similar to PROS in that it allows true multi-file support, but, unlike PROS, it uses the official API as developed by Robomatter, Inc.

# Dependencies

VCS4CMD requires the following:

[PCPP](https://pypi.org/project/pcpp/)

[Vex Coding Studio](https://vexrobotics.org)

Optional (needed for command line upload):

[PROS](https://pros.cs.purdue.edu)

[GnuWin32 Make](http://gnuwin32.sourceforge.net/packages/make.htm)

# Usage

VCS4CMD has a few command line options. As of now, unless you have PROS installed alongside VCS, it is recommended that you use this for loading programs onto your robot:

`python notvcs.py -po` or `python VCS4CMD.py -po`

If ProsV5 and GnuWin32 Make are installed, you can use this command instead:

`python VCS4CMD.py -l`

Please note that notvcs.py is discontinued and that updates will only be made to VCS4CMD.py.

Upload (-l) still requires testing. Use at your own risk.
