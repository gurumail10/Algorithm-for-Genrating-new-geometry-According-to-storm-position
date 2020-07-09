

import numpy as np
import matplotlib.pyplot as plt

def simplify(x,y,nmax,gamma):
    if x[0] == x[-1] and y[0] == y[-1]: # it's a loop
        n = len(x) - 1
    else:
        n = len(x) # number of vertices without repeats
        x.append(x[0])
        y.append(y[0])
    if n <= nmax:
        return x,y
    
    image_size = max(max(x)-min(x),max(y)-min(y))
    
    # calculate sides
    sides = []
    skips = []
    x.append(x[1]) # one more point from the beginning
    y.append(y[1])
    for i in range(n):
        a = np.sqrt((x[i+1]-x[i])*(x[i+1]-x[i])+
                    (y[i+1]-y[i])*(y[i+1]-y[i]))
        c = np.sqrt((x[i+2]-x[i])*(x[i+2]-x[i])+
                    (y[i+2]-y[i])*(y[i+2]-y[i]))
        sides.append(a)
        skips.append(c)
    sides.append(sides[0])
    
    # calculate heights
    h_only = []
    for i in range(n):
        a = sides[i]
        b = sides[i+1]
        c = skips[i]
        p = (a+b+c)/2
        s2 = p*(p-a)*(p-b)*(p-c)
        if s2 <= 0:
            s = 0
        else:
            s = np.sqrt(s2)
        h = s / c # it's 2h actually
        h_only.append(h) 
        
    # Now remove the smallest feature, update the list of sides
    # and skips, and iterate until done

    while True:
        n = len(skips)
        if n <= nmax or min(h_only) > image_size*gamma:
            break
        heights = [(h_only[i],i) for i in range(n)]
        (h,i) = sorted(heights)[0]
        i += 1 # the vertex is one step to the right
        if i == n:
            i = 0
            
        if i == 0:
            x.pop(n) # this is a copy of x[0]
            y.pop(n)
            x.pop(i)
            y.pop(i)
            x.append(x[1]) # copy of 2nd vertex
            y.append(y[1])
        
            sides.pop(-1) # this is a copy of sides[0]
            sides.pop(0)
            sides[-1] = skips[-1]
            sides.append(sides[0])
            
            # recalculate side c on the left
            a = sides[-2]
            b = sides[-1]
            c = np.sqrt((x[-3]-x[-1])*(x[-3]-x[-1])+
                        (y[-3]-y[-1])*(y[-3]-y[-1]))
            skips.pop(i)
            skips[-1] = c
            p = (a+b+c)/2
            s2 = p*(p-a)*(p-b)*(p-c)
            if s2 < 0:
                s = 0
            else:
                s = np.sqrt(s2)
            h = s / c # it's 2h actually
            h_only.pop(i)
            h_only[-1] = h
            
            # and one more position further to the left
            a = sides[-3]
            b = sides[-2]
            c = np.sqrt((x[-4]-x[-2])*(x[-4]-x[-2])+
                        (y[-4]-y[-2])*(y[-4]-y[-2]))
            skips[-2] = c
            p = (a+b+c)/2
            s2 = p*(p-a)*(p-b)*(p-c)
            if s2 < 0:
                s = 0
            else:
                s = np.sqrt(s2)
            h = s / c # it's 2h actually
            h_only[-2] = h

        elif i == n-1:
            x.pop(i)
            y.pop(i)
            sides[i-1] = skips[i-1]
            sides.pop(i)
            
            # recalculate side c 
            a = sides[-2]
            b = sides[-1]
            c = np.sqrt((x[-3]-x[-1])*(x[-3]-x[-1])+
                        (y[-3]-y[-1])*(y[-3]-y[-1]))
            skips[i-1] = c
            skips.pop(i)
            p = (a+b+c)/2
            s2 = p*(p-a)*(p-b)*(p-c)
            if s2 < 0:
                s = 0
            else:
                s = np.sqrt(s2)
            h = s / c # it's 2h actually
            h_only[i-1] = h
            h_only.pop(i)

            # and one more position on the left
            a = sides[-3]
            b = sides[-2]
            c = np.sqrt((x[-4]-x[-2])*(x[-4]-x[-2])+
                        (y[-4]-y[-2])*(y[-4]-y[-2]))
            skips[-2] = c
            p = (a+b+c)/2
            s2 = p*(p-a)*(p-b)*(p-c)
            if s2 < 0:
                s = 0
            else:
                s = np.sqrt(s2)
            h = s / c # it's 2h actually
            h_only[-2] = h
            
        else:
            n = len(skips)
            if i == 1:
                x.pop(-1) # this is a copy of x[1]
                y.pop(-1)
            x.pop(i)
            y.pop(i)
            if i == 1:
                x.append(x[1]) # append the new x[1]
                y.append(y[1])
            sides[i-1] = skips[i-1]
            sides.pop(i)
            sides.pop(-1)
            sides.append(sides[0])

            # recalculate side c on the left
            a = sides[i-1]
            b = sides[i]
            c = np.sqrt((x[i+1]-x[i-1])*(x[i+1]-x[i-1])+
                        (y[i+1]-y[i-1])*(y[i+1]-y[i-1]))
            skips[i-1] = c
            skips.pop(i)
            p = (a+b+c)/2
            s2 = p*(p-a)*(p-b)*(p-c)
            if s2 < 0:
                s = 0
            else:
                s = np.sqrt(s2)
            h = s / c # it's 2h actually
            h_only[i-1] = h
            h_only.pop(i)
            
            # and one more position to the left
            j = i-2 if i-2>=0 else n-2
            a = sides[j]
            b = sides[i-1]
            c = np.sqrt((x[i]-x[j])*(x[i]-x[j])+
                        (y[i]-y[j])*(y[i]-y[j]))
            skips[j] = c
            p = (a+b+c)/2
            s2 = p*(p-a)*(p-b)*(p-c)
            if s2 < 0:
                s = 0
            else:
                s = np.sqrt(s2)
            h = s / c # it's 2h actually
            h_only[j] = h

    x.pop(-1)
    y.pop(-1)
    return x,y


# generate a random irregular rectangle 

N = 10
x = [0]
y = [0]
for i in range(10):
    x.append(round(x[-1] + np.random.rand(),4))
    y.append(round(np.random.randn()/N,4))

x0 = x[-1]
for i in range(10):
    x.append(round(x0 + np.random.randn()/N,4))
    y.append(round(y[-1] + np.random.rand(),4))
    
y0 = y[-1]
for i in range(10):
    x.append(round(x[-1] - np.random.rand(),4))
    y.append(round(y0 + np.random.randn()/N,4))
    
x0 = x[-1]
for i in range(10):
    x.append(round(x0 + np.random.randn()/N,4))
    y.append(round(y[-1] - np.random.rand(),4))
    
x.append(x[0])
y.append(y[0])

x0 = x[:]
y0 = y[:]

fig = plt.figure(1, figsize=(5,5), dpi=90)
ax = fig.add_subplot(111)
ax.plot(x,y,color='#9999ff',linewidth=7)

nmax = 4
gamma = 10/256 # tolerance parameter
x,y = simplify(x,y,nmax,gamma)
ax.plot(x,y,color='#ff6600',linewidth=1)

print('Number of points dropped from %d to %d' % (len(x0)-1,len(x)-1))

