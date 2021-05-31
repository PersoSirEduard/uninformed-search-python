import math
import sys

class Node:
	def __init__(self, state, action, parent):
		self.state = state
		self.parent = parent
		self.action = action

class StackFrontier:

	# Depth first search

	def __init__(self):
		self.frontier = []
		self.explored = []

	def add(self, node):
		self.frontier.append(node) # Add node to end of the frontier array
	
	def remove(self):
		if self.empty():
			raise Exception("Frontier is empty")
		node = self.frontier[-1] # Get last node
		self.explored.append(node) # Add removed node to explored list
		self.frontier = self.frontier[:-1] # Remove last node from frontier list
		return node

	def getFrontierSize(self): # Get size of frontier list
		return len(self.frontier)

	def empty(self): # Verify if the frontier list is empty
		return len(self.frontier) == 0

	def contains_state_frontier(self, state): # Verify if a state is part of the frontier list
		return any(node.state == state for node in self.frontier)
	
	def contains_state_explored(self, state): # Verify if a state is part of the explored list
		return any(node.state == state for node in self.explored)

class QueueFrontier(StackFrontier):

	# Breath first search

	def remove(self):
		if self.empty():
			raise Exception("Frontier is empty")
		node = self.frontier[0] # Get first node
		self.explored.append(node) # Add removed node to explored list
		self.frontier = self.frontier[1:] # Remove last node from frontier list
		return node

class Maze:
	def __init__(self):
		self.maze = [] # Single dimension array
		self.size = (0, 0)
		self.solution = []

	def loadFile(self, file): # Load maze file

		# '#': Wall
		# ' ': Path
		# 'A': Initial position
		# 'B': Destination

		y_size = 0
		with open(file) as f:
			for line in f:
				y_size += 1
				for char in line:
					if char == '\n': continue
					self.maze.append(char)
		self.size = (int(len(self.maze) / y_size), y_size) # Get map size
	
	def getStates(self, node): # Get possible states from actions
		states = []
		for x in range(-1, 2):
			for y in range(-1, 2):
				if abs(x) == 1 and abs(y) == 1: continue # Corner cells are ignored
				if x == 0 and y == 0: continue # Self cell is ignored
				if node.state[0] + x >= self.size[0]: continue # Outside right border cell is ignored
				if node.state[0] + x < 0: continue # Outside left border cell is ignored
				if node.state[1] + y >= self.size[1]: continue # Outside bottom border cell is ignored
				if node.state[1] + y < 0: continue # Outside top border cell is ignored
				if self.getChar((node.state[0] + x, node.state[1] + y)) == '#': continue # Walls are ignored

				states.append((node.state[0] + x, node.state[1] + y))
		return states

	def getCharPosition(self, char): # Get position of a specific char ('A' or 'B')
		for i in range(0, len(self.maze)):
			cell = self.maze[i]
			if cell == char:
				x = i % self.size[0]
				y = int(math.floor(i / self.size[0]))
				return (x, y)

	def getChar(self, position): # Get the char at a specific position
		return self.maze[position[1] * self.size[0] + position[0]]

	def printMaze(self, includeSolution=False, writeToFile=False): # Print out the maze
		result = ""
		tempMaze = self.maze
		if includeSolution: # Draw solution path
			for s in self.solution:
				if tempMaze[s[1] * self.size[0] + s[0]] == " ": # If the path is not A or B, replace space with '*'
					tempMaze[s[1] * self.size[0] + s[0]] = "*"
		for y in range(self.size[1]):
			result += ''.join(tempMaze[y*self.size[0]: y*self.size[0] + self.size[0]]).replace('#', '█') + "\n"
		print(result)

		if writeToFile: # Save to text file
			with open('result.txt', 'w') as writer:
				writer.write(result.replace('█', '#'))

	def solve(self):
		frontier = StackFrontier()
		initialState = self.getCharPosition("A")
		frontier.add(Node(state=initialState, action=None, parent=None))

		while True:

			if frontier.empty():
				raise Exception("No solution was found")

			node = frontier.remove()

			
			if node.state == self.getCharPosition("B"): # Found a solution
				print("Solved!")
				while node.parent != None:
					self.solution.append(node.state)
					node = node.parent
				self.solution.reverse()
				return self.solution

			for child_state in self.getStates(node): # Get all possible states from actions
				child_action = (child_state[0] - node.state[0], child_state[1] - node.state[1])
				child_node = Node(state=child_state, action=child_action, parent=node)

				if not frontier.contains_state_frontier(child_node.state) and not frontier.contains_state_explored(child_node.state): # Check if child node was not already in the frontier or the explored arrays
					frontier.add(child_node)

	
if __name__ == '__main__':

	maze = Maze()
	maze.loadFile(sys.argv[1])
	maze.printMaze(includeSolution=False)
	solution = maze.solve()
	maze.printMaze(includeSolution=True, writeToFile=True)
	# print(solution)