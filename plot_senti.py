import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    pullData = open("tweets.txt","r").read()
    line = pullData.split('\n')
    xar = []
    yar = []
    x=0
    y=0
    for data in line:
        x+=1
        if data =='pos':
            y+=1
        else:
            y-=1
        xar.append(x)
        yar.append(y)
    ax1.clear()
    ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
