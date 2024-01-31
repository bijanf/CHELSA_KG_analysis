import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from osgeo import gdal
# Load the datasets

koppen_mapping = {
    1: "Af - Equatorial fully humid",
    2: "Am - Equatorial monsoonal",
    3: "As - Equatorial summer dry",
    4: "Aw - Equatorial winter dry",
    5: "BWk - Cold desert",
    6: "BWh - Hot desert",
    7: "BSk - Cold steppe",
    8: "BSh - Hot steppe",
    9: "Cfa - Warm temperate fully humid hot summer",
    10: "Cfb - Warm temperate fully humid warm summer",
    11: "Cfc - Warm temperate fully humid cool summer",
    12: "Csa - Warm temperate summer dry hot summer",
    13: "Csb - Warm temperate summer dry warm summer",
    14: "Csc - Warm temperate summer dry cool summer",
    15: "Cwa - Warm temperate winter dry hot summer",
    16: "Cwb - Warm temperate winter dry warm summer",
    17: "Cwc - Warm temperate winter dry cool summer",
    18: "Dfa - Snow fully humid hot summer",
    19: "Dfb - Snow fully humid warm summer",
    20: "Dfc - Snow fully humid cool summer",
    21: "Dfd - Snow fully humid extremely continental",
    22: "Dsa - Snow summer dry hot summer",
    23: "Dsb - Snow summer dry warm summer",
    24: "Dsc - Snow summer dry cool summer",
    25: "Dsd - Snow summer dry extremely continental",
    26: "Dwa - Snow winter dry hot summer",
    27: "Dwb - Snow winter dry warm summer",
    28: "Dwc - Snow winter dry cool summer",
    29: "Dwd - Snow winter dry extremely continental",
    30: "ET - Polar tundra",
    31: "EF - Polar frost"
}

koppen_mapping = {
    1: "Af ",
    2: "Am ",
    3: "As ",
    4: "Aw ",
    5: "BWk",
    6: "BWh",
    7: "BSk",
    8: "BSh",
    9: "Cfa",
    10: "Cfb",
    11: "Cfc",
    12: "Csa",
    13: "Csb",
    14: "Csc",
    15: "Cwa",
    16: "Cwb",
    17: "Cwc",
    18: "Dfa",
    19: "Dfb",
    20: "Dfc",
    21: "Dfd",
    22: "Dsa",
    23: "Dsb",
    24: "Dsc",
    25: "Dsd",
    26: "Dwa",
    27: "Dwb",
    28: "Dwc",
    29: "Dwd",
    30: "EF ",
    31: "ET "
}

# Define the bounding box (min_lon, min_lat, max_lon, max_lat)
bbox = [44, 33, 90, 56]

# Function to transform latitude/longitude to pixel coordinates
def world_to_pixel(geo_matrix, x, y):
    ulX = geo_matrix[0]
    ulY = geo_matrix[3]
    xDist = geo_matrix[1]
    yDist = geo_matrix[5]
    rtnX = geo_matrix[2]
    rtnY = geo_matrix[4]
    pixel = int((x - ulX) / xDist)
    line = int((ulY - y) / xDist)
    return (pixel, line)


# Function to count categories
def count_categories(data_array):
    unique, counts = np.unique(data_array, return_counts=True)
    return dict(zip(unique, counts))


file_1981_2010 = '/p/projects/gvca/data/chelsa_cmip6/envicloud/chelsa/chelsa_V2/GLOBAL/climatologies/1981-2010/bio/CHELSA_kg2_1981-2010_V.2.1.tif'
#dir_models = '/p/projects/gvca/data/chelsa_cmip6/envicloud/chelsa/chelsa_V2/GLOBAL/climatologies/2071-2100/'

#scenario='ssp585'
#scenario='ssp370'
scenario='ssp126'
#time_slice='2071-2100'
#time_slice='2011-2040'
#time_slice='2041-2070'
time = ['2011-2040', '2041-2070', '2071-2100']
k = 0
plt.figure(figsize=(20, 10))
for k in range(0, 3):
    time_slice = time[k]

    dir_models = '/p/projects/gvca/data/chelsa_cmip6/envicloud/chelsa/chelsa_V2/GLOBAL/climatologies/'+time_slice+'/'
    models = [dir_models+'GFDL-ESM4/'+scenario+'/bio/CHELSA_kg2_'+time_slice+'_gfdl-esm4_'+scenario+'_V.2.1.tif',
    dir_models+'IPSL-CM6A-LR/'+scenario+'/bio/CHELSA_kg2_'+time_slice+'_ipsl-cm6a-lr_'+scenario+'_V.2.1.tif',
    dir_models+'MPI-ESM1-2-HR/'+scenario+'/bio/CHELSA_kg2_'+time_slice+'_mpi-esm1-2-hr_'+scenario+'_V.2.1.tif',
    dir_models+'MRI-ESM2-0/'+scenario+'/bio/CHELSA_kg2_'+time_slice+'_mri-esm2-0_'+scenario+'_V.2.1.tif',
    dir_models+'UKESM1-0-LL/'+scenario+'/bio/CHELSA_kg2_'+time_slice+'_ukesm1-0-ll_'+scenario+'_V.2.1.tif']



    # Open the TIFF files
    dataset_1981_2010 = gdal.Open(file_1981_2010)
    # Get GeoTransform and calculate pixel coordinates
    geo_transform = dataset_1981_2010.GetGeoTransform()
    minx, maxy = world_to_pixel(geo_transform, bbox[0], bbox[1])
    maxx, miny = world_to_pixel(geo_transform, bbox[2], bbox[3])
    # Read the raster data as numpy arrays for the specified region
    array_1981_2010 = dataset_1981_2010.ReadAsArray(minx, miny, maxx - minx, maxy - miny)
    counts_1981_2010 = count_categories(array_1981_2010)  # Replace with actual counts




    def process_model_file(file_path):
        # Open the TIFF file
        dataset = gdal.Open(file_path)
        # Get GeoTransform from the dataset
        geo_transform = dataset.GetGeoTransform()
        # Convert the bounding box to pixel coordinates
        minx, maxy = world_to_pixel(geo_transform, bbox[0], bbox[1])
        maxx, miny = world_to_pixel(geo_transform, bbox[2], bbox[3])
        # Read the raster data within the bounding box
        array = dataset.ReadAsArray(minx, miny, maxx - minx, maxy - miny)
        # Count the categories in the array
        counts = count_categories(array)
        # Close the dataset
        dataset = None
        return counts



    # Initialize all_categories with categories from the reference dataset
    all_categories = list(range(1, 32))
    # Process each model file and update all_categories
    all_model_counts = []
    for model_file in models:
        model_counts = process_model_file(model_file)
        all_model_counts.append(model_counts)
        # Update all_categories to include categories from this model
#        all_categories.update(model_counts.keys())




    category_means = {}
    category_stds = {}
    for category in all_categories:
        category_values = [counts.get(category, 0) for counts in all_model_counts]
        category_means[category] = np.mean(category_values)
        category_stds[category] = np.std(category_values)


    # Plotting comparison with error bars
    def plot_comparison_with_errors(counts_ref, means, stds, categories, labels, title_ref, title_future):
        counts_ref_values = [counts_ref.get(category, 0) for category in categories]
        means_values = [means.get(category, 0) for category in categories]
        stds_values = [stds.get(category, 0) for category in categories]

        bar_width = 0.2
        index = np.arange(len(categories))

        if k == 0:
            plt.bar(index, counts_ref_values, bar_width, label=title_ref, color='b')
            plt.bar(index + bar_width, means_values, bar_width, yerr=stds_values, label=title_future, color='lightgray', capsize=5)
        if k == 1:
            plt.bar(index + (bar_width * 2), means_values, bar_width, yerr=stds_values, label=title_future, color='orange', capsize=5)
        if k == 2:
            plt.bar(index + (bar_width * 3), means_values, bar_width, yerr=stds_values, label=title_future, color='magenta', capsize=5)


        plt.xlabel('Category', fontsize = 15)
        plt.ylabel('Number of Grid Points', fontsize = 15)
        plt.title(scenario)
        plt.xticks(index + bar_width / 4, labels, rotation=90, fontsize=15)
        plt.legend(fontsize=14)
        plt.tight_layout()

    # Sort categories for consistent plotting
    sorted_categories = all_categories

    # Replace category codes with names for plotting
    category_labels = [koppen_mapping.get(category, f"Unknown ({category})") for category in sorted_categories]

    # Call the plotting function with error bars
    plot_comparison_with_errors(
        counts_1981_2010,
        category_means,
        category_stds,
        sorted_categories,
        category_labels,
        '1981-2010',
        time_slice+''
    )


# Save the figure
plt.savefig('climate_category_comparison_with_errors_'+scenario+'.png', format='png', dpi=300)
