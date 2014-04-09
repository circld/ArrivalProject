# Objective: explore LIRR arrival data in preparation for predictive analytics

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import pylab as pl

data = pd.read_table('ArrivalData.txt', sep=' ')

# build track number -> side dict
tracks = data['track'].unique()
tracks.sort()
trackSide = np.array([1, 0, 1, 0, 1, 2, 0, 1])
tracksMap = {i : j for i, j in zip(tracks, trackSide)}

def plotScatter(data, fig, plotNum, mapping=None):
    '''
    Inputs: dataframe, plt.figure, subplot number, track->side dict (opt)
    Returns: None
    '''
    num = plotNum
    delay = data['min']
    tracks = data['track']
    
    if mapping is not None:
        try:
            tracks = data['track'].apply(lambda x : mapping[x])
        except:
            raise ValueError('Please verify that mapping = dict obj')
    
    trkUnique = tracks.unique()
    trkUnique.sort()

    # build plot
    fig1 = fig
    ax1 = fig1.add_subplot('12' + str(num))
    x = ax1.scatter(delay, tracks, s=np.ones(data.shape[0]) * 50,
                    marker='o', c = tracks, alpha=0.8)
    pl.xlabel('Delay in Minutes')
    pl.ylabel('Track # / Side')
    ccm=x.get_cmap()
    
    # build legend (rescale since palette [0, 1])
    circles=[pl.Line2D(range(1), range(1), color='w', marker='o', markersize=10,
            markerfacecolor=item) for item in 
            ccm((trkUnique - trkUnique.min()) / 
                    float(trkUnique.max() - trkUnique.min()))]
    
    leg = pl.legend(circles, [str(i) for i in trkUnique], 
                    loc = "center left", bbox_to_anchor = (1, 0.5), 
                    numpoints = 1)

# need way to calculate probability of track-group-membership
# as a function of delay

if __name__ == '__main__':
    
    # visualization
    fig = pl.figure(1)
    pl.subplot(121)
    plotScatter(data, fig, 1)
    pl.subplot(122)
    plotScatter(data, fig, 2, tracksMap)