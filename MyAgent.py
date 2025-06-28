from Game2048 import *

class Player(BasePlayer):
	def __init__(self, timeLimit):
		BasePlayer.__init__(self, timeLimit)

		self._nodeCount = 0
		self._parentCount = 0
		self._childCount = 0
		self._depthCount = 0
		self._count = 0

	def findMove(self, state):
		self._count += 1
		actions = self.moveOrder(state)
		depth = 1
		while self.timeRemaining():
			self._depthCount += 1
			self._parentCount += 1
			self._nodeCount += 1
			print('Search depth', depth)
			
			best = -1000
			for a in actions:
				if not self.timeRemaining(): return
				result, score = state.result(a)
				v = self.value(result, depth-1)
				if v is None: return
				if v > best:
					best = v
					bestMove = a
					
			self.setMove(bestMove)
			print('\tBest value', best, bestMove)

			depth += 1
			
	def value(self, state, depth):
		self._nodeCount += 1
		self._childCount += 1

		if state.gameOver():
			return state.getScore()
			
		actions = self.moveOrder(state)

		if depth == 0:
			return self.heuristic(state)

		self._parentCount += 1
		
		best = -10000
		for a in actions:
			if not self.timeRemaining(): return None
			result, score = state.result(a)
			v = self.value(result, depth-1)
			if v is None: return None
			if v > best:
				best = v

		return best

	def heuristic(self, state):
		score     = state.getScore()
		board     = state._board
		empties   = board.count(0)
		max_tile  = max(board)

		corners     = (0, 3, 12, 15)
		corner_idx  = board.index(max_tile)
		corner_bonus = max_tile * 200 if corner_idx in corners else 0

		return score + empties * 100 + corner_bonus
		
	def moveOrder(self, state):
		return state.actions()

	def stats(self):
		print(f'Average depth: {self._depthCount/self._count:.2f}')
		print(f'Branching factor: {self._childCount / self._parentCount:.2f}')
