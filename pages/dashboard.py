import streamlit as st
import time
import pandas as pd
from moptamodel import MOPTAModel
from pyscipopt import SCIP_EVENTTYPE
import json

class Solution():
    def __init__(self, model, solution) -> None:
        
        self.optVal = model.getObjVal()
        self.training_schedule = []
        self.free_crews = []

def scipOutputhdlr(model, event):
    st.session_state.modelOutput.append(model.getStage())


def select_plan(solution):
    st.session_state.solution = solution

col1, col2, col3 = st.columns([4, 1, 1])

selection_box = None

with col1:
    st.title('Transavia Training Scheduling')

with col2:
    button = st.button('Run Optimization', type='primary')

with col3:
    selection_box = st.selectbox('Select a plan', options=st.session_state.optimization_runs)
    if selection_box is not None:
        select_plan(st.session_state.optimization_runs[selection_box])


if button:
    start_time = time.time()
    model = MOPTAModel(*st.session_state.data.values())
    model.model.attachEventHandlerCallback(scipOutputhdlr, [SCIP_EVENTTYPE.PRESOLVEROUND, SCIP_EVENTTYPE.BOUNDCHANGED])
        
    model.optimize()
    
    run_status = model.model.getStatus()

    if run_status == 'optimal':
        sol = model.model.getBestSol()
        st.session_state.optimization_runs[str(time.time())] = sol
        st.success(f'The plan was created successfully in {(time.time() - start_time):10.2f} seconds!')

        clean_solution = Solution(model.model, sol)
        select_plan(clean_solution)

    elif run_status == 'unbounded':
        st.warning('This configuration is unbounded and has no optimal solution')

    elif run_status == 'infeasible':
        st.warning('This configuration is infeasible and has no optimal solution')



l_col1, l_col2 = st.columns([1, 1])

with l_col1:
    st.dataframe(st.session_state.data['sim_df'])

with l_col2:
    st.line_chart(st.session_state.data['sim_df']['Available Simulators'].to_numpy())

    key_metric_cont = st.container()

    with key_metric_cont:
        st.write('### Key Metrics')

        u_col1, u_col2 = st.columns([1, 1])

        with u_col1:
            st.metric('Costs', st.session_state.solution.optVal)

        with u_col2:
            st.metric('EOY FO Status', '200/10')
            st.metric('EOY C Status', '200/10')

if len(st.session_state.modelOutput) != 0:
    st.write(st.session_state.modelOutput)

if st.session_state.boiboi is not None:
    st.write(st.session_state.boiboi)