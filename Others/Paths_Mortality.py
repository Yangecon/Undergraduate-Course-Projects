import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

# ----------------------------
# Globals / Dictionarys
# ----------------------------

# input file path
datapath = 'F:/IESR/CDC/data/RawMortality_age.dta'
# output file path
save_dir = 'F:/IESR/CDC/document/'
# define the list of variables to plot
variables = ['deathrate', 'deathrate0_1', 'deathrate1_44', 'deathrate45_64', 'deathrate65']
titles = ['All-cause Mortality', 'Mortality (Age 0-1)', 'Mortality (Age 1-44)', 'Mortality (Age 45-64)', 'Mortality (Age 65+)']
filenames = ['Mortality_County_Paths_All', 'Mortality_County_Paths_Age1', 'Mortality_County_Paths_Age1-44', 'Mortality_County_Paths_Age45-64', 'Mortality_County_Paths_Age65']

data = pd.read_stata(datapath)

# ----------------------------
# Plotting to check the paths
# ----------------------------

for var, title, filename in zip(variables, titles, filenames):
    # Extract core variables
    core_data_new = data[['state', 'county', 'year', var]]
    
    # Calculate the average mortality rate per state per year
    state_avg_new = core_data_new.groupby(['state', 'year'])[var].mean().reset_index()

    # Get the list of all states
    states_new = core_data_new['state'].unique()

    # 7 rows and 7 columns, 48 states
    fig, axes = plt.subplots(nrows=7, ncols=7, figsize=(15, 15), sharex=False, sharey=True)
    axes = axes.flatten()

    # Plot for each state
    for i, state in enumerate(states_new):
        ax = axes[i]

        # Get data
        state_data_new = core_data_new[core_data_new['state'] == state]

        # Plot mortality trends for each county
        for county in state_data_new['county'].unique():
            county_data_new = state_data_new[state_data_new['county'] == county]
            ax.plot(county_data_new['year'], county_data_new[var], color='gray', alpha=0.5, linewidth=0.7)

        # Plot the average mortality trend for the state
        state_avg_data_new = state_avg_new[state_avg_new['state'] == state]
        ax.plot(state_avg_data_new['year'], state_avg_data_new[var], color='red', alpha=0.7, linewidth=1)

        # Set axis color to gray
        ax.spines['bottom'].set_color('gray')
        ax.spines['top'].set_color('gray')
        ax.spines['right'].set_color('gray')
        ax.spines['left'].set_color('gray')

        # Set axis labels   
        ax.set_xlim(1979, 2016)
        ax.set_ylim(0, core_data_new[var].max())
        ax.set_xticks(range(1980, 2020, 10))
        ax.set_yticks([y/100 for y in range(0, int(core_data_new[var].max()*100)+1)])
        ax.yaxis.set_major_locator(MaxNLocator(nbins='auto', prune='lower'))

        # Add grid lines
        ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        # Set subplot title
        ax_title = state
        ax.text(0.5, 1.02, ax_title, transform=ax.transAxes, fontsize=13, color='black',
                ha='center', va='baseline')

        # Show x-axis labels only for the last two rows
        if i < 41:
            for label in ax.get_xticklabels():
                label.set_visible(False)

    # Hide extra subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Set main title
    fig.suptitle(f'County-level {title} Paths', fontsize=20)
    fig.text(0.5, 0.04, 'Year', ha='center', va='center', fontsize=15)
    fig.text(0.04, 0.5, 'Mortality', ha='center', va='center', rotation='vertical', fontsize=15)

    plt.subplots_adjust(left=0.07, right=0.93, top=0.93, bottom=0.07, wspace=0.2, hspace=0.2)

    fig.savefig(f'{save_dir}{filename}.png')
    plt.close(fig)
