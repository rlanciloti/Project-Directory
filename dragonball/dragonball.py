"""
...on their own, each dragon ball is useless. However, when combined together, you can summon
the mystical dragon!
"""
import random
import sys
import string


mode = ''
num_files = 0
in_files = []


def invert(val: bytes) -> bytearray:
	"""
	This function will invert a byte

	:param val: byte to be inverted
	:type val: bytes
	:return: inverted byte
	:rtype: bytearray
	"""
	res = []
	for b1, b2 in zip(val, [0xFF]):
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
	name_length = 5
	for file in range(f_count):
		file_name = ''
		for char in range(name_length):
			file_name += random.choice(string.ascii_letters)
		files.append(file_name + str(file) + '.encpt')

	return files


def encrypt(fname: str) -> None:
	"""
	This function will read an input file, and divide it into a certain number of files. The
	number of files is passed in as a commandline parameter

	:param fname: name of input file
	:type fname: str
	"""
	part = 0

	with open(fname, "rb") as f:
		outfiles = generate_random_files(num_files)
		files = [open(file, "wb") for file in outfiles]

		byte = f.read(1)

		while byte:
			b = invert(byte)
			files[part].write(b.to_bytes(1, 'big'))
			part += 1
			part %= num_files
			byte = f.read(1)

		for file in files:
			file.close()


def decrypt(file_names: list):
	"""
	This function will take in a given number of input files and combine them into a single
	output file.

	:param file_names: List of input files
	:type file_names: list
	"""
	files = [[open(file, "rb"), False] for file in file_names]
	outfile = generate_random_files(1)
	outfile = open(outfile[0], "wb+")

	index = 0
	done = False

	while not done:
		done = True
		for end_check in files:
			done &= end_check[1]

		for file in files:
			if file[1]:
				continue
			byte = file[0].read(1)
			if byte:
				b = invert(byte)
				outfile.write(b.to_bytes(1, 'big'))
			else:
				file[1] = True

	for file in files:
		file[0].close()
	outfile.close()


def parse_args(arguments: list) -> None:
	"""
	This function will parse the commandline arguments to determine what this script will do

	:param arguments: list of arguments to be parsed
	:type arguments: list
	"""
	global num_files
	global in_files
	global mode

	if(len(arguments) < 3):
		sys.exit(2)

	mode = arguments[1]

	if mode == '-d':
		num_files = int(arguments[2])
		in_files = arguments[3:]
		if len(in_files) != num_files:
			sys.exit(3)

		decrypt(in_files)

	if mode == '-e':
		num_files = int(arguments[2])
		in_files = [arguments[3]]


def main(arguments: list):
	"""
	Main function which invoked all of the core logic

	:param arguments: list of commandline arguments
	:type arguments: list
	"""
	global mode

	parse_args(arguments)
	if mode == '-e':
		encrypt(in_files[0])


if __name__ == '__main__':
	main(sys.argv)
