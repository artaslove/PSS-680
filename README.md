# PSS-680
Yamaha PortaSound PSS-680 Patches

This is a linux-based editor librarian for the Yamaha PortaSound PSS-680, using system exclusive data dumps. 

Requirements: Python3.2+, Qt5, PySide2, mido

![Alt text](/screenshot.png?raw=true "Work in Progress")

To Do:

- patch naming: using unusused bytes? with some trickery, about 13 characters of ascii are available. with CP359, maybe 20 characters? The keyboard has patch descriptions longer than 13 characters written on it. Abbreiviate or 6 bit ascii????
- send and trigger after edit checkbox (it's on by default now)
- preferences
- draw the envelopes

