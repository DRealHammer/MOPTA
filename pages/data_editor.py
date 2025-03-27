import streamlit as st


col1, col2 = st.columns([4, 1])
with col1:
    st.title("Data Upload & Editing")

with col2:
    if st.button("Export", type='primary'):
        st.toast("Not yet implemented")


st.file_uploader('upload', label_visibility='collapsed')

st.write('### Data Selection')
selection_options = [
    'Initial Crew',
    'Initial Crew Type Qualification',
    'Crew Leaving',
    'Crew Demand',
    'Simulator Availability',
    'Training',
    'Airbus Crew EOY Requirement'
]
current_selection = st.selectbox("data selection", options=selection_options, label_visibility='collapsed')


current_df = None

if current_selection == 'Initial Crew':
    current_df = st.session_state.model.init_crew_df


elif current_selection == 'Initial Crew Type Qualification':
    current_df = st.session_state.model.init_qual_df

elif current_selection == 'Crew Leaving':
    current_df = st.session_state.model.crew_leaving_df

elif current_selection == 'Crew Demand':
    current_df = st.session_state.model.demand_df

elif current_selection == 'Simulator Availability':
    current_df = st.session_state.model.sim_df

elif current_selection == 'Training':
    current_df = st.session_state.model.training_structures_df

elif current_selection == 'Airbus Crew EOY Requirement':
    current_df = st.session_state.model.EOY_requirement_df


edited_df = st.data_editor(current_df, num_rows='dynamic')



if current_selection == 'Initial Crew':
    st.session_state.model.init_crew_df = edited_df

elif current_selection == 'Initial Crew Type Qualification':
    st.session_state.model.init_qual_df = edited_df

elif current_selection == 'Crew Leaving':
    st.session_state.model.crew_leaving_df = edited_df

elif current_selection == 'Crew Demand':
    st.session_state.model.demand_df = edited_df

elif current_selection == 'Simulator Availability':
    st.session_state.model.sim_df = edited_df

elif current_selection == 'Training':
    st.session_state.model.training_structures_df = edited_df

elif current_selection == 'Airbus Crew EOY Requirement':
    st.session_state.model.EOY_requirement_df = edited_df