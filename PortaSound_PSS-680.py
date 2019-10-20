#!/usr/bin/env python
from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2.QtCore import QDateTime, Qt, QTimer
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

import random 
import sys
# from PySide2.QtWidgets import QApplication, QLabel, QComboBox, QCheckBox, QRadioButton, QPushButton, QSlider

class PortaSound:
	patch_header = [248, 67, 118, 0]
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
		allgood = 0
		while True:
			byte = f.read(1)
			if not byte:
				break
			#byte = byte_s[0]
			v = int.from_bytes(byte, byteorder="little")
			if i == 0: 
				if v != self.patch_header[0]:
					header = False
				else:
					header = True
			if i == 1 and v != self.patch_header[1]:
				header = False
			if i == 2 and v != self.patch_header[2]:
				header = False
			if i == 3 and v != self.patch_header[3]:
				header = False
			if i > 3 and i < 70:
				checksum = (checksum + v) % 128
				# ToDo: make sure patch values are within the limits
				# document the undocumented values
			if i == 70:
				value = v
				if self.twos_comp_b(checksum) == value:
					validsum = True
			if i == 71:
				if v == self.patch_footer:
					footer = True
				if header == True and validsum == True and footer == True:
					allgood = allgood + 1
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
		if allgood == 5: 
			return True
		else:
			return False
	
	def addrandomchar(self,f,low,high,mult,checksum):
		r = random.randint(low,high) * mult
		checksum = (checksum + r) % 128
		f.write((r).to_bytes(1, byteorder="little"))
		return checksum

	def addrandomchar2(self,f,arr,checksum):
		r = random.randint(0,len(arr)-1)
		checksum = (checksum + arr[r]) % 128
		f.write((arr[r]).to_bytes(1, byteorder="little"))
		return checksum

	def random_patches(self,path): 
		random.seed()
		f = open(path,'wb')
		bank = 0
		while bank < 5:
			f.write((self.patch_header[0]).to_bytes(1, byteorder="little"))	# 248, 67, 118, 0
			f.write((self.patch_header[1]).to_bytes(1, byteorder="little"))
			f.write((self.patch_header[2]).to_bytes(1, byteorder="little"))
			f.write((self.patch_header[3]).to_bytes(1, byteorder="little"))
			f.write((0).to_bytes(1, byteorder="little"))					# can be other than zero, but is ignored
			f.write((bank).to_bytes(1, byteorder="little"))						# 0-4, other values are ignored
			checksum = bank
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Modulator fine detune. 4th bit is sign bit
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Modulator Frequency Multiple
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Carrier fine detune. 4th bit is sign bit
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Carrier Frequency Multiple
			checksum = self.addrandomchar(f,0,7,1,checksum) 		# Modulator Total Level, upper 3 bits
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Modulator Total Level, 4 bits
			checksum = self.addrandomchar(f,0,1,1,checksum) 		# Carrier Total Level, upper 3 bits - it's nice to be able to hear the patches
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Carrier Total Level, 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Modulator Level Key Scaling Hi
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Modulator Level Key Scaling Lo
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Carrier Level Key Scaling Hi
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Carrier Level Key Scaling Lo
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Modulator Level Key Scaling 2 bits, Attack rate upper 2 bits
			checksum = self.addrandomchar(f,1,15,1,checksum)		# Modulator Attack rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Carrier Level Key Scaling 2 bits, Attack rate upper 2 bits
			checksum = self.addrandomchar(f,1,15,1,checksum)		# Carrier Attack rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Modulator Amplitude Modulation Enable 1 bit, Course Detune 1 bit, Decay 1 Rate upper 2bits
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Modulator Decay 1 Rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Carrier Amplitude Modulation Enable 1 bit, Course Detune 1 bit, Decay 1 Rate upper 2bits
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Carrier Decay 1 Rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Modulator Sine Table 2 bits, Decay 2 Rate upper 2 bits
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Modulator Decay 2 Rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Carrier Sine Table 2 bits, Decay 2 Rate upper 2 bits
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Carrier Decay 2 Rate 4 bits
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Modulator Decay 1 Level 
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Modulator Release Rate
			checksum = self.addrandomchar(f,0,15,1,checksum) 		# Carrier Decay 1 Level 
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Carrier Release Rate
			checksum = self.addrandomchar(f,0,3,1,checksum) 		# Feedback 2 bits 
			checksum = self.addrandomchar(f,0,1,8,checksum)			# Feedback bit 4 only
			checksum = self.addrandomchar(f,0,7,1,checksum) 		# Pitch Modulation sensitivity 3 bits 
			checksum = self.addrandomchar(f,0,3,1,checksum)			# Amplitude Modulation sensitivity 2 bits
			checksum = self.addrandomchar(f,9,10,1,checksum)		# 09 0A Here be dragons - these chr appear in patches, but are not in the manual
			checksum = self.addrandomchar(f,14,15,1,checksum)		# 0E 0F 
			checksum = self.addrandomchar(f,0,1,1,checksum)			# 00 01
			checksum = self.addrandomchar2(f,[0,7,11],checksum) 		# 00 07 0B
			checksum = self.addrandomchar2(f,[2,6,14],checksum) 		# 02 06 0E	
			checksum = self.addrandomchar(f,13,15,1,checksum) 		# 0D 0E 0F
			checksum = self.addrandomchar2(f,[0,4,5,6,15],checksum) 	# 00 04 05 06 0F
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Modulator Sustain Release Rate
			checksum = self.addrandomchar2(f,[5,6,7,9,15],checksum) 	# 05 06 07 09 0F
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Carrier Sustain Release Rate
			checksum = self.addrandomchar(f,0,7,1,checksum) 		# Vibrato Delay Time upper 3 bits 
			checksum = self.addrandomchar(f,0,15,1,checksum)		# Vibrato Delay Time
			f.write((0).to_bytes(1, byteorder="little"))					# This appears to always be zero
			checksum = self.addrandomchar2(f,[0,1,3,4,5,7,8,11],checksum) 	# 00 01 03 04 05 07 08 0B
			checksum = self.addrandomchar(f,0,3,4,checksum)			# Vibrato enable 1 bit, sustain enable 1 bit
			z = 0
			while z < 17:
				f.write((0).to_bytes(1, byteorder="little"))					# none of the patches have anything but zeros here
				z = z + 1
			f.write((self.twos_comp_b(checksum)).to_bytes(1, byteorder="little"))
			f.write((self.patch_footer).to_bytes(1, byteorder="little"))
			bank = bank + 1
		f.close()
			
p = PortaSound()
app = QApplication([])
if len(sys.argv) != 2:
	print("Usage: ", str(sys.argv[0]), "[filename]")
	exit()
p.random_patches(sys.argv[1])
if p.check_binary(sys.argv[1]) == True:
	label = "5 random patches saved to: " + str(sys.argv[1])
else:
	label = "Something went wrong with the patch generation." 
thelabel = QLabel(label)
thelabel.show()
app.exec_()

