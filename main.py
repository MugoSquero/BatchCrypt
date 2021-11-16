# -*- coding: utf-8 -*-
import base64
import re
from colorama import Fore, Style
from platform import system
from os import system as cmd

if system() == "Windows":
    cmd("color")


print(Fore.RED +
"""__________         __         .__    .__        
\______   \_____ _/  |_  ____ |  |__ |__|_____  
 |    |  _/\__  \\   __\/ ___\|  |  \|  \____ \ 
 |    |   \ / __ \|  | \  \___|   Y  \  |  |_> >
 |______  /(____  /__|  \___  >___|  /__|   __/ 
        \/      \/          \/     \/   |__|    """ + Style.RESET_ALL)

filePath = input(Fore.CYAN + "\033[4m\n\nEnter Batch File Path You Want To Encrypt: \033[0m" + Style.RESET_ALL)
with open(filePath, "r", encoding='utf-8') as subject:
    batchLines = subject.readlines()

result = open("result.bat", "w", encoding='utf-8')
result.close()
result = open("result.bat", "a", encoding='utf-8')
result.write("setlocal EnableDelayedExpansion\n")

countLines = 0

for bline in batchLines:
    if re.search("%", bline) and bline.count("%") == 2:
        newline = bline.replace("%", "%%")
        bline = "cmd /c " + newline
        batchLines[countLines] = bline
    countLines += 1
countLines = 0

for bline in batchLines:
    if bline[0] == ':':
        cani = False


def kodOlustur():
    global result
    for batch in batchLines:
        for line in batch:
            if line == '':
                continue
            elif line == '\n':
                continue
            if line == '%':
                cmd = ''
            elif line == '>':
                cmd = ''
            else:
                lineb = line.encode("utf-8")
                ln64b = base64.b64encode(lineb)
                ln64 = ln64b.decode('utf-8')
                ln64 = ln64.replace('=', '')
                cmd = ("set {}={}".format(ln64, line))
                result.write(cmd)
                result.write('\n')
    
    result.close()
    
    with open("result.bat", "r", encoding='utf-8') as rread:
        rlines = rread.readlines()
        dlines = set(rlines)
        with open("result.bat", "w", encoding='utf-8') as result:
            result.write("@echo off\n")
        result = open("result.bat", "a", encoding='utf-8')
        for i in dlines:
            result.write(i)
    
    result.write("cls\n")


def encodeIt():
    global result
    for batch in batchLines:
        if batch[0] == ':':
            cani = False
        else:
            cani = True
        if cani == False:
            result.write(batch)
            continue
        for line in batch:
            if line == '%':
                ln64 = '%'
            else:
                lineb = line.encode('utf-8')
                ln64b = base64.b64encode(lineb)
                ln64 = ln64b.decode('utf-8')
                ln64 = ln64.replace('=', '')
            if ln64 == 'Cg':
                exc = '\n'
            # elif ln64 == 'JQ':
            #     exc = ''
            elif ln64 == 'Pg':
                exc = '>'
            elif ln64 == 'Jg':
                exc = '&'
            elif ln64 == 'PA':
                exc = '<'
            elif ln64 == 'IQ':
                exc = '!'
            else:
                if ln64 != '%':
                    exc = "%" + ln64 + "%"
                else:
                    exc = "%"
    
            result.write(exc)


kodOlustur()
encodeIt()
result.close()

with open("result.bat", "rb") as batbytes:
    bb = batbytes.read().hex()
add = 'fffe0d0a'
with open("result.bat", "wb") as batg:
    batg.write(bytes.fromhex(add + bb))

print("Encrypted Batch File Saved in 'result.bat'!")
