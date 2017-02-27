import time
class BoardState:
	
	x_score=0
	o_score=0
	my_score=0
	#initialize states with the values of its depth, board, state, maximum dimensions, current player and parent
	def __init__(self,depth,state,now_play,parent,made_move):
		self.depth=depth
		self.state=state
		self.now_play=now_play
		if self.now_play=='X':
			self.opponent='O'
		else:
			self.opponent='X'
		self.parent=parent
		self.childnodes=[]
		self.made_move=made_move
	
	# return the current x and o scores of the board
	def return_scores(self):
		for i in range(0,dim):
	 		for j in range(0,dim):
	 			if self.state[i][j]=='X':
	 				self.x_score+=board[i][j]
	 			elif self.state[i][j]=='O':
	 				self.o_score+=board[i][j]
	 	if next_play=='X':
	 		return self.x_score-self.o_score
	 	else:
	 		return self.o_score-self.x_score

	#if possible, stake the current player at a given location [i,j]
	def stake(self,i,j):
		if (i>=0 and j>=0 and i<dim and j<dim):
			if self.state[i][j]=='.':
				nextstate=[x[:] for x in self.state]
				nextstate[i][j]=self.now_play
				colalph=str(unichr(65+j))
				rowno=str(i+1)
				return [nextstate,colalph+rowno+" Stake"]
	
	#create all stakes of the current player iteratively
	def can_stake(self):
		neighbors=[]
		for i in range(0,dim):
			for j in range(0,dim):
				neighbors.append(self.stake(i,j))
		return neighbors
	
	#once  a raid has been played, check if any neighbors of the new square have been captured 
	#and if yes, change its captor
	def raid_neighbors(self,nextstate,newr,newc):
		#check new neighbours, if they are opponents, capture them
		#check one square up
		if newr-1>=0 and nextstate[newr-1][newc] != self.now_play and nextstate[newr-1][newc]!='.':
			nextstate[newr-1][newc]=self.now_play
		#check one square down
		if newr+1<dim and nextstate[newr+1][newc] != self.now_play and nextstate[newr+1][newc]!='.':
			nextstate[newr+1][newc]=self.now_play
		#check one square left
		if newc-1>=0 and nextstate[newr][newc-1] != self.now_play and nextstate[newr][newc-1] !='.':
			nextstate[newr][newc-1]=self.now_play
		#check one square right
		if newc+1<dim and nextstate[newr][newc+1] != self.now_play and nextstate[newr][newc+1] !='.':
			nextstate[newr][newc+1]=self.now_play
		return nextstate

	#given a current state, check if a raid is possible by the current player and generate the intermediate state
	#before conquering any opponents
	'''
	def can_raid(self):
		neighbors=[]
		for i in range(0,dim):
			for j in range(0,dim):
				if self.state[i][j]==self.now_play:
					
					if i-1>=0 and self.state[i-1][j]=='.':
						nextstate=[x[:] for x in self.state]
						nextstate[i-1][j]=self.now_play
						colalph=str(unichr(65+j))
						rowno=str(i-1+1)
						neighbors.append([self.raid_neighbors(nextstate,i-1,j),colalph+rowno+" Raid"])
						
					if j-1>=0 and self.state[i][j-1]=='.':
						nextstate=[x[:] for x in self.state]
						nextstate[i][j-1]=self.now_play
						colalph=str(unichr(65+j-1))
						rowno=str(i+1)
						neighbors.append([self.raid_neighbors(nextstate,i,j-1),colalph+rowno+" Raid"])
											
					if j+1<dim and self.state[i][j+1]=='.':
						nextstate=[x[:] for x in self.state]
						nextstate[i][j+1]=self.now_play
						colalph=str(unichr(65+j+1))
						rowno=str(i+1)
						neighbors.append([self.raid_neighbors(nextstate,i,j+1),colalph+rowno+" Raid"])
											
					if i+1<dim and self.state[i+1][j]=='.':
						nextstate=[x[:] for x in self.state]
						nextstate[i+1][j]=self.now_play
						colalph=str(unichr(65+j))
						rowno=str(i+1+1)
						neighbors.append([self.raid_neighbors(nextstate,i+1,j),colalph+rowno+" Raid"])
						
		return neighbors
	
	'''
	def can_raid(self):
		neighbors=[]
		for i in range(0,dim):
			for j in range(0,dim):
				if self.state[i][j]=='.':
					
					if (i-1>=0 and self.state[i-1][j]==self.now_play) or (j-1>=0 and self.state[i][j-1]==self.now_play) or (j+1<dim and self.state[i][j+1]==self.now_play) or (i+1<dim and self.state[i+1][j]==self.now_play):
						nextstate=[x[:] for x in self.state]
						nextstate[i][j]=self.now_play
						colalph=str(unichr(65+j))
						rowno=str(i+1)
						neighbors.append([self.raid_neighbors(nextstate,i,j),colalph+rowno+" Raid"])					
		return neighbors
	
	
	#given a current state, check if any children are possible by either staking or raiding	
	def get_children(self):
		if self.depth!=limit:
			children_states=[]
			children=[]
			raid_children=self.can_raid()
			stake_children=self.can_stake()
			children_states=stake_children+raid_children
			for item in children_states:
				if item==None:
					continue
				child=BoardState(self.depth+1,item[0],self.opponent,self,item[1])
				self.childnodes.append(child)
				print child.return_scores(), child.made_move
			return self.childnodes

	#traverse through all children of a given node, and its children till you reach the maximum depth
	
	def find_min(self):
		x=self.get_children()
		if self.depth==limit or not x:
			return self.return_scores()
		else:
			v=float("inf")
			for item in x:
				v=min(v,item.find_max())
			return v

	def find_max(self):
		x=self.get_children()
		if self.depth==limit or not x:
			return self.return_scores()
		else:
			v=-float("inf")
			for item in x:
				v=max(v,item.find_min())
			return v
	
	def minimax(self):
		v=-float('inf')
		consider=None
		for item in self.get_children():
			i=item.find_min()
			if v<i:
				consider=item
				v=i
		return [consider.made_move,consider.state]

	def alpha_beta(self):
		v=-float('inf')
		consider=None
		for item in self.get_children():
			i=item.ab_find_min(-float('inf'),float('inf'))
			if v<i:
				consider=item
				v=i
		return [consider.made_move,consider.state]
		
	def ab_find_max(self,alpha,beta):
		x=self.get_children()
		if self.depth==limit or not x:
			return self.return_scores()
		else:
			v=-float("inf")
			for item in x:
				v=max(v,item.ab_find_min(alpha,beta))
				if v>=beta:
					return v
				alpha=max(alpha,v)
			return v

	def ab_find_min(self,alpha,beta):
		x=self.get_children()
		if self.depth==limit or not x:
			return self.return_scores()
		else:
			v=float("inf")
			for item in x:
				v=min(v,item.ab_find_max(alpha,beta))
				if v<=alpha:
					return v
				beta=min(beta,v)
			return v

#main program with given input
input=open('input.txt','r')
start= time.time()
lines=[]
for line in input:
	lines.append(line)
global dim, next_play, limit, board
dim=int(lines[0].rstrip('\n'))
algo=lines[1].rstrip('\n')
next_play=lines[2].rstrip('\n')
limit=int(lines[3].rstrip('\n'))


board=[]
for i in range(4,4+dim):
	row=[]
	points=lines[i].split()
	for x in points:
		row.append(int(x))
	board.append(row)

state=[]
for i in range(4+dim,4+dim+dim):
	row=[]
	for x in lines[i].strip('\n'):
		row.append(x)
	state.append(row)
initial_state=BoardState(0,state,next_play,None,"start")
of=open('output.txt','w')
if algo=='MINIMAX':
	ans=initial_state.minimax()
	of.write(ans[0]+'\n')
	for item in ans[1]:
		row=""
		for col in item:
			row+=col
		of.write(row+'\n')
else:
	ans=initial_state.alpha_beta()
	of.write(ans[0]+'\n')
	for item in ans[1]:
		row=""
		for col in item:
			row+=col
		of.write(row+'\n')

print time.time()-start
