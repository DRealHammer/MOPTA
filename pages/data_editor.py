import streamlit as st
import pandas as pd
from io import BytesIO

def create_csv(df):
    return df.to_csv().encode('utf-8')

def create_xlsx():

    buffer = BytesIO()

    with pd.ExcelWriter(buffer) as writer:
        st.session_state.data['init_crew_df'].to_excel(writer, sheet_name='Initial Crew', index=False)
        st.session_state.data['init_qual_df'].to_excel(writer, sheet_name='Initial Crew Type Qualification', index=False)
        st.session_state.data['crew_leaving_df'].to_excel(writer, sheet_name='Crew Leaving', index=False)
        st.session_state.data['demand_df'].to_excel(writer, sheet_name='Crew Demand', index=False)
        st.session_state.data['sim_df'].to_excel(writer, sheet_name='Simulator Availability', index=False)
        st.session_state.data['training_structures_df'].to_excel(writer, sheet_name='Training', index=False)
        st.session_state.data['EOY_requirement_df'].to_excel(writer, sheet_name='Airbus Crew EOY Requirement', index=False)
        st.session_state.data['grounded_cost_df'].to_excel(writer, sheet_name='Grounded Aircraft Cost', index=False)

    buffer.seek(0)
    return buffer

st.write("General Settings")
up_col1, up_col2 = st.columns([1, 1])


with up_col1:
    allow_hiring = st.toggle('Allow Hiring (will increase compute time significantly)', value=st.session_state.allow_hiring)
    
    st.session_state.allow_hiring = allow_hiring

    if st.session_state.allow_hiring:
        st.session_state.hiring_limit = st.number_input('Hiring Limit per Week', min_value=0, max_value=20, step=1, value=st.session_state.hiring_limit)

        st.session_state.hiring_cost = st.number_input('Hiring Cost per Hired Position', min_value=0, value=st.session_state.hiring_cost)
    else:
        st.session_state.hiring_limit = 0
        st.session_state.hiring_cost = 0

with up_col2:
    curr = st.radio('Currency', ['US Dollar ($)', 'Euro (€)'])

    if '$' in curr:
        st.session_state.currency = '$'
    elif '€' in curr:
        st.session_state.currency = '€'




col1, col2 = st.columns([4, 1])
with col1:
    st.title("Data Editor")

with col2:
    pass


#st.file_uploader('upload', label_visibility='collapsed')

st.write('### Data Selection')
selection_options = [
    'Initial Crew',
    'Initial Crew Type Qualification',
    'Crew Leaving',
    'Crew Demand',
    'Simulator Availability',
    'Training',
    'Airbus Crew EOY Requirement',
    'Grounded Aircraft Cost'
]
current_selection = st.selectbox("data selection", options=selection_options, label_visibility='collapsed')

but1, but2, but3 = st.columns([1, 1, 3])

current_df = None

if current_selection == 'Initial Crew':
    current_df = st.session_state.data['init_crew_df']

elif current_selection == 'Initial Crew Type Qualification':
    current_df = st.session_state.data['init_qual_df']

elif current_selection == 'Crew Leaving':
    current_df = st.session_state.data['crew_leaving_df']

elif current_selection == 'Crew Demand':
    current_df = st.session_state.data['demand_df']

elif current_selection == 'Simulator Availability':
    current_df = st.session_state.data['sim_df']

elif current_selection == 'Training':
    current_df = st.session_state.data['training_structures_df']

elif current_selection == 'Airbus Crew EOY Requirement':
    current_df = st.session_state.data['EOY_requirement_df']

elif current_selection == 'Grounded Aircraft Cost':
    current_df = st.session_state.data['grounded_cost_df']


edited_df = st.data_editor(current_df, num_rows='dynamic')


if current_selection == 'Initial Crew':
    st.session_state.data['init_crew_df'] = edited_df

elif current_selection == 'Initial Crew Type Qualification':
    st.session_state.data['init_qual_df'] = edited_df

elif current_selection == 'Crew Leaving':
    st.session_state.data['crew_leaving_df'] = edited_df

elif current_selection == 'Crew Demand':
    st.session_state.data['demand_df'] = edited_df

elif current_selection == 'Simulator Availability':
    st.session_state.data['sim_df'] = edited_df

elif current_selection == 'Training':
    st.session_state.data['training_structures_df'] = edited_df

elif current_selection == 'Airbus Crew EOY Requirement':
    st.session_state.data['EOY_requirement_df'] = edited_df

elif current_selection == 'Grounded Aircraft Cost':
    st.session_state.data['grounded_cost_df'] = edited_df


with but1:
    st.download_button('Download All (as .xlsx)', file_name='Flight Data.xlsx', data=create_xlsx(), icon=":material/download:", type='primary')

with but2:
    st.download_button(f'{current_selection}', file_name=f'{current_selection}.csv', data=create_csv(edited_df), icon=":material/download:", type='primary')
