#!/usr/bin/env python3
import random

banner = """ +-++-++-++-++-++-++-++-++-+
   |R||E||V| |0||1| |B||H|    
 +-++-++-++-++-++-++-++-++-+
 |H||a||c||k||a||f||l||a||g|
 +-++-++-++-++-++-++-++-++-+
     |K||e||y||g||e||n|         
 +-++-++-++-++-++-++-++-++-+  
   """
   
def generate_serial():
	start = [66,82,69,78,78,79,82,68,83,95]
	end = [95,82,65,84,70]
	sum_ascii_serial = 3645
	serial = []
	
	while sum_ascii_serial > 1:
		random_char_ascii_code = (random.randint(97,122))

		if (sum_ascii_serial < 122):
			random_char_ascii_code = sum_ascii_serial

		sum_ascii_serial = sum_ascii_serial - random_char_ascii_code
		serial.append(random_char_ascii_code)

	valid_serial = start + serial + end

	return (''.join(map(chr,valid_serial)))

def main():
	print(banner)
	keygens = int(input("Tell me how many keys do you want: "))
	while (keygens > 0):
		print (generate_serial())
		keygens = keygens - 1

if __name__ == '__main__':
	main()
