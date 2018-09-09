import sys
import tarfile, os
import json
import base64
import io

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

if __name__ == "__main__":
	args = unpackArgs()
	
if __name__ == "__main__" and ("help" in args.keys()):
	print("NotVCS.py Help Menu\n\nOptions:\n--help me - Shows help menu\n--mode <unpack/repack> - Specify whether to unpack or repack a .vex file\n--file <file name> - Specify the name of your file")
	
elif __name__ == "__main__" and "mode" in args.keys() and args["mode"] == "unpack":

	if not os.path.exists("unpacked/source/"):
		try:
			os.makedirs("unpacked/source/")
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	vexFile = args["file"]
	print("Reading from file %s" % vexFile)
	tar = tarfile.open(vexFile, mode="r:*")
	for containedFile in tar.getmembers():
		cFile = tar.extractfile(containedFile)
		dataJson = cFile.read()
	print(dataJson.decode())
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

elif __name__ == "__main__" and "mode" in args.keys() and args["mode"] == "repack":
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
	
elif __name__ == "__main__":
	print("Please specify parameters. Use the --help option for help.")
	