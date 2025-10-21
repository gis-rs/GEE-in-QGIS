import ee
from ee_plugin import Map

ee.Initialize()

# Load LSIB dataset
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")

# Select multiple countries
selected = countries.filter(
    ee.Filter.inList('country_na', ['Poland'])
)

# Add to map as vector
Map.addLayer(selected, {}, "Selected Countries")
