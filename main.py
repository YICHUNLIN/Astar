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

	def newPoint(self, x , y):
		return Point(self.x + x, self.y + y)


class Item:
	def __init__(self, point, itype):
		self.point = point
		self.itype = itype
		self.g = 0
		self.h = 0

	def savetype(self):
		return "%s,%s,%s;" % (self.point.x, self.point.y, self.itype)

	def F(self):
		return self.g + self.h

	def setGH(self, g, h):
		self.g = g 
		self.h = h


class NormalItem(Item):
	def __init__(self, point, itype = "yellow"):
		super().__init__(point.itype)

class StartItem(Item):
	def __init__(self, point, itype = "green"):
		super().__init__(point, itype)

class GoalItem(Item):
	def __init__(self, point, itype = "red"):
		super().__init__(point, itype)

class WallItem(Item):
	def __init__(self, point, itype = "brown"):
		super().__init__(point, itype)

class OBItem(Item):
	def __init__(self, point, itype = "black"):
		super().__init__(point, itype)

class PathItem(Item):
	def __init__(self, point, itype = "blue"):
		super().__init__(point, itype)

class ItemFactory:
	def generateNormal(self, point):
		return NormalItem(point)
	
	def generateStart(self, point):
		return StartItem(point)

	def generateGoal(self, point):
		return GoalItem(point)

	def generateWall(self, point):
		return WallItem(point)

	def generateOB(self, point):
		return OBItem(point)

	def generatePath(self, point):
		return PathItem(point)


class SearchMap:
	def __init__(self, xsize, ysize):
		self.start = None
		self.goal = None
		self.xsize = int(xsize)
		self.ysize = int(ysize)
		self.items = []
		for x in range(self.xsize):
			tmp = []
			for y in range(self.ysize):
				tmp.append(Item(Point(x,y),'yellow'))
			self.items.append(tmp)

	def addItem(self, newItem, x, y):
		self.items[x][y] = newItem

	def setStart(self, point):
		 ItemFactory().generateStart(point)

class NormalMap(SearchMap):
	def __init__(self, xsize, ysize):
		super().__init__(xsize, ysize)




class MapItems(SearchMap):
	def __init__(self):
		super().__init__()


	def addline(self, itemLine):
		self.items.append(itemLine)

	def output(self):
		for ils in self.items:
			for item in ils:
				print(item.savetype())

	def setItem(self, x, y, itype):
		self.items[x][y].itype = itype

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

	def getItemByXY(self, P):
		if(P.x > 0 and P.x < len(self.items)) and (P.y > 0 and P.y < len(self.items[1])):
			return self.items[P.x][P.y]
		return None

	def setItemByXY(self, P, value):
		if(P.x > 0 and P.x < len(self.items)) and (P.y > 0 and P.y < len(self.items[1])):
			self.items[P.x][P.y].itype = value
			return self.items[P.x][P.y]
		return None

	def getStartEnd(self):
		return (self.getItemByXY(self.start), self.getItemByXY(self.goal))



class Map:
	def __init__(self,mis = None, width = 1000, height = 600, gridsize = 10):
		self.width = width
		self.height = height
		self.gridsize = gridsize
		self.btnstatus = ActionPress.NOTHING
		self.mis = mis
		self.wgrids = int(self.width / self.gridsize)
		self.hgrids = int(self.height / self.gridsize)
		
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
		Ag = Astart(self.mis)
		Ag.do()
		pass

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
				#self.mis.endItem = None
				self.addItem(Point(p.x,p.y), itype)
				#self.mis.setItem(p.x,p.y,itype)
				#self.mis.endItem = p
			elif self.btnstatus == ActionPress.START:
				itype = "green"
				self.canvas.delete(itype)
				#self.mis.startItem = None
				self.addItem(Point(p.x,p.y), itype)
				#self.mis.setItem(p.x,p.y,itype)
				#self.mis.startItem = p
			elif self.btnstatus == ActionPress.NORMAL:
				itype = "black"
				self.addItem(Point(p.x,p.y), itype)
				#self.mis.setItem(p.x,p.y,itype)


	def e_clear(self, event):

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
			#tmp = []
			for h in range(1,self.hgrids -1):
				#tmp.append(Item(Point(w,h), 'yellow'))
				self.addItem(Point(w,h), 'yellow')
			#self.mis.addline(tmp)
		#self.mis.output()


	def addItem(self, p, color):
		self.canvas.create_rectangle(p.x*self.gridsize+1,p.y*self.gridsize+1,p.x*self.gridsize+self.gridsize-1,p.y*self.gridsize+self.gridsize-1, fill=color, outline=color, tag=color)


class Searching:
	def __init__(self, map):
		self.map = map


	def do(self):
		pass


class Astart(Searching):
	def __init__(self, map):
		super().__init__(map)
		self.openList = []
		self.closeList = []
		(self.start, self.end) = self.map.getStartEnd()
		self.start.g = 0
		self.start.h = self.Manhattan(self.start)
		self.openList.append(self.start)


	def Manhattan(self, item):
		dx = abs(item.point.x - self.end.point.x)
		dy = abs(item.point.y - self.end.point.y)
		return 0


	def findMinF(self):
		min = 9999
		mini = 0
		for i in range(0,len(self.openList)):
			if self.openList[i].F() < min:
				min = self.openList[i].F()
				mini = i
		return self.openList.pop(mini)

	def isGoal(self):
		for it in self.closeList:
			if it.itype == "red":
				return True
		return False

	def do(self):
		print("--- A* ---")

		while True:

			now = self.findMinF()
			now.itype = "blue"
			print("(%d,%d)" %(now.point.x, now.point.y))
			self.closeList.append(now)
			if self.isGoal():
				break
			# 上
			u = self.map.getItemByXY( now.point.newPoint(0, -1))
			# 下
			d = self.map.getItemByXY( now.point.newPoint(0, 1))
			# 左
			l = self.map.getItemByXY( now.point.newPoint(-1, 0))
			# 右
			r = self.map.getItemByXY( now.point.newPoint(0, -1))
			# 左上
			lu = self.map.getItemByXY( now.point.newPoint(-1, -1))
			# 右上
			ru = self.map.getItemByXY( now.point.newPoint(1, -1))
			# 左下
			ld = self.map.getItemByXY( now.point.newPoint(-1, 1))
			# 右下
			rd = self.map.getItemByXY( now.point.newPoint(1, 1))
			u.g = d.g = l.g = r.g = 10
			lu.g = ru.g = ld.g = rd.g = 14

			u.h = self.Manhattan(u)
			d.h = self.Manhattan(d)
			l.h = self.Manhattan(l)
			r.h = self.Manhattan(r)
			lu.h = self.Manhattan(lu)
			ru.h = self.Manhattan(ru)
			ld.h = self.Manhattan(ld)
			rd.h = self.Manhattan(rd)
			self.openList.append(u)
			self.openList.append(d)
			self.openList.append(l)
			self.openList.append(r)
			self.openList.append(lu)
			self.openList.append(ru)
			self.openList.append(ld)
			self.openList.append(rd)








def main():
	#mis = MapItems()
	mis = NormalMap(1000/10, 600/10)
	md = Map(mis=mis, width = 1000, height = 600, gridsize = 10)
	md.draw()



if __name__ == "__main__":
	main()













