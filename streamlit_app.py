import streamlit as st

# Define the pages for the multi-page "Lab" application.
Lab1 = st.Page("Lab1.py", title="Lab 1", icon="📄")
Lab2 = st.Page("Lab2.py", title="Lab 2", icon="📝", default=True)

# Lab2 is the default landing page.
pg = st.navigation([Lab2, Lab1])
pg.run()