import streamlit as st
import pandas as pd
import numpy as np



st.set_page_config(
    page_title="DOE Optimizer",
    layout="centered"
)

# Default page
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# Welcome Page

if st.session_state.page == "welcome":

    st.title("DOE Optimizer")

    st.subheader("Design of Experiments & Optimization")

    st.write(
        """
        A scientific tool for experimental design, statistical analysis,
        and optimization.
        """
    )

    st.write("")

    if st.button(
        "START OPTIMIZATION",
        use_container_width=True
    ):
        st.switch_page("pages/set_up.py")
        st.rerun()

