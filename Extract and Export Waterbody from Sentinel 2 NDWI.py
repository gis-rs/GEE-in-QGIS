#import libraries
import ee
import geemap
from ee_plugin import Map

# Load roi layer (shapefile or Geopackage)
roi_layer = r"C:\Users\user\Documents\aoi.gpkg"
roi = geemap.vector_to_ee(roi_layer)

# Create median composite
s2_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(roi)
    .filterDate('2024-01-01', '2024-07-31')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
)

median_composite = s2_collection.median().clip(roi)

# True Color (Natural Color)
vis_params_truecolor = {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 3000,
    'gamma': 1.2
}


# Add layers to map
Map.addLayer(median_composite, vis_params_truecolor, 'True Color')
Map.centerObject(median_composite)

# Calculate NDWI (Normalized Difference Water Index)
# NDWI = (Green - NIR) / (Green + NIR)
# For Sentinel-2: Green = B3, NIR = B8
ndwi = median_composite.normalizedDifference(['B3', 'B8']).rename('NDWI')
# NDWI visualization parameters
ndwi_vis = {
    'min': -1,
    'max': 1,
    'palette': ['red', 'yellow', 'green', 'blue']
}

# Add NDWI to map
Map.addLayer(ndwi, ndwi_vis, 'NDWI')

# Define NDWI threshold for water (typically 0.0 to 0.3)
ndwi_threshold = -0.1

# Create water mask
water_mask = ndwi.gt(ndwi_threshold)  # pixels where NDWI > threshold

# Optional: Apply additional filtering to remove small noise
water_mask = water_mask.selfMask()  # Only keep water pixels

# Add water mask to map
Map.addLayer(water_mask, {'palette': ['blue']}, 'Water Mask')

# Convert raster to vector (polygons)
water_polygons = water_mask.reduceToVectors(
    geometry=roi,
    scale=10,  # Sentinel-2 resolution
    geometryType='polygon',
    maxPixels=1e9,
    bestEffort=True
)

print(f"Number of water polygons: {water_polygons.size().getInfo()}")

# Add water polygons to map
Map.addLayer(water_polygons, {'color': 'blue', 'fillColor': '00000000'}, 'Water Polygons')

out_dir = os.path.join(os.path.expanduser("~"), "Downloads")
shapefile_path = os.path.join(out_dir, "water.shp")

# Export using geemap
geemap.ee_to_shp(
    water_polygons,
    filename=shapefile_path,
)

print(f"Water bodies exported to: {shapefile_path}")

# Load exported shapefile to Map
iface.addVectorLayer(shapefile_path, "Water", "ogr")