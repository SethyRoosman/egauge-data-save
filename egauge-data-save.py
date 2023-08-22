from egauge.webapi.device import Capture, TriggerMode
from egauge import webapi
import time, sys, os
import csv, json
'''
Getting waveform data

eGauge JSON API → save to .csv file

L1&L2 file for each day (same directory)

Each hour save the last 5 seconds (count down in terminal in increments of a minute)

Use eGauge88570

NEXT:
abstract main to separate function
have main automate poll each hour
ISO 8601 linux time <- translate ts
save filename as DATE_L1.csv in subdirectory
json setup <- somewhat done

by Seth Rossman
'''

# egauge variables
URI = ""
USR = ""
PWD = ""
DUR = 0.0

# loading config file
if (os.path.isfile("egauge-data-config.json")):
	print("loading json config file... ", end="")
	with open("egauge-data-config.json", "r") as config_file:
		config_json = json.load(config_file)
		URI = config_json["URI"]
		USR = config_json["USR"]
		PWD = config_json["PWD"]
		DUR = config_json["DUR"]
		config_file.close()
	print("finished reading json")
else:
	print("\033[0;31mERROR:\033[0;37m] JSON config file not found")
	print("exiting...")
	exit(1)

# egauge initialization
dev = webapi.device.Device(URI, webapi.JWTAuth(USR,PWD))
cap = Capture(dev)
channel = 'L1'
# terminal output variables
width, height = os.get_terminal_size()
# csv variables
fields = ["ts", "val"]

l1_rows = []
l2_rows = []
s1_rows = []
s2_rows = []

l1_filename = "L1eGaugeWaveform.csv"
l2_filename = "L2eGaugeWaveform.csv"
s1_filename = "S1eGaugeWaveform.csv"
s2_filename = "S2eGaugeWaveform.csv"

def clear_lines(n):
	LINE_UP = '\033[1A'
	LINE_CLEAR = '\x1b[2K'

	for i in range(n):
		print(LINE_UP, end=LINE_CLEAR)

def plot_points(data_samples):
	# opens the csv files and plots
	# multiline graph

def save_to_csv():
	print()
	with open(l1_filename, "w") as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(fields)
		csvwriter.writerows(l1_rows)
		csvfile.close()
	print("finished writing data to csv file [\033[0;33m %s \033[0;37m]" % l1_filename)
	with open(l2_filename, "w") as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(fields)
		csvwriter.writerows(l2_rows)
		csvfile.close()
	print("finished writing data to csv file [\033[0;33m %s \033[0;37m]" % l2_filename)
	with open(s1_filename, "w") as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(fields)
		csvwriter.writerows(s1_rows)
		csvfile.close()
	print("finished writing data to csv file [\033[0;33m %s \033[0;37m]" % s1_filename)
	with open(s2_filename, "w") as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(fields)
		csvwriter.writerows(s2_rows)
		csvfile.close()
	print("finished writing data to csv file [\033[0;33m %s \033[0;37m]" % s2_filename)

def setup():
	# setup
	print("\033[1;32;10m", end="")
	print(dev.get("/config/net/hostname")["result"] + " is alive...")
	print(f"\033[0;37mavailable channels: {cap.available_channels}")
	cap.channels = cap.available_channels
	print("\033[1;32;10msetup complete, starting data processing\033[0;37m")

def data_collect():
	# not sure if this should stay in function
	#setup()

	print("----------------------------------------")

	data = cap.acquire(duration=DUR)
	# the len() of ts and ys should always be equal for L1 - S2
	entry_length = len(data.samples[channel].ts)

	i = 0
	start_time = time.perf_counter()
	for i in range(entry_length):
		'''
		print processing blurb
		collect 4 datapoints -> display
		erase and redo
		'''

		blurb = "processing %d/%d" % (i, entry_length) + " datapoints"
		print(blurb)

		l1_ts_val = data.samples['L1'].ts[i]
		l1_data_val = data.samples['L1'].ys[i]
		l1_rows.append([l1_ts_val, l1_data_val])
		data_point = "L1: ts %s -> %s" % (l1_ts_val, l1_data_val)
		if (len(data_point) > width):
				data_point = data_point[:width]
		print(data_point)

		l2_ts_val = data.samples['L2'].ts[i]
		l2_data_val = data.samples['L2'].ys[i]
		l2_rows.append([l2_ts_val, l2_data_val])
		data_point = "L2: ts %s -> %s" % (l2_ts_val, l2_data_val)
		if (len(data_point) > width):
				data_point = data_point[:width]
		print(data_point)

		s1_ts_val = data.samples['S1'].ts[i]
		s1_data_val = data.samples['S1'].ys[i]
		s1_rows.append([s1_ts_val, s1_data_val])
		data_point = "S1: ts %s -> %s" % (s1_ts_val, s1_data_val)
		if (len(data_point) > width):
				data_point = data_point[:width]
		print(data_point)

		s2_ts_val = data.samples['S2'].ts[i]
		s2_data_val = data.samples['S2'].ys[i]
		s2_rows.append([s2_ts_val, s2_data_val])
		data_point = "S2: ts %s -> %s" % (s2_ts_val, s2_data_val)
		if (len(data_point) > width):
				data_point = data_point[:width]
		print(data_point)

		clear_lines(5)
		time.sleep(.05)

	blurb = "processing %d/%d" % (i, entry_length) + " datapoints"
	print(blurb)
	print("L1: ts %s -> %s" % (data.samples['L1'].ts[i], data.samples['L1'].ys[i]))
	print("L2: ts %s -> %s" % (data.samples['L2'].ts[i], data.samples['L2'].ys[i]))
	print("S1: ts %s -> %s" % (data.samples['S1'].ts[i], data.samples['S1'].ys[i]))
	print("S2: ts %s -> %s" % (data.samples['S2'].ts[i], data.samples['S2'].ys[i]))

	end_time = time.perf_counter()
	time_to_complete = end_time - start_time
	print("completed processing %d datapoints in %d seconds" % (entry_length, time_to_complete))
	save_to_csv()

	plot_points(data)

def main():
	# this is where the timing loop will be
	setup()
	data_collect()

if __name__ == '__main__':
	main()
