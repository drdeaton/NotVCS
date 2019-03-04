import argparse
import os
import pcpp
from io import StringIO
import base64
import json
import sys


#Exit if not the main file
if not __name__ == "__main__":
	exit()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="Choose to either install an existing .nvcx or create a new one from a .cc file")
iparser = subparsers.add_parser("install")
mparser = subparsers.add_parser("make")

iparser.add_argument("nvcx_file", help="The file with the extension .nvcx that you want to install")
iparser.set_defaults(type="install")

mparser.add_argument("src_file", help="The source file that you want to make your .nvcx file from")
mparser.add_argument("--output","-o", help="The name for your .nvcx file", default="Out.nvcx")
mparser.add_argument("--name","-n", help="The name of your NotVCS Extension", default=None)
mparser.set_defaults(type="make")


args = parser.parse_args()

if args.type == "install":
	print('Installing your .nvcx file.')
	print('To import an extension file in your NotVCS program, use the prefix "NV_"')
	
	nvcxf = open(args.nvcx_file, "r")
	
	fileDataJson = nvcxf.read()
	fileData = json.loads(fileDataJson)
	
	print('For example, for this extension, use the preprocessor directive:\n#import <NV_%s>' % fileData["name"])
	
	if not os.path.exists(os.getenv('APPDATA') + "/notvcs/extensions/"):
		try:
			print('Creating the NotVCS Extensions directory.')
			os.makedirs(os.getenv('APPDATA') + "/notvcs/extensions/")
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	
	if not os.path.exists(os.getenv('APPDATA') + "/notvcs/extensions/" + fileData["name"] + "/"):
		try:
			print('Creating a directory for this extension')
			os.makedirs(  os.getenv('APPDATA') + "/notvcs/extensions/" + fileData["name"] + "/")
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
				
	ifile = open(os.getenv('APPDATA') + "/notvcs/extensions/" + fileData["name"] + "/extension.nvcx", "w")
	ifile.write(fileDataJson)
	
elif args.type == "make" :
	print("Making from file %s" % args.src_file)
	sys.stdout.flush()
	old_stdout = sys.stdout
	sys.stdout = mystdout = StringIO()
	
	if os.path.exists(args.src_file):
		p = pcpp.cmd.CmdPreprocessor(["pcpp", args.src_file, "--line-directive", "--passthru-unfound-includes"])
	else:
		raise Exception("Nonexistant file: %s" % args.src_file)
	
	sys.stdout = old_stdout
	pCont = mystdout.getvalue()

	#Now, pCont should hold the preprocessed data
	#Create an array with all this stuff
	
	if not (args.name == None):
		name = args.name
	else:
		nar = args.src_file.split(".")[:-1]
		name = ".".join(nar)
	
	fileData = {"content":base64.b64encode(pCont.encode()).decode('utf-8'),"name":name}
	fileDataJson = json.dumps(fileData)
	
	print(fileDataJson)
	
	nvcxFile = open(args.output, "w")
	nvcxFile.write(fileDataJson)
	nvcxFile.close()
	