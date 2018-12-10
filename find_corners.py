from PIL import Image
import copy
import cv2
import numpy as np
import array
import queue
import sys
from collections import namedtuple
from collections import defaultdict

#Here begins graph and shortest path stuff
#--------------------------------------
#--------------------------------------
#--------------------------------------

Edge = namedtuple('Edge', ['vertex', 'weight'])


class GraphUndirectedWeighted(object):
	def __init__(self, vertex_count):
		self.vertex_count = vertex_count
		self.adjacency_list = [[] for _ in range(vertex_count)]
		self.edgePoints=[]

	def add_edge(self, source, dest, sPt, dPt, weight):
		#assert source < self.vertex_count
		#assert dest < self.vertex_count
		self.adjacency_list[source].append(Edge(dest, weight))
		self.adjacency_list[dest].append(Edge(source, weight))
		self.edgePoints.append((sPt,dPt))

	def get_edge(self, vertex):
		for e in self.adjacency_list[vertex]:
			yield e

	def get_vertex(self):
		for v in range(self.vertex_count):
			yield v


def dijkstra(graph, source, dest):
	q = queue.PriorityQueue()
	parents = []
	distances = []
	start_weight = float("inf")

	for i in graph.get_vertex():
		weight = start_weight
		if source == i:
			weight = 0
		distances.append(weight)
		parents.append(None)

	q.put(([0, source]))

	while not q.empty():
		v_tuple = q.get()
		v = v_tuple[1]

		for e in graph.get_edge(v):
			candidate_distance = distances[v] + e.weight
			if distances[e.vertex] > candidate_distance:
				distances[e.vertex] = candidate_distance
				parents[e.vertex] = v
				# primitive but effective negative cycle detection
				if candidate_distance < -1000:
					raise Exception("Negative cycle detected")
				q.put(([distances[e.vertex], e.vertex]))

	shortest_path = []
	end = dest
	while end is not None:
		shortest_path.append(end)
		end = parents[end]

	shortest_path.reverse()

	return shortest_path, distances[dest]





#Here begins image conversion stuff
#--------------------------------------
#--------------------------------------
#--------------------------------------

im = Image.open("roomwithoutmarkers.png")#sys.argv[1]
image = cv2.imread("roomwithoutmarkers.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray =  np.float32(gray)
dst = cv2.cornerHarris(gray, 2,3,0.04)
ret, dst = cv2.threshold(dst, 0.1*dst.max(), 255, 0)
dst = np.uint8(dst)
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray, np.float32(centroids), (10,10), (-1,-1), criteria)


startingPixel=(int(sys.argv[1]), int(sys.argv[2]))
endingPixel=(int(sys.argv[3]), int(sys.argv[4]))
nodes = []

cv2.circle(image,(startingPixel), 20, (0,255,0), -1)
cv2.circle(image,(endingPixel), 20, (255,0,255), -1)

for i in range(0, len(corners)):
	l,m = corners[i]
	item = (int(l),int(m))
	nodes.insert(i,item)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)
rows = gray.shape[0]
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, rows / 8, param1=100, param2=30, minRadius=1, maxRadius=50)
centers = []
centers.append(startingPixel)
centers.append(endingPixel)
rgb_im = im.convert("RGB")
distanceX = 0
distanceY = 0
"""
if circles is not None:
	circles = np.uint16(np.around(circles))
	for i in circles[0, :]:
		center = (i[0], i[1])
		centers.append(center)
		# circle center
		cv2.circle(image, center, 1, (0, 100, 100), 3)
		# circle outline
		radius = i[2]
		cv2.circle(image, center, radius, (255, 0, 255), 3)
else:
	print("none")
"""
centers2 = []
"""
for i in range(0, len(centers)):
	x,y = centers[i]
	r,g,b = rgb_im.getpixel((int(x+2),int(y+2)))
	if r < 100 and g >150 and b <100 :
		centers2.append(centers[i])
	elif r <100 and g > 255 and b < 100:
		centers2.append(centers[i])
"""
#for i in range(0, len(centers)):
#	print("centers")
#	print(centers[i])
centers2.append(startingPixel)
centers2.append(endingPixel)
x,y = centers2[0]

h,w = image.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
im = cv2.floodFill(image, mask, (x+20,y+20), 255, loDiff=(4,4,4,4), upDiff=(4,4,4,4))
cv2.imwrite("flooded.png", image)
im = Image.open("flooded.png")
pix = im.load()
rgb_im = im.convert("RGB")
r,g,b = rgb_im.getpixel((int(x+20),int(y+20)))
#print(r)
#print(g)
#print(b)


length = len(nodes)
finalNodes = []
intersectionNodes = []
topLeftNodes = []
topRightNodes = []
bottomLeftNodes = []
bottomRightNodes = []

#for i in range(0, len(nodes)):
	#print("nodes")
	#print(nodes[i])

#refine nodes
for i in range(0, len(nodes)):
	x,y = nodes[i]
	topLeftX = x-5
	topLeftY = y-5
	bottomLeftX = x-5
	bottomLeftY = y+5
	topRightX = x+5
	topRightY = y-5
	bottomRightX = x+5
	bottomRightY = y+5
	rNode, gNode, bNode = rgb_im.getpixel((int(x),int(y)))
	rLeft, gLeft, bLeft = rgb_im.getpixel((int(topLeftX), int(topLeftY)))
	rRight, gRight, bRight = rgb_im.getpixel((int(bottomLeftX), int(bottomLeftY)))
	rTop, gTop, bTop = rgb_im.getpixel((int(topRightX), int(topRightY)))
	rBottom, gBottom, bBottom = rgb_im.getpixel((int(bottomRightX), int(bottomRightY)))
	for m in range(i, len(nodes)):
		l,p = nodes[m]
		if abs(x-l)<10 and abs(y-p)<10:
			pass
		else:
			##if rNode == r == rLeft == rRight == rTop == rBottom and gLeft == g == gRight == gLeft == gTop == gBottom and bLeft == b == bRight == bLeft == bTop == bBottom:
			##	pass
			if rLeft == r and gLeft == g and bLeft == b:
				nodes[i] = (int(x), int(y))
				finalNodes.append(nodes[i])
			elif rRight == r and gRight == g and bRight == b:
				nodes[i] = (int(x), int(y))
				finalNodes.append(nodes[i])
			elif rTop == r and gTop == g and bTop == b:
				nodes[i] = (int(x), int(y))
				finalNodes.append(nodes[i])
			elif rBottom == r and gBottom == g and bBottom == b:
				nodes[i] = (int(x), int(y))
				finalNodes.append(nodes[i])
			else:
				pass

for i in range(0, len(finalNodes)):
	x,y = finalNodes[i]
	#cv2.circle(image, (x,y), 18, (255,0,255),-1)

finalNodes.sort()

for i in range(0, len(finalNodes)):
	x,y = finalNodes[i]
	topLeftX = x-5
	topLeftY = y-5
	topRightX = x+5
	topRightY = y-5
	bottomLeftX = x-5
	bottomLeftY = y+5
	bottomRightX = x+5
	bottomRightY = y+5
	topLeftR, topLeftG, topLeftB = rgb_im.getpixel((int(topLeftX),int(topLeftY)))
	topRightR, topRightG, topRightB = rgb_im.getpixel((int(topRightX),int(topRightY)))
	bottomLeftR, bottomLeftG, bottomLeftB = rgb_im.getpixel((int(bottomLeftX),int(bottomLeftY)))
	bottomRightR, bottomRightG, bottomRightB = rgb_im.getpixel((int(bottomRightX),int(bottomRightY)))
	if finalNodes[i] not in bottomRightNodes and topLeftR == topRightR == bottomLeftR == r and topLeftG == topRightG == bottomLeftG == g and topLeftB == topRightB == bottomLeftB == b:
		bottomRightNodes.append(finalNodes[i])
	elif finalNodes[i] not in bottomLeftNodes and topLeftR == topRightR == bottomRightR == r and topLeftG == topRightG == bottomRightG == g and topLeftB == topRightB == bottomRightB == b:
		bottomLeftNodes.append(finalNodes[i])
	elif finalNodes[i] not in topRightNodes and topLeftR == bottomLeftR == bottomRightR == r and topLeftG == bottomLeftG == bottomRightG == g and topLeftB == bottomLeftB == bottomRightB == b:
		topRightNodes.append(finalNodes[i])
	elif  finalNodes[i] not in topLeftNodes and topRightR == bottomRightR == bottomLeftR == r and topRightG == bottomRightG == bottomLeftG ==g and topRightB == bottomRightB == bottomLeftB == b:
		topLeftNodes.append(finalNodes[i])

"""
print("Top Left Nodes")
for i in range(0, len(topLeftNodes)):
	print(topLeftNodes[i])
print("Top Right Nodes")
for i in range(0, len(topRightNodes)):
	print(topRightNodes[i])
print("Bottom Left Nodes")
for i in range(0, len(bottomLeftNodes)):
	print(bottomLeftNodes[i])
print("Bottom Right Nodes")
for i in range(0, len(bottomRightNodes)):
	print(bottomRightNodes[i])
"""
actualNodes = []
"""
for i in range(0, len(finalNodes)-1):
	x,y = finalNodes[i]
	l,p = finalNodes[i+1]
	if abs(x-l)<20 and abs(y-p)<150:
		distanceX = int(abs(y-p)/2)
		print(distanceX)
		distanceY = int(abs(y-p)/2)
		print(distanceY)
		i = len(finalNodes)
	elif abs(y-p)<20 and abs(x-l)<150:
		distanceX = int(abs(x-l)/2)
		print(distanceX)
		dinstaceY = int(abs(x-l)/2)
		print(distanceY)
		i = len(finalNodes)
"""
x,y = finalNodes[0]
l = 0
p = 0
for i in range(1, len(finalNodes)):
	g,h = finalNodes[1]
	if abs(x-g)<20 or abs(y-h)<20:
		l = g
		p = h
		i = len(finalNodes)+1

"""
distanceX = abs(int(l)-int(x))
distanceY = abs(int(p)-int(y))
if distanceY<20:
	distanceX = int(distanceX/2)
	distanceY = distanceX
else:
	distanceY = int(distanceY/2)
	distanceX = distanceY
"""
distanceX = 50
distanceY = 50

for i in range(0, len(finalNodes)):
	x,y = finalNodes[i]
	for m in range(i, len(finalNodes)):
		l,p = finalNodes[m]
		if abs(l-x)<40 and abs(y-p)<150 and finalNodes[i] in topLeftNodes:
			actualNodes.append(((x+distanceX),(y+distanceY)))
		if abs(l-x)<40 and abs(y-p)<150 and finalNodes[i] in topRightNodes:
			actualNodes.append(((x-distanceX), (y+distanceY)))
		if abs(p-y)<40 and abs(x-l)<150 and finalNodes[i] in bottomRightNodes:
			actualNodes.append(((x-distanceX),(y-distanceY)))
		if abs(p-y)<40 and abs(x-l)<150  and finalNodes[i] in bottomLeftNodes:
			actualNodes.append(((x+distanceX),(y-distanceY)))


#print("actualNodes")
#for i in range(0, len(actualNodes)):
#	print(actualNodes[i])

realFinal = []
otherTry = []
realFinal.append(actualNodes[0])
for i in range(0, len(actualNodes)):
	if actualNodes[i] in realFinal:
		pass
	else:
		realFinal.append(actualNodes[i])

#print("real final")
#print(len(realFinal))

actualNodes = realFinal
f = 0
#print("actual Nodes length")
#print(len(actualNodes))
actualNodesCopy = copy.deepcopy(actualNodes)
i=0
m=0

for i in range(0, len(actualNodes)):
	x,y = actualNodes[i]
	for m in range(i+1, len(actualNodes)):
		l,p = actualNodes[m]
		if abs(x-l)<20 and abs(y-p)<20:
			actualNodes[m] = actualNodes[i]


actualNodes = list(set(actualNodes))
#print(len(actualNodes))
"""
otherTry.append(actualNodes[0])
for i in range(0, len(actualNodes)):
	x,y = actualNodes[i]
	if otherTry:
		l,p = otherTry[f]
		if abs(x-l)<25 and abs(y-p)<25:
			print("x,l,y,p")
			print(x)
			print(l)
			print(y)
			print(p)
			pass
		else:
			otherTry.append(actualNodes[i])
			f+=1
	else:
		otherTry.append(actualNodes[i])
"""
#print(len(otherTry))
#for i in range(0, len(otherTry)):
#	print("other try")
#	print(otherTry[i])

for i in range(0, len(actualNodes)):
	x,y = actualNodes[i]
	cv2.circle(image, (x,y), 18, (255,0,255),-1)
otherTry = actualNodes
centers.sort()
otherTry.sort()


final = []
finalWithLetters = []
x,y = centers[1]
final.append((x,y))
letter = "A"
finalWithLetters.append(((x,y),"A"))
finalNodes=[]
finalNodes.append((x,y))
for i in range(0, len(otherTry)):
	x,y = otherTry[i]
	final.append((x,y))
	letter = chr(ord(letter)+1)
	finalWithLetters.append(((x,y), letter))
	finalNodes.append((x,y))

x,y = centers[0]
final.append((x,y))
letter = chr(ord(letter)+1)
finalWithLetters.append(((x,y), letter))
finalNodes.append((x,y))
'''
print("Nodes")
for i in range(0, len(finalWithLetters)):
	print(finalWithLetters[i])
'''
edges = []
edgeDir=[]
"""
for i in range(0, len(final)-1):
	x,y = final[i]
	l,p = final[i+1]
	edges.append(((x,y),(l,p)))
	if((x-l in range(-50,50)) and (y>p)):
		edgeDir.append("North")
	elif((x-l in range(-50,50)) and (y<p)):
		edgeDir.append("South")
	elif((y-p in range(-50,50)) and (x>l)):
		edgeDir.append("West")
	elif((y-p in range(-50,50)) and (x<l)):
		edgeDir.append("East")
"""
finalEdgesWithLetters = []
finalEdges = []
#print("len final")
#print(len(final))
#print("len final with letters")
#print(len(finalWithLetters))
for i in range(0, len(final)):
	x,y = final[i]
	pts, letterA = finalWithLetters[i]
	for m in range(0, len(final)):
		l,p = final[m]
		pts, letterB = finalWithLetters[m]
		edges.append(((x,y),(l,p)))
		if((int(x)-int(l) in range(-50,50)) and (int(y)>int(p))):
			edgeDir.append("North")
			edgeHere = edges.pop(len(edges)-1)
			finalEdges.append((edges.pop(len(edges)-1), "North"))
			finalEdgesWithLetters.append((letterA,letterB))
			#cv2.line(image, (x,y), (l,p), (255,0,255), 4, 8, 0)
		elif((int(x)-int(l) in range(-50,50)) and (int(y)<int(p))):
			finalEdges.append((edges.pop(len(edges)-1), "South"))
			edgeDir.append("South")
			finalEdgesWithLetters.append((letterA, letterB))
			#cv2.line(image, (x,y), (l,p), (255,0,255), 4, 8, 0)
		elif((int(y)-int(p) in range(-50,50)) and (int(x)>int(l))):
			finalEdges.append((edges.pop(len(edges)-1), "West"))
			edgeDir.append("West")
			finalEdgesWithLetters.append((letterA, letterB))
			#cv2.line(image, (x,y), (l,p), (255, 0, 255), 4, 8, 0)
		elif((int(y)-int(p) in range(-50,50)) and (int(x)<int(l))):
			edgeDir.append("East")
			finalEdges.append((edges.pop(len(edges)-1), "East"))
			finalEdgesWithLetters.append((letterA, letterB))
			#cv2.line(image, (x,y), (l,p), (255,0,255), 4, 8, 0)


imageH = image.shape[0]
imageW = image.shape[1]

#print(" Final Edges ")
for i in range(0, len(edgeDir)):
	#print(finalEdges[i])
	#print("Direction: ",edgeDir[i])
	pts, direc= finalEdges[i]
	pt1, pt2 = pts

tryThisEdges = []
notTheseEdges = []
howAboutThese = []
for i in range(0, len(finalEdges)):
	pts, direc = finalEdges[i]
	pt1, pt2 = pts
	for m in range(i, len(finalEdges)):
		pts, direc2 = finalEdges[m]
		pt3, pt4 = pts
		if pt2==pt4 and direc==direc2:

			tryThisEdges.append(finalEdges[m])
			notTheseEdges.append(finalEdges[i])


for i in range(0,len(finalEdges)):
	if finalEdges[i] in notTheseEdges:
		pass
	elif finalEdges[i] in tryThisEdges:
		howAboutThese.append(finalEdges[i])
	else:
		howAboutThese.append(finalEdges[i])


actualEdges = []

'''for i in range(0, len(finalEdges)):
	print ("finalEdges: ",finalEdges[i])'''

for i in range(0, len(finalEdges)):
	pts, direc = finalEdges[i]
	pt1, pt2 = pts
	x,y = pt1
	l,p = pt2
	run = abs(int(x)-int(l))
	rise = abs(int(y)-int(p))
	p1 = (0,0)
	p2 = (0,0)
	p3 = (0,0)
	p4 = (0,0)
	p5 = (0,0)
	if y<p and run<40:
		points = int(rise/5)
		p1 = y+points
		p2 = p1+points
		p3 = p2+points
		p4 = p3+points
		p5 = p4+points
		p1r, p1g, p1b = rgb_im.getpixel((int(x),int(p1)))
		p2r, p2g, p2b = rgb_im.getpixel((int(x), int(p2)))
		p3r, p3g, p3b = rgb_im.getpixel((int(x), int(p3)))
		p4r, p4g, p4b = rgb_im.getpixel((int(x), int(p4)))
		p5r, p5g, p5b = rgb_im.getpixel((int(x), int(p5)))
		if p2r==p3r==p4r==0 and p2g==p3g==p4g==0 and p2b==p3b==p4b==255:
			actualEdges.append(finalEdges[i])
	elif y>p and run<40:
		points = int(rise/5)
		p1 = y-points
		p2 = p1-points
		p3 = p2-points
		p4 = p3-points
		p5 = p4-points
		p1r, p1g, p1b = rgb_im.getpixel((int(x),int(p1)))
		p2r, p2g, p2b = rgb_im.getpixel((int(x), int(p2)))
		p3r, p3g, p3b = rgb_im.getpixel((int(x), int(p3)))
		p4r, p4g, p4b = rgb_im.getpixel((int(x), int(p4)))
		p5r, p5g, p5b = rgb_im.getpixel((int(x), int(p5)))
		if p2r==p3r==p4r==0 and p2g==p3g==p4g==0 and p2b==p3b==p4b==255:
			actualEdges.append(finalEdges[i])
	elif x<l and rise<40:
		points = int(run/5)
		p1 = x+points
		p2 = p1+points
		p3 = p2+points
		p4 = p3+points
		p5 = p4+points
		p1r, p1g, p1b = rgb_im.getpixel((int(p1),int(y)))
		p2r, p2g, p2b = rgb_im.getpixel((int(p2),int(y)))
		p3r, p3g, p3b = rgb_im.getpixel((int(p3),int(y)))
		p4r, p4g, p4b = rgb_im.getpixel((int(p4),int(y)))
		p5r, p5g, p5b = rgb_im.getpixel((int(p5),int(y)))
		if p2r==p3r==p4r==0 and p2g==p3g==p4g==0 and p2b==p3b==p4b==255:
			actualEdges.append(finalEdges[i])
	elif x>l and rise<40:
		points = int(run/5)
		p1 = x-points
		p2 = p1-points
		p3 = p2-points
		p4 = p3-points
		p5 = p4-points
		p1r, p1g, p1b = rgb_im.getpixel((int(p1), int(y)))
		p2r, p2g, p2b = rgb_im.getpixel((int(p2), int(y)))
		p3r, p3g, p3b = rgb_im.getpixel((int(p3), int(y)))
		p4r, p4g, p4b = rgb_im.getpixel((int(p4), int(y)))
		p5r, p5g, p5b = rgb_im.getpixel((int(p5), int(y)))
		if p2r==p3r==p4r==0 and p2g==p3g==p4g==0 and p2b==p3b==p4b==255:
			actualEdges.append(finalEdges[i])


actualFinalEdges = copy.deepcopy(actualEdges)
for i in range(0, len(actualEdges)):
	pts, direc = actualEdges[i]
	pt1, pt2 = pts
	x1,y1 = pt1
	x2, y2 = pt2
	for m in range(0, len(actualEdges)):
		ptsb, direcb = actualEdges[m]
		pts1b, pts2b = ptsb
		l1,p1 = pts1b
		l2,p2 = pts2b
		if pt2 == pts2b and direc==direcb:
			length1X= abs(int(x1)-int(x2))
			length2X= abs(int(l1)-int(l2))
			length1Y= abs(int(y1)-int(y2))
			length2Y = abs(int(p1)-int(p2))
			if abs(length1X-length2X)<20:
				if length1Y>length2Y:
					actualEdges[i] = actualEdges[m]
				else:
					actualEdges[m] = actualEdges[i]
			elif abs(length1Y-length2Y)<20:
				if length1X>length2X:
					actualEdges[i] = actualEdges[m]
				else:
					actualEdges[m] = actualEdges[i]


r = 255
g = 0
b = 255
list(set(actualEdges))



'''for i in range(0, len(actualEdges)):
	print ("actualEdges: ",actualEdges[i])'''

newList=[]
for i in actualEdges:
	if i not in newList:
		newList.append(i)
actualActual = []

for i in range(0, len(newList)):
	color = list(np.random.choice(range(256), size=3))
	pts, direc = newList[i]
	#actualActual.append(pts)
	pt1, pt2 = pts
	x,y = pt1
	l,p = pt2
	if abs(x-l)<20:
		weight = abs(y-p)
	else:
		weight = abs(x-l)

	actualActual.append(pts)
	r,g,b = color
	r = int(r)
	g = int(g)
	b = int(b)
	#cv2.line(image, (x,y), (l,p), (r,g,b), 4, 8, 0)

if ((startingPixel,endingPixel)) in actualActual:
	actualActual.remove((startingPixel,endingPixel))
	#print("\n\nSTART AND END PIXEL EDGE FOUND\n\n")
if ((endingPixel,startingPixel)) in actualActual:
	actualActual.remove((endingPixel,startingPixel))
	#print("\n\nSTART AND END PIXEL EDGE FOUND\n\n")

'''for i in range(0, len(newList)):
	print ("newList: ",newList[i])'''
path = []
startingPoint = centers[0]
endingPoint = centers[0]

#time to put the nodes from the image into a graph

edgesWithStartAndEnd = []
g = GraphUndirectedWeighted(len(final))
for i in range(0,len(final)):
	pt = final[i]
	for m in range(i, len(final)):
		pt2 = final[m]

		if (pt, pt2) in actualActual or (pt2, pt) in actualActual:
			x,y = pt
			l,p = pt2
			if abs(x-l)<20:
				weight = abs(y-p)
			else:
				weight = abs(x-l)
			edgesWithStartAndEnd.append((pt, pt2, i, m))
			g.add_edge(i,m,(x,y),(l,p),weight)

'''for i in range(0, len(final)):
	print ("Nodes: ",final[i])
for i in range(0, len(actualActual)):
	print ("Edges: ",actualActual[i])
print("\n\n\n")'''


"""
#Validate input is good--------------------------------------
validIn=0;
while validIn!=1:
	start=int(input("Enter the starting node: "))
	end=int(input("Enter the destination node: "))
	if start==end:
		print("\033[H\033[J")
		print("Start and finish cannot be the same")
	elif start not in range(0,(len(final))) or end not in range(0,(len(final))):
		print("\033[H\033[J")
		print("Input(s) are not in range")
	else:
		print("\033[H\033[J")
		validIn=1;
"""


#Shortest path and non-clever directions
#shortest_path, distance = dijkstra(g, 0, len(final)-1)
shortest_path, distance = dijkstra(g, len(final)-1,0)

edgeDirFinal=[]
for i in range(0, len(shortest_path)-1):
	x,y = final[shortest_path[i]]
	l,p = final[shortest_path[i+1]]
	edges.append(((x,y),(l,p)))
	if((x-l in range(-50,50)) and (y>p)):
		cv2.line(image, (x,y), (l,p), (255, 0, 255), 4, 8, 0)
		edgeDirFinal.append("North")
	elif((x-l in range(-50,50)) and (y<p)):
		cv2.line(image, (x,y), (l,p), (255, 0, 255), 4, 8, 0)
		edgeDirFinal.append("South")
	elif((y-p in range(-50,50)) and (x>l)):
		cv2.line(image, (x,y), (l,p), (255, 0, 255), 4, 8, 0)
		edgeDirFinal.append("West")
	elif((y-p in range(-50,50)) and (x<l)):
		cv2.line(image, (x,y), (l,p), (255, 0, 255), 4, 8, 0)
		edgeDirFinal.append("East")

leftAndRights = []
for i in range(0, len(edgeDirFinal)-1):
	direction1 = edgeDirFinal[i]
	direction2 = edgeDirFinal[i+1]
	if direction1=="South" and direction2 == "West":
		leftAndRights.append("R")
	elif direction1=="South" and direction2 == "East":
		leftAndRights.append("L")
	elif direction1=="North" and direction2 =="West":
		leftAndRights.append("L")
	elif direction1=="North" and direction2 =="East":
		leftAndRights.append("R")
	elif direction1 =="East" and direction2 =="South":
		leftAndRights.append("R")
	elif direction1 == "East" and direction2 == "North":
		leftAndRights.append("L")
	elif direction1 == "West" and direction2 =="South":
		leftAndRights.append("L")
	elif direction1 == "West" and direction2 =="North":
		leftAndRights.append("R")
	else:
		leftAndRights.append("S")

open("directions.txt", "w").close()
f=open("directions.txt", "a+")
for i in range(0, len(leftAndRights)):
	f.write(""+leftAndRights[i]+"\n")
	#print(leftAndRights[i])

f.close()
image[dst>0.1*dst.max()] = [255,255,0]
#cv2.imshow("image", image)
#cv2.imshow("gray", gray)
cv2.imwrite('finalWithNodes.png',image)
#cv2.waitKey(15500)
cv2.destroyAllWindows
