
import numpy as np
import matplotlib.pyplot as plt

class Plotter():
	
	def __init__(self, nYaxis=1, fw='YOLO'):

		t = np.arange(0.01, 10.0, 0.01)
		data1 = np.exp(t)
		data2 = np.sin(2 * np.pi * t)
		
		self.fig, self.ax1 = plt.subplots()

		plt.grid(color='b', linestyle='--', linewidth=1)

		color = 'tab:red'
		self.ax1.set_xlabel('iterations', color='tab:blue')
		self.ax1.set_ylabel('loss', color=color)
		self.ax1.tick_params(axis='y', labelcolor=color)
		
		# instantiate a second axes that shares the same x-axis
		self.ax2 = self.ax1.twinx()  

		color = 'tab:green'
		self.ax2.set_ylabel('IOU', color=color)
		self.ax2.tick_params(axis='y', labelcolor=color)

		#clr = ["green", "red", "orange"]
		#ax = self.fig.add_subplot(111)
		#xr = np.arange(0)
		#labelStr = ["acc", "train-loss", "val-loss"]
		#nParams = 3
		#if fw == 'YOLO':
		#  labelStr[0] = "IOU"
		#  labelStr[1] = "loss"
		#  nParams = 2

		#for i in range(nParams):
		#	ax.plot(xr, i * xr, label='%s' % labelStr[i], color=clr[i])

		#ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1),
		#      fancybox=True, shadow=True, ncol=5)

		self.plot_points = [[], [], [], [], [], []]


	def get_points(self, x, y, z, ref=0):

		#remove points  that no longer fits the new interval
		if ref != 0 and False:
			i = 0;
			while i < len(self.plot_points):
				j = 1
				while j  < len(self.plot_points[i]):
					diff = abs(self.plot_points[i][j] - self.plot_points[i][0])
					if self.plot_points[i][j] % ref != 0 or diff > 500.0:
						#print "deleting:", plot_points[i][j], plot_points[i+1][j]
						del self.plot_points[i][j]
						del self.plot_points[i+1][j]
			  		else:
						j += 1
					i += 2

		#Add new points to plot
		if x >= 8000 and y >= 0 and z >= 0:
			self.plot_points[0].append(x)
			self.plot_points[1].append(y)
			self.plot_points[2].append(x)
			self.plot_points[3].append(z)
			self.plot_points[4].append(x)
			self.plot_points[5].append(z)


	def plot(self, x, y, z, p='iou'):

		self.get_points(x, y, z, 100)

		color = ['tab:green', 'tab:red', 'tab:blue']

		self.ax2.plot(self.plot_points[0], self.plot_points[1], 'bo-', color=color[0], linewidth=0.7, markersize=3)
		self.ax1.plot(self.plot_points[2], self.plot_points[3], 'bo-', color=color[1], linewidth=0.7, markersize=3)

		self.fig.tight_layout()

		plt.pause(0.01)
