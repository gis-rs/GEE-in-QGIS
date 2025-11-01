# Import libraries
import ee
from ee_plugin import Map

# Initialize the Earth Engine API
ee.Initialize()

# Load the GAUL dataset (level2 for administrative boundaries)
gaul = ee.FeatureCollection("FAO/GAUL/2015/level1")

# Filter for Germany
germany = gaul.filter(ee.Filter.eq('ADM0_NAME', 'Germany'))

# Get and print all state (ADM1) names in Germany
state_names = germany.aggregate_array('ADM1_NAME').getInfo()
print("All states in Germany:")
print(sorted(set(state_names)))

# 🔹 Select a specific state — change the name as you wish
selected_state_name = 'Bayern'   # Example: Bayern (Bavaria), Hessen, Berlin, etc.

# Filter for the selected state
selected_state = germany.filter(ee.Filter.eq('ADM1_NAME', selected_state_name))

# Add the selected state boundary to the map
Map.addLayer(selected_state, {'color': 'red'}, selected_state_name)
Map.centerObject(selected_state, 7)

# Optional: print info about the selected state
print(f"Loaded boundary for: {selected_state_name}")

