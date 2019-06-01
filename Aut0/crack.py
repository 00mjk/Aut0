# Made by Sam Mahoney
# For Testing Only

import sys
import subprocess
import time
import os

def listdict():
    caps = os.listdir("D:/CMUI-Lab/Captured/")
    for cap in caps:
        print(cap)
        newcap = cap.replace("^%", "-")
        path = "D:/CMUI-Lab/Captured/"
        newcappath = path + newcap
        cappath = path + cap
        print(newcappath)
        try:
            os.rename(cappath, newcappath)
        except Exception as e:
            print(e)
        print(cap)
        cracker(cap)
    print("[!] Thank you for using Aut0 Cracker")


def cracker(cap):
    print(cap)
    print("[!] Attempting To Crack {} ".format(cap))
    hashcat = ("hashcat64.exe -m 2500 -o D:/CMUI-Lab/Captured/{0}.txt D:/CMUI-Lab/Captured/{0} {1}").format(cap, "D:/WiFi/Wordlists/big/huge.txt")
    process = subprocess.Popen(hashcat.split(), cwd = "D:/WiFi/hashcat/", shell=True)
    process.communicate()
    print("---------------------------------------")

listdict()