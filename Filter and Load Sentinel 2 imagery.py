import ee 
from ee_plugin import Map 

# Get the polygon layer named 'poly' from QGIS
poly_layer = QgsProject.instance().mapLayersByName('poly')[0]

# Get the extent of the polygon and transform to WGS84 (EPSG:4326)
extent = poly_layer.extent()
transform = QgsCoordinateTransform(poly_layer.crs(), QgsCoordinateReferenceSystem('EPSG:4326'), QgsProject.instance())
extent_4326 = transform.transform(extent)

# Create Earth Engine geometry from the bounding box
roi = ee.Geometry.Rectangle([
    extent_4326.xMinimum(), 
    extent_4326.yMinimum(),
    extent_4326.xMaximum(), 
    extent_4326.yMaximum()
])

# Print ROI bounds for debugging
print("ROI bounds:", [extent_4326.xMinimum(), extent_4326.yMinimum(), extent_4326.xMaximum(), extent_4326.yMaximum()])

# Load Sentinel-2 Surface Reflectance imagery
dataset = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterDate('2023-06-01', '2023-09-30') \
    .filterBounds(roi) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))

# Check number of available images
image_count = dataset.size().getInfo()
print("Number of images found:", image_count)

if image_count > 0:
    # Create MEDIAN composite from all images in the collection
    sentinel_image = dataset.median()  # Changed from mosaic() to median()
    
    # True color visualization (Red: B4, Green: B3, Blue: B2)
    trueColorVis = {
        'bands': ['B4', 'B3', 'B2'],
        'min': 0,
        'max': 3000
    }
    
    # Center map on ROI and add layers
    Map.centerObject(roi, 10)
    Map.addLayer(sentinel_image, trueColorVis, 'Sentinel-2 True Color (Median Composite)')
    
    # Create proper EE feature for ROI outline
    roi_feature = ee.Feature(roi, {})
    roi_feature_collection = ee.FeatureCollection([roi_feature])
    Map.addLayer(roi_feature_collection, {'color': 'FF0000'}, 'ROI Area', False)
    
    print("Sentinel-2 median composite layer added successfully!")
else:
    print("No cloud-free Sentinel-2 images found for this area and time period!")
    
    # Show ROI location for reference
    roi_feature = ee.Feature(roi, {})
    roi_feature_collection = ee.FeatureCollection([roi_feature])
    Map.centerObject(roi, 10)
    Map.addLayer(roi_feature_collection, {'color': 'FF0000'}, 'ROI Extent')
