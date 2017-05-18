# encoding = utf-8

from tkinter import *
from enum import Enum

class ActionPress(Enum):
	NOTHING = 0
	START = 1
	END = 2
	NORMAL = 3
	DELETE = 4



class Point:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

	def span(self, x , y):
		return Point(self.x + x, self.y + y)




class Item:
	def __init__(self, itype):
		self.itype = itype
		self.g = 0
		self.h = 0


	def F(self):
		return self.g + self.h

	def setGH(self, g, h):
		self.g = g 
		self.h = h

	def info(self):
		print("(%s,%d,%d)" %(self.itype, self.g, self.h))



class NormalItem(Item):
	def __init__(self, itype = "yellow"):
		super().__init__(itype)

class StartItem(Item):
	def __init__(self,itype = "green"):
		super().__init__(itype)

class GoalItem(Item):
	def __init__(self, itype = "red"):
		super().__init__( itype)

class WallItem(Item):
	def __init__(self,itype = "brown"):
		super().__init__(itype)

class OBItem(Item):
	def __init__(self, itype = "black"):
		super().__init__(itype)

class PathItem(Item):
	def __init__(self,itype = "blue"):
		super().__init__(itype)



class SearchMap:
	def __init__(self, xsize, ysize):
		self.start = None
		self.goal = None
		self.startXY = None
		self.goalXY = None
		self.xsize = int(xsize)
		self.ysize = int(ysize)
		self.items = []
		self.initMap()

	def initMap(self):
		for x in range(self.xsize-1):
			tmp = []
			for y in range(self.ysize-1):
				tmp.append(NormalItem())
			self.items.append(tmp)

	def addItem(self, newItem, x, y):
		self.items[x][y] = newItem

	def setStart(self, point):
		if self.start :
			self.items[self.startXY.x][self.startXY.y] = NormalItem() # reset
		self.startXY = point
		self.start = StartItem()
		self.items[point.x][point.y] = self.start
		self.start.info()


	def setGoal(self, point):
		if self.goal :
			self.items[self.goalXY.x][self.goalXY.y] = NormalItem() # reset
		self.goalXY = point
		self.goal = GoalItem()
		self.items[point.x][point.y] = self.goal
		self.goal.info()

	def setNormal(self, point):
		self.items[point.x][point.y] = NormalItem()
		#self.items[point.x][point.y].info()

	def SetOB(self, point):
		self.items[point.x][point.y] = OBItem()
		#self.items[point.x][point.y].info()

	def getItemByXY(self, x, y):
		return (x, y, self.items[x][y])

	def clearStart(self):
		if self.start :
			self.items[self.startXY.x][self.startXY.y] = NormalItem() # reset
		self.start = None
		self.startXY = None

	def clearGoal(self):
		if self.goal :
			self.items[self.goalXY.x][self.goalXY.y] = NormalItem() # reset
		self.goal = None
		self.goalXY = None

	def clearOB(self):
		for x in range(0, self.xsize - 1):
			for y in range(0, self.ysize - 1):
				if self.items[x][y] == type(OBItem):
					self.item[x][y] = NormalItem()

	def getStart(self):
		return (self.startXY.x, self.startXY.y, self.start)

	def getGoal(self):
		return (self.goalXY.x, self.goalXY.y, self.goal)

	def saveFile(self, filename):
		f = open(filename, 'w')
		f.write(str(len(self.items)) + '\n')
		f.write(str(len(self.items[1])) + '\n')
		f.write("%d,%d\n" %(self.start.x, self.start.y))
		f.write("%d,%d\n" %(self.goal.x, self.goal.y))

		bcount = 0
		gcount = 0
		rcount = 0
		for x in self.items:
			for y in x:
				if y.itype == 'black':
					bcount = bcount + 1
				elif y.itype == 'red':
					rcount = rcount + 1
				elif y.itype == 'green':
					gcount = gcount + 1
				f.write(y.savetype())
			f.write('\n')
		f.close()
		print("File save as %s, x grids :%d , y grids :%d, 障礙物: %d, 起點:(%d,%d), 終點:(%d,%d)" %(filename, len(self.items), len(self.items[1]),bcount, self.startItem.x, self.startItem.y, self.endItem.x, self.endItem.y))

	def loadFile(self, filename):
		f = open(filename, 'r')
		width = int(f.readline().replace('\n', ''))
		height = int(f.readline().replace('\n', ''))
		start = f.readline()
		end = f.readline()
		while True:
			line = f.readline()
			line = line.replace('\n','')
			if not line:
				break
			line = line.split(';')
			for aitem in line:
				item_split = aitem.split(',')
				print(item_split)
		f.close()

class NormalMap(SearchMap):
	def __init__(self, xsize, ysize):
		super().__init__(xsize, ysize)


class ViewMap:
	def __init__(self, width = 1000, height = 600, gridsize = 10):
		self.width = width
		self.height = height
		self.gridsize = gridsize
		self.btnstatus = ActionPress.NOTHING
		self.wgrids = int(self.width / self.gridsize)
		self.hgrids = int(self.height / self.gridsize)
		self.mis = SearchMap(self.wgrids, self.hgrids)
		
	def draw(self):
		self.root = Tk()
		self.ButtonFrame = Frame(self.root)

		#----------- button frame -----------
		self.ButtonFrame.pack()
		self.astartbtn = Button(self.ButtonFrame, text ="A*")
		self.astartbtn.grid(row=0,column=0)
		self.astartbtn.bind("<Button-1>", self.e_do_A_start)

		self.placebtn = Button(self.ButtonFrame, text ="障礙")
		self.placebtn.grid(row=0,column=1)
		self.placebtn.bind("<Button-1>", self.e_place_ob)

		self.placestartbtn = Button(self.ButtonFrame, text ="起點")
		self.placestartbtn.grid(row=0,column=2)
		self.placestartbtn.bind("<Button-1>", self.e_place_start)

		self.placeendbtn = Button(self.ButtonFrame, text ="終點")
		self.placeendbtn.grid(row=0,column=3)
		self.placeendbtn.bind("<Button-1>", self.e_place_end)


		self.clearbtn = Button(self.ButtonFrame, text ="刪除")
		self.clearbtn.grid(row=0,column=4)
		self.clearbtn.bind("<Button-1>", self.e_clear)

		self.datafield = Entry(self.ButtonFrame)
		self.datafield.grid(row=0,column=5)

		self.loadbtn = Button(self.ButtonFrame, text ="載入")
		self.loadbtn.grid(row=0,column=6)
		self.loadbtn.bind("<Button-1>", self.e_load_map)


		self.savebtn = Button(self.ButtonFrame, text ="儲存")
		self.savebtn.grid(row=0,column=7)
		self.savebtn.bind("<Button-1>", self.e_save_map)
		#----------- button frame -----------


		#----------- canvas -----------
		self.canvas = Canvas(self.root)
		self.canvas['width'] = self.width
		self.canvas['height'] = self.height
		#self.canvas['bg'] = 'yellow'
		self.canvas.bind("<Button-1>", self.e_click_place)

		self.canvas.pack()
		self.init()

		#----------- canvas -----------

		self.root.mainloop()
	#-----------  event -----------
	def e_do_A_start(self, event):
		Ag = Astar(self.mis)
		path = Ag.do()
		
		for item in path:
			if item[2].itype == "yellow":
				self.drawItems((item[0], item[1], PathItem()))
			print("(%d,%d)"%(item[0], item[1]))


	def e_place_ob(self, event):

		if self.btnstatus == ActionPress.DELETE:
			self.canvas.delete('black')
		else:
			if self.btnstatus == ActionPress.NORMAL:
				self.btnstatus = ActionPress.NOTHING
			else:
				self.btnstatus = ActionPress.NORMAL

	def e_place_start(self, event):

		if self.btnstatus == ActionPress.DELETE:
			self.canvas.delete('green')
		else:
			if self.btnstatus == ActionPress.START:
				self.btnstatus = ActionPress.NOTHING
			else:
				self.btnstatus = ActionPress.START

	def e_place_end(self, event):
		if self.btnstatus == ActionPress.DELETE:
			self.canvas.delete('red')
		else:
			if self.btnstatus == ActionPress.END:
				self.btnstatus = ActionPress.NOTHING
			else:
				self.btnstatus = ActionPress.END

	def e_click_place(self,event):
		itype = "black"
		p = Point(event.x/self.gridsize, event.y/self.gridsize)
		print("(%d,%d)" %(p.x,p.y))
		if not ((p.x == 0) or (p.y == 0) or (p.x == self.wgrids-1) or (p.y == self.hgrids - 1)):
			if self.btnstatus == ActionPress.END:
				itype = "red"
				self.canvas.delete(itype)
				self.addItem(p, itype)
				self.mis.setGoal(p)
			elif self.btnstatus == ActionPress.START:
				itype = "green"
				self.canvas.delete(itype)
				self.addItem(p, itype)
				self.mis.setStart(p)
			elif self.btnstatus == ActionPress.NORMAL:
				itype = "black"
				self.addItem(p, itype)
				self.mis.SetOB(p)


	def e_clear(self, event):
		self.canvas.delete('green')
		self.canvas.delete('red')
		self.canvas.delete('blue')
		self.canvas.delete('black')
		self.mis.initMap();

		'''
		if self.btnstatus == ActionPress.DELETE:
			self.btnstatus = ActionPress.NOTHING
			self.placebtn['text'] = "障礙"
			self.placeendbtn['text'] = "終點"
			self.placestartbtn['text'] = "起點"
		else:
			self.btnstatus = ActionPress.DELETE
			self.placestartbtn['text'] = "起點(D)"
			self.placeendbtn['text'] = "終點(D)"
			self.placebtn['text'] = "障礙(D)"
		'''

	def e_save_map(self, event):
		self.btnstatus = ActionPress.NOTHING
		#if self.datafield.get():
			#self.mis.saveFile(self.datafield.get())

	def e_load_map(self, event):
		self.btnstatus = ActionPress.NOTHING
		#if self.datafield.get():
			#self.mis.loadFile(self.datafield.get())

	#-----------  event -----------


	def drawObstacle(self,dlist):
		for g in dlist:
			self.addItem(Point(g.x,g.y))


	def init(self):
		# 格子
		for w in range(0,self.width,self.gridsize):
			self.canvas.create_line(w,0,w,self.height,fill='gray')
		# 格子
		for h in range(0,self.height,self.gridsize):
			self.canvas.create_line(0,h,self.width,h,fill='gray')

		# 邊界
		for w in range(0, self.wgrids ):
			self.addItem(Point(w,0), 'brown')
			self.addItem(Point(w,self.hgrids - 1), 'brown')

		# 邊界
		for h in range(0,self.hgrids):
			self.addItem(Point(0,h), 'brown')
			self.addItem(Point(self.wgrids - 1, h), 'brown')


		for w in range(1, self.wgrids - 1):
			for h in range(1,self.hgrids -1):
				#self.addItem(Point(w,h), 'yellow')
				self.drawItems(self.mis.getItemByXY(w,h))


	def addItem(self, p, color):
		self.canvas.create_rectangle(p.x*self.gridsize+1,p.y*self.gridsize+1,p.x*self.gridsize+self.gridsize-1,p.y*self.gridsize+self.gridsize-1, fill=color, outline=color, tag=color)


	def drawItems(self, item):
		self.canvas.create_rectangle(item[0]*self.gridsize+1,item[1]*self.gridsize+1,item[0]*self.gridsize+self.gridsize-1,item[1]*self.gridsize+self.gridsize-1, fill=item[2].itype, outline=item[2].itype, tag=item[2].itype)





class Astar:
	def __init__(self, map):
		self.map = map
		self.openList = []
		self.closeList = []
		# init
		self.openList.append(self.map.getStart())
		self.goal = self.map.getGoal()

	def findMinF(self):
		minf = 99999
		mini = 0
		for i in range(0, len(self.openList)):
			if self.openList[i][2].F() < minf:
				minf = self.openList[i][2].F()
				print(minf)
				mini = i
		return self.openList.pop(mini)


	def Manhattan(self,a):
		dx = abs(a.x - self.goal[0])
		dy = abs(a.y - self.goal[1])
		return dx + dy

	def span(self, now):
		u = self.map.getItemByXY(now[0],now[1] - 1)
		d = self.map.getItemByXY(now[0],now[1] + 1)
		l = self.map.getItemByXY(now[0] - 1,now[1])
		r = self.map.getItemByXY(now[0] + 1,now[1])
		u[2].g = d[2].g = l[2].g = r[2].g = 10

		u[2].h = self.Manhattan(Point(u[0], u[1]))
		d[2].h = self.Manhattan(Point(d[0], d[1]))
		l[2].h = self.Manhattan(Point(l[0], l[1]))
		r[2].h = self.Manhattan(Point(r[0], r[1]))

		lu = self.map.getItemByXY(now[0] - 1,now[1] - 1)
		ru = self.map.getItemByXY(now[0] + 1,now[1] - 1)
		ld = self.map.getItemByXY(now[0] - 1,now[1] + 1)
		rd = self.map.getItemByXY(now[0] + 1,now[1] + 1)
		lu[2].g = ru[2].g = ld[2].g = rd[2].g = 14

		lu[2].h = self.Manhattan(Point(lu[0], lu[1]))
		ru[2].h = self.Manhattan(Point(ru[0], ru[1]))
		ld[2].h = self.Manhattan(Point(ld[0], ld[1]))
		rd[2].h = self.Manhattan(Point(rd[0], rd[1]))
		

		if u[2].itype != 'black' and not self.isInOpenList(u) and not self.isInCloseList(u):
			self.openList.append(u)
		if d[2].itype != 'black' and not self.isInOpenList(d) and not self.isInCloseList(d):
			self.openList.append(d)
		if l[2].itype != 'black' and not self.isInOpenList(l) and not self.isInCloseList(l):
			self.openList.append(l)
		if r[2].itype != 'black' and not self.isInOpenList(r) and not self.isInCloseList(r):
			self.openList.append(r)

		if lu[2].itype != 'black' and not self.isInOpenList(lu) and not self.isInCloseList(lu):
			self.openList.append(lu)
		if ru[2].itype != 'black' and not self.isInOpenList(ru) and not self.isInCloseList(ru):
			self.openList.append(ru)
		if ld[2].itype != 'black' and not self.isInOpenList(ld) and not self.isInCloseList(ld):
			self.openList.append(ld)
		if rd[2].itype != 'black' and not self.isInOpenList(rd) and not self.isInCloseList(rd):
			self.openList.append(rd)

	def isGoalinCloseList(self):
		for i in self.closeList:
			if i[2].itype == self.goal[2].itype:
				return True
		return False

	def isInOpenList(self, item):
		for i in self.openList:
			if (item[0] == i[0]) and (item[1] == i[1]):
				return True
		return False

	def isInCloseList(self, item):
		for i in self.closeList:
			if (item[0] == i[0]) and (item[1] == i[1]):
				return True
		return False
	def do(self):
		print("--- A* ---")
		# (x, y, item)
		limitmax = 0
		while limitmax < 5000:
			limitmax +=1
			now = self.findMinF()
			self.closeList.append(now)
			if self.isGoalinCloseList():
				break

			self.span(now)
		return self.closeList






def main():
	md = ViewMap(width = 1000, height = 600, gridsize = 10)
	md.draw()



if __name__ == "__main__":
	main()


