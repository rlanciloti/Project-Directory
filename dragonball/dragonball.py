"""
...on their own, each dragon ball is useless. However, when combined together, you can summon
the mystical dragon!
"""
import random
import sys
import string

help_menu = """
Welcome to DragonBall!

Named after the hit TV show 'Dragon Ball', this script can split any file into multiple other files.
Each individual piece will be encrypted with a psudeo-random bit stream before it's written out to
the out files.

This script can also recombine and decrypt the files previously encrypted with it...so long as you
have the keys D:

-h: Prints this message, will exit the program after
-d: Specifies that the script should run in decryption mode
-e: Specifies that the script should run in encryption mode
-fc: If in decryption mode, this is the number of files
needed to be read in to decrypt the file. In encryption mode, it specifies the number of output
files and in decryption mode, it specifies the number of input files.
-o: Used to specify the name of the output file.  Optional. Only used in decryption mode.
-s: Used to specify the random generator seed. Optional.
-r: Used for creating an output report. Used only in encryption mode. Optional
-f: Used for specifying the input files. When in decryption mode, these are the encrypted files,
when in encryption mode, this is the file to be encrypted
"""


class ArgParser:
	"""
	This class will be used for setting up the environment based on the commandline arguments
	"""

	def __init__(self, arguments: list) -> None:
		"""
		Creates the ArgParser object
		"""
		if '-h' in arguments:
			print(help_menu)
			sys.exit(0)
		if '-d' in arguments:
			self.mode = '-d'
		elif '-e' in arguments:
			self.mode = '-e'
		elif '-d' not in arguments and '-e' not in arguments:
			print("Error: mode not specified")
			sys.exit(1)

		self.seed = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
		self.outfile = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7)) + '.out'
		self.create_report = False
		self.files = []
		self.num_files = 0

		for index in range(len(arguments)):
			if self.mode == '-d':
				if arguments[index] == '-o':
					self.outfile = arguments[index + 1]
				if arguments[index] == '-f':
					self.files = arguments[index + 1: index + 1 + self.num_files]

			if self.mode == '-e':
				if arguments[index] == '-r':
					self.create_report = True
					self.report_name = arguments[index + 1]
				if arguments[index] == '-f':
					self.files = [arguments[index + 1]]

			if arguments[index] == '-s':
					self.seed = arguments[index + 1]
			if arguments[index] == '-fc':
				self.num_files = int(arguments[index + 1])

		if not self.files:
			print("Error: No input files specified")
			sys.exit(2)


def xor(val1: bytes, val2: bytes) -> bytearray:
	"""
	This function will invert a byte

	:param val: byte to be inverted
	:type val: bytes
	:return: inverted byte
	:rtype: bytearray
	"""
	res = []
	for b1, b2 in zip(val1, val2):
		res.append(b1 ^ b2)
	return res[0]


def generate_random_files(f_count: int) -> list:
	"""
	This function will generate a list of random file names

	:param f_count: number of files to be generated
	:type f_count: int
	:return: list of file names
	:rtype: list
	"""
	files = []
	name_length = 8
	for file in range(f_count):
		file_name = ''
		for char in range(name_length):
			file_name += random.choice(string.ascii_letters)
		files.append(file_name)

	return files


def encrypt(fname: str) -> None:
	"""
	This function will read an input file, and divide it into a certain number of files. The
	number of files is passed in as a commandline parameter

	:param fname: name of input file
	:type fname: str
	"""
	outfiles = []
	with open(fname, "rb") as f:
		outfiles = [name + '.encpt' for name in generate_random_files(parser.num_files)]
		files = [open(file, "wb") for file in outfiles]

		byte = f.read(1)
		random.seed(parser.seed)
		part = random.randint(0, parser.num_files - 1)

		while byte:
			b = xor(byte, [random.randint(0x00, 0xFF)])
			files[part].write(b.to_bytes(1, 'big'))
			part = random.randint(0, parser.num_files - 1)
			byte = f.read(1)

		for file in files:
			file.close()

	if parser.create_report:
		with open(parser.report_name, "w+") as f:
			f.writelines(f"Main File: {parser.files[0]}\n")
			f.writelines(''.join('-' for _ in range(64)) + '\n')

			for index in range(len(outfiles)):
				f.writelines(f"{index}: Out File - {outfiles[index]}\n")

			f.writelines(''.join('-' for _ in range(64)) + '\n')
			f.writelines(f"Seed: {parser.seed}\n")
			f.writelines(''.join('-' for _ in range(64)) + '\n')


def decrypt(file_names: list):
	"""
	This function will take in a given number of input files and combine them into a single
	output file.

	:param file_names: List of input files
	:type file_names: list
	"""
	file_struct = [{"file": open(file, "rb"), "done": False} for file in file_names]

	outfile_stream = open(parser.outfile, "wb+")

	done = False

	random.seed(parser.seed)

	while not done:
		done = True
		for file in file_struct:
			done &= file["done"]

		f = random.randint(0, parser.num_files - 1)

		if file_struct[f]["done"]:
			continue

		byte = file_struct[f]["file"].read(1)
		if byte:
			b = xor(byte, [random.randint(0x00, 0xFF)])
			outfile_stream.write(b.to_bytes(1, 'big'))
		else:
			file_struct[f]["done"] = True

	for file in file_struct:
		file["file"].close()
	outfile_stream.close()


def main(arguments: list):
	"""
	Main function which invoked all of the core logic

	:param arguments: list of commandline arguments
	:type arguments: list
	"""
	if parser.mode == '-e':
		encrypt(parser.files[0])

	if parser.mode == '-d':
		decrypt(parser.files)


if __name__ == '__main__':
	parser = ArgParser(sys.argv)
	main(parser)
