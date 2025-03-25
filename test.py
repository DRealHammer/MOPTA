import streamlit as st
from moptamodel import MOPTAModel

optmodel = MOPTAModel(ddir='.')
optmodel.setOptimizationTarget()

solved = False
if st.button('Run OPT'):
    optmodel.optimize()
    solved = True

    st.write(optmodel.model.getBestSol())
