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

class PortaSound:
	patch_header = [240, 67, 118, 0]
	patch_footer = 247

	def twos_comp_b(self,val):
		return 0b1111111 - val + 1

	def load_patches(self, path):
		if self.check_binary(path) == True:
			patches = []
			f = open(path,'rb')
			i = 0
			patch = {}
			while True:
				byte = f.read(1)
				if not byte:
					break
				v = int.from_bytes(byte, byteorder="little")
				if i == 5:
					patch['bank'] = v
				if i == 6:
					patch['modulator_fine_detune'] = v
				if i == 7:
					patch['modulator_frequency_multiple'] = v
				if i == 8:
					patch['carrier_fine_detune'] = v
				if i == 9:
					patch['carrier_frequency_multiple'] = v
				if i == 10:
					tempv = v << 4
				if i == 11:
					patch['modulator_total_level'] = tempv + v
				if i == 12:
					tempv = v << 4
				if i == 13:
					patch['carrier_total_level'] = tempv + v
				if i == 14:
					patch['modulator_key_scaling_high'] = v
				if i == 15:
					patch['modulator_key_scaling_low'] = v
				if i == 16:
					patch['carrier_key_scaling_high'] = v
				if i == 17:
					patch['carrier_key_scaling_high'] = v
				if i == 18:					
					patch['modulator_level_key_scaling'] = v >> 2
					mask = ~(3 << 2)
					tempv = (v & mask) << 4 
				if i == 19:
					patch['modulator_attack_rate'] = tempv + v
				if i == 20:
					patch['carrier_level key_scaling'] = v >> 2
					mask = ~(3 << 2)
					tempv = (v & mask) << 4
				if i == 21:
					patch['carrier_attack_rate'] = tempv + v					
				if i == 22:
					mask = 1 << 4
					tempv = v | mask
					if tempv > 0:
						patch['modulator_amplitude_modulation_enable'] = True
					else:
						patch['modulator_amplitude_modulation_enable'] = False
					mask = 1 << 3
					tempv = v | mask
					if tempv > 0:
						patch['modulator_coarse_detune_enable'] = True
					else:
						patch['modulator_coarse_detune_enable'] = False
					mask = ~(3 << 2)
					tempv = (v & mask) << 4
				if i == 23:
					patch['modulator_decay_rate_one'] = tempv + v
				if i == 24:
					mask = 1 << 4
					tempv = v | mask
					if tempv > 0:
						patch['carrier_amplitude_modulation_enable'] = True
					else:
						patch['carrier_amplitude_modulation_enable'] = False
					mask = 1 << 3
					tempv = v | mask
					if tempv > 0:
						patch['carrier_coarse_detune_enable'] = True
					else:
						patch['carrier_coarse_detune_enable'] = False
					mask = ~(3 << 2)
					tempv = (v & mask) << 4
				if i == 25:
					patch['carrier_decay_rate_one'] = tempv + v
				if i == 26:
					patch['modulator_sine_table'] = v >> 2
					mask = ~(3 << 2)
					tempv = (v & mask) << 4 
				if i == 27:
					patch['modulator_decay_rate_two'] = tempv + v
				if i == 28:
					patch['carrier_sine_table'] = v >> 2
					mask = ~(3 << 2)
					tempv = (v & mask) << 4 
				if i == 29:
					patch['carrier_decay_rate_two'] = tempv + v
				if i == 30:
					patch['modulator_decay_level_one'] = v
				if i == 31:
					patch['modulator_release_rate'] = v
				if i == 32:
					patch['carrier_decay_level_one'] = v
				if i == 33:
					patch['carrier_release_rate'] = v
				if i == 34:
					tempv = v << 1
				if i == 35:
					patch['feedback'] = tempv + ( v >> 3 )
				if i == 36:
					patch['pitch_modulation_sensitivity'] = v 							
				if i == 37:
					patch['amplitude_modulation_sensitivity'] = v
				if i == 38:
					patch['mystery_byte_one'] = v 							
				if i == 39:
					patch['mystery_byte_two'] = v 							
				if i == 40:
					patch['mystery_byte_three'] = v 							
				if i == 41:
					patch['mystery_byte_four'] = v 							
				if i == 42:
					patch['mystery_byte_five'] = v 							
				if i == 43:
					patch['mystery_byte_six'] = v 							
				if i == 44:
					patch['mystery_byte_seven'] = v 							
				if i == 45:
					patch['modulator_sustain_release_rate'] = v 							
				if i == 46:
					patch['mystery_byte_eight'] = v 							
				if i == 47:
					patch['carrier_sustain_release_rate'] = v 							
				if i == 48:
					tempv = v << 4
				if i == 49:
					patch['vibrato_delay_time'] = tempv + v
				if i == 51: 							
					patch['mystery_byte_nine'] = v 							
				if i == 60:
					mask = 1 << 4
					tempv = v | mask
					if tempv > 0:
						patch['vibrato_enable'] = True
					else:
						patch['vibrato_enable'] = False
					mask = 1 << 3
					tempv = v | mask
					if tempv > 0:
						patch['sustain_enable'] = True
					else:
						patch['sustain_enable'] = False
				if i == 71:
					i = -1
					patches.append(patch)
					patch = {}
				i = i + 1			
			return patches
		else:
			return False

	def check_binary(self,path):
		f = open(path,'rb')
		i = 0
		header = False
		headerbyte = 0
		footer = False
		footerbyte = 0
		checksum = 0
		validsum = False
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
				if self.twos_comp_b(checksum) == v:
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
			i = i + 1
		f.close()
		if allgood == 5: 
			return True
		else:
			return False
	
	def writerandomchar(self,f,low,high,mult,checksum):
		r = random.randint(low,high) * mult
		checksum = (checksum + r) % 128
		f.write((r).to_bytes(1, byteorder="little"))
		return checksum

	def writerandomchar2(self,f,arr,checksum):
		r = random.randint(0,len(arr)-1)
		checksum = (checksum + arr[r]) % 128
		f.write((arr[r]).to_bytes(1, byteorder="little"))
		return checksum

	def writepatchchar(self,f,i,checksum):
		checksum = (checksum + i) % 128
		f.write((i).to_bytes(1, byteorder="little"))
		return checksum

	def random_patches(self,path): 
		random.seed()
		f = open(path,'wb')
		bank = 0
		while bank < 5:
			for i in self.patch_header:
				f.write((i).to_bytes(1, byteorder="little"))	
			f.write((0).to_bytes(1, byteorder="little"))			# can be other than zero, but is ignored
			f.write((bank).to_bytes(1, byteorder="little"))			# 0-4, other values are ignored
			checksum = bank
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Modulator fine detune. 4th bit is sign bit
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Modulator Frequency Multiple
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Carrier fine detune. 4th bit is sign bit
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Carrier Frequency Multiple
			checksum = self.writerandomchar(f,0,7,1,checksum) 		# Modulator Total Level, upper 3 bits
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Modulator Total Level, 4 bits
			checksum = self.writerandomchar(f,0,1,1,checksum) 		# Carrier Total Level, upper 3 bits - it's nice to be able to hear the patches
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Carrier Total Level, 4 bits
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Modulator Level Key Scaling Hi
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Modulator Level Key Scaling Lo
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Carrier Level Key Scaling Hi
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Carrier Level Key Scaling Lo
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Modulator Level Key Scaling 2 bits, Attack rate upper 2 bits
			checksum = self.writerandomchar(f,1,15,1,checksum)		# Modulator Attack rate 4 bits
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Carrier Level Key Scaling 2 bits, Attack rate upper 2 bits
			checksum = self.writerandomchar(f,1,15,1,checksum)		# Carrier Attack rate 4 bits
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Modulator Amplitude Modulation Enable 1 bit, Course Detune 1 bit, Decay 1 Rate upper 2bits
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Modulator Decay 1 Rate 4 bits
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Carrier Amplitude Modulation Enable 1 bit, Course Detune 1 bit, Decay 1 Rate upper 2bits
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Carrier Decay 1 Rate 4 bits
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Modulator Sine Table 2 bits, Decay 2 Rate upper 2 bits
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Modulator Decay 2 Rate 4 bits
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Carrier Sine Table 2 bits, Decay 2 Rate upper 2 bits
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Carrier Decay 2 Rate 4 bits
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Modulator Decay 1 Level 
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Modulator Release Rate
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Carrier Decay 1 Level 
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Carrier Release Rate
			checksum = self.writerandomchar(f,0,3,1,checksum) 		# Feedback 2 bits 
			checksum = self.writerandomchar(f,0,1,8,checksum)		# Feedback bit 4 only
			checksum = self.writerandomchar(f,0,7,1,checksum) 		# Pitch Modulation sensitivity 3 bits 
			checksum = self.writerandomchar(f,0,3,1,checksum)		# Amplitude Modulation sensitivity 2 bits
			checksum = self.writerandomchar(f,9,10,1,checksum)		# 09 0A Here be dragons - these chr appear in patches, but are not in the manual
			checksum = self.writerandomchar(f,14,15,1,checksum)		# 0E 0F 
			checksum = self.writerandomchar(f,0,1,1,checksum)		# 00 01
			checksum = self.writerandomchar2(f,[0,7,11],checksum) 		# 00 07 0B
			checksum = self.writerandomchar2(f,[2,6,14],checksum) 		# 02 06 0E	
			checksum = self.writerandomchar(f,13,15,1,checksum) 		# 0D 0E 0F
			checksum = self.writerandomchar2(f,[0,4,5,6,15],checksum) 	# 00 04 05 06 0F
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Modulator Sustain Release Rate
			checksum = self.writerandomchar2(f,[5,6,7,9,15],checksum) 	# 05 06 07 09 0F
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Carrier Sustain Release Rate
			checksum = self.writerandomchar(f,0,7,1,checksum) 		# Vibrato Delay Time upper 3 bits 
			checksum = self.writerandomchar(f,0,15,1,checksum)		# Vibrato Delay Time
			f.write((0).to_bytes(1, byteorder="little"))			# This appears to always be zero
			checksum = self.writerandomchar2(f,[0,1,3,4,5,7,8,11],checksum) # 00 01 03 04 05 07 08 0B
			checksum = self.writerandomchar(f,0,3,4,checksum)		# Vibrato enable 1 bit, sustain enable 1 bit
			f.write((0).to_bytes(17, byteorder="little"))			# none of the patches have anything but zeros here
			f.write((self.twos_comp_b(checksum)).to_bytes(1, byteorder="little"))
			f.write((self.patch_footer).to_bytes(1, byteorder="little"))
			bank = bank + 1
		f.close()

	def write_patches(self, patches, path):
		f = open(path,'wb')
		for patch in patches:
			for i in self.patch_header:
				f.write((i).to_bytes(1, byteorder="little"))	
			f.write((0).to_bytes(1, byteorder="little"))			
			f.write((patch['bank']).to_bytes(1, byteorder="little"))	
			checksum = patch['bank']
			checksum = self.writepatchchar(f,patch['modulator_fine_detune'],checksum)
			checksum = self.writepatchchar(f,patch['modulator_frequency_multiple'],checksum)
			checksum = self.writepatchchar(f,patch['carrier_fine_detune'],checksum)
			checksum = self.writepatchchar(f,patch['carrier_frequency_multiple'],checksum)
			v = patch['modulator_total_level'] >> 4
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(7 << 4)
			v = patch['modulator_total_level'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			v = patch['carrier_total_level'] >> 4
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(7 << 4)
			v = patch['carrier_total_level'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			checksum = self.writepatchchar(f,patch['modulator_level_key_scaling_high'],checksum)
			checksum = self.writepatchchar(f,patch['modulator_level_key_scaling_low'],checksum)
			checksum = self.writepatchchar(f,patch['carrier_level_key_scaling_high'],checksum)
			checksum = self.writepatchchar(f,patch['carrier_level_key_scaling_low'],checksum)
			v = (patch['modulator_level_key_scaling'] << 2) + (patch['modulator_attack_rate'] >> 4)
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 4)
			v = patch['modulator_attack_rate'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			v = (patch['carrier_level_key_scaling'] << 2) + (patch['carrier_attack_rate'] >> 4)
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 4)
			v = patch['carrier_attack_rate'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			v = patch['modulator_decay_rate_one'] >> 4
			mask = 1 << 4
			if patch['modulator_amplitude_modulation_enable'] == True:
				v = v | mask
			mask = 1 << 3
			if patch['modulator_course_detune_enable'] == True:
				v = v | mask
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 4)
			v = patch['modulator_decay_rate_one'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			v = patch['carrier_decay_rate_one'] >> 4
			mask = 1 << 4
			if patch['carrier_amplitude_modulation_enable'] == True:
				v = v | mask
			mask = 1 << 3
			if patch['carrier_course_detune_enable'] == True:
				v = v | mask
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 4)
			v = patch['carrier_decay_rate_one'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			v = (patch['modulator_sine_table'] << 2) + (patch['modulator_decay_rate_two'] >> 4)
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 4)
			v = patch['modulator_decay_rate_two'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			v = (patch['carrier_sine_table'] << 2) + (patch['carrier_decay_rate_two'] >> 4)
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 4)
			v = patch['carrier_decay_rate_two'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			checksum = self.writepatchchar(f,patch['modulator_decay_level_one'],checksum)
			checksum = self.writepatchchar(f,patch['modulator_release_rate'],checksum)
			checksum = self.writepatchchar(f,patch['carrier_decay_level_one'],checksum)
			checksum = self.writepatchchar(f,patch['carrier_release_rate'],checksum)
			v = patch['feedback'] >> 1
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 1)
			v = (patch['feedback'] & mask) << 3
			checksum = self.writepatchchar(f,v,checksum)
			checksum = self.writepatchchar(f,patch['pitch_modulation_sensitivity'],checksum)
			checksum = self.writepatchchar(f,patch['amplitude_modulation_sensitivity'],checksum)
			checksum = self.writepatchchar(f,patch['mystery_byte_one'],checksum)
			checksum = self.writepatchchar(f,patch['mystery_byte_two'],checksum)
			checksum = self.writepatchchar(f,patch['mystery_byte_three'],checksum)
			checksum = self.writepatchchar(f,patch['mystery_byte_four'],checksum)
			checksum = self.writepatchchar(f,patch['mystery_byte_five'],checksum)
			checksum = self.writepatchchar(f,patch['mystery_byte_six'],checksum)
			checksum = self.writepatchchar(f,patch['mystery_byte_seven'],checksum)
			checksum = self.writepatchchar(f,patch['modulator_sustain_release_rate'],checksum)
			checksum = self.writepatchchar(f,patch['mystery_byte_eight'],checksum) 
			checksum = self.writepatchchar(f,patch['carrier_sustain_release_rate'],checksum)
			v = patch['vibrato_delay_time'] >> 4
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 4)
			v = patch['vibrato_delay_time'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			f.write((0).to_bytes(1, byteorder="little"))
			checksum = self.writepatchchar(f,patch['mystery_byte_nine'],checksum) 
			v = 0
			mask = 1 << 4
			if patch['vibrato_enable'] == True:
				v = v | mask
			mask = 1 << 3
			if patch['sustain_enable'] == True:
				v = v | mask
			checksum = self.writepatchchar(f,v,checksum)
			f.write((0).to_bytes(17, byteorder="little"))			
			f.write((self.twos_comp_b(checksum)).to_bytes(1, byteorder="little"))
			f.write((self.patch_footer).to_bytes(1, byteorder="little"))
		f.close()
			
p = PortaSound()
app = QApplication([])
if len(sys.argv) != 2:
	print("Usage: ", str(sys.argv[0]), "[filename]")
	exit()
p.random_patches(sys.argv[1])
if p.check_binary(sys.argv[1]) == True:
	label = "5 random patches saved to: " + str(sys.argv[1])
	patches = p.load_patches(sys.argv[1])
else:
	label = "Something went wrong with the patch generation." 
thelabel = QLabel(label)
thelabel.show()
app.exec_()
print(str(patches))

