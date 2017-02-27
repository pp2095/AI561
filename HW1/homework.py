#AI HOMEWORK 1 FINAL SUBMISSION
#GRAPH SEARCH
#read the data
def read_data():
	global ipaths, n_nodes, nodelist, lines, f,h,of
	global atype, source, goal, n_lines, n_sunday
	ipaths, nodelist, lines, h=[],[],[],[]
	f=open('input.txt','r')
	of=open('output.txt','w')
	for line in f:
		lines.append(line)
	
	#read metadata
	atype=lines[0].split()[0].rstrip('\n')
	#print atype
	source=lines[1].split()[0].rstrip('\n')
	goal=lines[2].split()[0].rstrip('\n')
	n_lines=int(lines[3].split()[0].rstrip('\n'))
	
	if source==goal:
		of.write(source+" 0")
		return
	#read traffic lines
	for i in range(4,4+n_lines):
		words=lines[i].split()
		a=words[0]
		b=words[1]
		if a not in nodelist:
			nodelist.append(a)
		if b not in nodelist:
			nodelist.append(b)
	
	#read traffic lines
	for i in range(4,4+n_lines):
		words=lines[i].split()
		a=nodelist.index(words[0])
		b=nodelist.index(words[1])
		c=int(words[2])
		ipaths.append([a,b,c])
	if atype.upper()=='BFS':
		bfs()
	elif atype.upper()=='DFS':
		dfs()
	elif atype.upper()=='UCS':
		ucs()
	elif atype.upper()=='A*':
		read_h()
		astar()

#read heuristic function
def read_h():
	n_sunday=int(lines[4+n_lines].rstrip('\n'))
	for i in range(0,n_sunday):
		h.append(-1)
	for i in range(5+n_lines,5+n_lines+n_sunday):
		#print i
		words=lines[i].split()
		a=nodelist.index(words[0])
		b=int(words[1])
		h[a]=b
		
#implement bfs
def bfs():
	
	s=nodelist.index(source)
	g=nodelist.index(goal)
	
	#nodes are of the form [state, parent, path_cost]
	open=[[s,-1,0]]
	closed=[]
	
	stop=0
	while stop==0:
		if not open:
			stop=1
		else:
			#print 'Current Q:'
			#print open
			#pop front of queue
			node=open.pop(0)
			closed.append(node)
			
			#check for goal
			if node[0]==g:
				goalnode=node
				stop=1
				continue
			else:
				children=[]
				for item in ipaths:
					if item[0]==node[0]:
						children.append([item[1],node[0],node[2]+1])
				for child in children:
					#if child not in open 
					child_in_open=False
					for item in open:
						if item[0]==child[0]:
							child_in_open=True
							break
					
					#if child not in closed:
					child_in_closed=False
					for item in closed:
						if item[0]==child[0]:
							child_in_closed=True
							break
					
					if child_in_open==False and child_in_closed==False:
						open.append(child)
	
	#print paths
	stop=0
	paths=[]
	while stop==0:
		paths.append([goalnode[0],goalnode[2]])
		if goalnode[1]==-1:
			stop=1
		for item in closed:
			if item[0]==goalnode[1]:
				goalnode=item
	
	for item in reversed(paths):
		of.write(nodelist[item[0]]+" "+str(item[1])+"\n")

#implement dfs 
def dfs():
	
	s=nodelist.index(source)
	g=nodelist.index(goal)
	
	#nodes are of the form [state, parent, path_cost]
	open=[[s,-1,0]]
	closed=[]
	
	stop=0
	while stop==0:
		if not open:
			stop=1
		else:
			#print 'Current Q:'
			#print open
			#pop rear of queue
			node=open.pop()
			closed.append(node)
			
			#check for goal
			if node[0]==g:
				goalnode=node
				stop=1
				continue
			else:
				children=[]
				for item in ipaths:
					if item[0]==node[0]:
						children.append([item[1],node[0],node[2]+1])
				for child in reversed(children):
					#if child not in open:
					child_in_open=False
					child_in_closed=False
					
					for item in open:
						if item[0]==child[0]:
							child_in_open=True
							openc=item
							break
					for item in closed:
						if item[0]==child[0]:
							child_in_closed=True
							closedc=item
							break
					if child_in_open==False and child_in_closed==False:
						open.append(child)

	#print paths
	stop=0
	paths=[]
	while stop==0:
		paths.append([goalnode[0],goalnode[2]])
		if goalnode[1]==-1:
			stop=1
		for item in closed:
			if item[0]==goalnode[1]:
				goalnode=item
	
	for item in reversed(paths):
		of.write(nodelist[item[0]]+" "+str(item[1])+"\n")

#implement ucs
def ucs():
	
	s=nodelist.index(source)
	g=nodelist.index(goal)
	
	#nodes are of the form [state, parent, path_cost]
	open=[[s,-1,0]]
	closed=[]
	stop=0
	while stop==0:
		if not open:
			stop=1
		else:
			#print 'Current Q:'
			#print open
			node=open.pop(0)
			closed.append(node)
			#check goal
			if node[0]==g:
				goalnode=node
				stop=1
				continue
			else:
				children=[]
				for item in ipaths:
					if item[0]==node[0]:
						children.append([item[1],node[0],node[2]+item[2]])
				
				for child in children:
					#check if child in open
					child_in_open=False
					for item in open:
						if item[0]==child[0]:
							child_in_open=True
							openc=item
							break
					#check if child in closed
					child_in_closed=False
					for item in closed:
						if item[0]==child[0]:
							child_in_closed=True
							closedc=item
							break
					if child_in_open==False and child_in_closed==False:
						open.append(child)
					elif child_in_open==False and child_in_closed==True:
						if child[2]<closedc[2]:
							closed.pop(closed.index(closedc))
							open.append(child)
					elif child_in_open==True and child_in_closed==False:
						if child[2]<openc[2]:
							open.pop(open.index(openc))
							open.append(child)
				open=sorted(open, key=lambda l:l[2])
	stop=0
	paths=[]
	while stop==0:
		paths.append([goalnode[0],goalnode[2]])
		if goalnode[1]==-1:
			stop=1
		for item in closed:
			if item[0]==goalnode[1]:
				goalnode=item
	
	for item in reversed(paths):
		of.write(nodelist[item[0]]+" "+str(item[1])+"\n")

#implement A*
def astar():
	
	s=nodelist.index(source)
	g=nodelist.index(goal)
	
	#nodes are of the form [state, parent, path_cost, estimated_cost]
	open=[[s,-1,0,h[s]]]
	closed=[]
	stop=0
	while stop==0:
		if not open:
			stop=1
		else:
			node=open.pop(0)
			closed.append(node)
			#check goal
			if node[0]==g:
				goalnode=node
				stop=1
				continue
			else:
				children=[]
				for item in ipaths:
					if item[0]==node[0]:
						children.append([item[1],node[0],node[2]+item[2],node[2]+item[2]+h[item[1]]])
				
				for child in children:
					#check if child in open
					child_in_open=False
					for item in open:
						if item[0]==child[0]:
							child_in_open=True
							openc=item
							break
					#check if child in closed
					child_in_closed=False
					for item in closed:
						if item[0]==child[0]:
							child_in_closed=True
							closedc=item
							break
					if child_in_open==False and child_in_closed==False:
						open.append(child)
					
					elif child_in_open==False and child_in_closed==True:
						if child[3]<closedc[3]:
							closed.pop(closed.index(closedc))
							open.append(child)
					
					elif child_in_open==True and child_in_closed==False:
						if child[3]<openc[3]:
							open.pop(open.index(openc))
							open.append(child)
				open=sorted(open, key=lambda l:l[3])
	stop=0
	paths=[]
	while stop==0:
		paths.append([goalnode[0],goalnode[2]])
		if goalnode[1]==-1:
			stop=1
		for item in closed:
			if item[0]==goalnode[1]:
				goalnode=item
	
	for item in reversed(paths):
		of.write(nodelist[item[0]]+" "+str(item[1])+"\n")

if __name__=="__main__":
	read_data()
						
				
	