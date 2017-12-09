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

# frame work name(caffe/YOLO)
frameWork = ""

# points to be plotted
plot_points = [[], [], [], [], [], []]

# color for curves
clr = ["green", "red", "orange"]

# function to plot points on graph
def Plot(x, y, z, p="all", refresh=0):
  
  if refresh: # refresh the graph to adjust interval
    # clear graph
    plt.clf()

    plt.title('%s training-plot' % frameWork)
    plt.ion()
    plt.xlabel('Iterations')


    ax = plt.subplot(111)
    xr = np.arange(0)
    lStr = ["acc", "train-loss", "val-loss"]
    nParams = 3
    if frameWork == "YOLO":
      lStr[0] = "IOUx10"
      nParams = 2

    for i in xrange(nParams):
      ax.plot(xr, i * xr, label='%s' % lStr[i], color=clr[i])
      

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.05,
                 box.width, box.height * 0.95])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1),
          fancybox=True, shadow=True, ncol=5)

    # remove points that no longer fits the new interval
    if refresh != 0:
      i = 0;
      while i < len(plot_points):
        j = 1
        while j  < len(plot_points[i]):
          if plot_points[i][j] % refresh != 0:
            #print "deleting:", plot_points[i][j], plot_points[i+1][j]
            del plot_points[i][j]
            del plot_points[i+1][j]
          else:
            j += 1
        i += 2

  # Add new points to polt
  if x >= 0 and y >= 0 and z >= 0:
    if p == "loss":
      plot_points[0].append(x)
      plot_points[1].append(y)
      plot_points[2].append(x)
      plot_points[3].append(z)
    else:
      plot_points[0].append(x)
      plot_points[1].append(y)
      plot_points[4].append(x)
      plot_points[5].append(z)

  # plot accuracy / IOU
  if len(plot_points[0]) > 0 and plot_points[1] > 0:
    plt.plot(plot_points[0], plot_points[1], color=clr[0])

  # plot loss
  if p == "loss":
    if len(plot_points[2]) > 0 and plot_points[3] > 0:
      plt.plot(plot_points[2], plot_points[3], color=clr[1])
  else:
    if len(plot_points[4]) > 0 and plot_points[5] > 0:
      plt.plot(plot_points[4], plot_points[5], color=clr[2])

  plt.pause(0.05)

# Function to parse files
def readAndPlot(inpFile):

  # initial interval
  interv = 10

  # open file to parse
  with open(inpFile) as f:
    last_IOU = -1
    first_itern = -1
    last_itern = -1
    prev_itern = -1
    avg_loss = -1
    train_loss = -1
    # read input file
    while True:
      line = f.readline()
      if not line:
        Plot(-1, -1, -1)
        time.sleep(0.5)
        continue
  
      # parsing for different framwork
      if frameWork == "YOLO":
        if line.find("IOU:") > 0 and line.find(",") > 0:
          last_IOU = float(line[line.find("IOU:")+len("IOU:"):line.find(",")])
        elif line.find("avg,") > 0 and line.find(":") > 0:
          last_itern = int(line[:line.find(":")])
          if line.find(",") > 0 and line.find("avg") > 0:
            avg_loss = float(line[line.find(",")+1:line.find("avg")])
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

      #print "itern = ", last_itern, "loss = " , avg_loss, "acc = ", last_IOU

      if last_itern != -1 and first_itern == -1:
        first_itern = last_itern

      if last_itern % interv != 0:
        continue

      ref = (prev_itern == -1)

      # update interval and refersh flag
      if last_itern >= 500 and interv < 50:
        interv = 50
        ref = 50
      elif last_itern >= 1000 and interv < 100:
        interv = 100
        ref = 100
      elif last_itern >= 10000 and interv < 1000:
        interv = 1000
        ref = 1000

      #plt.axis([first_itern-100, last_itern+200, 0.0, int(min(last_IOU, avg_loss)+1)])
      plt.axis([first_itern-100, last_itern+200, 0.0, 1.0])
      if last_itern > prev_itern and last_IOU >= 0:
        if prev_itern >= 0 and prev_itern == last_itern:
          Plot(-1, -1, -1)
        elif last_IOU >= 0 and avg_loss >= 0:
          if frameWork == "YOLO":
            Plot(last_itern, last_IOU, avg_loss/10.0, "loss", ref)
          else:
            Plot(last_itern, last_IOU, avg_loss, "val", ref)
            Plot(last_itern, last_IOU, train_loss, "loss", ref)

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

