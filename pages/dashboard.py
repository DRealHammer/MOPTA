import streamlit as st
import time
import numpy as np
from moptamodel import MOPTAModel
from pyscipopt import SCIP_EVENTTYPE
import json

class Solution():
    def __init__(self, mopta_model=None, solution=None) -> None:
        
        self.optVal = 23247806.085752122
        self.training_schedule = {"Training 1":[1,2,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"Training 2":[0,0,0,1,0,2,0,1,0,0,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,0,0,0,0,0,0],"Training 3":[0,0,2,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0],"Training 4":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"Training 5":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
        self.student_schedule = {"Training 1":[1,8,4,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"Training 2":[0,0,0,2,0,4,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,4,0,0,0,0,0,0],"Training 3":[0,0,8,0,4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,4,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0],"Training 4":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"Training 5":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
        self.hiring_schedule = {"A":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"B":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
        self.free_crews = {"A":{"First Officer":[62,59,59,59,59,61,58,57,58,59,63,64,71,76,75,76,76,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,78,77,78,77,78,79,77,77,78,79,80,84,88,88,88,88,86],"Captain":[69,69,67,65,65,61,63,63,63,64,60,59,62,62,61,73,71,79,79,79,79,73,73,72,72,72,78,79,79,78,78,78,77,80,81,80,78,77,76,73,75,73,73,74,73,77,78,78,78,84,84,94],"External":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]},"B":{"First Officer":[418,417,409,404,403,401,399,394,388,388,387,388,388,387,387,387,386,386,386,384,386,386,386,386,386,386,386,386,386,386,385,385,385,385,385,384,380,376,376,376,376,376,376,375,375,373,371,371,371,371,371,367],"Captain":[406,406,406,398,397,392,391,388,386,387,387,393,392,396,391,391,393,393,393,393,391,375,377,375,375,379,379,379,379,379,379,379,379,376,376,376,376,372,372,364,364,364,364,364,363,362,361,358,360,361,361,362],"External":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}}

        self.free_eoy_f = 86
        self.free_eoy_c = 94

        self.grounded = {"Airbus":[1,0,0,1,0,1,1,0,1,0,1,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,6,0,6,0,0,0,0,1,2,1,1,1,0,1,1,1,1,1,0],"Boeing":[0,0,0,0,1,0,0,1,0,1,0,1,1,1,1,0,0,0,1,1,1,0,1,1,1,1,20,38,1,1,1,37,1,46,1,51,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,30]}

        self.f_req = 86
        self.c_req = 94

        if mopta_model is None or solution is None:
            return

        if mopta_model.model.getStatus() == 'optimal':

            # store eoy requirement
            req = st.session_state.data['EOY_requirement_df']
            self.f_req = req[req['Rating'] == 'Airbus FO']['Required EOY'].item()
            self.c_req = req[req['Rating'] == 'Airbus C']['Required EOY'].item()

            # store optimal value
            self.optVal = mopta_model.model.getObjVal()

            # store the training schedule
            for training, vars_week in mopta_model.training_vars_weeks.items():

                vals_week = []
                for var in vars_week:
                    vals_week.append(int(solution[var]))
                
                self.training_schedule[f'Training {training}'] = vals_week

            # store the student schedule
            for training, vars_week in mopta_model.student_vars_week.items():

                vals_week = []
                for var in vars_week:
                    vals_week.append(int(solution[var]))
                
                self.student_schedule[f'Training {training}'] = vals_week

            # store the hiring
            for aircraft, vars_week in mopta_model.hiring_vars_week.items():

                vals_week = []
                for var in vars_week:
                    vals_week.append(int(solution[var]))
                
                self.hiring_schedule[aircraft] = vals_week
            
            # store the number of free crew members
            
            for aircraft, qual_vars_week in mopta_model.free_crew_vars_week.items():

                self.free_crews[aircraft] = {}
                for qual, vars_week in qual_vars_week.items():
                    vals = []
                    for var in vars_week:
                        vals.append(int(solution[var]))

                    name_map = {'F': 'First Officer', 'C': 'Captain', 'E': 'External'}
                    self.free_crews[aircraft][name_map[qual]] = vals

                self.free_eoy_f = self.free_crews['A'][name_map['F']][-1]
                self.free_eoy_c = self.free_crews['A'][name_map['C']][-1]

            # store grounded planes
                
            for aircraft, grounded_vars_week in mopta_model.grounded_vars_week.items():

                vals = []
                for var in grounded_vars_week:
                    vals.append(solution[var])

                name_map = {'A': 'Airbus', 'B': 'Boeing'}
                self.grounded[name_map[aircraft]] = vals

        
                
# create the main solution
if 'solution' not in st.session_state:
    st.session_state.solution = Solution()
    st.session_state.optimization_runs['Main Optimization'] = st.session_state.solution

def scipOutputhdlr(model, event):
    st.session_state.modelOutput.append(model.getStage())


def select_plan(solution):
    st.session_state.solution = solution

col1, col2, col3 = st.columns([4, 1, 1])

selection_box = None

with col1:
    st.title('Transavia Training Scheduling')

with col2:
    button = st.button('Run Optimization', type='primary', icon=':material/flight:')

with col3:
    selection_box = st.selectbox('Select a plan', options=st.session_state.optimization_runs)
    if selection_box is not None:
        select_plan(st.session_state.optimization_runs[selection_box])


if button:
    start_time = time.time()
    mopta_model = MOPTAModel(*st.session_state.data.values())
    mopta_model.model.attachEventHandlerCallback(scipOutputhdlr, [SCIP_EVENTTYPE.PRESOLVEROUND, SCIP_EVENTTYPE.BOUNDCHANGED])
    mopta_model.hiring_limit = st.session_state.hiring_limit

    mopta_model.optimize()
    
    run_status = mopta_model.model.getStatus()

    if run_status == 'optimal':
        sol = mopta_model.model.getBestSol()
        st.success(f'The plan was created successfully in {(time.time() - start_time):10.2f} seconds!')

        clean_solution = Solution(mopta_model, sol)
        select_plan(clean_solution)
        st.session_state.optimization_runs[str(time.time())] = clean_solution

    elif run_status == 'unbounded':
        st.warning('This configuration is unbounded and has no optimal solution')

    elif run_status == 'infeasible':
        st.warning('This configuration is infeasible and has no optimal solution')



l_col1, l_col2 = st.columns([1, 1])

with l_col1:

    key_metric_cont = st.container()

    with key_metric_cont:
        st.write('## Key Metrics')

        u_col1, u_col2 = st.columns([1, 1])

        with u_col1:
            st.metric('Estimated Grounded Costs', f'{st.session_state.solution.optVal:,.2f} {st.session_state.currency}')

        with u_col2:
            st.metric('EOY FO Status', f'{st.session_state.solution.free_eoy_f}/{st.session_state.solution.f_req}')
            st.metric('EOY C Status', f'{st.session_state.solution.free_eoy_c}/{st.session_state.solution.c_req}')


    st.write('### Training Overview')

    t1, t2 = st.tabs(['Graph', 'Table'])

    with t1:
        st.line_chart(st.session_state.solution.training_schedule, x_label='Weeks', y_label='Number of Trainings')
    with t2:
        st.dataframe(st.session_state.solution.training_schedule)
    

    st.write('### Students Overview')

    t1, t2 = st.tabs(['Graph', 'Table'])

    with t1:
        st.line_chart(st.session_state.solution.student_schedule, x_label='Weeks', y_label='Number of Students')
    with t2:
        st.dataframe(st.session_state.solution.student_schedule)
    

with l_col2:

    st.write('### Free Crews Boeing')
    st.line_chart(st.session_state.solution.free_crews['B'], x_label='Weeks', y_label='Number of Crews')

    st.write('### Free Crews Airbus')
    st.line_chart(st.session_state.solution.free_crews['A'], x_label='Weeks', y_label='Number of Crews')

    st.write('### Grounded Planes')
    st.bar_chart(st.session_state.solution.grounded)

    

#if len(st.session_state.modelOutput) != 0:
    #st.write(st.session_state.modelOutput)
