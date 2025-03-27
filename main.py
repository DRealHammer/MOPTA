import streamlit as st
from moptamodel import MOPTAModel
import time
from datetime import datetime
import pandas as pd
from pyscipopt import SCIP_EVENTTYPE



st.set_page_config(layout="wide")

# Initialize session state
if "optimization_runs" not in st.session_state:
    st.session_state.optimization_runs = {}
if "current_run" not in st.session_state:
    st.session_state.current_run = None


def scipOutputhdlr(model, event):
    st.session_state.modelOutput.append(model.getStage())


if "model" not in st.session_state:
        st.session_state.model = MOPTAModel(ddir='data')
        st.session_state.model.model.attachEventHandlerCallback(scipOutputhdlr, [SCIP_EVENTTYPE.PRESOLVEROUND, SCIP_EVENTTYPE.BOUNDCHANGED])
        st.session_state.modelOutput = []

# Seitenverwaltung
def main():

    pg = st.navigation([st.Page("pages/dashboard.py", title="Dashboard"), st.Page("pages/data_editor.py", title='Data Upload & Editing')])
    pg.run()
    


def dashboard_page():

    start_time = time.time()
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "duration": time.time() - start_time,
        "success": True,
        "schedule": pd.DataFrame({
            "Week": range(1, 13),
            **{f"Training {i+1}": [f"Crew {w*10+i}" for w in range(12)] for i in range(5)}
        }),
        "crew_data": pd.DataFrame({
            "Week": range(1, 13),
            "Available Crews": [50 - w*3 for w in range(12)]
        }),
        "metrics": {
            "Total Cost": 1_250_000,
            "EOY Status": {
                "FO": {"required": 140, "current": 118},
                "C": {"required": 30, "current": 22}
            }
        }
    }

    # Header section
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Transavia Training Schedule")
    
    with col2:
        run_options = ["Latest"] + [f"Run {i+1}" for i in range(len(st.session_state.optimization_runs))]
        selected_run = st.selectbox("Select run", options=run_options)
        
        if st.button("Run Optimization", type='primary'):
            with st.spinner("Optimizing schedule..."):
                result = mock_optimization()

    if result["success"]:
        st.session_state.current_run = result
        st.session_state.optimization_runs.append(result)
        st.success(f"Optimization completed in {result['duration']:.1f} seconds")
    else:
        st.error("Optimization failed")

    # Display results
    if st.session_state.current_run:
        display_optimization_results()

def mock_optimization():
    start_time = time.time()
    time.sleep(2)  # Simulate processing
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "duration": time.time() - start_time,
        "success": True,
        "schedule": pd.DataFrame({
            "Week": range(1, 13),
            **{f"Training {i+1}": [f"Crew {w*10+i}" for w in range(12)] for i in range(5)}
        }),
        "crew_data": pd.DataFrame({
            "Week": range(1, 13),
            "Available Crews": [50 - w*3 for w in range(12)]
        }),
        "metrics": {
            "Total Cost": 1_250_000,
            "EOY Status": {
                "FO": {"required": 140, "current": 118},
                "C": {"required": 30, "current": 22}
            }
        }
    }

def display_optimization_results():
    data = st.session_state.current_run
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Training Schedule")
        st.dataframe(data["schedule"], height=500)

    with col_right:
        st.subheader("Crew Availability")
        st.line_chart(data["crew_data"].set_index("Week"))
        
        st.subheader("Key Metrics")
        st.metric("Total Cost", f"${data['metrics']['Total Cost']/1e6:.2f}M")
        
        eoy_df = pd.DataFrame({
            "Position": ["FO", "C"],
            "Current": [118, 22],
            "Required": [140, 30],
            "Progress": ["84.3%", "73.3%"]
        }).set_index("Position")
        st.dataframe(eoy_df)

main()