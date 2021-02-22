# -*- coding: utf-8 -*-
"""
@title:     You sank my battleship, or did you? Epistemic uncertainty in agent-based models
@purpose:   Propagate epistemic uncertainty in an agent-based model
@date:      22 Jan 2021
@author:    ferson
"""

##################################################################
# 
# Kleene logic class library
#
##################################################################

# https://en.wikipedia.org/wiki/Three-valued_logic#Kleene_and_Priest_logics

import numpy as np
from enum import IntEnum, unique

@unique
class kleene(IntEnum) :  
    
    false = 0
    true  = 1
    dunno = 2
       
    def __str__(self) : 
        if self==kleene.false : return 'false'
        if self==kleene.true : return 'true'
        return 'dunno'
    
    def __repr__(self):
        return f'kleene.{str(self)}'

    def __invert__(self) : # not
        if self==kleene.false : return kleene.true
        if self==kleene.true : return kleene.false
        return kleene.dunno

    def __and__(self,other) :
        if (self==kleene.false) or (other==kleene.false) : return kleene.false
        if (self==kleene.true) and (other==kleene.true) : return kleene.true
        return kleene.dunno

    def __or__(self,other) :
        if self==kleene.true  or other==kleene.true : return kleene.true
        if self==kleene.false and other==kleene.false : return kleene.false
        return kleene.dunno   

    def __xor__(self,other) : # is this correct?
        if self==kleene.dunno or other==kleene.dunno : return kleene.dunno
        if self==other : return kleene.false
        return kleene.true

    def negate(self) : # as a method
        if self==kleene.false : return kleene.true
        if self==kleene.true : return kleene.false
        return kleene.dunno

    def c(self) : # colored string
        kolor = ['\x1b[33m\x1b[1m', '\x1b[32m\x1b[1m', '\x1b[37m\x1b[1m', '\x1b[0m']
        return kolor[int(self)] + str(self) + kolor[-1]
   
    # &=	__IAND__(SELF, OTHER)
    # |=	__IOR__(SELF, OTHER)
    # ^=	__IXOR__(SELF, OTHER)       

    # def __bool__(self) :
    #     #return bool(self.value)
    #     if self==kleene.false : return False
    #     if self==kleene.true : return True
    #     return np.nan
  
##################################################################
# 
# Interval computations class library
#
##################################################################         
            
def isnum(a) : return isinstance(a, numbers.Number)

def istr(n) : 
    if n==trunc(n) : return str(trunc(n))
    else : return str(n)

import numbers

class I: 

    cO = -1     # opposite dependence
    cI = 0      # independence
    cP = 1      # perfect dependence
    cF = 2      # Frechet case (any dependence)
    cW = cF     # dependence flag
    vF = False  # flag for verbosity about swapped endpoints
    
    def __init__(self, lo, hi=None) :
        if I.vF : 
            if hi < lo : print('swapped interval endpoints')
        self.lo = lo
        if hi==None : hi = lo
        self.hi = hi
        self.__stations = [lo, hi]

    def __iter__(self) : # you can iterate over an interval (left then right)
        self.__i = 0
        return iter(self.__stations)

    def __next__(self) :
        if self.__i<1:
            self.__i += 1         
            return self.__stations[self.__i]
        else:
            raise StopIteration

    def __str__(self) : 
        if self.lo == self.hi : return str(self.lo)
        amend = ' dual' if self.hi < self.lo else ''
        return '[' + istr(self.lo) + ',' + istr(self.hi) + ']' + amend
    
    def __repr__(self) :
        return f'I({self.lo}, {self.hi})'

    def __add__(self, other) : 
        if isnum(other) : other = I(other,other)
        return I(self.lo + other.lo, self.hi + other.hi)
  
    def __sub__(self, other) : 
        if isnum(other) : other = I(other,other)
        return I(self.lo - other.hi, self.hi - other.lo)

    def __mul__(self, other) :                               # not general !!
        if isnum(other) : other = I(other,other)
        return I(self.lo * other.lo, self.hi * other.hi)
  
    def __truediv__(self, other) : 
        if isnum(other) : other = I(other,other)
        return I(self.lo / other.hi, self.hi / other.lo)
    
    def min(self, other) : 
        if isnum(other) : other = I(other,other)
        return I(min(self.lo,other.lo), min(self.hi, other.hi))
    
    def max(self, other) : 
        if isnum(other) : other = I(other,other)
        return I(max(self.lo,other.lo), max(self.hi, other.hi))
    
    def env(self, other) : 
        if isnum(other) : other = I(other,other)
        #print('@',type(self),type(other),other)
        return I(min(self.lo,other.lo), max(self.hi, other.hi))
    
    def imp(self, other) : 
        if isnum(other) : other = I(other,other)
        return I(max(self.lo,other.lo), min(self.hi, other.hi))
    
    def dual(self) :
        return I(self.hi, self.lo)
    
    def __invert__(self) : # this is not 'not'; it is ~
        return I(1-self.hi, 1-self.lo)

    def __and__(self, other) :
        if isnum(other) : other = I(other,other)
        if I.cW==I.cI : return self * other
        if I.cW==I.cF : return I.env(I.max(I(0,0),self+other-I(1,1)),I.min(self,other))

    def __or__(self, other) :
        if isnum(other) : other = I(other,other)
        if I.cW==I.cI : return ~((~self) * (~other))
        if I.cW==I.cF : return I.env(I.max(self, other), I.min(I(1,1), self + other))

    def __xor__(self, other) : # NOT YET IMPLEMENTED
        if isnum(other) : other = I(other,other)
        if cW==cI : return I(0,1)

    def __lt__(self, other):
        if isnum(other) : other = I(other,other)
        if self.hi < other.lo : return kleene.true
        if other.hi <= self.lo : return kleene.false
        return kleene.dunno

    def __le__(self, other):
        if isnum(other) : other = I(other,other)
        if self.hi <= other.lo : return kleene.true
        if other.hi < self.lo : return kleene.false
        return kleene.dunno

    def __eq__(self, other):
        if isnum(other) : other = I(other,other)
        if self.lo == self.hi and other.lo == other.hi and self.lo == other.lo : return kleene.true
        if self.hi < other.lo or other.hi < self.lo : return kleene.false
        return kleene.dunno

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        if isnum(other) : other = I(other,other)
        if self.lo > other.hi : return kleene.true
        if other.lo >= self.hi : return kleene.false
        return kleene.dunno

    def __ge__(self, other):
        if isnum(other) : other = I(other,other)
        if self.lo >= other.hi : return kleene.true
        if other.lo > self.hi : return kleene.false
        return kleene.dunno
    
One = I(1,1) 
Zero = I(0,0)
Dunno = I(0,1)
Logicals = I(0,1)
Empty = I(float('inf'),float('-inf'))
Anynumber = I(float('-inf'),float('inf'))
Positives = I(0,float('inf'))
Negatives = I(float('-inf'),0)

def left(a) :
    if isnum(a) : return a
    if type(a)==list : return [left(A) for A in a]
    return a.lo

def right(a) :
    if isnum(a) : return a
    if type(a)==list : return [right(A) for A in a]
    return a.hi

def trunc(a) :
    if isnum(a) : return int(a)
    if type(a)==list : return [trunc(A) for A in a]
    return I(int(a.lo), int(a.hi))

def midpoint(a) :
    if isnum(a) : return a
    if type(a)==list : return [midpoint(A) for A in a]
    return (a.lo + a.hi) / 2

def interval(a,b=None,r=0) :
    if b==None : b = a
    if 0<r : return I(a-r,a+r)
    if a <= b : return I(a,b)
    else : return I(b,a)      
    
def env(*args): 
    e = Empty
    for a in args : 
        if type(a)==list :
            for s in a :
                if isnum(s) : s = I(s,s)
                e = I.env(e,s)
        else : 
            if isnum(a) : a = I(a,a)
            e = I.env(e,a)
    return e

def ifelse(k, yes, no, maybe=None) :
    if k==kleene.false : return no
    if k==kleene.true : return yes
    if maybe==None : return env(yes,no)
    return maybe

def pmin(a,b) :
    a = [I(_,_) if isnum(_) else _ for _ in a]
    return [I.min(*z) for z in zip(a,b)]

def pmax(a,b) :
    a = [I(_,_) if isnum(_) else _ for _ in a]
    return [I.max(*z) for z in zip(a,b)]

def penv(a,b): 
    return [env(*z) for z in zip(a,b)]

def pifelse(k, yes, no, maybe=None) :
    if maybe==None : return [ifelse(*z) for z in zip(k,yes,no)]
    return [ifelse(*z) for z in zip(k,yes,no,maybe)]

colorscheme = { # works in Spyder's Console
    'black': '30m','red': '31m','green': '32m','orange': '33m','blue': '34m',
    'purple': '35m','cyan': '36m','lightgrey': '37m','darkgrey': '90m',
    'lightred': '91m','lightgreen': '92m','yellow': '93m','lightblue': '94m',
    'pink': '95m','lightcyan': '96m',
    # background colors are capitalised 
    'Black': '40m','Red': '41m','Green': '42m','Orange':'43m','Blue': '44m',
    'Purple': '45m', 'Cyan': '46m', 'Lightgrey': '47m', 
    # effects
    'reset': '0m','bold': '01m','disable': '02m','underline': '04m',
    'reverse': '07m','strikethrough': '09m','invisible': '08m'}
colorprefix = '\033['
coloroff = colorprefix + colorscheme['reset']

def c(num,dec=2,col='',prefix='',off='') : # use within a print command
    if col!='' : 
        prefix = colorprefix + colorscheme[col] + prefix
        off += coloroff
    if isinstance(num, numbers.Number) : return prefix+('%.2f' % num)+off
    else :
        amend = ' dual' if num.hi < num.lo else ''
        return prefix+'['+(('%.'+str(dec)+'f') % num.lo)+','+(('%.'+str(dec)+'f')%num.hi)+']'+amend+off

def surely(logical) :
    if type(logical)==bool : return logical
    if type(logical)==type(kleene.true) : return logical==kleene.true
    if isnum(logical) : return logical==1
    return all(logical)    




##################################################################
# 
# Battleship combat theatre
#
##################################################################

# The battleship simulation does not use a current/next data structure, but 
# rather the behaviours of each ship in order are played out (which may impact 
# other ships).  After all behaviours have been expressed, the consequences on 
# each ship are then assessed.  The behaviours of each ship are 
#    1) display on the canvas
#    2) sail to a new position
#    3) target and fire upon other ships
#    4) assess the damage from other ships

# Run the main program to do an animated simulation.  Use singlepath() to see 
# an example of a single ships possible path.

# Compared to the precise version (vladimirABM.py) this simulation has very few
# ships that definitely sink.  This seems counterintuitive, and it seems that 
# the uncertainty should not insulate ships from their sure fates. This may be
# because
#
# It's a logic error in the target function
# It is the result of puffiness caused by repeated uncertain numbers
# It is actually correct and our intuition is incorrect
      
import numpy as np
from numpy.random import *
import matplotlib.pyplot as plt
from time import sleep

seed(0)                 # remove to randomize
n = 102                 # length of each side of the theatre
times = range(150)      # duration of the battle
targeting = 0.5         # chance missile hit its target
killthreshold = 3       # number of landed missiles to destroy
combatants = range(20)  # number of agents in the battle
inertia = 15            # resistance to direction change
delay = 1; fast = 0.03  # seconds between animations
# more details in the initialisation section below

#---------------------------------------------------------------
def mkcoord() : return float(rand(1) * n)

def mkangle() : return float(rand(1) * 2 * np.pi)

def swerve(a) : return float(a + randn(1) * np.pi / inertia)
#---------------------------------------------------------------
#def mkcoord() : return rand(1) * n

#def mkangle() : return rand(1) * 2 * np.pi

#def swerve(a) : return a + randn(1) * np.pi / inertia
#---------------------------------------------------------------
#def mkcoord(d=10) : return interval(rand() * n,r=rand()*d)

#def mkangle() : return float(rand(1) * 2 * np.pi)

#def swerve(a) : return float(a + randn(1) * np.pi / inertia)
#---------------------------------------------------------------

def mult(lista, listb) : # elementwise multiply lists...why this doesn't exist?
    return [a*b for a,b in zip(lista,listb)]  # map(lambda x,y:x*y,lista,listb)

def plural(k,word='',words='s') : 
    if type(k)==bool : kk=''
    else : kk = str(k) + ' '    
    kk+word+'s' if words=='s' else kk+words
    if words=='s' : words = word + 's'
    if word=='' : words = '' 
    return ifelse(k == 1, '1 ' + word, kk+words, kk+words)

def circle(x,y,r,c='b',l='solid') :
    C = plt.Circle((x,y),r,color=c,fill=False,linestyle=l)
    fig = plt.gcf()
    ax = fig.gca()    
    ax.add_patch(C)  
    
def imprecise(a,d=0.2):
    if type(a)==list : return [imprecise(_,d*rand()) for _ in a]
    return I(a-d*a, a+d*a)

def binom(n,p) : # both n and p can be imprecise
    #print('n',n,type(n))
    #print('p',p,type(p))
    i = 0
    for _ in range(int(left(n))) : i = ifelse(p<rand(),i+1,i)
    j = i
    for _ in range(int(right(n) - left(n))) : i = ifelse(p<rand(),i+1,i)
    return env(i,j)
           
def radar(x,y,r,c='b',l='solid') :
    # it's pretty easy to depict uncertainty in r, but x,y would be trickier
    assert isnum(x), 'radar does not handle interval coordinates yet'
    if type(r)==I : 
        for R in r : circle(x,y,R,c,l=l)
    else : circle(x,y,r,c,l=l)

def showship(s,c='b',l='solid') :
    if not e[s] : return
    radar(x[s],y[s],1,c=c,l=l)
    radar(x[s],y[s],r[s],c=c,l=l)

def canvas() : 
    top = 1.1 * n
    bot =-0.1 * n
    plt.scatter([bot,top,top,bot],[bot,bot,top,top],c='w')

def showtheatre(time='') :
    canvas()
    for s in combatants :         
        color = ifelse( h[s] < I(1,2), 'b', 'r', 'tab:orange')     
        linestyle = ifelse(e[s], 'solid', (0,(0,5)), (0,(1,5)))
        showship(s,c=color,l=linestyle)
    left = I(e.count(True), len(e)-e.count(False))
    arms = sum(trunc(mult(m,e)),I(0,0))
    plt.title(plural(arms,'missile')+' across '+plural(left,'ship')+time)
    plt.show()  
    return(left)
    
def exists(s) : return e[s]    

def dist(s,t) :
    #global x
    #global y
    return float((x[s]-x[t])**2+(y[s]-y[t])**2)**0.5

def fire(s,t) :
    launch = min(3,m[s])
    m[s] -= launch
    for i in range(launch) : 
        if rand(1) < targeting : h[t] += 1

def target(s) :
    for t in combatants :
      launch = m[s].min(3)
      landed = binom(launch,targeting)
      # doit = e[s] & e[t] & (t!=s) & (dist(s,t) < r[s])
      # m[s] = ifelse(doit, (m[s]-launch).max(0), m[s])
      # h[t] = ifelse(doit, h[t]+landed, h[t])
      ############################# don't insulate the dotted ships from attack
      doit = e[s] & (t!=s) & (dist(s,t) < r[s])
      m[s] = ifelse(doit & e[t], (m[s]-launch).max(0),  m[s])
      h[t] = ifelse(doit,        h[t]+landed,           h[t])

def assess(s) :
    assert type(killthreshold < h[s])==type(kleene(0)), 'Improper logical in assess'
    e[s] = ~(killthreshold < h[s])

def wrap(i) :
    if i < 0 : i = n + i
    if n <= i : i = i - n
    return i

def move(x,y,d,a) :
    return wrap(x + d * np.cos(a)), wrap(y + d * np.sin(a))

def sail(s) :
    a[s] = swerve(a[s]) # wiggle direction
    x[s], y[s] = move(x[s],y[s],d[s],a[s])   

def singlepath(s=-1) : # depicts how a single ship wanders during the battle
  canvas()
  if s<0 : s = int(randint(min(combatants),1+max(combatants),1))
  save = e[s]; e[s] = True
  print(s)
  for time in times : 
      sail(s)
      showship(s)
  e[s] = save

def inventory(s) :
    color = '\x1b[36m\x1b[2m'; coloroff = '\x1b[0m'    
    if e[s] : color = '\x1b[35m\x1b[1m' #print( '\x1b[35m\x1b[1m' + 'hello' + '\x1b[0m') # prints 'hello' in magenta
    print(color,'Ship',s,'currently',ifelse(e[s],'exists','does not exist','both exists and does not exist'),'having suffered', plural(h[s],'missile strike'),coloroff)
    print(color,'\tLast location: ('+c(x[s])+',',c(y[s])+'), bearing',c(a[s]),'at speed',c(d[s]),coloroff)
    print(color,'\tRemaining complement:',plural(m[s],'missile'),'with a range of',c(r[s]),coloroff)


##################################################################
# 
# initialisations

#i = list(combatants)                       # ship index
e = [True           for _ in combatants]    # whether the ship still exists
x = [mkcoord()      for _ in combatants]    # starting x position
y = [mkcoord()      for _ in combatants]    # starting y position
d = [mkcoord()/20+1 for _ in combatants]    # speed (displacement per time step)
a = [mkangle()      for _ in combatants]    # starting angle of travel
r = [mkcoord()/8+2 for _ in combatants]     # radar range
m = list(randint(10,60,len(combatants)))    # how many missiles the ship has
h = [0              for _ in combatants]    # how many missiles have hit it!

# make imprecise
e = imprecise(e,0)
#x = imprecise(x,0)
#y = imprecise(y,0)
#d = imprecise(d,0)
#a = imprecise(a,0)
r = imprecise(r,0.5)
m = trunc(imprecise(m,0))
h = imprecise(h,0)

##################################################################
# 
# simulation

showtheatre(' at start')
for time in times :
    sleep(delay)
    for s in combatants : sail(s)
    for s in combatants : target(s)
    for s in combatants : assess(s)
    if surely(0==showtheatre(' at time '+str(time))) : break
    if e.count(True) < 10 : delay = fast

# report
for s in combatants : inventory(s)    

##################################################################
# 
# END
# 
##################################################################











###############################################################################
# testing for the Kleene logic implementation in Pandas

def pandaswrong() : 
    ###############################################################################
    # The Pandas User Guide https://pandas.pydata.org/pandas-docs/stable/user_guide/boolean.html#boolean-kleene
    # claims that its arrays.BooleanArray implements Kleene Logic.
    # It seems this is not true, or rather that its implementation
    # is incorrect vis-a-vis https://en.wikipedia.org/wiki/Three-valued_logic#Kleene_and_Priest_logics
    
    # Pandas uses the infix operators {&, |} instead of the words {and, or}
    # for conjunction and disunction respectively (so does my implementation above)
    
    import pandas as pd
    k = pd.array((False, np.nan, True),dtype='boolean')
    
    wow = '\x1b[35m\x1b[1m'
    mom = '\x1b[32m\x1b[1m'
    off = '\x1b[0m'
    print('\n\nThe magenta answers should be "False" and the green should be "True" rather than "<NA>"')
    print('\nConjunction')
    print('\t\t', False, '\t ', np.nan, '\t', True)
    i = k[0]; print(i, '\t', i & k[0],  '\t',wow, i & k[1],off, '', i & k[2])
    i = k[1]; print(i, wow,'\t',  i & k[0], off, '\t ', i & k[1], '\t', i & k[2])
    i = k[2]; print(i, '\t', i & k[0], '\t ', i & k[1], '\t', i & k[2],off)
            
    print('\nDisjunction')
    print('\t\t', False, '\t', np.nan, '\t', True)
    i = k[0]; print(i, '\t', i | k[0], '\t', i | k[1], '\t', i | k[2])
    i = k[1]; print(i, '\t', i | k[0], '\t', i | k[1], '\t', mom, i | k[2],off)
    i = k[2]; print(i, '\t', i | k[0], mom,'\t', i | k[1],off, '\t', i | k[2],'\n')
    
    print('Interestingly, the operations are correct when applied to arrays, rather than isolated objects')
    kk1 = pd.array((False, np.nan, True, False, np.nan, True, False, np.nan, True),dtype='boolean')
    kk2 = pd.array((False, False, False, np.nan, np.nan, np.nan, True, True, True),dtype='boolean')
    
    print('\nConjunction')
    print(kk1 & kk2)
    print('\nDisjunction')
    print(kk1 | kk2)


###############################################################################
# testing for the Kleene logic code

'''
a = kleene(0)
a = kleene(False) 

b = kleene(1)
b = kleene(True) 

c = kleene(2)
c = kleene(kleene.dunno)
#c = kleene()
#c = kleene((0,1))

bool(kleene(0))  # False
bool(kleene(1))  # True
bool(kleene(2))  # True

print(repr(a))
print(repr(b))
print(repr(c))

print(a.c())
print(b.c())
print(c.c())

print(kleene.c(a))
print(kleene.c(b))
print(kleene.c(c))

k = [a,c,b]
print('\nConjunction')
print('\t\t', False, '\t', 'Dunno', '\t', True,sep='')
i = k[0]; print(i, '\t',(i & k[0]).c(), '\t',(i & k[1]).c(), '\t',(i & k[2]).c(), sep='')
i = k[1]; print(i, '\t',(i & k[0]).c(), '\t',(i & k[1]).c(), '\t',(i & k[2]).c(), sep='')
i = k[2]; print(i, '\t',(i & k[0]).c(), '\t',(i & k[1]).c(), '\t',(i & k[2]).c(), sep='')
        
print('\nDisjunction')
print('\t\t', False, '\t', 'Dunno', '\t', True,sep='')
i = k[0]; print(i, '\t', (i | k[0]).c(), '\t', (i | k[1]).c(), '\t', (i | k[2]).c(), sep='')
i = k[1]; print(i, '\t', (i | k[0]).c(), '\t', (i | k[1]).c(), '\t', (i | k[2]).c(), sep='')
i = k[2]; print(i, '\t', (i | k[0]).c(), '\t', (i | k[1]).c(), '\t', (i | k[2]).c(), sep='')
''' 


###############################################################################
# testing for the interval computations code

'''
a = I(1,3)
b = I(2,4)
c = I(3,5)
d = I(4,6)

print(a, '\t\t', repr(a)) 
print(b, '\t\t', repr(b))

print(a < b)  # dunno
print(a < c)  # dunno
print(a < d)  # true

print('\t',a <= b)  # dunno
print('\t',a <= c)  # true
print('\t',a <= d)  # true

print('\t','\t',a > b)  # dunno
print('\t','\t',a > c)  # false
print('\t','\t',a > d)  # false

print('\t','\t','\t',a >= b)  # dunno
print('\t','\t','\t',a >= c)  # dunno
print('\t','\t','\t',a >= d)  # false

print(a==b)  # dunno
print(a==c)  # dunno
print(a==d)  # false

print(env(0, a,-3,b,c,d, [One,Zero,Logicals,Dunno], 7))

a = I(0.195, 0.205)
b = I(0.495, 0.505)

# Conjunction (intersection, and)  
I.cW = I.cI
print(a & b)
print(a and b) ############## WRONG!  Can we overload/redefine 'and', etc.
print(a * b)  
print('[ 0.0965, 0.104]')

I.cW = I.cF
print(a & b)
print(a and b) ############## WRONG!  Can we overload/redefine 'and', etc.
print(I.env(I.max(I(0,0),a + b - I(1,1)), I.min(a, b)))  
print('[ 0, 0.205]')
  
# Disjunction (union, or)
I.cW = I.cI
print(a | b)
print(a or b) ############## WRONG!  Can we overload/redefine 'and', etc.
print(~((~a)*(~b)))
print('[ 0.593, 0.607]')

I.cW = I.cF
print(a | b)
print(a or b) ############## WRONG!  Can we overload/redefine 'and', etc.
print(I.env(I.max(a, b), I.min(I(1,1), a + b)))  
print('[ 0.495, 0.71]')

# how to define, and access, the 'xor' function?
'''


###############################################################################
# comparisons with Risk Calc

'''
func I() return [$1,$2]

a = I(1,3)
b = I(2,4)
c = I(3,5)
d = I(4,6)

print a < b   // dunno
print a < c   // dunno
print a < d   // true

print '\t',a <= b   // dunno
print '\t',a <= c   // true
print '\t',a <= d   // true

print '\t','\t',a > b   // dunno
print '\t','\t',a > c   // false
print '\t','\t',a > d   // false

print '\t','\t','\t',a >= b   // dunno
print '\t','\t','\t',a >= c   // dunno
print '\t','\t','\t',a >= d   // false

print a==b   // dunno
print a==c   // dunno
print a==d   // false
'''
###############################################################################
# testing for other utilities

'''
binom(3,I(0.1,0.5))     # I(1, 3)
binom(3,I(0.1,0.5))     # I(2, 3)
binom(3,I(0.1,0.5))     # I(2, 3)
binom(3,I(0.1,0.5))     # I(1, 3)
binom(3,I(0.1,0.5))     # I(1, 3)
binom(3,I(0.1,0.5))     # I(1, 2)
binom(I(3,5),I(0.1,0.5))     # I(1, 4)
binom(I(3,5),I(0.1,0.5))     # I(2, 4)
binom(I(3,5),I(0.1,0.5))     # I(0, 5)
binom(I(3,5),I(0.1,0.5))     # I(2, 4)


print(plural(0,'second'))    # 0 seconds
print(plural(1,'second'))    # 1 second
print(plural(2,'second'))    # 2 seconds

print(plural(0,'datum','data'))    # 0 data
print(plural(1,'datum','data'))    # 1 datum
print(plural(2,'datum','data'))    # 2 data

print(plural(0))    # 0 
print(plural(1))    # 1 
print(plural(2))    # 2 

print(plural(I(0,1),'second'))    # [0,1] seconds
print(plural(I(1,1),'second'))    # 1 second
print(plural(I(1,2),'second'))    # [1,2] seconds

print(plural(I(0,1),'datum','data'))    # [0,1] data
print(plural(I(1,1),'datum','data'))    # 1 datum
print(plural(I(1,2),'datum','data'))    # [1,2] data

print(plural(I(0,1)))    # [0,1]  
print(plural(I(1,1)))    # 1 
print(plural(I(1,2)))    # [1,2] 


def many(a) :
    cf = 0
    ct = 0
    cu = 0
    for _ in a :
        if _ == kleene.false : cf += 1
        if _ == kleene.true  : ct += 1
        if _ == kleene.dunno : cu += 1
    return (cf,ct,cu)

f = kleene(0)
t = kleene(1)
u = kleene(2)

e = [f,f,f,f,f, t,t,t,t, u,u,u]

print(many(e))
print(e.count(True), len(e) - e.count(False))

left = I(e.count(True),len(e)-e.count(False))
print(left)

'''

###############################################################################
# first stab at implementing a light-weight Kleene logic [it works pretty well]

'''
import numpy as np

def isnan(num): return num != num

class k: 
  
    kind = 'logical'
    
    def __init__(self, l='?') : 
        if (l==0) or (l==False)    : self.l = False
        if (l==1) or (l==True)     : self.l = True
        if (l=='?') or k.isnan(l)  : self.l = float('nan')
        
    def __str__(self) : return str(self.l)

    def __repr__(self) : 
        if isnan(self.l) : return 'k()'
        return 'k('+str(self.l)+')'
    
    def __and__(self,other) :
        if (self.l==False) or (other.l==False) : return k(False)
        if (self.l==True) and (other.l==True) : return k(True)
        return k()

    def __eq__(self,other) :
        if isnan(self.l) or isnan(other.l) : return k()
        return k(self.l==other.l)

    def __not__(self) : 
        if (self.l==False) : return k(True)
        if (self.l==True) : return k(False)
        return k()  

a = k(False) 
b = k(True) 
c = k()
A = k(0)
B = k(1)
C = k('?')
print(a==a)         # true
print(a==k(False))  # true
print(a==A)         # true
print(b==B)         # true
print(c==C)         # nan
print(c==c)         # nan, even this is nan
print(a & a)        # false
print(b & b)        # true
print(c & c)        # nan
print(a & b)        # false
print(a & c)        # false
print(b & c)        # nan
e = a & b
f = a & c
print(type(e), type(f))
'''


###############################################################################
# WOODPILE

'''
from collections import namedtuple

I = namedtuple('I', 'lo hi')

Ship = namedtuple('Ship', 'i e x y s a r m h') #x coord, y coord, speed, angle, range, missiles, hits

def coord(r,a) : return (I(r.lo * np.cos(a.lo), r.hi * np.cos(a.hi)),
                         I(r.hi * np.sin(a.hi), r.hi * np.sin(a.hi)))
def canvas() : plt.scatter([sh.x for sh in ships],[sh.y for sh in ships],c='w')

index = 0
def increment() : 
    global index
    index += 1; 
    return index-1

def mkship() : return Ship(i=increment(),      e=True,
                           x=mkcoord(),        y=mkcoord(), 
                           s=1+mkcoord()/20,   a=mkangle(), 
                           r=2+mkcoord()/15,   m=rand(1)*10, h=randint(5))
ships = []; 
for sh in fleet : ships = ships + [mkship()]
'''

# ---------------------------------------------------------------------------
# # User-defined classes
# class mc:
#     p = 0.003
#     u = 23
#     _priv = 13  # Python doesn't have private variables, but prefixing with _ conventionally denotes private
# x = mc()
# mc.p        # 0.003

# class Employee:
#     pass

# john = Employee()  # Create an empty employee record

# # Fill the fields of the record
# john.name = 'John Doe'
# john.dept = 'computer lab'
# john.salary = 1000

# john.__dict__
# Out[25]: {'name': 'John Doe', 'dept': 'computer lab', 'salary': 1000}


'''

def mkcoord(N=1) : return np.sort(rand(N)) * n

for s in combatants : 
    c = mkcoord(2)/15+2
    r[s] = I(*c)

'''

'''
randomly generate an interval in [0,1]
randomly generate an interval integer in [n1, n2]

round
'''
