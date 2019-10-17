#!/usr/bin/env python
import random 

class PortaSound:
	patch_header = [240,67,118,0]
	patch_footer = 247

	def twos_comp_b(self,val):
		return 0b1111111 - val + 1

	def check_binary(self,path):
		f = open(path,'rb')
		i = 0
		header = False
		headerbyte = 0
		footer = False
		footerbyte = 0
		checksum = 0
		validsum = False
		value = 0
		while True:
			byte_s = f.read(1)
			if not byte_s:
				break
			byte = byte_s[0]
			if i == 0: 
				if ord(byte) != self.patch_header[0]:
					header = False
				else:
					header = True
				headerbyte = ord(byte)
			if i == 1 and ord(byte) != self.patch_header[1]:
				header = False
			if i == 2 and ord(byte) != self.patch_header[2]:
				header = False
			if i == 3 and ord(byte) != self.patch_header[3]:
				header = False
			if i > 3 and i < 70:
				checksum = (checksum + ord(byte)) % 128
			if i == 70:
				value = ord(byte)
				if self.twos_comp_b(checksum) == value:
					validsum = True
			if i == 71:
                                footerbyte = ord(byte)
				if ord(byte) == self.patch_footer:
					footer = True
				if header == True: 
					print "Header present."
				else:
					print "Header invalid.", headerbyte
				if validsum == True:
					print "Checksum correct."
				else:
					print "Checksum invalid.", self.twos_comp_b(checksum), value

				if footer == True:
					print "Footer present."
				else:
					print "Footer invalid.", footerbyte
				i = -1
				header = False
				headerbyte = 0
				footer = False
				footerbyte = 0
				checksum = 0
				validsum = False
				value = 0
			i = i + 1
		f.close()
	
	def random_patches(self,path):
		random.seed()
		f = open(path,'wb')
		bank = 0
		while bank < 5:
			f.write(chr(self.patch_header[0]))
			f.write(chr(self.patch_header[1]))
			f.write(chr(self.patch_header[2]))
			f.write(chr(self.patch_header[3]))
			f.write(chr(0))
			f.write(chr(bank))
			z = 0
			checksum = bank
			while z < 64:
				r = random.randint(0,15)
				checksum = (checksum + r) % 128
				f.write(chr(r))
				z = z + 1
			f.write(chr(self.twos_comp_b(checksum)))
			f.write(chr(self.patch_footer))
			bank = bank + 1
		f.close()
			
p = PortaSound()
p.random_patches('random_test.syx')
p.check_binary('random_test.syx')
