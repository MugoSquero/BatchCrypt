# Batchip

![__init__](https://github.com/MugoSquero/Batchip/raw/main/welcome.png)

----------
#### Description:
You can encrypt your BATCH files with Batchip.
It simply allows you to encrypt batch files so no one can see the data, even antiviruses.

---------
There is two encryption methods:

 1. Encryption through variables
 2. Hex Encryption

#### Encryption through variables:
It's just make commands more complicated.
##### Original:
	echo hello world
##### Encrypted:
	@echo off
	setlocal EnableDelayedExpansion
	set ZA=d
	set bA=l
	set aA=h
	set bw=o
	set ZQ=e
	set Yw=c
	set dw=w
	set IA= 
	set cg=r
	cls
	%ZQ%%Yw%%aA%%bw%%IA%%aA%%ZQ%%bA%%bA%%bw%%IA%%dw%%bw%%cg%%bA%%ZA%

#### Hex Encryption:
In this encryption type, we add some hex values in the beginning of the file, what makes it unreadable but still executable!
##### Original:
	echo hello world
##### Encrypted:
	਍捥潨栠汥潬眠牯摬

So yeah, it's obviously unreadable, but still works.
Of course it's not gonna work when you paste them in the .bat file, because they are some hex values, not text or alien language.

Credit: [RavelCros_Cro](https://www.youtube.com/c/RavelCrosCro/featured)

----------

#### Installing:
	pip3 install colorama

or just...

	pip3 install -r requirements.txt

Because we need colorama for colored output.

And then, just run it.

	python3 main.py

It works both in Windows or Linux
