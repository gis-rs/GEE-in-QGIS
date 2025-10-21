# import libraries
import ee
import geemap
from ee_plugin import Map

# Initialize the Earth Engine API
ee.Initialize()
     
# Load the GAUL dataset (level2 for administrative boundaries)
gaul = ee.FeatureCollection("FAO/GAUL/2015/level2")

# Filter and Print city names of Australia
australia = gaul.filter(ee.Filter.eq('ADM0_NAME', 'Australia'))
names = australia.aggregate_array('ADM1_NAME').getInfo()
print(sorted(set(names)))
     

# Filter for Canberra
canberra = gaul.filter(ee.Filter.eq('ADM1_NAME', 'New South Wales'))

# Add Vienna boundary to the map
Map.addLayer(canberra, {'color': 'red'}, 'Canberra Boundary')
Map.centerObject(canberra,10)
