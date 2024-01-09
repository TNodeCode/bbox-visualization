import streamlit as st

import pandas as pd
import numpy as np
from PIL import Image, ImageDraw


# Base path where to look for the images
basepath = ""

csv_filename = "df.csv"

# Load the DataFrame
df = pd.read_csv(csv_filename)

class Pagination:
    def __init__(self, df) -> None:
        self.df = df
        if not 'selected_index' in st.session_state.keys():
            st.session_state['selected_index'] = 0
        self.selected_index = st.session_state['selected_index']
        self.num_filenames = len(df['filename'].unique())
        self.previous_index = (self.selected_index - 1) % self.num_filenames
        self.next_index = (self.selected_index + 1) % self.num_filenames

    def forward(self):
        self.selected_index = self.next_index
        st.session_state['selected_index'] = self.selected_index
        self.previous_index = (self.selected_index - 1) % self.num_filenames
        self.next_index = (self.selected_index + 1) % self.num_filenames

    def backward(self):
        self.selected_index = self.previous_index
        st.session_state['selected_index'] = self.selected_index
        self.previous_index = (self.selected_index - 1) % self.num_filenames
        self.next_index = (self.selected_index + 1) % self.num_filenames

    def update_selected_index(self, filename):
        self.selected_index = int(np.where(df['filename'].unique() == filename)[0][0])
        st.session_state['selected_index'] = self.selected_index
        self.previous_index = (self.selected_index - 1) % self.num_filenames
        self.next_index = (self.selected_index + 1) % self.num_filenames



pagination = Pagination(df=df)

# Create a selectbox for filename selection
selected_filename = st.selectbox(
    'Select a filename',
    df['filename'].unique(),
    index=pagination.selected_index,
)

pagination.update_selected_index(selected_filename)

# Create buttons for selecting previous and next images
col1, col2 = st.columns(2)
col1.button('Previous', key='previous', on_click=pagination.backward)
col2.button('Next', key='next', on_click=pagination.forward)

# Filter the DataFrame based on the selected filename
filtered_df = df[df['filename'] == selected_filename]

# Load the image corresponding to the selected filename
image = Image.open(f"{selected_filename}")
image = image.convert(mode='RGB')

# Create a new image with bounding boxes drawn
draw = ImageDraw.Draw(image)

# Define color mappings for different classes
color_mappings = {
    'class1': '#00ff00',
    'class2': 'blue',
    'class3': 'green',
    # Add more class-color mappings as needed
}

# Draw bounding boxes and labels on the image
for _, row in filtered_df.iterrows():
    class_name = row['class']
    xmin = row['xmin']
    ymin = row['ymin']
    xmax = row['xmax']
    ymax = row['ymax']
    color = color_mappings.get(class_name, 'yellow')  # Default to yellow if class color not defined
    draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=color, width=2)
    #draw.text((xmin, ymin-15), class_name, fill=color)

# Display the image with bounding boxes
st.image(image)