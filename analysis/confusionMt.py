# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
# Source     : http://flowingdata.com/2010/01/21/how-to-make-a-heatmap-a-quick-and-easy-solution/
#
# Other Links:
#     http://stackoverflow.com/questions/14391959/heatmap-in-matplotlib-with-pcolor
#
# ------------------------------------------------------------------------

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
#%pylab inline
sys.path.append('../server/')
from city_polygons import *


page = open("cf_data_manhattan.csv", "r")
taxi = pd.read_csv(page, index_col=0)

# Normalize data columns
taxi_norm = taxi

#taxi_norm = (taxi - taxi.mean()) / (taxi.max() - taxi.min())
#print taxi.mean()
#print taxi.max()
#rint taxi.min()

#taxi_sort = taxi_norm.sort('PTS', ascending=True)

# Plot it out
fig, ax = plt.subplots()
heatmap = ax.pcolor(taxi_norm, cmap=plt.cm.Blues)#, alpha=0.8)

# Format
fig = plt.gcf()
fig.set_size_inches(18, 16.5)

# turn off the frame
ax.set_frame_on(False)

# put the major ticks at the middle of each cell
ax.set_yticks(np.arange(taxi_norm.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(taxi_norm.shape[1]) + 0.5, minor=False)

# want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()

# Set the labels
labels, labels2 = get_polygons_header()
# note I could have used nba_sort.columns but made "labels" instead
ax.set_xticklabels(taxi_norm.index, minor=False)
ax.set_yticklabels(taxi_norm.index, minor=False)
#ax.set_yticklabels(labels, minor=False)

# rotate the
plt.xticks(rotation=90)


ax.grid(False)

# Turn off all the ticks
ax = plt.gca()

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False


plt.ylabel('Origin Neighborhood')
plt.xlabel('Destination Neighborhood')
fig.colorbar(heatmap)

fig.savefig("CM_manhattan3.pdf")