import ee
from ee_plugin import Map

ee.Initialize()

# Load LSIB dataset
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")

# List of European countries
european_countries = [
    'Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus',
    'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus',
    'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia',
    'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan',
    'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta',
    'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia',
    'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino',
    'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
    'Turkey', 'Ukraine', 'United Kingdom', 'Vatican City'
]

# Filter countries in Europe
europe = countries.filter(ee.Filter.inList('country_na', european_countries))

# Add to map
Map.addLayer(europe, {}, 'Europe Countries')

# Center map
Map.setCenter(10, 50, 3)  # longitude, latitude, zoom

