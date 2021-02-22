# -*- coding: utf-8 -*-
"""
@title:     You sank my battleship!
@date:      22 Jan 2021
@author:    ferson
"""

import numpy as np
from numpy.random import *
import matplotlib.pyplot as plt
from time import sleep

#seed(0)                 # comment out to randomize
n = 102                 # length of each side of the theatre
times = range(150)      # duration of the battle
targeting = 0.5         # chance missile hits its target
killthreshold = 3       # number of landed missiles to destroy
combatants = range(60)  # number of agents in the battle
inertia = 15            # resistance to direction change
delay = 0.7; fast = 0.3 # seconds between animations
# more details in the initialisation section below

def mkcoord() : return float(rand(1) * n)

def mkangle() : return float(rand(1) * 2 * np.pi)

def swerve(a) : return float(a + randn(1) * np.pi / inertia)

def mkcoord() : return rand(1) * n

def mkangle() : return rand(1) * 2 * np.pi

def swerve(a) : return a + randn(1) * np.pi / inertia

def mult(lista, listb) : # elementwise multiply lists...why this doesn't exist?
    return [a*b for a,b in zip(lista,listb)]  # map(lambda x,y:x*y,lista,listb)

def circle(x,y,r,c='b') :
    C = plt.Circle((x,y),r,color=c,fill=False)
    fig = plt.gcf()
    ax = fig.gca()
    ax.add_patch(C)
    
def showship(s,c='b') :
    if not e[s] : return
    circle(x[s],y[s],1,c=c)
    circle(x[s],y[s],r[s],c=c)

def plural(k,word='',words='s') : 
    if type(k)==bool : kk=''
    else : kk = str(k)+' ' 
    if k==1 : return(kk+word)
    else : return kk+word+'s' if words=='s' else kk+words 
 
def canvas() : 
    top = 1.1 * n
    bot =-0.1 * n
    plt.scatter([bot,top,top,bot],[bot,bot,top,top],c='w')

def showtheatre() :
    canvas()
    for s in combatants : 
        if   2<h[s] : showship(s,'r')          # lots of fire
        elif 1<h[s] : showship(s,'tab:orange') # small fire
        else        : showship(s)
    left = e.count(True)
    arms = sum(mult(m,e))
    plt.title(plural(arms,'missile')+' across '+plural(left,'ship'))
    # plt.show()  
    return(left)
    
def exists(s) : return e[s]    

def dist(s,t) :
    return ((x[s]-x[t])**2+(y[s]-y[t])**2)**0.5

def fire(s,t) :
    launch = min(3,m[s])
    m[s] -= launch
    for i in range(launch) : 
        if rand(1) < targeting : h[t] += 1
           
def target(s) :
    if e[s] : 
      for t in combatants :
        if e[t] :
          if (t!=s) and (dist(s,t) < r[s]) : fire(s,t)

def assess(s) :
    if killthreshold < h[s] : e[s] = False

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
    print(color,'Ship',s,'currently',plural(e[s],'exists','does not exist'),'having suffered', plural(h[s],'missile strike'),coloroff)
    print(color,'\tLast location: ('+c(x[s])+',',c(y[s])+'), bearing',c(a[s]),'at speed',c(d[s]),coloroff)
    print(color,'\tRemaining complement:',plural(m[s],'missile'),'with a range of',c(r[s]),coloroff)

# initialise  
#i = list(combatants)                       # ship index
e = [True           for _ in combatants]    # whether the ship still exists
x = [mkcoord()      for _ in combatants]    # starting x position
y = [mkcoord()      for _ in combatants]    # starting y position
d = [mkcoord()/20+1 for _ in combatants]    # speed (displacement per time step)
a = [mkangle()      for _ in combatants]    # starting angle of travel
r = [mkcoord()/15+2 for _ in combatants]    # radar range
m = randint(10,60,len(combatants))          # how missiles it has
h = [0              for _ in combatants]    # 

# simulate
showtheatre()
for time in times :
    sleep(delay)
    for s in combatants : sail(s)
    for s in combatants : target(s)
    for s in combatants : assess(s)
    if 0==showtheatre() : break
    if e.count(True) < 10 : delay = fast

# report
for s in combatants : inventory(s)    

