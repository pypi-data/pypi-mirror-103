import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

class Plot(object):

	def __init__(self,title="",xlabel="",ylabel="",xlim=[],ylim=[],figSizeX = 25.6, figSizeY=14.4, largeFontSize=50, smallFontSize = 30):

		self.fig =	plt.figure(figsize=(figSizeX,figSizeY))
		self.fig.patch.set_facecolor([1,1,1])
		self.fig.suptitle(title, fontsize=smallFontSize, fontweight='bold')

		self.ax = self.fig.add_subplot(1,1,1)
		self.ax.set_xlabel(xlabel,fontsize=largeFontSize)
		self.ax.set_ylabel(ylabel,fontsize=largeFontSize)

		self.ylim = ylim	
		self.xlim = xlim

		self.setAxisLimits(xlim,ylim)
			
		self.xlabel = xlabel
		self.ylabel = ylabel

		self.ax.grid(False)

		self.ax.spines["top"].set_edgecolor([1,1,1])
		self.ax.tick_params(top=False)

		self.ax.spines["right"].set_edgecolor([1,1,1])
		self.ax.tick_params(right=False)
		
		self.ax.tick_params(labelsize=smallFontSize)
		
		self.smallFontSize = smallFontSize
		self.largeFontSize = largeFontSize
		
		self.legendObjects = []
		
		
	def setAxisTicks(self,axis,tickPos,tickLabels):
		
		if axis.lower() == "x":
			plt.xticks(tickPos,tickLabels)
		elif axis.lower() == "y":
			plt.yticks(tickPos,tickLabels)
		else:
			print("Unknown axis string: ",axis)
			
	def setAxisLimits(self,xlim=[],ylim=[]):
		if ylim != []:
			self.ax.set_ylim(ylim)
			self.ylim = ylim	

		if xlim != []:
			self.ax.set_xlim(xlim)
			self.xlim = xlim

	def line(self, x, y, lab="",col="k",width=2.5,style="-",alpha=1.0):

		line = self.ax.plot(x, y, color=col, linewidth=width, linestyle=style,label=lab,alpha=alpha)
		
		if len(lab) > 0:
			self.legendObjects.append(line[0])

	def scatter(self, x, y, size=15, style='o', lab="", col=[0.95686,0.396078,0.15686]):

		points = self.ax.plot(x,y,style, markersize=size, color=col,label=lab)
		
		if len(lab) > 0:
			self.legendObjects.append(points[0])

	
	def fill(self,x,bottom,top,col="grey",alpha=0.5,lab=""):

		self.ax.fill_between(x, bottom, top, color=col, alpha=alpha)

		if len(lab)>0:
			self.legendObjects.append(Patch(facecolor=col, edgecolor='k',alpha=alpha,label=lab))


	def bars(self,x,bars,bottom=None,width=0.8,col="k",alpha=1,lab=""):
		
		if bottom is not None:
			barPlot = self.ax.bar(x,bars,bottom=bottom,width=0.8,color=col,alpha=alpha,label=lab)
		else:
			barPlot = self.ax.bar(x,bars,width=0.8,color=col,alpha=alpha,label=lab)
		
		self.legendObjects.append(barPlot)
		
	def boxes(self,xlabels,boxes,percentiles=[5,95]):
	   
		self.ax.boxplot(boxes,labels=xlabels,whis=percentiles,showmeans=True,meanline=True,medianprops = dict(linestyle='-', linewidth=2.5, color='r'),meanprops = dict(linestyle='--', linewidth=2.5, color='r'))
		
		self.legendObjects.append(Line2D([0], [0], marker='o', color='w', label='$B_i$',markerfacecolor='w',markeredgecolor="k", markersize=15))		
		self.legendObjects.append(Line2D([0], [0], color='r',  linewidth=2.5, linestyle="--", label='$U^{mean}$'))
		self.legendObjects.append(Line2D([0], [0], color='r',  linewidth=2.5, label='$U^{med}$'))
		
	def legend(self,loc=1,fontSize=-1):
	
		if fontSize == -1:
			fontSize = self.largeFontSize
	
		if len(self.legendObjects)>0:
			self.ax.legend(handles=self.legendObjects, loc=loc,fontsize=fontSize,framealpha=0.1,edgecolor="k")
		
	def clearAxes(self):

		self.ax.cla()
		self.ax.set_xlabel(self.xlabel)
		self.ax.set_ylabel(self.ylabel)
		
		self.setAxisLimits(self.xlim,self.ylim)

	def save(self, fileName, fileType="png",dpi=400):

		if fileType in fileName:
			self.fig.savefig(fileName,dpi=dpi,bbox_inches = 'tight')
		else:
			self.fig.savefig(fileName+"."+fileType,dpi=dpi,bbox_inches = 'tight')
			
		plt.close()

	def show(self):

		plt.show()
