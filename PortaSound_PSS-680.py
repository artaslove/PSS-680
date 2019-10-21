#!/usr/bin/env python
from PySide2.QtCore import QDateTime, Qt, QTimer
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

import random 
import sys
import hashlib

class PortaSound(QDialog):
	patch_header = [240, 67, 118, 0]
	patch_footer = 247

	def twos_comp_b(self,val):
		return 0b1111111 - val + 1

	def load_patches(self, path):
		if self.check_binary(path) == True:
			self.patches = []
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
						patch['modulator_amplitude_modulation_enable'] = True
					else:
						patch['modulator_amplitude_modulation_enable'] = False
					mask = 1 << 2
					tempv = v & mask
					if tempv > 0:
						patch['modulator_coarse_detune_enable'] = True
					else:
						patch['modulator_coarse_detune_enable'] = False
					mask = ~(3 << 2)
					tempv = (v & mask) << 4
				if i == 23:
					patch['modulator_decay_rate_1'] = tempv + v
				if i == 24:
					mask = 1 << 3
					tempv = v & mask
					if tempv > 0:
						patch['carrier_amplitude_modulation_enable'] = True
					else:
						patch['carrier_amplitude_modulation_enable'] = False
					mask = 1 << 2
					tempv = v & mask
					if tempv > 0:
						patch['carrier_coarse_detune_enable'] = True
					else:
						patch['carrier_coarse_detune_enable'] = False
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
					tempv = v << 1
				if i == 35:
					patch['feedback'] = tempv + ( v >> 3 )
				if i == 36:
					patch['pitch_modulation_sensitivity'] = v 							
				if i == 37:
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
					self.patches.append(patch)
					#for key in sorted(patch.keys()):
					#	print("%s: %s" % (key, patch[key]))
					patch = {}
				i = i + 1			
			return True
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
			if patch['modulator_amplitude_modulation_enable'] == True:
				v = v | mask
			mask = 1 << 2
			if patch['modulator_coarse_detune_enable'] == True:
				v = v | mask
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 4)
			v = patch['modulator_decay_rate_1'] & mask
			checksum = self.writepatchchar(f,v,checksum)
			v = patch['carrier_decay_rate_1'] >> 4
			mask = 1 << 3
			if patch['carrier_amplitude_modulation_enable'] == True:
				v = v | mask
			mask = 1 << 2
			if patch['carrier_coarse_detune_enable'] == True:
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
			v = patch['feedback'] >> 1
			checksum = self.writepatchchar(f,v,checksum)
			mask = ~(3 << 1)
			v = (patch['feedback'] & mask) << 3
			checksum = self.writepatchchar(f,v,checksum)
			checksum = self.writepatchchar(f,patch['pitch_modulation_sensitivity'],checksum)
			checksum = self.writepatchchar(f,patch['amplitude_modulation_sensitivity'],checksum)
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
		f.close()

	def __init__(self, parent=None):
		super(PortaSound, self).__init__(parent)
		self.bankComboBox = QComboBox()
		self.bankComboBox.addItems(["0","1","2","3","4"])
		self.bank = 0
		bankLabel = QLabel("&Bank:")
		bankLabel.setBuddy(self.bankComboBox)
		self.bankComboBox.activated[str].connect(self.changeBank)

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
		self.crateksSlider.setMaximum(15)
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
		self.mrateksSlider.setMaximum(15)
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

		self.unknownBox = QGroupBox("Mystery Bytes")

		#mystery_byte_1: 9 10
		#mystery_byte_2: 14 15
		#mystery_byte_3: 0 1
		#mystery_byte_4: 0 7 11
		#mystery_byte_5: 2 6 14
		#mystery_byte_6: 13 14 15
		#mystery_byte_7: 0 4 5 6 15
		#mystery_byte_8: 5 6 7 9 15
		#mystery_byte_9: 0 1 3 4 5 7 8 11

		topLayout = QHBoxLayout()
		topLayout.addWidget(bankLabel)
		topLayout.addWidget(self.bankComboBox)
		topLayout.addStretch(1)

		bottomBox = QVBoxLayout()
		bottomBox.addWidget(feedbackLabel)
		bottomBox.addWidget(self.feedbackSlider)
		bottomBox.addWidget(pitchmodLabel)
		bottomBox.addWidget(self.pitchmodSlider)
		bottomBox.addWidget(vibdelayLabel)
		bottomBox.addWidget(self.vibdelaySlider)
		bottomBox.addWidget(self.vibrato)		
		bottomBox.addWidget(self.sustain)
		bottomBox.addStretch(1)


		mainLayout = QGridLayout()
		mainLayout.addLayout(topLayout, 0, 0, 1, 2)
		mainLayout.addWidget(self.carrierBox, 1, 0)		
		mainLayout.addWidget(self.modulatorBox, 1, 1)		
		mainLayout.addWidget(self.unknownBox, 1, 2)
		mainLayout.addLayout(bottomBox, 2, 0, 1, 3)
		mainLayout.setRowStretch(2,1)		

		self.setLayout(mainLayout)
		self.setWindowTitle("PortaSound PSS-680 patch editor")

	def changeFeedback(self):
		self.patches[self.bank]['feedback'] = self.feedbackSlider.value()

	def changePitchMod(self):
		self.patches[self.bank]['pitch_modulation_sensitivity'] = self.pitchmodSlider.value()

	def changeVibDelay(self):
		self.patches[self.bank]['vibrato_delay_time'] = self.vibdelaySlider.value()

	def changeSustain(self):
		self.patches[self.bank]['sustain_enable'] = self.sustain.checkState()

	def changeVibrato(self):
		self.patches[self.bank]['vibrato_enable'] = self.vibrato.checkState()


	def changeCST(self):
		self.patches[self.bank]['carrier_sine_table'] = self.cstComboBox.currentIndex()

	def changeCCDetune(self):
		self.patches[self.bank]['carrier_coarse_detune'] = self.ccdetune.checkState()

	def changeCFDetune(self):
		self.patches[self.bank]['carrier_fine_detune'] = self.cfdetuneSlider.value()

	def changeCFMult(self):
		self.patches[self.bank]['carrier_frequency_multiple'] = self.cfmultSlider.value()

	def changeCAmpMod(self):
		self.patches[self.bank]['carrier_amplitude_modulation_enable'] = self.campmod.checkState()

	def changeCTLevel(self):
		self.patches[self.bank]['carrier_total_level'] = self.ctlevelSlider.value()
	
	def changeCARate(self):
		self.patches[self.bank]['carrier_attack_rate'] = self.carateSlider.value()

	def changeCDRate1(self):
		self.patches[self.bank]['carrier_decay_rate_1'] = self.cdrate1Slider.value()

	def changeCDLevel(self):
		self.patches[self.bank]['carrier_decay_level'] = self.cdlevelSlider.value()

	def changeCDRate2(self):
		self.patches[self.bank]['carrier_decay_rate_2'] = self.cdrate2Slider.value()

	def changeCRRate(self):
		self.patches[self.bank]['carrier_release_rate'] = self.crrateSlider.value()

	def changeCSRRate(self):
		self.patches[self.bank]['carrier_sustain_release_rate'] = self.csrrateSlider.value()

	def changeCRateKS(self):
		self.patches[self.bank]['carrier_rate_key_scaling'] = self.crateksSlider.value()

	def changeCLevelKSH(self):
		self.patches[self.bank]['carrier_level_key_scaling_high'] = self.clevelkshSlider.value()

	def changeCLevelKSL(self):
		self.patches[self.bank]['carrier_level_key_scaling_low'] = self.clevelkslSlider.value()

	def changeMST(self):
		self.patches[self.bank]['modulator_sine_table'] = self.mstComboBox.currentIndex()

	def changeMCDetune(self):
		self.patches[self.bank]['modulator_coarse_detune'] = self.mcdetune.checkState()

	def changeMFDetune(self):
		self.patches[self.bank]['modulator_fine_detune'] = self.mfdetuneSlider.value()

	def changeMFMult(self):
		self.patches[self.bank]['modulator_frequency_multiple'] = self.mfmultSlider.value()

	def changeMAmpMod(self):
		self.patches[self.bank]['modulator_amplitude_modulation_enable'] = self.mampmod.checkState()

	def changeMTLevel(self):
		self.patches[self.bank]['modulator_total_level'] = self.mtlevelSlider.value()
	
	def changeMARate(self):
		self.patches[self.bank]['modulator_attack_rate'] = self.marateSlider.value()

	def changeMDRate1(self):
		self.patches[self.bank]['modulator_decay_rate_1'] = self.mdrate1Slider.value()

	def changeMDLevel(self):
		self.patches[self.bank]['modulator_decay_level'] = self.mdlevelSlider.value()

	def changeMDRate2(self):
		self.patches[self.bank]['modulator_decay_rate_2'] = self.mdrate2Slider.value()

	def changeMRRate(self):
		self.patches[self.bank]['modulator_release_rate'] = self.mrrateSlider.value()

	def changeMSRRate(self):
		self.patches[self.bank]['modulator_sustain_release_rate'] = self.msrrateSlider.value()

	def changeMRateKS(self):
		self.patches[self.bank]['modulator_rate_key_scaling'] = self.mrateksSlider.value()

	def changeMLevelKSH(self):
		self.patches[self.bank]['modulator_level_key_scaling_high'] = self.mlevelkshSlider.value()

	def changeMLevelKSL(self):
		self.patches[self.bank]['modulator_level_key_scaling_low'] = self.mlevelkslSlider.value()


	def changeBank(self):
		self.bank = int(self.bankComboBox.currentText())
		self.feedbackSlider.setValue(self.patches[self.bank]['feedback'])
		self.pitchmodSlider.setValue(self.patches[self.bank]['pitch_modulation_sensitivity'])
		self.vibdelaySlider.setValue(self.patches[self.bank]['vibrato_delay_time'])
		self.sustain.setChecked(self.patches[self.bank]['sustain_enable'])
		self.vibrato.setChecked(self.patches[self.bank]['vibrato_enable'])

		self.cstComboBox.setCurrentIndex(self.patches[self.bank]['carrier_sine_table'])
		self.ccdetune.setChecked(self.patches[self.bank]['carrier_coarse_detune_enable'])
		self.cfdetuneSlider.setValue(self.patches[self.bank]['carrier_fine_detune'])
		self.cfmultSlider.setValue(self.patches[self.bank]['carrier_frequency_multiple'])
		self.campmod.setChecked(self.patches[self.bank]['carrier_amplitude_modulation_enable'])
		self.ctlevelSlider.setValue(self.patches[self.bank]['carrier_total_level'])
		self.carateSlider.setValue(self.patches[self.bank]['carrier_attack_rate'])
		self.cdrate1Slider.setValue(self.patches[self.bank]['carrier_decay_rate_1'])
		self.cdlevelSlider.setValue(self.patches[self.bank]['carrier_decay_level'])
		self.cdrate2Slider.setValue(self.patches[self.bank]['carrier_decay_rate_2'])
		self.crrateSlider.setValue(self.patches[self.bank]['carrier_release_rate'])
		self.csrrateSlider.setValue(self.patches[self.bank]['carrier_sustain_release_rate'])
		self.crateksSlider.setValue(self.patches[self.bank]['carrier_rate_key_scaling'])
		self.clevelkshSlider.setValue(self.patches[self.bank]['carrier_level_key_scaling_high'])
		self.clevelkslSlider.setValue(self.patches[self.bank]['carrier_level_key_scaling_low'])

		self.mstComboBox.setCurrentIndex(self.patches[self.bank]['modulator_sine_table'])
		self.mcdetune.setChecked(self.patches[self.bank]['modulator_coarse_detune_enable'])
		self.mfdetuneSlider.setValue(self.patches[self.bank]['modulator_fine_detune'])
		self.mfmultSlider.setValue(self.patches[self.bank]['modulator_frequency_multiple'])
		self.mampmod.setChecked(self.patches[self.bank]['modulator_amplitude_modulation_enable'])
		self.mtlevelSlider.setValue(self.patches[self.bank]['modulator_total_level'])
		self.marateSlider.setValue(self.patches[self.bank]['modulator_attack_rate'])
		self.mdrate1Slider.setValue(self.patches[self.bank]['modulator_decay_rate_1'])
		self.mdlevelSlider.setValue(self.patches[self.bank]['modulator_decay_level'])
		self.mdrate2Slider.setValue(self.patches[self.bank]['modulator_decay_rate_2'])
		self.mrrateSlider.setValue(self.patches[self.bank]['modulator_release_rate'])
		self.msrrateSlider.setValue(self.patches[self.bank]['modulator_sustain_release_rate'])
		self.mrateksSlider.setValue(self.patches[self.bank]['modulator_rate_key_scaling'])
		self.mlevelkshSlider.setValue(self.patches[self.bank]['modulator_level_key_scaling_high'])
		self.mlevelkslSlider.setValue(self.patches[self.bank]['modulator_level_key_scaling_low'])



		#mystery_byte_1: 9 10
		#mystery_byte_2: 14 15
		#mystery_byte_3: 0 1
		#mystery_byte_4: 0 7 11
		#mystery_byte_5: 2 6 14
		#mystery_byte_6: 13 14 15
		#mystery_byte_7: 0 4 5 6 15
		#mystery_byte_8: 5 6 7 9 15
		#mystery_byte_9: 0 1 3 4 5 7 8 11

		#modulator_amplitude_modulation_enable: True or False
		#modulator_attack_rate: 0-63 
		#modulator_coarse_detune_enable: True or False
		#modulator_decay_level: 0-15
		#modulator_decay_rate_1: 0-63
		#modulator_decay_rate_2: 0-63
		#modulator_fine_detune: -7 +7, bit 4 is sign bit
		#modulator_frequency_multiple: 0-15
		#modulator_level_key_scaling_high: 0-15
		#modulator_level_key_scaling_low: 3
		#modulator_rate_key_scaling: 0-4
		#modulator_release_rate: 0-15
		#modulator_sine_table: 0-4
		#modulator_sustain_release_rate: 0-15
		#modulator_total_level: 0-99
		

if __name__ == '__main__':			
	app = QApplication([])
	p = PortaSound()
	if len(sys.argv) != 2:
		print("Usage: ", str(sys.argv[0]), "[filename]")
		exit()
	p.random_patches(sys.argv[1])
	if p.check_binary(sys.argv[1]) == True:
		if p.load_patches(sys.argv[1]) == True:
			p.write_patches(p.patches,'test.syx')
			rfile = open(sys.argv[1],'rb')
			data = rfile.read()
			rfilemd5 = hashlib.md5()
			rfilemd5.update(data)
			pfile = open('test.syx','rb')
			data = pfile.read()
			pfilemd5 = hashlib.md5()
			pfilemd5.update(data)
			if rfilemd5.digest() == pfilemd5.digest():
				print("Patch routines seem to be working!")

	else:
		 print("Something went wrong with the patch generation.")
	p.changeBank()
	p.show()
	app.exec_()

