# PSS-680
Yamaha PortaSound PSS-680 Patches

This is a program to create and verify five random patches for the Yamaha PortaSound PSS-680 as a system exclusive data dump. 

Work in progress. Just starting on a GUI.  

Python3.2+, Qt5, PySide2

To send patches, for example under linux: amidi -p hw:1,0,0 -s random_test.syx

Eventually I will integrate editing, loading and saving patches and MIDI communication. 
