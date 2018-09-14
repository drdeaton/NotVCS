import sys
import tarfile, os
import json
import base64
import io
import pcpp
import time
from io import StringIO
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--preprocess", help="Pack with preprocessor", action="store_true")
parser.add_argument("-r", "--repack", help="Pack without preprocessor", action="store_true")
parser.add_argument("-u", "--unpack", help="Unpack (requires file parameter)", action="store_true")
parser.add_argument("--file", help="Specify file name for unpacking")
parser.add_argument("-o", "--open", help="Opens file in VCS after it is processed. VCS must be installed.", action="store_true")
args = parser.parse_args()
#print(type(args))

def unpackArgs() :
	arguments = {}
	tracker = ""
	for arg in sys.argv:
		if(arg.startswith("--")):
			tracker = arg[2:]
		elif(tracker == ""):
			continue
		else:
			arguments[tracker] = arg
			tracker = ""
	return arguments 

# if __name__ == "__main__":
	# args = unpackArgs()
	
#if __name__ == "__main__" and ():
#	print("NotVCS.py Help Menu\n\nOptions:\n--help me - Shows help menu\n--mode <unpack/repack> - Specify whether to unpack or repack a .vex file\n--file <file name> - Specify the name of your file")
	
if __name__ == "__main__" and args.unpack:
	try:
		assert args.file != None
	except:
		raise Exception("You must specify a file!")
	if not os.path.exists("unpacked/source/"):
		try:
			os.makedirs("unpacked/source/")
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	vexFile = args.file
	print("Reading from file %s" % vexFile)
	tar = tarfile.open(vexFile, mode="r:*")
	for containedFile in tar.getmembers():
		cFile = tar.extractfile(containedFile)
		dataJson = cFile.read()
	#print(dataJson.decode())
	dataExtracted = json.loads(dataJson)
	
	files = dataExtracted.pop('files', None)
	if files == None:
		raise Exception("Invalid file")
	
	with open('unpacked/vexfile_info.json', 'w', newline='') as csvFile:
		csvFile.write(json.dumps(dataExtracted))
			
	for fileName in files:
		with open("unpacked/source/" + fileName, "w") as el_file:
			notb64 = base64.b64decode(files[fileName])
			el_file.write(notb64.decode('utf-8'))

elif __name__ == "__main__" and args.repack:
	with open('unpacked/vexfile_info.json', 'r') as csv_file:
		vfi = json.loads(csv_file.read())
	files = {}
	for fileName in os.listdir('unpacked/source/'):
		e = open("unpacked/source/" + fileName, "r")
		files[fileName] = base64.b64encode(e.read().encode()).decode('utf-8')
		e.close()
		
	vfi["files"] = files
	fn = vfi["title"]
	jvfi = json.dumps(vfi)
	#jvfi = jvfi.replace("'", "\"")
	abuf = io.BytesIO()
	abuf.write(jvfi.encode())
	abuf.seek(0)
	tar = tarfile.open(fn + ".vex", mode="w:")
	jsonfiletarinfo = tarfile.TarInfo(name="___ThIsisATemPoRaRyFiLE___.json")
	jsonfiletarinfo.size = len(abuf.getbuffer())
	tar.addfile(tarinfo=jsonfiletarinfo,fileobj=abuf)
	
elif __name__ == "__main__" and args.preprocess:

	if not os.path.exists("build/"):
		try:
			os.makedirs("build/")
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	sys.stdout.flush()
	old_stdout = sys.stdout
	sys.stdout = mystdout = StringIO()
	p = pcpp.cmd.CmdPreprocessor(["pcpp", "unpacked/source/main.cpp", "--line-directive", "--passthru-unfound-includes"])
	sys.stdout = old_stdout
	pCont = mystdout.getvalue()
	#print(vars(p))
	pCont.replace('\n'*2, '\n')
	topMessage = "/***********************************************************************************\nThis code was generated from multiple source files using NotVCS, by AusTIN CANs 2158\n https://github.com/dysproh/notvcs \n***********************************************************************************/\n"
	uCont = topMessage + pCont
	time.sleep(1)
	#sys.stdout.flush()
	#int("h" + preprocessedFile.read())
	#print(pCont)
	files = {"main.cpp": base64.b64encode(uCont.encode()).decode('utf-8'), "robot-config.h": ""}
	config = open("unpacked/vexfile_info.json", "r")
	ufi = config.read()
	config.close()
	vfi = {}
	vfi = json.loads(ufi)
	#print(type(vfi))
	vfi["files"] = files
	fn = vfi["title"]
	fn = fn.replace(" ", "-")
	jvfi = json.dumps(vfi)
	#jvfi = jvfi.replace("'", "\"")
	abuf = io.BytesIO()
	abuf.write(jvfi.encode())
	abuf.seek(0)
	tar = tarfile.open(fn + ".vex", mode="w:")
	jsonfiletarinfo = tarfile.TarInfo(name="___ThIsisATemPoRaRyFiLE___.json")
	jsonfiletarinfo.size = len(abuf.getbuffer())
	tar.addfile(tarinfo=jsonfiletarinfo,fileobj=abuf)
	tar.close()
	if args.open:
		try:
			retcode = subprocess.call("start " + fn + ".vex", shell=True)
			if retcode < 0:
				print("Child was terminated by signal")
			else:
				pass
				#print("Child returned something idk")
		except:
			raise
elif __name__ == "__main__":
	print("Please specify parameters. Use the --help option for help.")
	