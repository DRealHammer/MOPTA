import streamlit as st
import time
from datetime import datetime
import pandas as pd



st.set_page_config(layout="wide")

# Initialize session state
if "optimization_runs" not in st.session_state:
    st.session_state.optimization_runs = {}
if "current_run" not in st.session_state:
    st.session_state.current_run = None


if "modelOutput" not in st.session_state:
    st.session_state.modelOutput = []

if "allow_hiring" not in st.session_state:
    st.session_state.allow_hiring = False

if "hiring_limit" not in st.session_state:
    st.session_state.hiring_limit = 0

if "hiring_cost" not in st.session_state:
    st.session_state.hiring_cost = 0

if "currency" not in st.session_state:
    st.session_state.currency = '$'

def read_csv(dir):

    init_crew_df = pd.read_csv(f'{dir}/Initial Crew.csv')
    init_qual_df = pd.read_csv(f'{dir}/Initial Crew Type Qualification.csv')
    crew_leaving_df = pd.read_csv(f'{dir}/Crew Leaving.csv').fillna(0)
    demand_df = pd.read_csv(f'{dir}/Crew Demand.csv')[['Week', 'Aircraft', 'Demand']]
    sim_df = pd.read_csv(f'{dir}/Simulator Availability.csv')
    training_structures_df = pd.read_csv(f'{dir}/Training.csv').fillna(0)
    EOY_requirement_df = pd.read_csv(f'{dir}/Airbus Crew EOY Requirement.csv')
    grounded_cost_df = pd.read_csv(f'{dir}/Grounded Aircraft Cost.csv')

    return {'init_crew_df': init_crew_df,
            'init_qual_df': init_qual_df,
            'crew_leaving_df': crew_leaving_df,
            'demand_df': demand_df,
            'sim_df': sim_df,
            'training_structures_df': training_structures_df,
            'EOY_requirement_df': EOY_requirement_df,
            'grounded_cost_df': grounded_cost_df}

if 'data' not in st.session_state:
    st.session_state.data = read_csv('data')

# Seitenverwaltung
def main():

    with st.sidebar:
        st.write('Hello there! Welcome to this Optimization Suite for the Transavia [MOPTA Challenge 2025](https://coral.ise.lehigh.edu/mopta2025/competition/)')
        st.write('Just so you know: You can collapse this sidebar, so you have more space on the main page')
        st.write('To run the optimization, just click on the green button.')
        st.write('If you want to change something, maybe you\'ll find what you are looking for in the Data Editor')
        st.write('If you want to run this locally or have a look at the code in more detail take a look at [GitHub](https://github.com/DRealHammer/MOPTA)')
        st.write("Created by Daniel Hammer")

    p_dashboard = st.Page("pages/dashboard.py", title="Dashboard")
    p_edit = st.Page("pages/data_editor.py", title='Data Editor')
    pg = st.navigation([p_dashboard, p_edit])
    pg.run()
    


main()
