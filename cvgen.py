#!/usr/bin/env python3
import sys

if not (sys.version_info[0] >= 3 and sys.version_info[1] >= 5):
	raise Exception("This program needs Python 3.5 or newer to be executed.")

if len(sys.argv) < 2:
	raise Exception("This program needs a JSON file to be passed as first command line parameter.")

from os.path import join, dirname, realpath

try:
	from PIL import __version__
	
	pillow_version = float(''.join(__version__.rsplit(".", 1)))
	if pillow_version < 4.2: raise ImportError

	sys.path.append(join(dirname(realpath(__file__)), "top"))
	sys.path.append(join(dirname(realpath(__file__)), "center"))
	sys.path.append(join(dirname(realpath(__file__)), "bottom"))

	from time import time, sleep
	from threading import Thread
	from cv import Cv

	out = None
	start = time()
	def loader():
		for c in __import__("itertools").cycle(["|", "/", "-", "\\"]):
			if out: break
			sys.stdout.write("\rGenerating CV... " + c)
			sys.stdout.flush()
			sleep(0.1)
		print("\rCV successfully generated (%.2fs elapsed): %s" % (time() - start, out))
	Thread(target=loader).start()
	out = Cv(sys.argv[1]).generate()

except ImportError:

	from subprocess import check_call

	command = ' '.join([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
	print("Trying to install missing dependencies with command: %s" % command)
	check_call(command.split())
	command = ' '.join([sys.executable, join(dirname(realpath(__file__)), sys.argv[0]), sys.argv[1]])
	print("Running the program again after installing missing dependencies: %s" % command)
	check_call(command.split())
