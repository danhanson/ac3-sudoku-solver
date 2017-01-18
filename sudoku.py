
from itertools import combinations,chain
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import json
import sys

def notEqual(a,b):
	return a != b

class Variable:
	def __init__(self,name,domain):
		self.name = name
		self.domain = domain
		self.constraints = []

	def addConstraint(self,cons,var):
		self.constraints.append((cons,var))

	def getArcs(self,exclude=None):
		return ((cons, var, self) for (cons,var) in self.constraints if var is not exclude)

	def __repr__(self):
		return '('+'|'.join(str(val) for val in self.domain)+')'

def solve(initVals):

	# initialize the variables and arrange them by row, column, and square
	rows = tuple(tuple(Variable((i,j),{initVals[(i,j)]} if (i,j) in initVals else set(xrange(1,10)))
	                  for j in xrange(9)) for i in xrange(9))
	columns = tuple(tuple(rows[i][j] for i in xrange(9)) for j in xrange(9))

	squares = tuple(
		tuple(
			rows[i][j] for i in xrange(y,y+3) for j in xrange(x,x+3)
		) for x in xrange(0,7,3) for y in xrange(0,7,3)
	)

	# add not equal constraints for elements in same column or row
	for row in chain(rows,columns):
		for (x,y) in combinations(row,2):
			x.addConstraint(notEqual, y)
			y.addConstraint(notEqual, x)

	# add not equal constraints for elements in same sub square
	for square in squares:
		for (x,y) in combinations(square,2):
			if(x.name[0] == y.name[0] or x.name[1] == y.name[1]):
				continue
			x.addConstraint(notEqual,y)
			y.addConstraint(notEqual,x)

	# initislize the queue using the initial values
	queue = [arc for arc in chain.from_iterable(rows[i][j].getArcs() for (i,j) in initVals)]
	while len(queue) > 0:
		con,x,y = queue.pop()
		toRemove = []
		for xVal in x.domain:
			if all(not con(xVal,yVal) for yVal in y.domain):
				toRemove.append(xVal)
		if len(toRemove) > 0:
			for xVal in toRemove:
				x.domain.remove(xVal)
			if len(x.domain) == 0:
				return False
			else:
				queue.extend(x.getArcs(y))

	return [[(next(iter(rows[i][j].domain)) if len(rows[i][j].domain) == 1 else None) for j in xrange(9)] for i in xrange(9)]

class SudokuServerHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		conLen = int(self.headers['Content-Length'])
		body = json.loads(self.rfile.read(conLen))
		initVals = {(int(val['row']),int(val['col'])):int(val['value']) for val in body}
		solution = solve(initVals)
		response = json.dumps(solution)
		#response = json.dumps([{'row':row,'col':col,'val':val} for ((row,col),val) in solution.iteritems()])
		self.send_response(200)
		self.send_header('Content-Length',len(response))
		self.send_header('Content-Type','application/json')
		self.end_headers()
		self.wfile.write(response)
		self.wfile.close()

	def do_GET(self):
		path = None
		cType = None
		if(self.path == '/'):
			path = 'sudoku.html'
			cType = 'text/html'
		else:
			path = '.'+self.path
			if path.endswith('.js'):
				cType = 'text/javascript'
			elif path.endswith('.css'):
				cType = 'text/css'
		try:
			f = open(path)
			self.send_response(200)
			self.send_header('Content-Type',cType)
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
		except IOError:
			self.send_error(404,'File Not Found: ' + path)
		finally:
			self.wfile.close()

class SudokuServer(HTTPServer):
	def __init__(self,port):
		HTTPServer.__init__(self,('',port),SudokuServerHandler)

def main(argv):
	SudokuServer(int(argv[1])).serve_forever()

if __name__ == "__main__":
	main(sys.argv)

