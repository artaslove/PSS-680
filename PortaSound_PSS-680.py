#!/usr/bin/env python
from PySide2.QtCore import QDateTime, Qt, QTimer
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QFileDialog)

import random
from time import sleep
import sys, os
import hashlib
import subprocess
#import jack

class PortaSound(QDialog):
	patch_header = [240, 67, 118, 0]
	patch_footer = 247
	detune = [15,14,13,12,11,10,9,8,0,1,2,3,4,5,6,7]
	lks_hi = [15,14,13,12,11,10,9,8,7,6,5,4,0,3,2,1]
	lks_lo = [15,14,13,12,11,10,9,8,0,7,6,5,4,3,2,1]
	mbytes1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	mbytes2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	mbytes3 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	mbytes4 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	mbytes5 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	mbytes6 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	mbytes7 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	mbytes8 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	mbytes9 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
#	mbytes1 = [9,10]
#	mbytes2 = [14,15]
#	mbytes3 = [0,1]
#	mbytes4 = [0,7,11]
#	mbytes5 = [2,6,14]
#	mbytes6 = [13,14,15]
#	mbytes7 = [0,4,5,6,15]
#	mbytes8 = [5,6,7,9,15]
#	mbytes9 = [0,1,3,4,5,7,8,11]

	tmp_filename = "/tmp/temp.syx"
	note_length = 1000 # milliseconds

	def twos_comp_b(self,val):
		return 0b1111111 - val + 1

	def load_patches(self, num, filename):
		if self.check_binary(filename) > 0:
			if num == 5:
				self.patches = []
			f = open(filename,'rb')
			i = 0
			z = 0
			patch = {}
			while True:
				byte = f.read(1)
				if not byte:
					break
				v = int.from_bytes(byte, byteorder="little")
				if i == 5:
					if num == 5:
						patch['bank'] = v
					else:
						patch['bank'] = self.bankComboBox.currentIndex()
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
					patch['modulator_level_key_scaling_high'] = v
				if i == 15:
					patch['modulator_level_key_scaling_low'] = v
				if i == 16:
					patch['carrier_level_key_scaling_high'] = v
				if i == 17:
					patch['carrier_level_key_scaling_low'] = v
				if i == 18:					
					patch['modulator_rate_key_scaling'] = v >> 2
					mask = ~(3 << 2)
					tempv = (v & mask) << 4 
				if i == 19:
					patch['modulator_attack_rate'] = tempv + v
				if i == 20:
					patch['carrier_rate_key_scaling'] = v >> 2
					mask = ~(3 << 2)
					tempv = (v & mask) << 4
				if i == 21:
					patch['carrier_attack_rate'] = tempv + v					
				if i == 22:
					mask = 1 << 3
					tempv = v & mask
					if tempv > 0:
						patch['modulator_amplitude_modulation'] = True
					else:
						patch['modulator_amplitude_modulation'] = False
					mask = 1 << 2
					tempv = v & mask
					if tempv > 0:
						patch['modulator_coarse_detune'] = True
					else:
						patch['modulator_coarse_detune'] = False
					mask = ~(3 << 2)
					tempv = (v & mask) << 4
				if i == 23:
					patch['modulator_decay_rate_1'] = tempv + v
				if i == 24:
					mask = 1 << 3
					tempv = v & mask
					if tempv > 0:
						patch['carrier_amplitude_modulation'] = True
					else:
						patch['carrier_amplitude_modulation'] = False
					mask = 1 << 2
					tempv = v & mask
					if tempv > 0:
						patch['carrier_coarse_detune'] = True
					else:
						patch['carrier_coarse_detune'] = False
					mask = ~(3 << 2)
					tempv = (v & mask) << 4
				if i == 25:
					patch['carrier_decay_rate_1'] = tempv + v
				if i == 26:
					patch['modulator_sine_table'] = v >> 2
					mask = ~(3 << 2)
					tempv = (v & mask) << 4 
				if i == 27:
					patch['modulator_decay_rate_2'] = tempv + v
				if i == 28:
					patch['carrier_sine_table'] = v >> 2
					mask = ~(3 << 2)
					tempv = (v & mask) << 4 
				if i == 29:
					patch['carrier_decay_rate_2'] = tempv + v
				if i == 30:
					patch['modulator_decay_level'] = v
				if i == 31:
					patch['modulator_release_rate'] = v
				if i == 32:
					patch['carrier_decay_level'] = v
				if i == 33:
					patch['carrier_release_rate'] = v
				if i == 34:
					mask = 1 << 2
					tempv = v & mask
					if tempv > 0:
						patch['mystery_bit_1'] = True
						v = v - 4
					else:
						patch['mystery_bit_1'] = False
					tempv = v << 1
				if i == 35:
					patch['feedback'] = tempv + ( v >> 3 )
				if i == 36:
					patch['pitch_modulation_sensitivity'] = v 							
				if i == 37:
					mask = 1 << 3
					tempv = v & mask
					if tempv > 0:
						patch['mystery_bit_2'] = True
						v = v - 8
					else:
						patch['mystery_bit_2'] = False
					patch['amplitude_modulation_sensitivity'] = v
				if i == 38:
					patch['mystery_byte_1'] = v 							
				if i == 39:
					patch['mystery_byte_2'] = v 							
				if i == 40:
					patch['mystery_byte_3'] = v 							
				if i == 41:
					patch['mystery_byte_4'] = v 							
				if i == 42:
					patch['mystery_byte_5'] = v 							
				if i == 43:
					patch['mystery_byte_6'] = v 							
				if i == 44:
					patch['mystery_byte_7'] = v 							
				if i == 45:
					patch['modulator_sustain_release_rate'] = v 							
				if i == 46:
					patch['mystery_byte_8'] = v 							
				if i == 47:
					patch['carrier_sustain_release_rate'] = v 							
				if i == 48:
					tempv = v << 4
				if i == 49:
					patch['vibrato_delay_time'] = tempv + v
				if i == 51: 							
					patch['mystery_byte_9'] = v 							
				if i == 52:
					mask = 1 << 3
					tempv = v & mask
					if tempv > 0:
						patch['vibrato_enable'] = True
					else:
						patch['vibrato_enable'] = False
					mask = 1 << 2
					tempv = v & mask
					if tempv > 0:
						patch['sustain_enable'] = True
					else:
						patch['sustain_enable'] = False
				if i == 71:
					i = -1
					if num == 5:
						self.patches.append(patch)
					if num == 1:
						self.patches[patch['bank']] = patch
						break
					z = z + 1
					patch = {}
				i = i + 1
			f.close()
			self.changeBank()
			return True
		else:
			f.close()
			print("That doesn't appear to be a valid file. Check for extra bytes in front of the system excusive dump. A future version may do this for you.")
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
		return allgood
	
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
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Modulator Rate Key Scaling 2 bits, Attack rate upper 2 bits
			checksum = self.writerandomchar(f,1,15,1,checksum)		# Modulator Attack rate 4 bits
			checksum = self.writerandomchar(f,0,15,1,checksum) 		# Carrier Rate Key Scaling 2 bits, Attack rate upper 2 bits
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
			checksum = self.writerandomchar(f,0,7,1,checksum) 		# Feedback 2 bits and an unknown mystery bit at 3 
			checksum = self.writerandomchar(f,0,1,8,checksum)		# Feedback bit 4 only
			checksum = self.writerandomchar(f,0,7,1,checksum) 		# Pitch Modulation sensitivity 3 bits 
			checksum = self.writerandomchar2(f,[0,1,2,3,8,9,10,11],checksum) # Amplitude Modulation sensitivity 2 bits and an unknown bit at 4
			checksum = self.writerandomchar(f,9,10,1,checksum)		# 09 0A Here be dragons - these appear in patches, but are not in the manual
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
			self.write_patch(f,patch)
		f.close()

	def write_and_send_patch(self,patch,path):
		f = open(path,'wb')
		self.write_patch(f,patch)
		bank = patch['bank'] + 100
		f.write(int(192 + self.midi_channel).to_bytes(1,byteorder="little"))
		f.write(bank.to_bytes(1, byteorder="little"))
		f.write(int(144 + self.midi_channel).to_bytes(1,byteorder="little"))
		f.write(int(self.midi_note).to_bytes(1, byteorder="little"))
		f.write(int(127).to_bytes(1, byteorder="little"))
		f.close()
		self.try_to_send_file(path)

	def try_to_send_file(self,path):
		if self.sending == False and self.ready == True:
			self.sending = True
			self.send_to_amidi(self.midi_device,path)
			timer = QTimer(self)
			timer.singleShot(self.note_length, lambda: self.note_off(self.midi_device,self.midi_note,self.midi_channel))
			timer.start()

	def note_off(self,device,note,channel):
		path = "/tmp/note_off.syx"
		f = open(path,'wb')
		f.write(int(127 + channel).to_bytes(1, byteorder="little"))
		f.write(int(note).to_bytes(1, byteorder="little"))
		f.write(int(127).to_bytes(1, byteorder="little"))
		f.close()
		while self.sending == True or self.ready == False:
			sleep(0.05)
		self.sending = True
		self.send_to_amidi(device,path)

	def send_to_amidi(self,midi_device,path):
		subprocess.call(["amidi","-p",self.midi_device,"-s",path])
		sleep(0.05)	
		self.sending = False

	def write_patch(self, f, patch):
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
		v = (patch['modulator_rate_key_scaling'] << 2) + (patch['modulator_attack_rate'] >> 4)
		checksum = self.writepatchchar(f,v,checksum)
		mask = ~(3 << 4)
		v = patch['modulator_attack_rate'] & mask
		checksum = self.writepatchchar(f,v,checksum)
		v = (patch['carrier_rate_key_scaling'] << 2) + (patch['carrier_attack_rate'] >> 4)
		checksum = self.writepatchchar(f,v,checksum)
		mask = ~(3 << 4)
		v = patch['carrier_attack_rate'] & mask
		checksum = self.writepatchchar(f,v,checksum)
		v = patch['modulator_decay_rate_1'] >> 4
		mask = 1 << 3
		if patch['modulator_amplitude_modulation'] == True:
			v = v | mask
		mask = 1 << 2
		if patch['modulator_coarse_detune'] == True:
			v = v | mask
		checksum = self.writepatchchar(f,v,checksum)
		mask = ~(3 << 4)
		v = patch['modulator_decay_rate_1'] & mask
		checksum = self.writepatchchar(f,v,checksum)
		v = patch['carrier_decay_rate_1'] >> 4
		mask = 1 << 3
		if patch['carrier_amplitude_modulation'] == True:
			v = v | mask
		mask = 1 << 2
		if patch['carrier_coarse_detune'] == True:
			v = v | mask
		checksum = self.writepatchchar(f,v,checksum)
		mask = ~(3 << 4)
		v = patch['carrier_decay_rate_1'] & mask
		checksum = self.writepatchchar(f,v,checksum)
		v = (patch['modulator_sine_table'] << 2) + (patch['modulator_decay_rate_2'] >> 4)
		checksum = self.writepatchchar(f,v,checksum)
		mask = ~(3 << 4)
		v = patch['modulator_decay_rate_2'] & mask
		checksum = self.writepatchchar(f,v,checksum)
		v = (patch['carrier_sine_table'] << 2) + (patch['carrier_decay_rate_2'] >> 4)
		checksum = self.writepatchchar(f,v,checksum)
		mask = ~(3 << 4)
		v = patch['carrier_decay_rate_2'] & mask
		checksum = self.writepatchchar(f,v,checksum)
		checksum = self.writepatchchar(f,patch['modulator_decay_level'],checksum)
		checksum = self.writepatchchar(f,patch['modulator_release_rate'],checksum)
		checksum = self.writepatchchar(f,patch['carrier_decay_level'],checksum)
		checksum = self.writepatchchar(f,patch['carrier_release_rate'],checksum)
		if patch['mystery_bit_1'] == True:
			v = (patch['feedback'] >> 1) + 4
		else:
			v = patch['feedback'] >> 1
		checksum = self.writepatchchar(f,v,checksum)
		mask = ~(3 << 1)
		v = (patch['feedback'] & mask) << 3
		checksum = self.writepatchchar(f,v,checksum)
		checksum = self.writepatchchar(f,patch['pitch_modulation_sensitivity'],checksum)
		if patch['mystery_bit_2'] == True:
			v = patch['amplitude_modulation_sensitivity'] + 8
		else: 
			v = patch['amplitude_modulation_sensitivity']
		checksum = self.writepatchchar(f,v,checksum)
		checksum = self.writepatchchar(f,patch['mystery_byte_1'],checksum)
		checksum = self.writepatchchar(f,patch['mystery_byte_2'],checksum)
		checksum = self.writepatchchar(f,patch['mystery_byte_3'],checksum)
		checksum = self.writepatchchar(f,patch['mystery_byte_4'],checksum)
		checksum = self.writepatchchar(f,patch['mystery_byte_5'],checksum)
		checksum = self.writepatchchar(f,patch['mystery_byte_6'],checksum)
		checksum = self.writepatchchar(f,patch['mystery_byte_7'],checksum)
		checksum = self.writepatchchar(f,patch['modulator_sustain_release_rate'],checksum)
		checksum = self.writepatchchar(f,patch['mystery_byte_8'],checksum) 
		checksum = self.writepatchchar(f,patch['carrier_sustain_release_rate'],checksum)
		v = patch['vibrato_delay_time'] >> 4
		checksum = self.writepatchchar(f,v,checksum)
		mask = ~(7 << 4)
		v = patch['vibrato_delay_time'] & mask
		checksum = self.writepatchchar(f,v,checksum)
		f.write((0).to_bytes(1, byteorder="little"))
		checksum = self.writepatchchar(f,patch['mystery_byte_9'],checksum) 
		v = 0
		mask = 1 << 3
		if patch['vibrato_enable'] == True:
			v = v | mask
		mask = 1 << 2
		if patch['sustain_enable'] == True:
			v = v | mask
		checksum = self.writepatchchar(f,v,checksum)
		f.write((0).to_bytes(17, byteorder="little"))			
		f.write((self.twos_comp_b(checksum)).to_bytes(1, byteorder="little"))
		f.write((self.patch_footer).to_bytes(1, byteorder="little"))

	def test_routine(self):
		rfile1="/tmp/random_test1.syx"
		rfile2="/tmp/random_test2.syx"
		self.random_patches(rfile1)
		if self.check_binary(rfile1) == 5:
			if self.load_patches(5,rfile1) == True:
				self.write_patches(self.patches,rfile2)
				rfile = open(rfile1,'rb')
				data = rfile.read()
				rfilemd5 = hashlib.md5()
				rfilemd5.update(data)
				pfile = open(rfile2,'rb')
				data = pfile.read()
				pfilemd5 = hashlib.md5()
				pfilemd5.update(data)
				if rfilemd5.digest() != pfilemd5.digest():
					print("Something is not right!")
				else:
					print("That worked.")
		else:
			 print("Something went wrong with the patch generation.")

	def __init__(self, parent=None):
		super(PortaSound, self).__init__(parent)
		#self.connection = jack.Client('PSS-680 Editor')
		#self.inport = self.connection.midi_inports.register('midi_in')
		#self.outport = self.connection.midi_outports.register('midi_out')
		self.midi_devices = {}
		amidi_hw = subprocess.check_output(["amidi","-l"]).decode('utf-8').split('\n')
		for hw in amidi_hw:
			hw_split = hw.split('  ')
			if len(hw_split) > 1:
				if hw_split[0][0] != 'D':
					self.midi_devices[hw_split[2]] = hw_split[1]
		self.sending = False

		#### Carrier
		self.carrierBox = QGroupBox("Carrier")

		self.cstComboBox = QComboBox()
		self.cstComboBox.addItems(["Sine","Squared Sine","Half Sine","Squared Half Sine"])
		cstLabel = QLabel("Waveform:")
		cstLabel.setBuddy(self.cstComboBox)
		self.cstComboBox.activated[str].connect(self.changeCST)

		self.ccdetune = QCheckBox("Coarse Detune")
		self.ccdetune.toggled.connect(self.changeCCDetune)

		self.cfdetuneSlider = QSlider(Qt.Horizontal)
		self.cfdetuneSlider.setMinimum(0)
		self.cfdetuneSlider.setMaximum(15)
		self.cfdetuneSlider.setTickPosition(QSlider.TicksBelow)
		self.cfdetuneSlider.setTickInterval(8)
		cfdetuneLabel = QLabel("Fine Detune:")
		cfdetuneLabel.setBuddy(self.cfdetuneSlider)		
		self.cfdetuneSlider.valueChanged.connect(self.changeCFDetune)

		self.cfmultSlider = QSlider(Qt.Horizontal)
		self.cfmultSlider.setMinimum(0)
		self.cfmultSlider.setMaximum(15)
		cfmultLabel = QLabel("Frequency Muliplier:")
		cfmultLabel.setBuddy(self.cfmultSlider)		
		self.cfmultSlider.valueChanged.connect(self.changeCFMult)

		self.campmod = QCheckBox("Amplitude Modulation")
		self.campmod.toggled.connect(self.changeCAmpMod)

		self.ctlevelSlider = QSlider(Qt.Horizontal)
		self.ctlevelSlider.setMinimum(0)
		self.ctlevelSlider.setMaximum(99)
		self.ctlevelSlider.setInvertedAppearance(True)
		ctlevelLabel = QLabel("Total Level:")
		ctlevelLabel.setBuddy(self.ctlevelSlider)		
		self.ctlevelSlider.valueChanged.connect(self.changeCTLevel)

		self.carateSlider = QSlider(Qt.Horizontal)
		self.carateSlider.setMinimum(0)
		self.carateSlider.setMaximum(63)
		carateLabel = QLabel("Attack Rate:")
		carateLabel.setBuddy(self.carateSlider)		
		self.carateSlider.valueChanged.connect(self.changeCARate)

		self.cdrate1Slider = QSlider(Qt.Horizontal)
		self.cdrate1Slider.setMinimum(0)
		self.cdrate1Slider.setMaximum(63)
		cdrate1Label = QLabel("Decay Rate One:")
		cdrate1Label.setBuddy(self.cdrate1Slider)		
		self.cdrate1Slider.valueChanged.connect(self.changeCDRate1)

		self.cdlevelSlider = QSlider(Qt.Horizontal)
		self.cdlevelSlider.setMinimum(0)
		self.cdlevelSlider.setMaximum(15)
		self.cdlevelSlider.setInvertedAppearance(True)
		cdlevelLabel = QLabel("Decay Level:")
		cdlevelLabel.setBuddy(self.cdlevelSlider)		
		self.cdlevelSlider.valueChanged.connect(self.changeCDLevel)

		self.cdrate2Slider = QSlider(Qt.Horizontal)
		self.cdrate2Slider.setMinimum(0)
		self.cdrate2Slider.setMaximum(63)
		cdrate2Label = QLabel("Decay Rate Two:")
		cdrate2Label.setBuddy(self.cdrate2Slider)		
		self.cdrate2Slider.valueChanged.connect(self.changeCDRate2)

		self.crrateSlider = QSlider(Qt.Horizontal)
		self.crrateSlider.setMinimum(0)
		self.crrateSlider.setMaximum(15)
		crrateLabel = QLabel("Release Rate:")
		crrateLabel.setBuddy(self.crrateSlider)		
		self.crrateSlider.valueChanged.connect(self.changeCRRate)

		self.csrrateSlider = QSlider(Qt.Horizontal)
		self.csrrateSlider.setMinimum(0)
		self.csrrateSlider.setMaximum(15)
		csrrateLabel = QLabel("Sustain Release Rate:")
		csrrateLabel.setBuddy(self.csrrateSlider)		
		self.csrrateSlider.valueChanged.connect(self.changeCSRRate)

		self.crateksSlider = QSlider(Qt.Horizontal)
		self.crateksSlider.setMinimum(0)
		self.crateksSlider.setMaximum(3)
		crateksLabel = QLabel("Rate Key Scaling:")
		crateksLabel.setBuddy(self.crateksSlider)		
		self.crateksSlider.valueChanged.connect(self.changeCRateKS)

		self.clevelkshSlider = QSlider(Qt.Horizontal)
		self.clevelkshSlider.setMinimum(0)
		self.clevelkshSlider.setMaximum(15)
		clevelkshLabel = QLabel("Level Key Scaling High:")
		clevelkshLabel.setBuddy(self.clevelkshSlider)		
		self.clevelkshSlider.valueChanged.connect(self.changeCLevelKSH)

		self.clevelkslSlider = QSlider(Qt.Horizontal)
		self.clevelkslSlider.setMinimum(0)
		self.clevelkslSlider.setMaximum(15)
		clevelkslLabel = QLabel("Level Key Scaling Low:")
		clevelkslLabel.setBuddy(self.clevelkslSlider)		
		self.clevelkslSlider.valueChanged.connect(self.changeCLevelKSL)

		carrierboxlayout = QVBoxLayout()
		carrierboxlayout.addWidget(cstLabel)
		carrierboxlayout.addWidget(self.cstComboBox)
		carrierboxlayout.addWidget(self.ccdetune)
		carrierboxlayout.addWidget(cfdetuneLabel)
		carrierboxlayout.addWidget(self.cfdetuneSlider)
		carrierboxlayout.addWidget(cfmultLabel)
		carrierboxlayout.addWidget(self.cfmultSlider)
		carrierboxlayout.addWidget(self.campmod)
		carrierboxlayout.addWidget(ctlevelLabel)
		carrierboxlayout.addWidget(self.ctlevelSlider)
		carrierboxlayout.addWidget(carateLabel)
		carrierboxlayout.addWidget(self.carateSlider)
		carrierboxlayout.addWidget(cdrate1Label)
		carrierboxlayout.addWidget(self.cdrate1Slider)
		carrierboxlayout.addWidget(cdlevelLabel)
		carrierboxlayout.addWidget(self.cdlevelSlider)
		carrierboxlayout.addWidget(cdrate2Label)
		carrierboxlayout.addWidget(self.cdrate2Slider)
		carrierboxlayout.addWidget(crrateLabel)
		carrierboxlayout.addWidget(self.crrateSlider)
		carrierboxlayout.addWidget(csrrateLabel)
		carrierboxlayout.addWidget(self.csrrateSlider)
		carrierboxlayout.addWidget(crateksLabel)
		carrierboxlayout.addWidget(self.crateksSlider)
		carrierboxlayout.addWidget(clevelkshLabel)
		carrierboxlayout.addWidget(self.clevelkshSlider)
		carrierboxlayout.addWidget(clevelkslLabel)
		carrierboxlayout.addWidget(self.clevelkslSlider)
		carrierboxlayout.addStretch(1)
		self.carrierBox.setLayout(carrierboxlayout)

		#### Modulator
		self.modulatorBox = QGroupBox("Modulator")

		self.mstComboBox = QComboBox()
		self.mstComboBox.addItems(["Sine","Squared Sine","Half Sine","Squared Half Sine"])
		mstLabel = QLabel("Waveform:")
		mstLabel.setBuddy(self.mstComboBox)
		self.mstComboBox.activated[str].connect(self.changeMST)

		self.mcdetune = QCheckBox("Coarse Detune")
		self.mcdetune.toggled.connect(self.changeMCDetune)

		self.mfdetuneSlider = QSlider(Qt.Horizontal)
		self.mfdetuneSlider.setMinimum(0)
		self.mfdetuneSlider.setMaximum(15)
		self.mfdetuneSlider.setTickPosition(QSlider.TicksBelow)
		self.mfdetuneSlider.setTickInterval(8)
		mfdetuneLabel = QLabel("Fine Detune:")
		mfdetuneLabel.setBuddy(self.mfdetuneSlider)		
		self.mfdetuneSlider.valueChanged.connect(self.changeMFDetune)

		self.mfmultSlider = QSlider(Qt.Horizontal)
		self.mfmultSlider.setMinimum(0)
		self.mfmultSlider.setMaximum(15)
		mfmultLabel = QLabel("Frequency Muliplier:")
		mfmultLabel.setBuddy(self.mfmultSlider)		
		self.mfmultSlider.valueChanged.connect(self.changeMFMult)

		self.mampmod = QCheckBox("Amplitude Modulation")
		self.mampmod.toggled.connect(self.changeMAmpMod)

		self.mtlevelSlider = QSlider(Qt.Horizontal)
		self.mtlevelSlider.setMinimum(0)
		self.mtlevelSlider.setMaximum(99)
		self.mtlevelSlider.setInvertedAppearance(True)
		mtlevelLabel = QLabel("Total Level:")
		mtlevelLabel.setBuddy(self.mtlevelSlider)		
		self.mtlevelSlider.valueChanged.connect(self.changeMTLevel)

		self.marateSlider = QSlider(Qt.Horizontal)
		self.marateSlider.setMinimum(0)
		self.marateSlider.setMaximum(63)
		marateLabel = QLabel("Attack Rate:")
		marateLabel.setBuddy(self.marateSlider)		
		self.marateSlider.valueChanged.connect(self.changeMARate)

		self.mdrate1Slider = QSlider(Qt.Horizontal)
		self.mdrate1Slider.setMinimum(0)
		self.mdrate1Slider.setMaximum(63)
		mdrate1Label = QLabel("Decay Rate One:")
		mdrate1Label.setBuddy(self.mdrate1Slider)		
		self.mdrate1Slider.valueChanged.connect(self.changeMDRate1)

		self.mdlevelSlider = QSlider(Qt.Horizontal)
		self.mdlevelSlider.setMinimum(0)
		self.mdlevelSlider.setMaximum(15)
		self.mdlevelSlider.setInvertedAppearance(True)
		mdlevelLabel = QLabel("Decay Level:")
		mdlevelLabel.setBuddy(self.mdlevelSlider)		
		self.mdlevelSlider.valueChanged.connect(self.changeMDLevel)

		self.mdrate2Slider = QSlider(Qt.Horizontal)
		self.mdrate2Slider.setMinimum(0)
		self.mdrate2Slider.setMaximum(63)
		mdrate2Label = QLabel("Decay Rate Two:")
		mdrate2Label.setBuddy(self.mdrate2Slider)		
		self.mdrate2Slider.valueChanged.connect(self.changeMDRate2)

		self.mrrateSlider = QSlider(Qt.Horizontal)
		self.mrrateSlider.setMinimum(0)
		self.mrrateSlider.setMaximum(15)
		mrrateLabel = QLabel("Release Rate:")
		mrrateLabel.setBuddy(self.mrrateSlider)		
		self.mrrateSlider.valueChanged.connect(self.changeMRRate)

		self.msrrateSlider = QSlider(Qt.Horizontal)
		self.msrrateSlider.setMinimum(0)
		self.msrrateSlider.setMaximum(15)
		msrrateLabel = QLabel("Sustain Release Rate:")
		msrrateLabel.setBuddy(self.msrrateSlider)		
		self.msrrateSlider.valueChanged.connect(self.changeMSRRate)

		self.mrateksSlider = QSlider(Qt.Horizontal)
		self.mrateksSlider.setMinimum(0)
		self.mrateksSlider.setMaximum(3)
		mrateksLabel = QLabel("Rate Key Scaling:")
		mrateksLabel.setBuddy(self.mrateksSlider)		
		self.mrateksSlider.valueChanged.connect(self.changeMRateKS)

		self.mlevelkshSlider = QSlider(Qt.Horizontal)
		self.mlevelkshSlider.setMinimum(0)
		self.mlevelkshSlider.setMaximum(15)
		mlevelkshLabel = QLabel("Level Key Scaling High:")
		mlevelkshLabel.setBuddy(self.mlevelkshSlider)		
		self.mlevelkshSlider.valueChanged.connect(self.changeMLevelKSH)

		self.mlevelkslSlider = QSlider(Qt.Horizontal)
		self.mlevelkslSlider.setMinimum(0)
		self.mlevelkslSlider.setMaximum(15)
		mlevelkslLabel = QLabel("Level Key Scaling Low:")
		mlevelkslLabel.setBuddy(self.mlevelkslSlider)		
		self.mlevelkslSlider.valueChanged.connect(self.changeMLevelKSL)

		modulatorboxlayout = QVBoxLayout()
		modulatorboxlayout.addWidget(mstLabel)
		modulatorboxlayout.addWidget(self.mstComboBox)
		modulatorboxlayout.addWidget(self.mcdetune)
		modulatorboxlayout.addWidget(mfdetuneLabel)
		modulatorboxlayout.addWidget(self.mfdetuneSlider)
		modulatorboxlayout.addWidget(mfmultLabel)
		modulatorboxlayout.addWidget(self.mfmultSlider)
		modulatorboxlayout.addWidget(self.mampmod)
		modulatorboxlayout.addWidget(mtlevelLabel)
		modulatorboxlayout.addWidget(self.mtlevelSlider)
		modulatorboxlayout.addWidget(marateLabel)
		modulatorboxlayout.addWidget(self.marateSlider)
		modulatorboxlayout.addWidget(mdrate1Label)
		modulatorboxlayout.addWidget(self.mdrate1Slider)
		modulatorboxlayout.addWidget(mdlevelLabel)
		modulatorboxlayout.addWidget(self.mdlevelSlider)
		modulatorboxlayout.addWidget(mdrate2Label)
		modulatorboxlayout.addWidget(self.mdrate2Slider)
		modulatorboxlayout.addWidget(mrrateLabel)
		modulatorboxlayout.addWidget(self.mrrateSlider)
		modulatorboxlayout.addWidget(msrrateLabel)
		modulatorboxlayout.addWidget(self.msrrateSlider)
		modulatorboxlayout.addWidget(mrateksLabel)
		modulatorboxlayout.addWidget(self.mrateksSlider)
		modulatorboxlayout.addWidget(mlevelkshLabel)
		modulatorboxlayout.addWidget(self.mlevelkshSlider)
		modulatorboxlayout.addWidget(mlevelkslLabel)
		modulatorboxlayout.addWidget(self.mlevelkslSlider)
		modulatorboxlayout.addStretch(1)
		self.modulatorBox.setLayout(modulatorboxlayout)

		#### Mystery bytes
		self.extrasbox = QGroupBox("Extras")
		q = 1
		self.mbyteSliders = []
		mbyteLabels = []
		extrasboxlayout = QVBoxLayout()
		self.mbyteSlider1 = QSlider(Qt.Horizontal)
		self.mbyteSlider1.setMinimum(0)
		self.mbyteSlider1.setMaximum(15)
		mbyteLabel1 = QLabel('Mystery Byte 1')
		mbyteLabel1.setBuddy(self.mbyteSlider1)	
		self.mbyteSlider1.valueChanged.connect(self.changeMByte1)
		extrasboxlayout.addWidget(mbyteLabel1)
		extrasboxlayout.addWidget(self.mbyteSlider1)
		self.mbyteSlider2 = QSlider(Qt.Horizontal)
		self.mbyteSlider2.setMinimum(0)
		self.mbyteSlider2.setMaximum(15)
		mbyteLabel2 = QLabel('Mystery Byte 2')
		mbyteLabel2.setBuddy(self.mbyteSlider2)	
		self.mbyteSlider2.valueChanged.connect(self.changeMByte2)
		extrasboxlayout.addWidget(mbyteLabel2)
		extrasboxlayout.addWidget(self.mbyteSlider2)
		self.mbyteSlider3 = QSlider(Qt.Horizontal)
		self.mbyteSlider3.setMinimum(0)
		self.mbyteSlider3.setMaximum(15)
		mbyteLabel3 = QLabel('Mystery Byte 3')
		mbyteLabel3.setBuddy(self.mbyteSlider3)	
		self.mbyteSlider3.valueChanged.connect(self.changeMByte3)
		extrasboxlayout.addWidget(mbyteLabel3)
		extrasboxlayout.addWidget(self.mbyteSlider3)
		self.mbyteSlider4 = QSlider(Qt.Horizontal)
		self.mbyteSlider4.setMinimum(0)
		self.mbyteSlider4.setMaximum(15)
		mbyteLabel4 = QLabel('Mystery Byte 4')
		mbyteLabel4.setBuddy(self.mbyteSlider4)	
		self.mbyteSlider4.valueChanged.connect(self.changeMByte4)
		extrasboxlayout.addWidget(mbyteLabel4)
		extrasboxlayout.addWidget(self.mbyteSlider4)
		self.mbyteSlider5 = QSlider(Qt.Horizontal)
		self.mbyteSlider5.setMinimum(0)
		self.mbyteSlider5.setMaximum(15)
		mbyteLabel5 = QLabel('Mystery Byte 5')
		mbyteLabel5.setBuddy(self.mbyteSlider5)	
		self.mbyteSlider5.valueChanged.connect(self.changeMByte5)
		extrasboxlayout.addWidget(mbyteLabel5)
		extrasboxlayout.addWidget(self.mbyteSlider5)
		self.mbyteSlider6 = QSlider(Qt.Horizontal)
		self.mbyteSlider6.setMinimum(0)
		self.mbyteSlider6.setMaximum(15)
		mbyteLabel6 = QLabel('Mystery Byte 6')
		mbyteLabel6.setBuddy(self.mbyteSlider6)	
		self.mbyteSlider6.valueChanged.connect(self.changeMByte6)
		extrasboxlayout.addWidget(mbyteLabel6)
		extrasboxlayout.addWidget(self.mbyteSlider6)
		self.mbyteSlider7 = QSlider(Qt.Horizontal)
		self.mbyteSlider7.setMinimum(0)
		self.mbyteSlider7.setMaximum(15)
		mbyteLabel7 = QLabel('Mystery Byte 7')
		mbyteLabel7.setBuddy(self.mbyteSlider7)	
		self.mbyteSlider7.valueChanged.connect(self.changeMByte7)
		extrasboxlayout.addWidget(mbyteLabel7)
		extrasboxlayout.addWidget(self.mbyteSlider7)
		self.mbyteSlider8 = QSlider(Qt.Horizontal)
		self.mbyteSlider8.setMinimum(0)
		self.mbyteSlider8.setMaximum(15)
		mbyteLabel8 = QLabel('Mystery Byte 8')
		mbyteLabel8.setBuddy(self.mbyteSlider8)	
		self.mbyteSlider8.valueChanged.connect(self.changeMByte8)
		extrasboxlayout.addWidget(mbyteLabel8)
		extrasboxlayout.addWidget(self.mbyteSlider8)
		self.mbyteSlider9 = QSlider(Qt.Horizontal)
		self.mbyteSlider9.setMinimum(0)
		self.mbyteSlider9.setMaximum(15)
		mbyteLabel9 = QLabel('Mystery Byte 9')
		mbyteLabel9.setBuddy(self.mbyteSlider9)	
		self.mbyteSlider9.valueChanged.connect(self.changeMByte9)
		extrasboxlayout.addWidget(mbyteLabel9)
		extrasboxlayout.addWidget(self.mbyteSlider9)

		self.mbitCheckBox1 = QCheckBox("Mystery Bit 1")
		self.mbitCheckBox1.toggled.connect(self.changeMBit1)
		extrasboxlayout.addWidget(self.mbitCheckBox1)

		self.mbitCheckBox2 = QCheckBox("Mystery Bit 2")
		self.mbitCheckBox2.toggled.connect(self.changeMBit2)
		extrasboxlayout.addWidget(self.mbitCheckBox2)

		loadpatchesbutton = QPushButton("Load 5 Patches", self)
		loadpatchesbutton.clicked.connect(lambda x: self.loadPatches(5,"Load 5 Patches"))
		extrasboxlayout.addWidget(loadpatchesbutton)

		loadpatchbutton = QPushButton("Load 1 Patch", self)
		loadpatchbutton.clicked.connect(lambda x: self.loadPatches(1,"Load 1 Patch"))
		extrasboxlayout.addWidget(loadpatchbutton)

		savepatchesbutton = QPushButton("Save 5 Patches", self)
		savepatchesbutton.clicked.connect(lambda x: self.savePatches(5, "Save 5 Patches"))
		extrasboxlayout.addWidget(savepatchesbutton)

		savepatchbutton = QPushButton("Save 1 Patch", self)
		savepatchbutton.clicked.connect(lambda x: self.savePatches(1, "Save 1 Patch"))
		extrasboxlayout.addWidget(savepatchbutton)

		randompatchesbutton = QPushButton("&5 Random Patches", self)
		randompatchesbutton.clicked.connect(lambda x: self.randomPatches(5))
		extrasboxlayout.addWidget(randompatchesbutton)

		randompatchbutton = QPushButton("&1 Random Patch", self)
		randompatchbutton.clicked.connect(lambda x: self.randomPatches(1))
		extrasboxlayout.addWidget(randompatchbutton)

		extrasboxlayout.addStretch(1)
		self.extrasbox.setLayout(extrasboxlayout)

		#### Others
		self.bankComboBox = QComboBox()
		self.bankComboBox.addItems(["1","2","3","4","5"])
		bankLabel = QLabel("&Bank:")
		bankLabel.setBuddy(self.bankComboBox)
		self.bankComboBox.activated[str].connect(self.changeBank)

		self.mididComboBox = QComboBox()
		for key in sorted(self.midi_devices):
			self.mididComboBox.addItem(key)
		mididLabel = QLabel("MIDI Device:")
		mididLabel.setBuddy(self.mididComboBox)
		self.mididComboBox.activated[str].connect(self.changeMIDID)

		self.midicComboBox = QComboBox()
		c = 1
		while c < 17:
			self.midicComboBox.addItem(str(c))
			c = c + 1
		midicLabel = QLabel("MIDI Channel:")
		midicLabel.setBuddy(self.midicComboBox)
		self.midicComboBox.activated[str].connect(self.changeMIDIC)
		
		self.midinoteSlider = QSlider(Qt.Horizontal)
		self.midinoteSlider.setMinimum(36)
		self.midinoteSlider.setMaximum(96)
		midinoteLabel = QLabel("Midi Note:")
		midinoteLabel.setBuddy(self.midinoteSlider)		
		self.midinoteSlider.valueChanged.connect(self.changeMIDINote)

		self.feedbackSlider = QSlider(Qt.Horizontal)
		self.feedbackSlider.setMinimum(0)
		self.feedbackSlider.setMaximum(7)
		feedbackLabel = QLabel("&Feedback:")
		feedbackLabel.setBuddy(self.feedbackSlider)		
		self.feedbackSlider.valueChanged.connect(self.changeFeedback)

		self.pitchmodSlider = QSlider(Qt.Horizontal)
		self.pitchmodSlider.setMinimum(0)
		self.pitchmodSlider.setMaximum(7)
		pitchmodLabel = QLabel("&Pitch Modulation Sensitivity:")
		pitchmodLabel.setBuddy(self.pitchmodSlider)
		self.pitchmodSlider.valueChanged.connect(self.changePitchMod)

		self.ampmodSlider = QSlider(Qt.Horizontal)
		self.ampmodSlider.setMinimum(0)
		self.ampmodSlider.setMaximum(3)
		ampmodLabel = QLabel("&Amplitude Modulation Sensitivity:")
		ampmodLabel.setBuddy(self.ampmodSlider)
		self.ampmodSlider.valueChanged.connect(self.changeAmpMod)

		self.vibdelaySlider = QSlider(Qt.Horizontal)
		self.vibdelaySlider.setMinimum(0)
		self.vibdelaySlider.setMaximum(127)
		vibdelayLabel = QLabel("&Vibrato Delay Time:")
		vibdelayLabel.setBuddy(self.vibdelaySlider)
		self.vibdelaySlider.valueChanged.connect(self.changeVibDelay)

		self.sustain = QCheckBox("&Sustain Enable")
		self.sustain.toggled.connect(self.changeSustain)

		self.vibrato = QCheckBox("V&ibrato Enable")
		self.vibrato.toggled.connect(self.changeVibrato)
		
		topLayout = QHBoxLayout()
		topLayout.addWidget(bankLabel)
		topLayout.addWidget(self.bankComboBox)
		topLayout.addWidget(mididLabel)
		topLayout.addWidget(self.mididComboBox)
		topLayout.addWidget(midicLabel)
		topLayout.addWidget(self.midicComboBox)
		topLayout.addWidget(midinoteLabel)
		topLayout.addWidget(self.midinoteSlider)
		topLayout.addStretch(1)

		bottomBox = QVBoxLayout()
		bottomBox.addWidget(feedbackLabel)
		bottomBox.addWidget(self.feedbackSlider)
		bottomBox.addWidget(pitchmodLabel)
		bottomBox.addWidget(self.pitchmodSlider)
		bottomBox.addWidget(ampmodLabel)
		bottomBox.addWidget(self.ampmodSlider)
		bottomBox.addWidget(vibdelayLabel)
		bottomBox.addWidget(self.vibdelaySlider)
		bottomBox.addStretch(1)

		verybottomBox = QHBoxLayout()
		verybottomBox.addWidget(self.vibrato)		
		verybottomBox.addWidget(self.sustain)


		mainLayout = QGridLayout()
		mainLayout.addLayout(topLayout, 0, 0, 1, 3)
		mainLayout.addWidget(self.carrierBox, 1, 0)		
		mainLayout.addWidget(self.modulatorBox, 1, 1)		
		mainLayout.addWidget(self.extrasbox, 1, 2)
		mainLayout.addLayout(bottomBox, 2, 0, 1, 3)
		mainLayout.addLayout(verybottomBox, 3, 0, 1, 3)
		mainLayout.setRowStretch(2,1)		

		self.setLayout(mainLayout)
		self.setWindowTitle("PortaSound PSS-680 patch editor")

	def changeFeedback(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['feedback'] = self.feedbackSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changePitchMod(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['pitch_modulation_sensitivity'] = self.pitchmodSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeAmpMod(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['amplitude_modulation_sensitivity'] = self.ampmodSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeVibDelay(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['vibrato_delay_time'] = self.vibdelaySlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeSustain(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['sustain_enable'] = self.sustain.isChecked()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeVibrato(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['vibrato_enable'] = self.vibrato.isChecked()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCST(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_sine_table'] = self.cstComboBox.currentIndex()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCCDetune(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_coarse_detune'] = self.ccdetune.isChecked()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCFDetune(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_fine_detune'] = self.detune[self.cfdetuneSlider.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCFMult(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_frequency_multiple'] = self.cfmultSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCAmpMod(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_amplitude_modulation'] = self.campmod.isChecked()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCTLevel(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_total_level'] = self.ctlevelSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)
	
	def changeCARate(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_attack_rate'] = self.carateSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCDRate1(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_decay_rate_1'] = self.cdrate1Slider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCDLevel(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_decay_level'] = self.cdlevelSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCDRate2(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_decay_rate_2'] = self.cdrate2Slider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCRRate(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_release_rate'] = self.crrateSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCSRRate(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_sustain_release_rate'] = self.csrrateSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCRateKS(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_rate_key_scaling'] = self.crateksSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCLevelKSH(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_level_key_scaling_high'] = self.lks_hi[self.clevelkshSlider.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeCLevelKSL(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['carrier_level_key_scaling_low'] = self.lks_lo[self.clevelkslSlider.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMST(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_sine_table'] = self.mstComboBox.currentIndex()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMCDetune(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_coarse_detune'] = self.mcdetune.isChecked()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMFDetune(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_fine_detune'] = self.detune[self.mfdetuneSlider.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMFMult(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_frequency_multiple'] = self.mfmultSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMAmpMod(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_amplitude_modulation'] = self.mampmod.isChecked()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMTLevel(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_total_level'] = self.mtlevelSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)
	
	def changeMARate(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_attack_rate'] = self.marateSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMDRate1(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_decay_rate_1'] = self.mdrate1Slider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMDLevel(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_decay_level'] = self.mdlevelSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMDRate2(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_decay_rate_2'] = self.mdrate2Slider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMRRate(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_release_rate'] = self.mrrateSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMSRRate(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_sustain_release_rate'] = self.msrrateSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMRateKS(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_rate_key_scaling'] = self.mrateksSlider.value()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMLevelKSH(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_level_key_scaling_high'] = self.lks_hi[self.mlevelkshSlider.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMLevelKSL(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['modulator_level_key_scaling_low'] = self.lks_lo[self.mlevelkslSlider.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMByte1(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_byte_1'] = self.mbytes1[self.mbyteSlider1.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMByte2(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_byte_2'] = self.mbytes2[self.mbyteSlider2.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMByte3(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_byte_3'] = self.mbytes3[self.mbyteSlider3.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMByte4(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_byte_4'] = self.mbytes4[self.mbyteSlider4.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMByte5(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_byte_5'] = self.mbytes5[self.mbyteSlider5.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)
	
	def changeMByte6(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_byte_6'] = self.mbytes6[self.mbyteSlider6.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMByte7(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_byte_7'] = self.mbytes7[self.mbyteSlider7.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMByte8(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_byte_8'] = self.mbytes8[self.mbyteSlider8.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMByte9(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_byte_9'] = self.mbytes9[self.mbyteSlider9.value()]
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMBit1(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_bit_1'] = self.mbitCheckBox1.isChecked()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMBit2(self):
		if len(self.patches) > 0:
			self.patches[self.bank]['mystery_bit_2'] = self.mbitCheckBox2.isChecked()
			self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeMIDID(self):
		self.midi_device = self.midi_devices[self.mididComboBox.currentText()]

	def changeMIDIC(self):
		self.midi_channel = int(self.midicComboBox.currentIndex())

	def changeMIDINote(self):
		self.midi_note = self.midinoteSlider.value()
		self.write_and_send_patch(self.patches[self.bank],self.tmp_filename)

	def changeBank(self):
		self.ready = False
		self.bank = int(self.bankComboBox.currentText()) - 1
		self.feedbackSlider.setValue(self.patches[self.bank]['feedback'])
		self.pitchmodSlider.setValue(self.patches[self.bank]['pitch_modulation_sensitivity'])
		self.ampmodSlider.setValue(self.patches[self.bank]['amplitude_modulation_sensitivity'])
		self.vibdelaySlider.setValue(self.patches[self.bank]['vibrato_delay_time'])
		self.sustain.setChecked(self.patches[self.bank]['sustain_enable'])
		self.vibrato.setChecked(self.patches[self.bank]['vibrato_enable'])

		self.cstComboBox.setCurrentIndex(self.patches[self.bank]['carrier_sine_table'])
		self.ccdetune.setChecked(self.patches[self.bank]['carrier_coarse_detune'])
		self.cfdetuneSlider.setValue(self.detune.index(self.patches[self.bank]['carrier_fine_detune']))
		self.cfmultSlider.setValue(self.patches[self.bank]['carrier_frequency_multiple'])
		self.campmod.setChecked(self.patches[self.bank]['carrier_amplitude_modulation'])
		self.ctlevelSlider.setValue(self.patches[self.bank]['carrier_total_level'])
		self.carateSlider.setValue(self.patches[self.bank]['carrier_attack_rate'])
		self.cdrate1Slider.setValue(self.patches[self.bank]['carrier_decay_rate_1'])
		self.cdlevelSlider.setValue(self.patches[self.bank]['carrier_decay_level'])
		self.cdrate2Slider.setValue(self.patches[self.bank]['carrier_decay_rate_2'])
		self.crrateSlider.setValue(self.patches[self.bank]['carrier_release_rate'])
		self.csrrateSlider.setValue(self.patches[self.bank]['carrier_sustain_release_rate'])
		self.crateksSlider.setValue(self.patches[self.bank]['carrier_rate_key_scaling'])
		self.clevelkshSlider.setValue(self.lks_hi.index(self.patches[self.bank]['carrier_level_key_scaling_high']))
		self.clevelkslSlider.setValue(self.lks_lo.index(self.patches[self.bank]['carrier_level_key_scaling_low']))

		self.mstComboBox.setCurrentIndex(self.patches[self.bank]['modulator_sine_table'])
		self.mcdetune.setChecked(self.patches[self.bank]['modulator_coarse_detune'])
		self.mfdetuneSlider.setValue(self.detune.index(self.patches[self.bank]['modulator_fine_detune']))
		self.mfmultSlider.setValue(self.patches[self.bank]['modulator_frequency_multiple'])
		self.mampmod.setChecked(self.patches[self.bank]['modulator_amplitude_modulation'])
		self.mtlevelSlider.setValue(self.patches[self.bank]['modulator_total_level'])
		self.marateSlider.setValue(self.patches[self.bank]['modulator_attack_rate'])
		self.mdrate1Slider.setValue(self.patches[self.bank]['modulator_decay_rate_1'])
		self.mdlevelSlider.setValue(self.patches[self.bank]['modulator_decay_level'])
		self.mdrate2Slider.setValue(self.patches[self.bank]['modulator_decay_rate_2'])
		self.mrrateSlider.setValue(self.patches[self.bank]['modulator_release_rate'])
		self.msrrateSlider.setValue(self.patches[self.bank]['modulator_sustain_release_rate'])
		self.mrateksSlider.setValue(self.patches[self.bank]['modulator_rate_key_scaling'])
		self.mlevelkshSlider.setValue(self.lks_hi.index(self.patches[self.bank]['modulator_level_key_scaling_high']))
		self.mlevelkslSlider.setValue(self.lks_lo.index(self.patches[self.bank]['modulator_level_key_scaling_low']))
		
		self.mbyteSlider1.setValue(self.mbytes1.index(self.patches[self.bank]['mystery_byte_1']))
		self.mbyteSlider2.setValue(self.mbytes2.index(self.patches[self.bank]['mystery_byte_2']))
		self.mbyteSlider3.setValue(self.mbytes3.index(self.patches[self.bank]['mystery_byte_3']))
		self.mbyteSlider4.setValue(self.mbytes4.index(self.patches[self.bank]['mystery_byte_4']))
		self.mbyteSlider5.setValue(self.mbytes5.index(self.patches[self.bank]['mystery_byte_5']))
		self.mbyteSlider6.setValue(self.mbytes6.index(self.patches[self.bank]['mystery_byte_6']))
		self.mbyteSlider7.setValue(self.mbytes7.index(self.patches[self.bank]['mystery_byte_7']))
		self.mbyteSlider8.setValue(self.mbytes8.index(self.patches[self.bank]['mystery_byte_8']))
		self.mbyteSlider9.setValue(self.mbytes9.index(self.patches[self.bank]['mystery_byte_9']))

		self.mbitCheckBox1.setChecked(self.patches[self.bank]['mystery_bit_1'])
		self.mbitCheckBox2.setChecked(self.patches[self.bank]['mystery_bit_2'])

		self.ready = True

	def initBanks(self):
		self.ready = False
		self.bank = 0
		self.patches = []
		self.feedbackSlider.setValue(0)
		self.pitchmodSlider.setValue(0)
		self.ampmodSlider.setValue(0)
		self.vibdelaySlider.setValue(0)
		self.sustain.setChecked(False)
		self.vibrato.setChecked(False)

		self.cstComboBox.setCurrentIndex(0)
		self.ccdetune.setChecked(False)
		self.cfdetuneSlider.setValue(self.detune.index(0))
		self.cfmultSlider.setValue(0)
		self.campmod.setChecked(False)
		self.ctlevelSlider.setValue(99)
		self.carateSlider.setValue(0)
		self.cdrate1Slider.setValue(0)
		self.cdlevelSlider.setValue(15)
		self.cdrate2Slider.setValue(0)
		self.crrateSlider.setValue(0)
		self.csrrateSlider.setValue(0)
		self.crateksSlider.setValue(0)
		self.clevelkshSlider.setValue(self.lks_hi.index(0))
		self.clevelkslSlider.setValue(self.lks_lo.index(0))

		self.mstComboBox.setCurrentIndex(0)
		self.mcdetune.setChecked(False)
		self.mfdetuneSlider.setValue(self.detune.index(0))
		self.mfmultSlider.setValue(0)
		self.mampmod.setChecked(False)
		self.mtlevelSlider.setValue(99)
		self.marateSlider.setValue(0)
		self.mdrate1Slider.setValue(0)
		self.mdlevelSlider.setValue(15)
		self.mdrate2Slider.setValue(0)
		self.mrrateSlider.setValue(0)
		self.msrrateSlider.setValue(0)
		self.mrateksSlider.setValue(0)
		self.mlevelkshSlider.setValue(self.lks_hi.index(0))
		self.mlevelkslSlider.setValue(self.lks_lo.index(0))
		
		self.mbyteSlider1.setValue(self.mbytes1.index(9))
		self.mbyteSlider2.setValue(self.mbytes2.index(14))
		self.mbyteSlider3.setValue(self.mbytes3.index(0))
		self.mbyteSlider4.setValue(self.mbytes4.index(0))
		self.mbyteSlider5.setValue(self.mbytes5.index(2))
		self.mbyteSlider6.setValue(self.mbytes6.index(13))
		self.mbyteSlider7.setValue(self.mbytes7.index(0))
		self.mbyteSlider8.setValue(self.mbytes8.index(5))
		self.mbyteSlider9.setValue(self.mbytes9.index(0))

		self.mbitCheckBox1.setChecked(False)
		self.mbitCheckBox2.setChecked(False)

		self.mididComboBox.setCurrentIndex(0)
		self.midicComboBox.setCurrentIndex(0)
		self.midinoteSlider.setValue(36)

		self.ready = True
		i = 0
		while i < 5:
			patch = {}
			patch['bank'] = i
			patch['feedback'] = self.feedbackSlider.value()
			patch['pitch_modulation_sensitivity'] = self.pitchmodSlider.value()
			patch['amplitude_modulation_sensitivity'] = self.pitchmodSlider.value()
			patch['vibrato_delay_time'] = self.vibdelaySlider.value()
			patch['sustain_enable'] = self.sustain.isChecked()
			patch['vibrato_enable'] = self.vibrato.isChecked()
			patch['carrier_sine_table'] = self.cstComboBox.currentIndex()
			patch['carrier_coarse_detune'] = self.ccdetune.isChecked()
			patch['carrier_fine_detune'] = self.detune[self.cfdetuneSlider.value()]
			patch['carrier_frequency_multiple'] = self.cfmultSlider.value()
			patch['carrier_amplitude_modulation'] = self.campmod.isChecked()
			patch['carrier_total_level'] = self.ctlevelSlider.value()
			patch['carrier_attack_rate'] = self.carateSlider.value()
			patch['carrier_decay_rate_1'] = self.cdrate1Slider.value()
			patch['carrier_decay_level'] = self.cdlevelSlider.value()
			patch['carrier_decay_rate_2'] = self.cdrate2Slider.value()
			patch['carrier_release_rate'] = self.crrateSlider.value()
			patch['carrier_sustain_release_rate'] = self.csrrateSlider.value()
			patch['carrier_rate_key_scaling'] = self.crateksSlider.value()
			patch['carrier_level_key_scaling_high'] = self.lks_hi[self.clevelkshSlider.value()]
			patch['carrier_level_key_scaling_low'] = self.lks_lo[self.clevelkslSlider.value()]
			patch['modulator_sine_table'] = self.mstComboBox.currentIndex()
			patch['modulator_coarse_detune'] = self.mcdetune.isChecked()
			patch['modulator_fine_detune'] = self.detune[self.mfdetuneSlider.value()]
			patch['modulator_frequency_multiple'] = self.mfmultSlider.value()
			patch['modulator_amplitude_modulation'] = self.mampmod.isChecked()
			patch['modulator_total_level'] = self.mtlevelSlider.value()
			patch['modulator_attack_rate'] = self.marateSlider.value()
			patch['modulator_decay_rate_1'] = self.mdrate1Slider.value()
			patch['modulator_decay_level'] = self.mdlevelSlider.value()
			patch['modulator_decay_rate_2'] = self.mdrate2Slider.value()
			patch['modulator_release_rate'] = self.mrrateSlider.value()
			patch['modulator_sustain_release_rate'] = self.msrrateSlider.value()
			patch['modulator_rate_key_scaling'] = self.mrateksSlider.value()
			patch['modulator_level_key_scaling_high'] = self.lks_hi[self.mlevelkshSlider.value()]
			patch['modulator_level_key_scaling_low'] = self.lks_lo[self.mlevelkslSlider.value()]
			patch['mystery_byte_1'] = self.mbytes1[self.mbyteSlider1.value()]
			patch['mystery_byte_2'] = self.mbytes2[self.mbyteSlider2.value()]
			patch['mystery_byte_3'] = self.mbytes3[self.mbyteSlider3.value()]
			patch['mystery_byte_4'] = self.mbytes4[self.mbyteSlider4.value()]
			patch['mystery_byte_5'] = self.mbytes5[self.mbyteSlider5.value()]
			patch['mystery_byte_6'] = self.mbytes6[self.mbyteSlider6.value()]
			patch['mystery_byte_7'] = self.mbytes7[self.mbyteSlider7.value()]
			patch['mystery_byte_8'] = self.mbytes8[self.mbyteSlider8.value()]
			patch['mystery_byte_9'] = self.mbytes9[self.mbyteSlider9.value()]
			patch['mystery_bit_1'] = self.mbitCheckBox1.isChecked()
			patch['mystery_bit_2'] = self.mbitCheckBox2.isChecked()
			self.patches.append(patch)
			i = i + 1

	def loadPatches(self,num,desc):
		filename = QFileDialog.getOpenFileName(self, desc, "", "Sysex files (*.syx)")[0]
		self.load_patches(num,filename)

	def savePatches(self,num,desc):
		filename = QFileDialog.getSaveFileName(self, desc, "", "Sysex files (*.syx)")[0]
		f = open(filename,'wb')
		if num == 5:
			for patch in self.patches:
				self.write_patch(f,patch)
		if num == 1:
			self.write_patch(f,self.patches[self.bankComboBox.currentIndex()])
		f.close()

	def randomPatches(self,num):
		self.random_patches(self.tmp_filename)
		self.load_patches(num,self.tmp_filename)


if __name__ == '__main__':
	#os.environ['QT_SCALE_FACTOR'] = '1'
	amidicheck = subprocess.Popen(["which","amidi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
	if amidicheck == 1:
		print("amidi not in path, exiting.")
		exit(1)
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
	app = QApplication(sys.argv)
	p = PortaSound()
	p.initBanks()
	p.changeMIDID()
	p.changeMIDIC()
	p.changeMIDINote()			
	p.show()
	app.exec_()
	#p.connection.deactivate()
	#p.connection.close()
