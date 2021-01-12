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

for i, tagTimeSec in enumerate(abf.tagTimesSec):
    posX = abf.tagTimesSec[i]
    comment = abf.tagComments[i]
    color = 'C%d' % (i + 1)
    ax.axvline(posX, label = comment, color = color, ls = '--')

# this also hides the frame and axes
pyabf.plot.scalebar(abf = abf)
plt.show()
