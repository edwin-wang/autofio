#! /usr/bin/env python

'''
      If you have any question, please feel free to contact
      me at wym@marvell.com.
                                          Yangming Wang
'''

import os
import sys
import time

# ####################################################################
# vars definition
# ####################################################################

# total_runtime = 72 # in hour
runtime_var = 30 # in second
ramp_time = 5 # in second
rw_var = ["read", "write", "randread", "randwrite"]
bs_var = ["512", "1k", "4k", "128k", "512k", "1m", "8m"]
iodepth_var = ["64"]

# ####################################################################
# find installed fio
# ####################################################################

if not os.path.exists("/usr/local/bin/fio") | os.path.exists("/usr/bin/fio"):
    print "fio isn't installed. Can not find fio at /usr/local/bin/fio and /usr/bin/fio."
    sys.exit()

# ####################################################################
# start running
# ####################################################################

print "\n\n"
print "========== fio performance ==========\n"
print "Please input your device name, such as: sdb, sdc, sdd. (split with comma)"
device_name = raw_input(":")
print "\n"

device_name_list = device_name.split(",")
# print device_name_list
for device_name_item in device_name_list:
    # print device_name_item
    if not os.path.exists("/dev/" + device_name_item):
        print device_name_item, "not exist!!!"
        sys.exit()

# ####################################################################
# calc runtime
# ####################################################################

device_num = len(device_name_list)
# runtime_var = total_runtime*60*60/len(bs_var)/len(rw_var)/len(iodepth_var)

# ####################################################################
# clear previous log
# ####################################################################

os.system("rm log* -fr")
os.makedirs("log")

# ####################################################################
# show current config
# ####################################################################

# print "Total Runtime\t\t: ", total_runtime, "hr"
print "Device Count\t\t: ", device_num
print "Device Name\t\t: ", ", ".join(device_name_list)
print "RW Policy\t\t: ", ", ".join(rw_var)
print "Block Size\t\t: ", ", ".join(bs_var)
print "IO Depth\t\t: ", ", ".join(iodepth_var)
print "Separate Runtime\t: ", runtime_var, " seconds"


# ####################################################################
# write system info log
# ####################################################################

present_time = time.strftime("%Y-%m-%d-%H-%M-%S")
log_details = "sys_log_details_" + present_time + ".txt"

f = open("sys_log_details_" + present_time + ".txt", "w")
f.write("Running Spec\n")
# f.write("Total Runtime\t\t: " + str(total_runtime) + "hr\n")
f.write("Device Count\t\t: " + str(device_num) + "\n")
f.write("Device Name\t\t: " + ", ".join(device_name_list) + "\n")
f.write("RW Policy\t\t: " + ", ".join(rw_var) + "\n")
f.write("Block Size\t\t: " + ", ".join(bs_var) + "\n")
f.write("IO Depth\t\t: " + ", ".join(iodepth_var) + "\n")
f.write("Separate Runtime\t: " + str(runtime_var) + "seconds\n")
f.write("\n\n\n")
f.flush()
f.close()

os.system("cat /proc/cpuinfo                      >> " + log_details)
os.system("uname -a                               >> " + log_details)
os.system("lspci -vtn                             >> " + log_details)
os.system("lspci -v                               >> " + log_details)
os.system("lsmod                                  >> " + log_details)
os.system("lsscsi                                 >> " + log_details)
os.system("echo \"Queue Depth\"                   >> " + log_details)
os.system("cat /sys/block/sd?/device/queue_depth  >> " + log_details)

# ####################################################################
# running
# ####################################################################

opt_device_name = " --name=/dev/" + " --name=/dev/".join(device_name_list)
print "\n===== Now testing HDDs:  " + opt_device_name

for rw_item in rw_var:
    for bs_item in bs_var:
        for iodepth_item in iodepth_var:
            present_time = time.strftime("%Y-%m-%d-%H-%M-%S")
            print "\nRW: " + rw_item + "  Block Size: " + bs_item + "  IO Depth: " + iodepth_item
            fio_opt = " --ioengine=libaio --prio=0 --numjobs=1 --direct=1 --fadvise_hint=0 --bwavgtime=5000 --time_based --norandommap "
            fio_opt += " --rw=" + rw_item
            fio_opt += " --bs=" + bs_item
            fio_opt += " --iodepth=" + iodepth_item
            fio_opt += " --runtime=" + str(runtime_var)
            fio_opt += " --output=" + "log/" + present_time + "_" + rw_item + "_" + bs_item + "_" + iodepth_item + ".txt"
            fio_opt += opt_device_name
            os.system("fio " + fio_opt)
            time.sleep(ramp_time)

# ####################################################################
# fio performance finished
# ####################################################################

print "========== fio performance finished ==========\n"






