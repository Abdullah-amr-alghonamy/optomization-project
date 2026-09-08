import streamlit as st
import pandas as pd

from calculations.plackett_burman import generate_pbd


st.set_page_config(
    page_title="Screening - DOE Optimizer",
    page_icon="🧪",
    layout="wide"
)


# Get setup data
variable_table = st.session_state["variable_table"]

response_name = st.session_state["response_name"]


# Number of factors
number_of_factors = len(variable_table)


# Factor names
factor_names = variable_table["variable_name"].tolist()


# Title
st.title("🔬 Screening Experiment")

st.write(
    "Plackett–Burman Design for factor screening."
)


# Generate PBD
design = generate_pbd(number_of_factors)


# Rename X1, X2, X3...
# to the actual variable names

design = design.rename(
    columns={
        f"X{i + 1}": factor_names[i]
        for i in range(number_of_factors)
    }
)


# Display design
st.subheader("Plackett–Burman Design")

st.dataframe(
    design,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader(f"Enter {response_name}")

st.write(
    "Enter the experimental response obtained for each run."
)

response_values = []

for run in design["Run"]:

    response = st.number_input(
        f"Run {run}",
        key=f"response_{run}",
        format="%.4f"
    )

    response_values.append(response)

if st.button(
    "Continue to Analysis →",
    type="primary",
    use_container_width=True
):

    results = design.copy()

    results[response_name] = response_values

    st.session_state["pbd_results"] = results

    st.success("Responses saved successfully!")

