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


# Function to process each model and calculate changes
def process_model(model_path):
    future_dataset = gdal.Open(model_path)
    future_array = future_dataset.ReadAsArray(minx, miny, maxx - minx, maxy - miny)

    changes_dict_model = {}
    for i in range(historical_array.shape[0]):
        for j in range(historical_array.shape[1]):
            historical_class = historical_array[i, j]
            future_class = future_array[i, j]
            if historical_class != future_class:
                change_pair = (historical_class, future_class)
                if change_pair not in changes_dict_model:
                    changes_dict_model[change_pair] = 1
                else:
                    changes_dict_model[change_pair] += 1
    return changes_dict_model
