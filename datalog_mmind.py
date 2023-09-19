
import itertools
import random
import pandas as pd
from pyDatalog import pyDatalog	# after: pip install pyDatalog : Successfully installed pyDatalog-0.17.4
import pytholog as pl	# after: pip install pytholog		Successfully installed more-itertools-10.1.0 pytholog-2.4.1


# https://sites.google.com/site/pydatalog/Online-datalog-tutorial

terms = '''
Red_CodePeg, Green_CodePeg, Blue_CodePeg, Fucsia_CodePeg, Yellow_CodePeg, Azure_CodePeg,
Secret,
Hole1, Hole2, Hole3, Hole4,
Black_KeyPeg, White_KeyPeg,
GuessList,
FeedbackList,
X, Y
'''
# They must start with an upper-case letter

terms1line = "".join(terms.split('\n'))

if False:
	pyDatalog.create_terms(terms1line)
	# https://en.wikipedia.org/wiki/Mastermind_(board_game)
	# Turns

	#Secret = ['Red','Yellow','Blue','Blue']
	Secret[0] = 'Red'
	Secret[1] = 'Yellow'
	Secret[2] = 'Blue'
	Secret[3] = 'Blue'
	print(Secret[X]==Y)
	print(Secret[X]=='Yellow')

#
# https://pypi.org/project/pytholog/
# https://github.com/MNoorFawi/pytholog
# https://github.com/mnoorfawi/traversing-graphs-using-pytholog

# Prolog takes facts and rules. A fact or a rule has a predicate which in “likes(noor, sausage)” is “likes” and in “friend(X, Y)” is “friend”. 
# Rules have “Left Hand Side (LHS)” which has a predicate and “Right Hand Sides (RHS)” or “goals” to be searched to answer the queries about the rules. 
# LHS and RHS in a rule are separated with “:-”. Each predicate has “Terms”. 
# Prolog uses lowercased variables to describe “constant values” and uppercased values to describe “variables” that need to be updated from the query.

# Let’s take an example: likes(noor, sausage) is a fact which has likes as a predicate and (noor and sausage) as terms. 
# friend(X, Y) :- +(X = Y), likes(X, Z), likes(Y, Z) is a rule which defines that two persons are considered friends if they like the same dish. 
# This rule has an LHS friend(X, Y) and RHS or goals [+(X = Y), likes(X, Z), likes(Y, Z)]. The comma separating the goals means and while ; will mean or. 
# Variables in the fact are lowercased meaning they are truths and cannot change. While in a rule they are Uppercased meaning they need to be changed while in a query.


city_color = pl.KnowledgeBase("city_color")
city_color([
    "different(red, green)",
    "different(red, blue)",
    "different(green, red)", 
    "different(green, blue)",
    "different(blue, red)", 
    "different(blue, green)",
    "coloring(A, M, G, T, F) :- different(M, T),different(M, A),different(A, T),different(A, M),different(A, G),different(A, F),different(G, F),different(G, T)"
])

print(city_color.query(pl.Expr("coloring(Alabama, Mississippi, Georgia, Tennessee, Florida)"), cut = True))
# [{'Alabama': 'green', 'Mississippi': 'blue', 'Georgia': 'blue', 'Tennessee': 'red', 'Florida': 'red'}]

#

print('- ALB - 1 -')
mm_gamez = pl.KnowledgeBase("mm_gamez")
KBmultilineText='''
# facts - (lowercased variables)
different(red, green)
different(red, blue)
different(green, red)
different(green, blue)
different(blue, red)
different(blue, green)
# rules = LHS predicate := RHS goal
coloring(A, M, G, T, F) :- different(M, T),different(M, A),different(A, T),different(A, M),different(A, G),different(A, F),different(G, F),different(G, T)
'''

rawKBList = KBmultilineText.split('\n')
commentstrippedKBList = [ s.split('#')[0] for s in rawKBList ]
trimmedKBList = [ s.strip() for s in commentstrippedKBList ]
cleanKBList = list(filter(lambda x: len(x)>0, trimmedKBList))
print(cleanKBList)

assert len(cleanKBList) == 7
mm_gamez(cleanKBList)
print('solution:')
print(mm_gamez.query(pl.Expr("coloring(Alabama, Mississippi, Georgia, Tennessee, Florida)"), cut = True))
# [{'Alabama': 'green', 'Mississippi': 'blue', 'Georgia': 'blue', 'Tennessee': 'red', 'Florida': 'red'}]


print('- ALB - 2 -')
print('\n'*8)

KBmultilineText='''

# facts
# (lowercased variables = konstants)

canAccept(kHole1, kRed_____)
canAccept(kHole1, kGreen___)
canAccept(kHole1, kBlue____)
canAccept(kHole1, kFuchsia_)
#
canAccept(kHole2, kRed_____)
canAccept(kHole2, kGreen___)
canAccept(kHole2, kBlue____)
canAccept(kHole2, kFuchsia_)
#
canAccept(kHole3, kRed_____)
canAccept(kHole3, kGreen___)
canAccept(kHole3, kBlue____)
canAccept(kHole3, kFuchsia_)
#

# rules
# (uppercased variables = variable / existential variables)

guess2(Xhole1,Hole1,Xhole2,Hole2) :- canAccept(Xhole1, Hole1), canAccept(Xhole2, Hole2)
guess3(Xhole1,Hole1,Xhole2,Hole2,Xhole3,Hole3) :- canAccept(Xhole1, Hole1), canAccept(Xhole2, Hole2), canAccept(Xhole3, Hole3)
'''






# rules = LHS predicate := RHS goal		e.g. 		fly(X) :- bird(X) ; wings(X)
# ok: not Hole3 is 'kRed'		H1=hole1,H2=hole2,H3=hole3
# , not canAccept(hole3,red)
# , H1=hole2, accept(C2,red), not accept(C2,red)
# pluggedInto(C,H) :- accept(H, C)
#different(hole1, hole2)
#different(hole2, hole3)

'''
try1:				{'Hole1': 'red', 'Hole2': 'red', 'Hole3': 'red'}
feedback1:		{'blacks': 1, 'whites': 0}
assumption1:	black#1 is Hole1 -> hole1=red
'''

# https://courses.cs.duke.edu/fall16/compsci516/Lectures/Lecture-21-Datalog.pdf		slide 17 ss



class Mlog:
	
	def __init__(self,KBmultilineText,secret):
		print('='*128)
		self.secret=secret
		self.hole_dim = 3
		self.debug = False
		self.mm_game = pl.KnowledgeBase("mm_game")
		self.loadKB(KBmultilineText)
		self.guesses = []
		self.feedbacks = []
		self.lastGuesses = []
		self.cleanKBList = []

	def loadKB(self,KBmultilineText):
		rawKBList = KBmultilineText.split('\n')
		commentstrippedKBList = [ line.split('#')[0] for line in rawKBList ]		# same,		commentstrippedKBList = map(lambda line: line.split('#')[0], rawKBList)
		trimmedKBList = [ line.strip() for line in commentstrippedKBList ]
		self.cleanKBList = list(filter(lambda line: len(line)>0, trimmedKBList))
		self.mm_game(self.cleanKBList)
		self.printKB()
	
	def printKB(self):
		self.header('KB')
		[ print(c) for c in cleanKBList ]
	
	def header(self,text):
		print('')
		print('='*4)
		print(text)
		print('='*4)
		
	def query(self,expr,top):
		self.header('query')
		print(expr)
		guessAll = self.mm_game.query(pl.Expr(expr), cut = False)
		self.displayResults(guessAll,top)
		self.lastGuesses = guessAll
		
	def displayResults(self,guessAll,top):
		self.header('result size')
		print(len(guessAll))
		guess1=guessAll[0]
		if top==0:
			topGuesses=guessAll
			self.header('result (all)')
		else:
			topGuesses=guessAll[0:top]
			self.header('result top '+str(top))
		print_line_number = True
		if print_line_number:
			for i, item in enumerate(topGuesses):
				print(f"{i+1}.\t{item}")
		else:
			[ print(g) for g in topGuesses ]

	def pickGuess(self,take_random123):
		assert self.lastGuesses[0]!='No', 'no guess to pick'
		if take_random123 is None:
			r012 = random.randint(0, len(self.lastGuesses)-1)	# when len=3: randint in [0,3-1]
		else:
			r012 = take_random123-1
		# {'Hole1': 'kRed', 'Hole2': 'kRed', 'Hole3': 'kRed'}	
		self.guesses.append(self.lastGuesses[r012])
		print('picking guess:')
		print(f"{r012+1}.\t{self.lastGuesses[r012]}")
			

	def printLearned(self):
		self.header('printLearned')
		print(self.secret,'<=','secret')
		for L in range(len(self.guesses)):
			print(self.guesses[L],self.feedbacks[L])

	def takeFeedback(self):
		i_lastguess = len(self.guesses)-1
		self.feedbacks.append(self.giveFeedback(self.guesses[i_lastguess]))

	def giveFeedback(self,guess):
		self.header('giveFeedback')
		print('secret:',self.secret)
		print('guess: ',guess)
		secret_list = list(self.secret.values())
		guess_colors = list(guess.values())
		if True:
			assert  set(self.secret.keys())=={'Hole1','Hole2','Hole3'}
			assert  set(guess.keys())=={'Hole1','Hole2','Hole3'}
			assert len(secret_list) == len(guess_colors) and len(guess_colors) == self.hole_dim
		if self.debug: print('guess_colors:',guess_colors)
		if self.debug: print('secret_list :',secret_list)
		eq_list = [ guess_colors[p]==secret_list[p] for p in range(self.hole_dim) ]
		if self.debug: print('eq_list :',eq_list)
		bb=0
		ww=0
		for p in range(self.hole_dim):
			if guess_colors[p]==secret_list[p]:
				bb+=1
				secret_list[p]='_assigned_'
				if self.debug: print('pos',p,'guess color',guess_colors[p],'=>','ok and same pos','=>','black')
			else:
				try:
					x=secret_list.index(guess_colors[p])
					ww+=1
					secret_list[x]='_assigned_'
					if self.debug: print('pos',p,'guess color',guess_colors[p],'=>','ok but different pos (',x,')','=>','white')
				except:
					if self.debug: print('pos',p,'guess color',guess_colors[p],'=>','not found')
		#self.hint_list.append((bb,ww))
		fb = {'blacks':bb,'whites':ww,'total':bb+ww}
		print('feedback: ',fb)
		return fb
		#self.updateMask()


# ############### end of class

secret = {'Hole1': 'kRed_____', 'Hole2': 'kGreen___', 'Hole3': 'kBlue____'}		
mlog = Mlog(KBmultilineText,secret)

print('-')
[ print('BTW:',4,'^',p,'=',4**p) for p in range(0,4) ]

mlog.query("canAccept(kHole1,Hole1)",0)

#	mlog.query("guess2(kHole1,Hole1,kHole2,Hole2)",5)
mlog.query("guess2(kHole1,Hole1,kHole2,Hole2)",0)

#	mlog.query("guess3(kHole1,Hole1,kHole2,Hole2,kHole3,Hole3)",5)
mlog.query("guess3(kHole1,Hole1,kHole2,Hole2,kHole3,Hole3)",0)	

mlog.pickGuess(14)
mlog.takeFeedback()
mlog.printLearned()


# {'Hole1': 'kRed_____', 'Hole2': 'kFuchsia_', 'Hole3': 'kGreen___'} {'blacks': 1, 'whites': 1}

'''
now you replace rule guess3 with:

guess3 and h1=red 		ie the guess1 color
guess3 and h2=fuchsia	ie the guess1 color
guess3 and h3=green		ie the guess1 color


'''













exit(0)

#random.seed(202308)	#	red blue blue yellow

class Game:

	def __init__(self,mode):
		self.mode=mode
		self.debug=True
		if self.mode:
			print('Hi, please prepare a secret, I will try and guess')
		else:
			print('Hi, I am going to prepare a secret and I will try and guess')
		self.peg_color_list = 'Red,Green,Blue,Fucsia,Yellow,Azure'.split(',')
		self.peg_color_dim = len(self.peg_color_list)
		self.hole_dim = 4
		self.guess_made=0
		self.guess_list = []
		self.guess_list_color = []
		self.hint_list = []
		self.maskdf = self.newMask()

	def newMask(self):
		headers=['hole'+str(i) for i in range(self.hole_dim)]
		maskdf = pd.DataFrame(data=[], columns=headers,index=self.peg_color_list)
		maskdf['min']=0
		maskdf['max']=self.hole_dim
		print('=')
		print(maskdf)
		print('=')
		return maskdf

	def updateMask(self):
		#self.hint_list.append((bb,ww))
		return

	def genSecret(self):
		assert self.mode==False
		self.secret_list = 'Red,Yellow,Blue,Blue'.split(',')
		print('secret:',self.secret_list)
		
	def inputHints(self):
		inb = input("how many black pegs? ")
		inw = input("how many white pegs? ")
		print("You entered: " + inb,inw)

	def makeGuess(self):
		if self.guess_made==0:
			guess = [ random.randint(0, self.peg_color_dim-1) for n in range(self.hole_dim)]
			guess_colors = [ self.peg_color_list[i] for i in guess ]
			self.guess_list.append(guess)
			self.guess_list_color.append(guess_colors)
			self.guess_made += 1
		else:
			assert False
	
	def giveFeedback(self):
		assert self.guess_made>0
		
		secret_list = self.secret_list + []	# will be modified
		guess_colors = self.guess_list_color[self.guess_made-1]
		assert len(secret_list) == len(guess_colors) and len(guess_colors) == self.hole_dim
		if self.debug: print('guess_colors:',guess_colors)
		if self.debug: print('secret_list :',secret_list)
		eq_list = [ guess_colors[p]==secret_list[p] for p in range(self.hole_dim) ]
		if self.debug: print('eq_list :',eq_list)
		bb=0
		ww=0
		for p in range(self.hole_dim):
			if guess_colors[p]==secret_list[p]:
				bb+=1
				secret_list[p]='_assigned_'
				if self.debug: print('pos',p,'guess color',guess_colors[p],'=>','ok and same pos','=>','black')
			else:
				try:
					x=secret_list.index(guess_colors[p])
					ww+=1
					secret_list[x]='_assigned_'
					if self.debug: print('pos',p,'guess color',guess_colors[p],'=>','ok but different pos (',x,')','=>','white')
				except:
					if self.debug: print('pos',p,'guess color',guess_colors[p],'=>','not found')
		self.hint_list.append((bb,ww))
		print('blacks',bb,'whites',ww)
		self.updateMask()



#for i in xrange(1, len(lst)+1):
#combs.append(i)
#els = [list(x) for x in itertools.combinations(lst, i)]
#combs.append(els)
myg = Game(False)
myg.genSecret()
myg.makeGuess()
myg.giveFeedback()



