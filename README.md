# SAIL-Net POPS Data Analysis

### Introduction to SAIL-Net

SAIL-Net was a DOE funded project in the East River Watershed near Crested Butte, Colorado with the goal of advancing our understanding of aerosol-cloud interactions in complex, mountainous regions. 
Through the deployment of a network of six low-cost microphysics nodes in Fall 2021 in the same domain at the SAIL campaign, SAIL-Net provides data on aerosol size distributions, cloud condensation nuclei (CCN), and ice nucleating particles (INP). 
This network enabled he investigation of small-scale variations in complex terrain, thus enhancing our understanding of aerosol's role in precipitation formation and water resource dynamics.

### Introduction to the dataset and code

To view the analysis and figures associated with the SAIL-Net paper "SAIL-Net: An investigation of the spatiotemporalvariability of aerosol in the mountainous terrain of the Upper Colorado River Basin" (Gibson, et al., 2024), run the code in acp_figures_and_analysis.py. 
First, the POPS data, which are available on the [ARM Data Discovery](https://doi.org/10.5439/2203692) as netCDF files must be downloaded and added to a directory called ''data''.
This code will produce all figures and analysis of the paper, except for the figures and analysis associated with the comparison to TBS data. To see these figures, download the [TBS data](https://doi.org/10.5439/1827703) in Gunnison from the ARM Data Discovery, put it in a directory called ''TBS_data'' and run the TBSAnalysis.py file.


