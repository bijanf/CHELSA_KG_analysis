import argparse
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import koppen_mappings
from matplotlib.colors import ListedColormap
from utilities import world_to_pixel  # Ensure this function is defined in your utilities module
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Setup command line arguments
parser = argparse.ArgumentParser(description='Process climate data.')
parser.add_argument('--scenario', type=str, help='Climate scenario', default=None)
parser.add_argument('--time_slice', type=str, help='Time slice', default=None)
parser.add_argument('--target_cat', type=int, help='Target category', default=30)
parser.add_argument('--bbox', type=float, nargs=4, help='Bounding box (min_lon, min_lat, max_lon, max_lat)', default=[63, 25, 105, 56])
args = parser.parse_args()

# If arguments are not provided, use these default lists
scenarios = ['ssp126', 'ssp370', 'ssp585'] if args.scenario is None else [args.scenario]
time_slices = ['2011-2040', '2041-2070', '2071-2100'] if args.time_slice is None else [args.time_slice]

# Loop over scenarios and time slices
for scenario in scenarios:
    for time_slice in time_slices:
        print(f"Processing {scenario} for {time_slice}...")

        historical_dataset_path = '/p/projects/gvca/data/chelsa_cmip6/envicloud/chelsa/chelsa_V2/GLOBAL/climatologies/1981-2010/bio/CHELSA_kg2_1981-2010_V.2.1.tif'  # Update this path
        historical_dataset = gdal.Open(historical_dataset_path)
        geo_transform = historical_dataset.GetGeoTransform()
        minx, maxy = world_to_pixel(geo_transform, args.bbox[0], args.bbox[1])
        maxx, miny = world_to_pixel(geo_transform, args.bbox[2], args.bbox[3])
        historical_array = historical_dataset.ReadAsArray(minx, miny, maxx - minx, maxy - miny)
        historical_ET_mask = (historical_array == args.target_cat)

        agreement_array = np.zeros(historical_array.shape)
        model_agreements = [np.sum(historical_ET_mask)]  # Store the agreement counts here
        model_names = ['historical','GFDL-ESM4', 'IPSL-CM6A-LR', 'MPI-ESM1-2-HR', 'MRI-ESM2-0', 'UKESM1-0-LL']
        
        # List of model paths for the time-slice
        dir_models = f'/p/projects/gvca/data/chelsa_cmip6/envicloud/chelsa/chelsa_V2/GLOBAL/climatologies/{time_slice}/'
        model_paths = [
            f'{dir_models}GFDL-ESM4/{scenario}/bio/CHELSA_kg2_{time_slice}_gfdl-esm4_{scenario}_V.2.1.tif',
            f'{dir_models}IPSL-CM6A-LR/{scenario}/bio/CHELSA_kg2_{time_slice}_ipsl-cm6a-lr_{scenario}_V.2.1.tif',
            f'{dir_models}MPI-ESM1-2-HR/{scenario}/bio/CHELSA_kg2_{time_slice}_mpi-esm1-2-hr_{scenario}_V.2.1.tif',
            f'{dir_models}MRI-ESM2-0/{scenario}/bio/CHELSA_kg2_{time_slice}_mri-esm2-0_{scenario}_V.2.1.tif',
            f'{dir_models}UKESM1-0-LL/{scenario}/bio/CHELSA_kg2_{time_slice}_ukesm1-0-ll_{scenario}_V.2.1.tif'
        ]
        # Process each model
        for model_path in model_paths:
            dataset = gdal.Open(model_path)
            model_array = dataset.ReadAsArray(minx, miny, maxx - minx, maxy - miny)
            is_cat = model_array == args.target_cat

            # Update the agreement counter
            agreement_array += is_cat
            model_agreements.append(np.sum(is_cat))

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
        extent = [args.bbox[0], args.bbox[2], args.bbox[1], args.bbox[3]]
        cmap = ListedColormap(['#FFFFFF00', '#5555FF', '#AAAAFF', '#FFAAAA', '#FF5555', '#FF0000'])

        # Plot historical "ET" category
        ax.imshow(historical_ET_mask.astype(int), cmap=ListedColormap(['#FFFFFF', '#98FB98']), interpolation='nearest', extent=extent, aspect='equal')
        cax = ax.imshow(agreement_array, cmap=cmap, interpolation='nearest', extent=extent, vmin=0, vmax=len(model_paths), aspect='equal')

        # Add map features
        ax.coastlines(linewidth=.5)
        ax.add_feature(cfeature.BORDERS, linewidth=.5)

        plt.xlabel('Longitude Index')
        plt.ylabel('Latitude Index')

        # Colorbar
        cbar_ax = fig.add_axes([0.93, 0.3, 0.03, 0.39])
        cbar = fig.colorbar(cax, cax=cbar_ax)
        cbar.set_label(f'Number of Models Agreeing on the {koppen_mappings.koppen_mapping_short[args.target_cat]}')

        # Gridlines
        gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.1, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False

        # Inset for the bar chart
        axins = inset_axes(ax, width="30%", height="20%", loc='upper left', bbox_to_anchor=(0.15, 0.12, 1, .8), bbox_transform=ax.transAxes)
        # Define colors for each bar: one for historical and one for each model 
        colors = ['#98FB98']  # Color for the historical bar
        model_colors = ['skyblue'] * len(model_paths)  # Same color for all model bars
        all_colors = colors + model_colors  # Combine the colors
        axins.barh(model_names, model_agreements, color=all_colors)
        axins.set_xlabel('Grid Points')
#        axins.set_title('Köppen Category Agreement')

        plt.savefig(f'figure_{args.target_cat}_{time_slice}_{scenario}.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

