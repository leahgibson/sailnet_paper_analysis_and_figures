"""
Analysis of the network mean timeseries.
"""

# import Python packages
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
import matplotlib.colors as colors
from scipy.stats import gaussian_kde
import pytz

# Set the font size for different plot elements
plt.rcParams.update({
    'font.size': 8,               # Font size for general text
    'axes.titlesize': 8,          # Font size for plot titles
    'axes.labelsize': 8,          # Font size for axis labels
    'xtick.labelsize': 8,         # Font size for x-axis ticks
    'ytick.labelsize': 8,         # Font size for y-axis ticks
    'legend.fontsize': 8,         # Font size for legend
    'lines.linewidth': 2.5         # Set linewidth 
})

class basicVisualization:
    """
    Class for basic visualization of data.
    """

    def __init__(self):
        self.standard_bins = ['b' + str(i) for i in range(16)]
        # for particle size distributions
        # self.dlogdp = [0.03645458169, 0.03940255269, 0.04033092159, 0.03849895488,
        #             0.03655010672, 0.04559350564, 0.08261548653, 0.06631586816,
        #             0.15575785, 0.1008071129, 0.1428650493, 0.1524763279,
        #             0.07769393472, 0.1571866015, 0.1130751916, 0.0867054262]
        
        # self.dlogdp = [0.035114496, 0.037103713, 0.040219114, 0.044828027, 0.050001836, 0.056403989, 0.129832168,
        #   0.137674163, 0.078941363, 0.09085512, 0.177187651, 0.137678593, 0.096164793, 0.112758467,
        #   0.107949615, 0.10986499]
        
        # CORRECTED USING UPDATED NOAA MIE TABLE
        self.dlogdp = [0.03645458169, 0.03940255269, 0.04033092159, 0.03849895488,
                    0.03655010672, 0.04559350564, 0.08261548653, 0.141566381,
                    0.080507337, 0.1008071129, 0.1428650493, 0.1559862,
                    0.112588743, 0.118781921, 0.1130751916, 0.0867054262]
        

        
        # self.diameter_midpoints = [149, 163, 178, 195, 213, 234, 272, 322, 422, 561, 748,
        #                     1054, 1358, 1802, 2440, 3062]
        
        self.diameter_midpoints = [149, 163, 178, 195, 213, 234, 272, 355, 455, 562, 749,
                            1059, 1431, 1870, 2440, 3062]
        
        # colorblind friendly colors
        # self.colors = ['#377eb8', '#ff7f00', '#4daf4a',
        #           '#f781bf', '#a65628', '#984ea3',
        #           '#999999', '#e41a1c', '#dede00']

        self.colors = plt.cm.viridis(np.linspace(0, 1, 6))

    def plot_network_timeseries(self, df, bin_name, rolling=None):
        """
        Basic plotting of network mean for specified bin.

        Inputs:
        - df: df of network mean
        - bin_name: name of bin to be plotted
        - rolling: default None or int for number of values to use in a rolling mean

        Output: plot

        Returns: none
        """


        if rolling is not None:
            timeseries_df = df.rolling(window=rolling, min_periods=1).mean()
            timeseries_df['DateTime'] = df['DateTime']
        else:
            timeseries_df = df


        plt.plot(timeseries_df['DateTime'], timeseries_df[bin_name])
        plt.gca().xaxis.set_major_locator(ticker.AutoLocator())
        plt.title(bin_name)
        plt.ylabel('cm$^{-3}$')
        plt.show()
    
    def plot_overlapping_timeseries(self, data, bin_name):
        """
        Plots the multiple years of data my overlaying them by day.
        
        Inputs:
        - data: df of notwork mean
        - bin_name: name of bin to be plotted

        Output: plot

        Returns: nothing
        """
        data['DateTime'] = pd.to_datetime(data['DateTime'])

        data['Year'] = data['DateTime'].dt.year

        year_groups = data.groupby('Year')

        fig, ax = plt.subplots(figsize=(6.6,2.5), dpi=300)
        for idx, group in enumerate(year_groups):
            df = group[1]
            # replace all years with 2023
            df['DateTime'] = df['DateTime'].apply(lambda x: x.replace(year=2023))
            # now remove year
            #df['DateTime'] = pd.to_datetime(df['DateTime'].dt.strftime('%m-%d %H:%M:%S'))
            

            ax.plot(group[1]['DateTime'], group[1][bin_name], linewidth=1.5, color=self.colors[idx*2], label=str(group[0]))
        plt.legend()

        custom_ticks = [
        (datetime(2023, 1, 1, 0, 0, 0), "Jan"),
        (datetime(2023, 2, 1, 0, 0, 0), "Feb"),
        (datetime(2023, 3, 1, 0, 0, 0), 'March'),
        (datetime(2023, 4, 1, 0, 0, 0), 'April'),
        (datetime(2023, 5, 1, 0, 0, 0), 'May'),
        (datetime(2023, 6, 1, 0, 0, 0), 'June'),
        (datetime(2023, 7, 1, 0, 0, 0), 'July'),
        (datetime(2023, 8, 1, 0, 0, 0), "Aug"),
        (datetime(2023, 9, 1, 0, 0, 0), "Sept"),
        (datetime(2023, 10, 1, 0, 0, 0), "Oct"),
        (datetime(2023, 11, 1, 0, 0, 0), "Nov"),
        (datetime(2023, 12, 1, 0, 0, 0), "Dec")
        ]
        ax.set_xticks([tick[0] for tick in custom_ticks])
        ax.set_xticklabels([tick[1] for tick in custom_ticks])
        #ax.set_title(bin_name)
        ax.set_ylabel('cm$^{-3}$')
        #ax.set_xlabel('UTC')
        plt.tight_layout()
        plt.show()

    def plot_psd(self, data, data2=None, data3=None):
        """
        Given the data, overages over all of it and plots a PSD 

        Option for adding a second psd

        Only takes 16 bin data
        
        Inputs:
        - data: df of data
        - data2: df of second data, default None
        
        Returns: none
        
        Outputs: plot of raw data, smoothed curve, and curve overlaying raw
        
        """

        psd = []
        for i, bin in enumerate(self.standard_bins):
            bin_avg = data[bin].mean()
            dndlogdp_val = bin_avg/self.dlogdp[i]
            psd.append(dndlogdp_val)
        
        # plot raw distribution
        plt.loglog(self.diameter_midpoints, psd, marker='o', color='black', label='2022-06-14')
        
        if data2 is not None:
            psd2 = []
            for i, bin in enumerate(self.standard_bins):
                bin_avg = data2[bin].mean()
                dndlogdp_val = bin_avg/self.dlogdp[i]
                psd2.append(dndlogdp_val)
            
            plt.loglog(self.diameter_midpoints, psd2, marker='^', color='blue', label='2022-06-16')
            plt.legend()
        
        if data3 is not None:
            psd3 = []
            for i, bin in enumerate(self.standard_bins):
                bin_avg = data3[bin].mean()
                dndlogdp_val = bin_avg/self.dlogdp[i]
                psd3.append(dndlogdp_val)
            
            plt.plot(self.diameter_midpoints, psd3, marker='s', color='green', label='2023-05-23')
            plt.legend()
        
        
        
        plt.ylabel('dN/dlogD$_p$')
        plt.xlabel('Diameter (nm)')
        plt.show()

    def plot_different_time_segments(self, data1, data2, bin_name):
        """
        Accepts two dfs of same length and will plot on same plot.
        
        Data can be from different time periods.
        
        Inputs:
        - data1: df of first timeseries
        - data2: df of second timeseries
        
        Output: plot
        
        Returns: none
        """

        data1['DateTime'] = pd.to_datetime(data1['DateTime'])
        data2['DateTime'] = pd.to_datetime(data2['DateTime'])

        fig = plt.figure()
        ax1 = fig.add_subplot(111, label='1')
        ax2 = fig.add_subplot(111, label='2', frame_on=False)

        color1='black'
        ax1.plot(data1['DateTime'], data1[bin_name], color=color1)
        ax1.set_ylabel('cm$^{-3}$', color=color1)  
        ax1.set_xlabel('Date', color=color1)
        ax1.tick_params(axis='x', labelcolor=color1)
        ax1.tick_params(axis='y', labelcolor=color1)

        # second plot
        color2='blue'
        ax2.plot(data2['DateTime'], data2[bin_name], color=color2)
        ax2.xaxis.tick_top()
        ax2.yaxis.tick_right()
        ax2.set_ylabel('cm$^{-3}$', color=color2)       
        ax2.xaxis.set_label_position('top') 
        ax2.yaxis.set_label_position('right') 
        ax2.tick_params(axis='x', colors=color2)
        ax2.tick_params(axis='y', colors=color2)

        plt.show()


        # # create secondary xaxis
        # ax2 = ax1.twiny()
        # ax2.plot(data2['DateTime'], data2[bin_name], color='magenta')
        # ax2.tick_params(axis='x', labelcolor='magenta')

        # # create secondary y-axis
        # ax3 = ax1.twinx()
        # ax3.plot(data1['DateTime'], data2[bin_name], color='magenta')
        # ax3.tick_params(axis='y', labelcolor='magenta')



        plt.show()





class temporalAnalysis:
    """
    Class for more in depth analysis of temporal trends in the network mean.
    """

    def __init__(self):
        self.years = [2021, 2022, 2023]
        self.months = [1,2,3,4,5,6,7,8,9,10,11,12]
        self.standard_bins = ['b' + str(i) for i in range(16)]

        # for particle size distributions
        # self.dlogdp = [0.03645458169, 0.03940255269, 0.04033092159, 0.03849895488,
        #             0.03655010672, 0.04559350564, 0.08261548653, 0.06631586816,
        #             0.15575785, 0.1008071129, 0.1428650493, 0.1524763279,
        #             0.07769393472, 0.1571866015, 0.1130751916, 0.0867054262]
        
        # self.diameter_midpoints = [149, 163, 178, 195, 213, 234, 272, 322, 422, 561, 748,
        #                     1054, 1358, 1802, 2440, 3062]

        self.dlogdp = [0.03645458169, 0.03940255269, 0.04033092159, 0.03849895488,
                    0.03655010672, 0.04559350564, 0.08261548653, 0.141566381,
                    0.080507337, 0.1008071129, 0.1428650493, 0.1559862,
                    0.112588743, 0.118781921, 0.1130751916, 0.0867054262]
        
        self.diameter_midpoints = [149, 163, 178, 195, 213, 234, 272, 355, 455, 562, 749,
                            1059, 1431, 1870, 2440, 3062]
        
        # colorblind friendly colors
        # self.colors = ['#377eb8', '#ff7f00', '#4daf4a',
        #           '#f781bf', '#a65628', '#984ea3',
        #           '#999999', '#e41a1c', '#dede00']

        self.colors = plt.cm.viridis(np.linspace(0, 1, 6))


    def basic_stats(self, data, bin_name):
        """
        Returns basic stats of the nework mean data for the given bin.
        
        Inputs:
        - data: df of network mean data
        - bin_name: name of bin header
        
        Prints:
        - maximum concentration and the day it occurs
        - minimum concentration and the day it occurs
        - average concentration 
        - average absolute percent change between timesteps
        """

        # max concentration data
        max_conc = data[bin_name].max()
        max_index = data[bin_name].idxmax()
        max_date = data.loc[max_index, 'DateTime']

        # min concentration data
        min_conc = data[bin_name].min()
        min_index = data[bin_name].idxmin()
        min_date = data.loc[min_index, 'DateTime']

        # average concentration
        avg_conc = np.mean(data[bin_name])
        # absolute percent change between time steps
        abs_percent_change = data[bin_name].pct_change().abs() # abs percent change = (|conc_{t+1} - conc_t|/conc_t)
        # compute average
        avg_change = (np.nanmean(abs_percent_change)*100)

        # # plot this data
        # plt.plot(abs_percent_change)
        # plt.title('Absolute Percent Change')
        # plt.show()

        print('BASIC STATISTICS') 
        print(f'Maximum Concentration: {max_conc} Occured on: {max_date}')
        print(f'Minimum Concentration: {min_conc} Occured on {min_date}')
        print(f'The average concentration is {avg_conc}')
        print(f'The average percent change between time steps is {avg_change}')
     
    

    def plot_monthly_diurnal(self, data, bin_names):
        """
        Plots the average diurnal cycle for each month
        averaging over each day in the month.

        Note: there must be more than one month present for plot to work.
        
        Inputs:
        - data: df of network mean, should be binned hourly
        - bin_name: list of name of bins to analyze
            if data is cov data, use bin_name='' #### FILL THIS IN ###
        
        Outputs: plot, range and percent change of diurnal pattern for each month
        
        Returns: none
        """

        month_dict = {
            1: 'Jan',
            2: 'Feb',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'Aug',
            9: 'Sept',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
        }
        data = data.copy()

        
        data['DateTime'] = pd.to_datetime(data['DateTime'])

        # convert to Colorado time
        colorado_tz = pytz.timezone('America/Denver')
        data['DateTime'] = data['DateTime'].dt.tz_localize('UTC').dt.tz_convert(colorado_tz)


        # group data
        data['Time'] = data['DateTime'].dt.time
        data['Month'] = data['DateTime'].dt.month
        data['Year'] = data['DateTime'].dt.year
        data['Day'] = data['DateTime'].dt.day

        print(data)

        # number of months in data
        num_months = data['Month'].nunique()
        

        daily_averages = {}
        for bin in bin_names:
            daily_averages[bin] = data.groupby(['Year', 'Month', 'Time'])[bin].mean()
        
        

        fig, axs = plt.subplots(nrows=1, ncols=num_months, sharex=True, sharey=True, figsize=(6.6,2.5), dpi=300)
        #colors=['blue', 'orange', 'green']
        ranges = {}
        percent_changes = {}
        for bin in bin_names:
            idx = 0
            for year in self.years:
                
                for month in self.months:
                    try:
                        axs[month-1].plot(daily_averages[bin][year][month].values, linewidth=1.5, label=bin, color=self.colors[idx*2])
                        axs[month-1].set_title(month_dict[month])
                        axs[month-1].set_xticks([6, 18])
                        axs[month-1].set_xticklabels(['6', '18'])

                        # compute the range for each month
                        max = np.nanmax(daily_averages[bin][year][month].values)
                        min = np.nanmin(daily_averages[bin][year][month].values)
                        range = max - min
                        percent_change = ((max-min)/min)*100

                        ranges[f'{bin}_{year}_{month}'] = range
                        percent_changes[f'{bin}_{year}_{month}'] = percent_change
                        
                        
                    except:
                        pass
                idx+=1
        axs[0].set_ylabel('cm$^{-3}$')
        axs[int(np.round(num_months/2))].set_xlabel('Local Time')
        
        # Create custom handles and labels for the legend
        legend_handles = [Line2D([0], [0], color=self.colors[0], lw=2),
                        Line2D([0], [0], color=self.colors[2], lw=2),
                        Line2D([0], [0], color=self.colors[4], lw=2)]

        legend_labels = ['2021', '2022', '2023']

        # Create a legend with custom handles and labels
        axs[-1].legend(handles=legend_handles, labels=legend_labels, loc='upper right')

        
                
        plt.show()

        # print(f'The ranges of each cycle are {ranges}')
        # print(f'The percent changes of each cycle are {percent_changes}')

    
    def plot_monthly_psd(self, data):
        """
        Plots the average monthly psd and the average normalized psd for each month.

        NOTE: data converted to local time for this analysis

        Note: only works for 16 bins and for 2022 year.
        
        Inputs:
        - data: df of network mean

        Outputs: twp diffrent plots

        Reutns: noone
        """
        
        # make groups into months 
        data['DateTime'] = pd.to_datetime(data['DateTime'])


        data['Time'] = data['DateTime'].dt.time
        data['Month'] = data['DateTime'].dt.month
        data['Year'] = data['DateTime'].dt.year
        data['Day'] = data['DateTime'].dt.day

        # number of months in data
        num_months = data['Month'].nunique()
        

        # organize dict to contain average for bin and months
        psd_dict = {}
        normalized_psd = {}

        # get averages for the sum
        total_averages = data.groupby(['Year', 'Month', 'Day'])['total'].mean()
        
  
        for i, bin in enumerate(self.standard_bins):
            # compute average over the days in the month for each bin
            daily_avgs = data.groupby(['Year', 'Month', 'Day'])[bin].mean()
            # avg over months
            for year in self.years:
                if str(year) in psd_dict:
                    pass
                else:
                    psd_dict[str(year)] = {}
                    normalized_psd[str(year)] = {}
                for month in self.months:
                    if str(month) in psd_dict[str(year)]:
                        pass
                    else:
                        psd_dict[str(year)][str(month)] = []
                        normalized_psd[str(year)][str(month)] = []
                    try:
                        # compute monthly average of bin
                        monthly_avg = np.mean(daily_avgs[year][month])
                        # convert to dndlogdp
                        dndlogdp_val = monthly_avg#/self.dlogdp[i]
                        psd_dict[str(year)][str(month)].append(dndlogdp_val)

                        # compute normalized average
                        monthly_total = np.mean(total_averages[year][month])
                        normalized_bin = monthly_avg/monthly_total
                        normalized_dndlogdp = normalized_bin/self.dlogdp[i]
                        normalized_psd[str(year)][str(month)].append(normalized_dndlogdp)
            
                    except:
                        pass
       
        
        month_names = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        
        # plot the particle dize distributions
        fig, axs = plt.subplots(nrows=1, ncols=12, sharex=True, sharey=True, figsize=(6.6,3), dpi=300)
        #year_colors = ['blue', 'orange', 'green']
        idx=0
        for year in self.years:
            i=0
            for month in self.months:
                try:
                    axs[month-1].loglog(self.diameter_midpoints, psd_dict[str(year)][str(month)], linewidth=1.5, color=self.colors[idx*2], label=str(year))
                    axs[month-1].set_title(month_names[(month)-1])

                    i+=1
                except:
                    pass
            idx+=1
        axs[0].set_ylabel('cm$^{-3}$')#('dn/dlogdp')
        # Create custom handles and labels for the legend
        legend_handles = [Line2D([0], [0], color=self.colors[0], lw=2),
                        Line2D([0], [0], color=self.colors[2], lw=2),
                        Line2D([0], [0], color=self.colors[4], lw=2)]

        legend_labels = ['2021', '2022', '2023']

        # Create a legend with custom handles and labels
        axs[-1].legend(handles=legend_handles, labels=legend_labels, ncols=3, handlelength=0.5, handletextpad=0.5, loc='upper right')

        fig.supxlabel('Diameter (nm)')

        plt.tight_layout()
        plt.show()

        # # normalized psd plot
        # fig, axs = plt.subplots(nrows=1, ncols=num_months, sharex=True, sharey=True)
        # i=0
        # for month in self.months:
        #     try:
        #         axs[i].loglog(self.diameter_midpoints, normalized_psd[str(month)])
        #         axs[i].set_title('2022'+'-'+str(month))

        #         i+=1
        #     except:
        #         pass
        # axs[0].set_ylabel('normalized dn/dlogdp')
        # axs[int(np.round(num_months/2))].set_xlabel('Diameter (nm)')

        # plt.show()

    def plot_psd_timeseries(self, data):
        """
        Plots a colormap of the psd over time.
        
        Only works for the 16 bin structure

        Inputs:
        - data: df of network mean data
        
        Returns: none

        Output: colormap plot
        """

        # Replace values equal to 0 with NaN
        data.replace(0, np.nan, inplace=True) 

        # compute dn/dlogdp lavlues and reformat for plotting
        dndlogdp_matrix = []
        # rehape to [[bin0time0, bin0time1, ...',
        #               bin1time0, bin1time1, ...], ...]
        for i, bin in enumerate(self.standard_bins):
            # compute dn/dlogdp for each bin
            row = np.array((data[bin]/self.dlogdp[i]).tolist())
            # remove values that are too small    
            dndlogdp_matrix.append(row)
        
        dndlogdp_matrix = np.array(dndlogdp_matrix)
        
        # set up meshgrid
        diameters = self.diameter_midpoints
        times = data['DateTime'].tolist()
        #times, diameters = np.meshgrid(data['DateTime'].tolist(), diameters)

        # plot contour plot with log-y axis
        fig, ax = plt.subplots(figsize=(6.6,2.4), dpi=300)
        contour_levels = np.logspace(np.log10(np.nanmin(dndlogdp_matrix)), np.log10(np.nanmax(dndlogdp_matrix)), 500)
        contour = ax.contourf(times, diameters, dndlogdp_matrix, norm=colors.LogNorm(), levels=contour_levels, cmap='inferno')
        ax.set_yscale('log')

        # make sure colorbar shows
        cbar = fig.colorbar(contour)

        # make cbar labels
        cbar_ticks = np.logspace(np.ceil(np.log10(np.nanmin(dndlogdp_matrix))), np.floor(np.log10(np.nanmax(dndlogdp_matrix))), 6)
        cbar.set_ticks(cbar_ticks)
        cbar.set_ticklabels(['$10^{{{}}}$'.format(int(np.log10(tick))) for tick in cbar_ticks])

        # make label for colorbar
        cbar.set_label('dN/dlogD$_p$')

        # y-axis label
        ax.set_ylabel('D$_p$ (nm)')
        #ax.set_xlabel('UTC')

        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))

        plt.tight_layout()
        plt.show()
 
    def plot_monthly_bin_average(self, data, bin_names):
        """
        Plots the average value of the specified bins for each month.

        Inputs:
        - data: df of network mean
        - bin_names: list of bin names

        Output: plot

        Returns: none
        """

        # make groups into months 
        data['DateTime'] = pd.to_datetime(data['DateTime'])

        data['Time'] = data['DateTime'].dt.time
        data['Month'] = data['DateTime'].dt.month
        data['Year'] = data['DateTime'].dt.year
        data['Day'] = data['DateTime'].dt.day

        # number of months in data
        num_months = data['Month'].nunique()

        
        daily_averages = {}
        for bin in bin_names:
            daily_averages[bin] = data.groupby(['Year', 'Month', 'Time'])[bin].mean()

        # compute the average value of each month for each bin and save to dict
        bin_averages = {}
        for bin in bin_names:
            bin_averages[bin] = {}
            for year in self.years:
                for month in self.months:
                    try:
                        avg = np.mean(daily_averages[bin][year][month])
                        bin_averages[bin][f'{year}-{month}'] = avg
                    except:
                        pass
        
        # plot data
        for bin in bin_names:
            plt.semilogy(list(bin_averages[bin].values()), label=bin)
        plt.xlabel('Date')
        plt.ylabel('cm$^{-3}$')
        # make custom ticks
        custom_ticks = [i for i in range(num_months)] 
        custom_labels = list(bin_averages[bin].keys()) # use last bin because all same
        plt.xticks(custom_ticks, custom_labels)
        plt.legend()
        plt.show()
                
    def plot_seasonal_diurnal(self, network_data, site_data, bin_name):
        """
        Groups data seasonally (March-May, June-Aug, Sept-Nov, Dec-Feb)
        and plots average diurnal for network mean with shading based on sites

        Inputs:
        - network_data: network mean
        - site_data: site data as a dict
        - bin_name: name of bin to plot
        """

    
        # convert to MST
        colorado_tz = pytz.timezone('MST')
        network_data = network_data.copy()
        network_data['DateTime'] = pd.to_datetime(network_data['DateTime'])

        network_data['DateTime'] = network_data['DateTime'].dt.tz_localize('UTC').dt.tz_convert(colorado_tz)
        
        site_dict = {}
        # group data by meterological seasons
        for site, df in site_data.items():
            df = df.copy()
            df['DateTime'] = pd.to_datetime(df['DateTime'])
            df['DatetIme'] = df['DateTime'].dt.tz_localize('UTC').dt.tz_convert(colorado_tz)
            site_dict[site] = df
        
        # group data by season
        network_data['Season'] = network_data['DateTime'].dt.month.apply(self._sort_season)
        # group by time
        network_data['Hour'] = network_data['DateTime'].dt.time

        # averages
        network_averages = network_data.groupby(['Season', 'Hour']).mean().reset_index()
        network_averages['Hour'] = network_averages['Hour'].apply(lambda x: x.strftime('%H'))
        network_q1 = network_data.groupby(['Season', 'Hour']).quantile(0.25).reset_index()
        network_q1['Hour'] = network_q1['Hour'].apply(lambda x: x.strftime('%H'))
        network_q3 = network_data.groupby(['Season', 'Hour']).quantile(0.75).reset_index()
        network_q3['Hour'] = network_q3['Hour'].apply(lambda x: x.strftime('%H'))
        
        seasonal_averages_dict = {}
        seasonal_q1_dict = {}
        seasonal_q3_dict = {}
        for site, df in site_dict.items():
            df['Season'] = df['DateTime'].dt.month.apply(self._sort_season)
            df['Hour'] = df['DateTime'].dt.time
            seasonal_averages_dict[site] = df.groupby(['Season', 'Hour']).mean().reset_index()
            seasonal_q1_dict[site] = df.groupby(['Season', 'Hour']).quantile(0.25).reset_index()
            seasonal_q3_dict[site] = df.groupby(['Season', 'Hour']).quantile(0.75).reset_index()
        
        n_sites = len(site_dict.keys())

        fig, axes = plt.subplots(ncols=4, nrows=n_sites, sharey=True, sharex=True, figsize=(6.6,1.2*n_sites), dpi=300)

        for i, site in enumerate(site_dict.keys()):
            averages = seasonal_averages_dict[site]
            q1 = seasonal_q1_dict[site]
            q3 = seasonal_q3_dict[site]

            # convert hours to strings
            averages['Hour'] = averages['Hour'].apply(lambda x: x.strftime('%H'))
            q1['Hour'] = q1['Hour'].apply(lambda x: x.strftime('%H'))
            q3['Hour'] = q3['Hour'].apply(lambda x: x.strftime('%H'))

            # spring
            spring_avgs = averages[averages['Season'] == 'Spring']
            spring_q1 = q1[q1['Season'] == 'Spring']
            spring_q3 = q3[q3['Season'] == 'Spring']
            network_spring = network_averages[network_averages['Season'] == 'Spring']
            axes[i,0].plot(spring_avgs['Hour'], spring_avgs[bin_name], color='#f781bf')
            # fill between q1 and q3
            axes[i,0].fill_between(spring_q1['Hour'], spring_q1[bin_name], spring_q3[bin_name], color='#f781bf', alpha=0.3)
            axes[i,0].set_ylabel(f'{site} \n cm$^{-3}$')
            axes[i,0].set_xticks([0, 12, 23])

            # summer
            summer_avgs = averages[averages['Season'] == 'Summer']
            summer_q1 = q1[q1['Season'] == 'Summer']
            summer_q3 = q3[q3['Season'] == 'Summer']
            axes[i,1].plot(summer_avgs['Hour'], summer_avgs[bin_name], color='#4daf4a')
            # fill between q1 and q3
            axes[i,1].fill_between(summer_q1['Hour'], summer_q1[bin_name], summer_q3[bin_name], color='#4daf4a', alpha=0.3)

            # fall
            fall_avgs = averages[averages['Season'] == 'Fall']
            fall_q1 = q1[q1['Season'] == 'Fall']
            fall_q3 = q3[q3['Season'] == 'Fall']
            axes[i,2].plot(fall_avgs['Hour'], fall_avgs[bin_name], color='#ff7f00')
            # fill between q1 and q3
            axes[i,2].fill_between(fall_q1['Hour'], fall_q1[bin_name], fall_q3[bin_name], color='#ff7f00', alpha=0.3)
            
            # winter
            winter_avgs = averages[averages['Season'] == 'Winter']
            winter_q1 = q1[q1['Season'] == 'Winter']
            winter_q3 = q3[q3['Season'] == 'Winter']
            axes[i,3].plot(winter_avgs['Hour'], winter_avgs[bin_name], color="#377eb8")
            # fill between q1 and q3
            axes[i,3].fill_between(winter_q1['Hour'], winter_q1[bin_name], winter_q3[bin_name], color="#377eb8", alpha=0.3)
     
        # plot network mean in the last row
        network_spring = network_averages[network_averages['Season'] == 'Spring']
        network_summer = network_averages[network_averages['Season'] == 'Summer']
        network_fall = network_averages[network_averages['Season'] == 'Fall']
        network_winter = network_averages[network_averages['Season'] == 'Winter']

        # quantiles
        network_spring_q1 = network_q1[network_q1['Season'] == 'Spring']
        network_summer_q1 = network_q1[network_q1['Season'] == 'Summer']
        network_fall_q1 = network_q1[network_q1['Season'] == 'Fall']
        network_winter_q1 = network_q1[network_q1['Season'] == 'Winter']
        network_spring_q3 = network_q3[network_q3['Season'] == 'Spring']
        network_summer_q3 = network_q3[network_q3['Season'] == 'Summer']
        network_fall_q3 = network_q3[network_q3['Season'] == 'Fall']
        network_winter_q3 = network_q3[network_q3['Season'] == 'Winter']

        # # spring
        # axes[-1,0].plot(network_spring['Hour'], network_spring[bin_name], color='#4daf4a')
        # # fill between q1 and q3
        # axes[-1,0].fill_between(network_spring_q1['Hour'], network_spring_q1[bin_name], network_spring_q3[bin_name], color='#4daf4a', alpha=0.3)
        # axes[-1,0].set_ylabel('Network Mean \n cm$^{-3}$')

        # # summer
        # axes[-1,1].plot(network_summer['Hour'], network_summer[bin_name], color='#4daf4a')
        # # fill between q1 and q3
        # axes[-1,1].fill_between(network_summer_q1['Hour'], network_summer_q1[bin_name], network_summer_q3[bin_name], color='#4daf4a', alpha=0.3)

        # # fall
        # axes[-1,2].plot(network_fall['Hour'], network_fall[bin_name], color='#ff7f00')
        # # fill between q1 and q3
        # axes[-1,2].fill_between(network_fall_q1['Hour'], network_fall_q1[bin_name], network_fall_q3[bin_name], color='#ff7f00', alpha=0.3)

        # # winter
        # axes[-1,3].plot(network_winter['Hour'], network_winter[bin_name], color="#377eb8")
        # # fill between q1 and q3
        # axes[-1,3].fill_between(network_winter_q1['Hour'], network_winter_q1[bin_name], network_winter_q3[bin_name], color="#377eb8", alpha=0.3)
                                          
        # set season names
        axes[0,0].set_title("Spring")
        axes[0,1].set_title("Summer")
        axes[0,2].set_title("Fall")
        axes[0,3].set_title("Winter")

        # set xlabel for fig
        fig.supxlabel('MST')

        plt.tight_layout()
        plt.savefig('new_fig.png')
        plt.show()


    
    def _sort_season(self, month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall'

