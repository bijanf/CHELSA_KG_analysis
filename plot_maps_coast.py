import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patches as mpatches


koppen_colors = {
    1: '#960000',
    2: '#ff0000',
    3: '#ffcccc',
    4: '#ffcc00',
    5: '#ffff64',
    6: '#cc8d14',
    7: '#ccaa54',
    8: '#00ff00',
    9: '#96ff00',
    10: '#c8ff00',
    11: '#b46400',
    12: '#966400',
    13: '#5a3c00',
    14: '#003200',
    15: '#005000',
    16: '#007800',
    17: '#ff6eff',
    18: '#ffb4ff',
    19: '#e6c8ff',
    20: '#c8c8c8',
    21: '#c8b4ff',
    22: '#9a7fb3',
    23: '#8759b3',
    24: '#6f24b3',
    25: '#320032',
    26: '#640064',
    27: '#c800c8',
    28: '#c81485',
    29: '#64ffff',
    30: '#6496ff',
    31: '#6000ff',
}

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

koppen_mapping_short = {
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
    30: "ET ",
    31: "EF "
}



# Define the bounding box (min_lon, min_lat, max_lon, max_lat)
#bbox = [36, 20, 93, 63]
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



file_1981_2010 = '/p/projects/gvca/data/chelsa_cmip6/envicloud/chelsa/chelsa_V2/GLOBAL/climatologies/1981-2010/bio/CHELSA_kg2_1981-2010_V.2.1.tif'
name='historical.png'
scenario=''
#file_1981_2010='/p/projects/gvca/data/chelsa_cmip6/envicloud/chelsa/chelsa_V2/GLOBAL/climatologies/2071-2100/GFDL-ESM4/ssp585/bio/CHELSA_kg2_2071-2100_gfdl-esm4_ssp585_V.2.1.tif'
#name='future_CHELSA_kg2_2071-2100_gfdl-esm4_ssp585_V.2.1.png'
#scenario = 'ssp585'
# Open the TIFF files
dataset_1981_2010 = gdal.Open(file_1981_2010)
# Get GeoTransform and calculate pixel coordinates
geo_transform = dataset_1981_2010.GetGeoTransform()
minx, maxy = world_to_pixel(geo_transform, bbox[0], bbox[1])
maxx, miny = world_to_pixel(geo_transform, bbox[2], bbox[3])
# Read the raster data as numpy arrays for the specified region
array_2d = dataset_1981_2010.ReadAsArray(minx, miny, maxx - minx, maxy - miny)

unique_values = np.unique(array_2d)
unique_values_sorted = np.sort(unique_values)

print("Unique values in array:", unique_values)
# Check if all unique values have a corresponding entry in koppen_mapping
missing_keys = [value for value in unique_values if value not in koppen_mapping_short]
print("Missing keys in koppen_mapping:", missing_keys)



# Create a ListedColormap from the dictionary
from matplotlib.colors import ListedColormap
cmap = ListedColormap([koppen_colors[key] for key in sorted(koppen_colors.keys()) if key in unique_values])




# List of categories you want to plot
categories_to_plot = [  5,  6,  7,  8,  9, 10, 12, 15, 16, 18, 19, 20, 22, 23, 24, 26, 27,
       28,30]

# Create a mask for these categories
mask = np.isin(array_2d, categories_to_plot)

# Create a masked array where only the values of interest are not masked
masked_array = np.ma.masked_where(~mask, array_2d)

# Now create a color map that includes only the colors for these categories
selected_colors = [koppen_colors.get(category, 'ignore') for category in categories_to_plot]
selected_cmap = ListedColormap(selected_colors)








fig, ax = plt.subplots(figsize=(10, 10),
                       subplot_kw={'projection': ccrs.PlateCarree()})

# Existing code to plot your data...
extent = [44, 90, 33, 56]  # [min_longitude, max_longitude, min_latitude, max_latitude]
#print(cmap.colors)
plt.imshow(masked_array, cmap=selected_cmap, interpolation='nearest', extent=extent)
categories_to_plot = [31]
# Create a mask for these categories
mask = np.isin(array_2d, categories_to_plot)

# Create a masked array where only the values of interest are not masked
masked_array = np.ma.masked_where(~mask, array_2d)

# Now create a color map that includes only the colors for these categories
selected_colors = [koppen_colors.get(category, 'ignore') for category in categories_to_plot]
selected_cmap = ListedColormap(selected_colors)
plt.imshow(masked_array, cmap=selected_cmap, interpolation='nearest', extent=extent)

# Add coastlines and country boundaries
ax.coastlines()
ax.add_feature(cfeature.BORDERS)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Overlay country boundaries and lakes
countries = cfeature.NaturalEarthFeature(category='cultural', scale='50m', facecolor='none', name='admin_0_countries')
lakes = cfeature.NaturalEarthFeature(category='physical', scale='50m', facecolor='none', name='lakes')

legend_labels = {value: key for key, value in koppen_mapping_short.items()}
# Create patches for the legend

patches = [mpatches.Patch(color=koppen_colors[key], label=koppen_mapping_short[key]) for key in unique_values if key in koppen_colors]

# Adjust the legend's location
leg = plt.legend(handles=patches, bbox_to_anchor=(1.0, 1.05) , loc='upper left')
# Add gridlines and labels
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = False
gl.right_labels = False

plt.title(scenario)

plt.savefig(name, format='png', dpi=300, bbox_inches='tight')
# Count the occurrences of each unique value
counts = {koppen_mapping_short[val]: np.count_nonzero(array_2d == val) for val in unique_values if val in koppen_mapping_short}

