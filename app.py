import streamlit as st

from apputil import *

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')


st.write(
'''
# Titanic Visualization 1

'''
)
st.write("We've all heard the saying 'Women and Children first' from the retelling of the titanic. However, did the class of an individual affect the survival rate of women and children?")
# Generate and display the figure
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)

st.write(
'''
# Titanic Visualization 2
'''
)
st.write("What is the average family size for each class?")
# Generate and display the figure
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)
