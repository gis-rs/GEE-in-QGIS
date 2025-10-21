import ee
from ee_plugin import Map

ee.Initialize()

# Load LSIB dataset
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")

# List of European countries
european_countries = [
    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece',
    'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania',
    'Luxembourg', 'Malta', 'Netherlands', 'Norway', 'Poland', 'Portugal',
    'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
    'United Kingdom'
]

# Filter countries in Europe
europe = countries.filter(ee.Filter.inList('country_na', european_countries))

# Add to map
Map.addLayer(europe, {}, 'Europe Countries')

# Center map
Map.setCenter(10, 50, 3)  # longitude, latitude, zoom
