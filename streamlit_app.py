import streamlit as st
import pandas as pd
import numpy as np

# Set the title and favicon that appear in the browser's tab bar.
st.set_page_config(
    page_title='Water Quality Dashboard',
    page_icon=':ocean:',  # This is an emoji shortcode. Could be a URL too.
)

# ------------------------------------------------------------------------
# Load and preprocess data

@st.cache_data
def get_cleaned_data():
    """Load the cleaned water quality dataset."""
    # Load the cleaned dataset
    data = pd.read_csv('data/cleaned_water_quality_data.csv')
    
    # Ensure the Date column exists if you later add it to the dataset
    # Uncomment the following if you have a date column for temporal filtering
    # data['Date'] = pd.to_datetime(data['Date'])
    
    return data

wq_df = get_cleaned_data()

# ------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :ocean: Water Quality Dashboard

Monitor and analyze water quality parameters collected by the BlueShield USV. Explore real-time data, insights, and machine learning predictions.
'''

# Add some spacing
''

# Sidebar filters for interactivity
locations = wq_df['Water_Supply_Scheme'].dropna().unique()

selected_locations = st.sidebar.multiselect(
    'Select the water supply schemes to view:',
    locations,
    default=locations[:3]  # Preselect the first 3 locations
)

# Filter by location
filtered_wq_df = wq_df[wq_df['Water_Supply_Scheme'].isin(selected_locations)]

# Parameter selection
parameters = st.sidebar.multiselect(
    'Select parameters to visualize:',
    ['EC', 'pH', 'Turbidity', 'TDS', 'Fe', 'As', 'Na', 'K'],
    default=['EC', 'pH', 'Turbidity']
)

# ------------------------------------------------------------------------
# Visualization

# Display filtered data insights
st.header('Filtered Data Overview', divider='gray')
st.write("Below is the filtered dataset based on your selections:")
st.dataframe(filtered_wq_df)

# Download filtered data
st.download_button(
    label="Download Filtered Data",
    data=filtered_wq_df.to_csv(index=False),
    file_name='filtered_water_quality_data.csv',
    mime='text/csv'
)

# Plot the selected parameters
for parameter in parameters:
    st.subheader(f'{parameter} Over Samples')
    st.line_chart(filtered_wq_df, x='Sample_Code', y=parameter)

# Display metrics for each location
st.header('Summary Metrics by Location', divider='gray')

cols = st.columns(len(selected_locations))

for i, location in enumerate(selected_locations):
    col = cols[i % len(cols)]
    with col:
        location_data = filtered_wq_df[filtered_wq_df['Water_Supply_Scheme'] == location]
        avg_values = location_data[parameters].mean()
        
        for param in parameters:
            st.metric(
                label=f'{location} - Avg {param}',
                value=f'{avg_values[param]:.2f}'
            )
