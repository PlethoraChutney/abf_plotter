import pyabf
import sys
import pyabf.plot
import matplotlib.pyplot as plt

try:
    abf = pyabf.ABF(sys.argv[1])
except IndexError:
    print('Must include name of file to analyze')
    sys.exit(1)

abf.setSweep(0)


fig, ax = plt.subplots()


ax.plot(abf.sweepX, abf.sweepY, color = 'black')

ax.set(xlabel = 'Time (sec)', ylabel = 'Clamp Current (pA)')

# add horizontal tag lines
yvals = []
xmins = []
xmaxes = []
colors = []
legends = []
for i, tagTimeSec in enumerate(abf.tagTimesSec):
    start_x = abf.tagTimesSec[i]
    try:
        end_x = abf.tagTimesSec[i+1]
    except IndexError:
        end_x = max(abf.sweepX)
    comment = abf.tagComments[i]
    color = 'C%d' % (int(comment[-3]))
    yvals.append(10)
    xmins.append(start_x)
    xmaxes.append(end_x)
    colors.append(color)
    legends.append(comment[-3])

ax.hlines(yvals, xmins, xmaxes, colors = colors, linewidths = 3)

for y, xmin, xmax, color in zip(yvals, xmins, xmaxes, colors):
    mid = (xmin + xmax) / 2
    ax.text(mid, y + 7, color[-1], horizontalalignment = 'center')

# this also hides the frame and axes
pyabf.plot.scalebar(abf = abf)
plt.show()
