'''
#### ------------------------------

 Training curve plotter(ver: 1.0)
-----------------------------------
Parse traing output and plot curve
using values like IOU, accuracy and loss.

Data:   20171207
Author: Danish
#### ------------------------------
'''

import matplotlib.pyplot as plt
import sys, random, time, numpy as np

from TrainingPlotter import Plotter

# frame work name(caffe/YOLO)
frameWork = ""

# Function to parse files
def readAndPlot(inpFile):

  # initial interval
  interv = 10

  plotter = Plotter(2, 'YOLO')

  # open file to parse
  with open(inpFile) as f:
	last_IOU, num = 0, 0
	first_itern = -1
	last_itern = -1
	prev_itern = -1
	avg_loss = -1
	train_loss = -1
	# read input file
	while True:
	  line = f.readline()
	  if not line:
		#Plot(-1, -1, -1)
		plotter.plot(-1, -1, -1)
		time.sleep(0.5)
		continue

	  # parsing for different framwork
	  if frameWork == "YOLO":
		if line.find("IOU:") > 0 and line.find(",") > 0:
		  if num == 0:
			last_IOU = 0.0
		  last_IOU += float(line[line.find("IOU:")+len("IOU:"):line.find(",")])
		  num += 1
		elif line.find("avg,") > 0 and line.find(":") > 0:
		  last_itern = int(line[:line.find(":")])
		  if line.find(",") > 0 and line.find("avg") > 0:
			avg_loss = float(line[line.find(",")+1:line.find("avg")])
			last_IOU /= num
			num = 0
	  else: # caffe
		if line.find("Iteration ") > 0 and line.find(",") > 0 and line.find("(") < 0:
		  last_itern = int(line[line.find("Iteration ")+len("Iteration "):line.find(",")])
		if line.find("Iteration ") > 0 and line.find("(") > 0 and line.find("iter/s") > 0:
		  last_itern = int(line[line.find("Iteration ")+len("Iteration "):line.find("(")])
		if line.find("Train") > 0 and line.find("loss = ") and line.find("("):
		  line = line[line.find("loss = ")+len("loss = "):line.find("(")]
		  train_loss = float(line[:line.find(" ")])
		if line.find("Test") > 0 and line.find("loss = ") > 0 and line.find("("):
		  line = line[line.find("loss = ")+len("loss = "):line.find("(")]
		  avg_loss = float(line[:line.find(" ")])
		if line.find("accuracy = ") > 0:
		  last_IOU = float(line[line.find("accuracy = ")+len("accuracy = "):])

	  if last_itern != -1 and first_itern == -1:
		first_itern = last_itern

	  if last_itern % interv != 0:
		continue

	  if frameWork == "YOLO" and num != 0:
		continue

	  #print "itern = ", last_itern, "loss = " , avg_loss, "acc = ", last_IOU, num

	  ref = (prev_itern == -1)

	  # update interval and refersh flag
	  if last_itern >= 100 and interv < 25:
		interv = 25
		ref = 25
	  elif last_itern >= 500 and interv < 50:
		interv = 50
		ref = 50
	  elif last_itern >= 750 and interv < 75:
		interv = 75
		ref = 75
	  elif last_itern >= 1000 and interv < 100:
		interv = 100
		ref = 100
	  elif last_itern >= 5000 and interv < 200:
		interv = 200
		ref = 200
	  elif last_itern >= 10000 and interv < 1000:
		interv = 1000
		ref = 1000
	  elif last_itern >= 50000 and interv < 5000:
		interv = 5000
		ref = 5000
	  elif last_itern >= 100000 and interv < 10000:
		interv = 10000
		ref = 10000


	  #plt.axis([first_itern-100, last_itern+200, 0.0, int(min(last_IOU, avg_loss)+1)])
	  plt.axis([first_itern-100, last_itern+200, 0.0, 1.0])
	  if last_itern > prev_itern and last_IOU >= 0:
		if prev_itern >= 0 and prev_itern == last_itern:
		  #Plot(-1, -1, -1)
		  plotter.plot(-1, -1, -1)
		elif last_IOU >= 0 and avg_loss >= 0:
		  if frameWork == "YOLO":
			#Plot(last_itern, last_IOU, avg_loss/10.0, "loss", ref)
			plotter.plot(last_itern, last_IOU, avg_loss, "loss")
		  #else:
			#Plot(last_itern, last_IOU, avg_loss, "val", ref)
			#Plot(last_itern, last_IOU, train_loss, "loss", ref)

		  prev_itern = last_itern

def main():

  if len(sys.argv) < 3:
	print "usage: python", sys.argv[1], "<log-file> <framework>"
	return 

  inpFile = str(sys.argv[1])

  global frameWork
  frameWork = str(sys.argv[2])

  readAndPlot(inpFile);

if __name__=="__main__":
  main()
