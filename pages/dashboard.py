import streamlit as st
import time

col1, col2, col3 = st.columns([4, 1, 1])

sel_box_empty = None

with col1:
    st.title('Transavia Training Scheduling')

with col2:
    button = st.button('Run Optimization', type='primary')

with col3:
    selection_box = st.selectbox('Select a plan', options=st.session_state.optimization_runs)


if button:
    start_time = time.time()
    st.session_state.model.optimize()
    
    st.session_state.optimization_runs[str(time.time())] = st.session_state.model.model.getBestSol()
    st.success(f'The plan was created successfully in {(time.time() - start_time):10.2f} seconds!')


l_col1, l_col2 = st.columns([1, 1])

with l_col1:
    st.dataframe(st.session_state.model.sim_df)

with l_col2:
    st.line_chart(st.session_state.model.sim_df['Available Simulators'].to_numpy(), )

    key_metric_cont = st.container()

    with key_metric_cont:
        st.write('### Key Metrics')

        u_col1, u_col2 = st.columns([1, 1])

        with u_col1:
            st.metric('Costs', 10)

        with u_col2:
            st.metric('EOY FO Status', '200/10')
            st.metric('EOY C Status', '200/10')

if len(st.session_state.modelOutput) != 0:
    st.write(st.session_state.modelOutput)

