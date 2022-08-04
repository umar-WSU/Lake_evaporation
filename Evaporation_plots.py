#!/data/lar/bin/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:08:46 2022

@author: UmarFarooq
"""

import numpy as np
from scipy.stats import theilslopes
from statistics import mean
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl


def PMvsLISSS_plot(dfs,variable,error_values,fig_name):
    """
    To plot seasonal spatial difference in the PM and LISSS E, and respective mean bias error.
    input: 1) variable: list of seasonal dataframes
           2) variable: name of variable for spatial plots
           3) Error values for mean bias plot
           4) fig_name: figure name to save
    output: subplots a) the entire periods with open water, b) summer, c) autumn
    """
    nrows = 3
    ncols = 2
    fig, axes = plt.subplots(nrows, ncols, figsize=(7,6),sharex='col',sharey='col',gridspec_kw={'width_ratios':[1.2,.8]})
    marker_size = 0.3
    labels = list('abc')
    
    for i in range(len(nrows)):
        ##---------------------- base map -------------------------------------  
        map = Basemap(projection='cyl',llcrnrlat=-60,urcrnrlat=71,llcrnrlon=-180,urcrnrlon=180,resolution='c',ax = axes[i,0])
        map.drawcoastlines(color='gray',linewidth = 0.1)
        axes[i,0].tick_params(axis = 'both', direction = 'in',which = 'major', labelsize = 7)
        plt.setp(axes[i,0], xticks=[-120,-60,0,60,120], yticks=[-60,-30,0,30,60,75])
        axes[i,0].set_yticklabels(('60S','30S','EQ','30N','60N',''))
        axes[i,0].set_xticklabels(('120W','60W','0','60E','120E'))
        axes[i,0].yaxis.set_ticks_position('both')
        axes[i,0].xaxis.set_ticks_position('both')
        axes[i,0].set_aspect(1.3)

        cmap = mpl.colors.ListedColormap(['#0099ff','yellow','#ffb300','#ff8000','red','#b30000'])
        cmap.set_over('#4c0000')
        cmap.set_under('#000080')
        bounds = [-.3,0,.3,.6,.9,1.2,1.5] 
        ticks  = bounds
        decimel = '%.1f'
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cs = map.scatter(dfs[i]['lon'],dfs[i]['lat'],marker_size,latlon=True, c=dfs[i][variable],cmap=cmap,norm=norm)
   
    ##---------------------- bar chart-----------------------------------------
        barWidth = 0.4
        r1 = np.arange(len(error_values))
        axes[i,1].bar(r1, error_values, color='m', width=barWidth, edgecolor='k', label='MBE')
        axes[i,1].set_xlabel(None)
        plt.setp(axes[i,0], xticks=[0,1,2,3,4,5])
        axes[i,1].set_xticklabels(['Global','Tropical', 'Temperate', 'Arid', 'Cold', 'Polar'],rotation=90)
        axes[i,1].tick_params(axis = 'both', direction = 'in', labelsize = 8)
        axes[i,1].set_ylabel('MBE (%)', fontsize="8")
        axes[i,1].yaxis.set_ticks_position('both')
        axes[i,1].annotate(f'{labels[i]}', xy=(-.13, 1.02), xycoords='axes fraction',fontweight='bold',fontsize= 10)

    cb_ax = fig.add_axes([.145, 0.09, 0.36, 0.015])
    cbar = fig.colorbar(cs,cax=cb_ax, cmap=cmap,orientation='horizontal', pad = 0.92, aspect=30,
                        ticks=ticks, shrink=0.92, format=decimel,extend = 'both')
    cbar.ax.tick_params(labelsize=8, direction = 'in')
    cbar.set_label('ΔE (mm d$^-$$^1$)',size=8)
    plt.savefig(fig_name, dpi = 300)       


def timeseries_plots(anomaly_dfs,trend_dfs,fig_name):
    """
    To plot anomaly time-series of the PM, LISSS, and PM_LISSS, and zonal and mean trend values of the cliamte regions
    input: 1) anomaly_dfs: A list containg anomaly df for each season
           2) trend_dfs:  A list containg trends df for each season
           3) fig_name: figure name to save plot
    output: subplots subplots a) the entire periods with open water, b) summer, c) autumn,
    """
    nrows = 3
    ncols = 2
    fig, axes = plt.subplots(nrows, ncols, figsize=(6,4.5),sharex='col',gridspec_kw={'width_ratios':[1.2,.8]})
    labels = list('abc')
    
    for i in range(len(nrows)):
        x_values = np.arange(2001, 2017,1)
        axes[i,0].plot(x_values, anomaly_dfs[i]['PM'],       color='r', linestyle = 'dashed', marker='o', markersize=2, linewidth = .8, label='PM')
        axes[i,0].plot(x_values, anomaly_dfs[i]['LISSS'],    color='b', linestyle = 'dashed', marker='x', markersize=2, linewidth = .8, label='LISSS')
        axes[i,0].plot(x_values, anomaly_dfs[i]['PM_LISSS'], color='g', linestyle = 'dashed', marker='^', markersize=2, linewidth = .8, label='PM-LISSS')
        axes[i,0].tick_params(axis='both', direction = 'in', colors= 'k', labelsize = '6')
        plt.setp(axes[i,0], xticks=[2001,2008,2016])
        axes[i,0].set_ylabel('E anomaly \n (mm yr$^-$$^1$)' ,fontsize = '6')
        axes[i,0].legend(frameon=False,fontsize=5,loc='upper left')
        axes[2,0].set_xlabel('Year' ,fontsize = '6')
 
    #-----------   bar plot --------------------------------------------------
        barWidth = 0.2
        r1 = np.arange(trend_dfs[i]['PM'].shape[1])
        r2 = [x+.01 + barWidth for x in r1]
        r3 = [x+.01 + barWidth for x in r2]

        axes[i,1].bar(r1, trend_dfs[i]['PM'],       color='r', width=barWidth, edgecolor='k', linewidth=0.5,label='PM')
        axes[i,1].bar(r2, trend_dfs[i]['LISSS'],    color='b', width=barWidth, edgecolor='k', linewidth=0.5,label='LISSS')
        axes[i,1].bar(r3, trend_dfs[i]['PM_LISSS'], color='g', width=barWidth, edgecolor='k', linewidth=0.5,label='PM-LISSS')
        plt.setp(axes[i,1], xticks=[0,1,2,3,4,5])
        axes[i,1].set_xlabel(None)
        axes[i,1].set_xticklabels(['Global','Tropical', 'Temperate', 'Arid', 'Cold', 'Polar'],rotation=90)
        axes[i,1].yaxis.set_ticks_position('both')
        axes[i,1].tick_params(axis = 'both', direction = 'in', which = 'major', labelsize = 6)
        axes[i,1].set_ylabel('E trend (mm yr$^-$$^2$)', fontsize="6")
        axes[0,1].legend(frameon=False,fontsize=4)
        axes[i,0].annotate(labels[i], xy=(-0.22, 1), xycoords='axes fraction',fontsize=8,fontweight ='bold')\

    plt.savefig(fig_name, dpi = 300)
