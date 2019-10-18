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
				# ToDo: make sure patch values are within the limits
				# document the undocumented values
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
	
	def addrandomchar(self,f,low,high,mult,checksum):
		r = random.randint(low,high) * mult
		checksum = (checksum + r) % 128
		f.write(chr(r))
		return checksum

	def random_patches(self,path):						# A more polite way of randomizing, avoiding most of the unused bits according to the manual 
		random.seed()
		f = open(path,'wb')
		bank = 0
		while bank < 5:
			f.write(chr(self.patch_header[0]))
			f.write(chr(self.patch_header[1]))
			f.write(chr(self.patch_header[2]))
			f.write(chr(self.patch_header[3]))
			f.write(chr(0))
			f.write(chr(bank))					# 0-4, other values are ignored
			checksum = bank
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Modulator fine detune. 4th bit is sign bit
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Modulator Frequency Multiple
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Carrier fine detune. 4th bit is sign bit
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Carrier Frequency Multiple
			checksum = self.addrandomchar(f,0,7,1,checksum) 	# Modulator Total Level, upper 3 bits
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Modulator Total Level, 4 bits
			checksum = self.addrandomchar(f,0,0,1,checksum) 	# Carrier Total Level, upper 3 bits	# It's nice to be able to hear the patches
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Carrier Total Level, 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Modulator Level Key Scaling Hi
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Modulator Level Key Scaling Lo
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Carrier Level Key Scaling Hi
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Carrier Level Key Scaling Lo
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Modulator Level Key Scaling 2 bits, Attack rate upper 2 bits
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Modulator Attack rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Carrier Level Key Scaling 2 bits, Attack rate upper 2 bits
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Carrier Attack rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Modulator Amplitude Modulation Enable 1 bit, Course Detune 1 bit, Decay 1 Rate upper 2bits
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Modulator Decay 1 Rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Carrier Amplitude Modulation Enable 1 bit, Course Detune 1 bit, Decay 1 Rate upper 2bits
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Carrier Decay 1 Rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Modulator Sine Table 2 bits, Decay 2 Rate upper 2 bits
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Modulator Decay 2 Rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Carrier Sine Table 2 bits, Decay 2 Rate upper 2 bits
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Carrier Decay 2 Rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Modulator Decay 1 Level 
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Modulator Release Rate
			checksum = self.addrandomchar(f,0,15,1,checksum) 	# Carrier Decay 1 Level 
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Carrier Release Rate
			checksum = self.addrandomchar(f,0,3,1,checksum) 	# Feedback 2 bits 
			checksum = self.addrandomchar(f,0,1,8,checksum)		# Feedback bit 4 only
			checksum = self.addrandomchar(f,0,7,1,checksum) 	# Pitch Modulation sensitivity 3 bits 
			checksum = self.addrandomchar(f,0,3,1,checksum)		# Amplitude Modulation sensitivity 2 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 	########  09 Here be dragons
			checksum = self.addrandomchar(f,0,15,1,checksum) 	########  0F 
			f.write(chr(0))	
			checksum = self.addrandomchar(f,0,15,1,checksum) 	########  0B
			checksum = self.addrandomchar(f,0,15,1,checksum) 	########  06 	
			checksum = self.addrandomchar(f,0,15,1,checksum) 	########  0E
			checksum = self.addrandomchar(f,0,15,1,checksum) 	########  0F
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Modulator Sustain Release Rate
			checksum = self.addrandomchar(f,0,15,1,checksum) 	########  0F
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Carrier Sustain Release Rate
			checksum = self.addrandomchar(f,0,7,1,checksum) 	# Vibrato Delay Time upper 3 bits 
			checksum = self.addrandomchar(f,0,15,1,checksum)	# Vibrato Delay Time
			f.write(chr(0))	
			checksum = self.addrandomchar(f,0,15,1,checksum) 	########  05
			checksum = self.addrandomchar(f,0,3,4,checksum)		# Vibrato enable 1 bit, sustain enable 1 bit
			z = 0
			while z < 17:
				f.write(chr(0))
				z = z + 1

			f.write(chr(self.twos_comp_b(checksum)))
			f.write(chr(self.patch_footer))
			bank = bank + 1
		f.close()
			
p = PortaSound()
p.random_patches('random_test.syx')
p.check_binary('random_test.syx')
