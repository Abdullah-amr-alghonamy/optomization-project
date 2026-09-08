import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Setup - DOE Optimizer",
    layout="centered"
)


st.title("Experiment Setup")
st.write("Enter the variables and their experimental ranges.")


number_of_variables = st.number_input(
    "Number of variables",
    min_value=1,
    max_value=50,
    value=3,
    step=1
)


st.divider()

# Variable inputs

st.subheader("Variable Information")


variable_table = []


for n in range(number_of_variables):

    st.markdown(f"### Variable {n + 1}")

    col1, col2, col3 = st.columns(3)

    with col1:
        variable_name = st.text_input(
            "Variable name",
            key=f"variable_name_{n}"
        )

    with col2:
        low_level = st.number_input(
            "Low level",
            key=f"low_level_{n}"
        )

    with col3:
        high_level = st.number_input(
            "High level",
            key=f"high_level_{n}"
        )

    variable_table.append({
        "variable_name": variable_name,
        "high_level": high_level,
        "low_level": low_level
    })


st.divider()

# Response name

st.subheader("Response")

response_name = st.text_input(
    "Response name",
    placeholder="e.g. Yield, Activity, Concentration..."
)


st.divider()

# Continue button

if st.button(
    "Continue →",
    type="primary",
    use_container_width=True
):
    df_variable_table = pd.DataFrame(variable_table)

    st.session_state["variable_table"] = df_variable_table
    st.session_state["response_name"] = response_name

    st.switch_page("pages/screening.py")