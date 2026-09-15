import streamlit as st
import pandas as pd

from calculations.plackett_burman import generate_pbd
from database.projects import save_project


st.set_page_config(
    page_title="Screening - DOE Optimizer",
    page_icon="🧪",
    layout="wide"
)


# ============================================================
# LOAD PROJECT DATA
# ============================================================

# Normal flow:
# Setup → Screening
#
# Resume flow:
# Home → Resume → Screening

if "variable_table" not in st.session_state:

    project_data = st.session_state.get("project_data", {})

    if "variable_table" in project_data:

        st.session_state["variable_table"] = pd.DataFrame(
            project_data["variable_table"]
        )

    if "response_name" in project_data:

        st.session_state["response_name"] = project_data[
            "response_name"
        ]


# Check that setup data exists
if (
    "variable_table" not in st.session_state
    or "response_name" not in st.session_state
):

    st.error(
        "Setup data not found. Please return to the Setup page."
    )

    if st.button("← Back to Home"):
        st.switch_page("Home.py")

    st.stop()


# Get setup data
variable_table = st.session_state["variable_table"]

response_name = st.session_state["response_name"]


# ============================================================
# NUMBER OF FACTORS
# ============================================================

number_of_factors = len(variable_table)


# ============================================================
# FACTOR NAMES
# ============================================================

factor_names = variable_table["variable_name"].tolist()


# ============================================================
# TITLE
# ============================================================

st.title("Screening Experiment")

st.write(
    "Plackett–Burman Design for factor screening."
)


# ============================================================
# GENERATE PBD
# ============================================================

design = generate_pbd(number_of_factors)


# Rename X1, X2, X3...
# to the actual variable names

design = design.rename(
    columns={
        f"X{i + 1}": factor_names[i]
        for i in range(number_of_factors)
    }
)


# ============================================================
# DISPLAY VARIABLES
# ============================================================

st.subheader("Variables")

st.table(variable_table)

st.divider()


# ============================================================
# DISPLAY DESIGN
# ============================================================

st.subheader("Plackett–Burman Design")

st.dataframe(
    design,
    use_container_width=True,
    hide_index=True
)

st.divider()


# ============================================================
# ENTER RESPONSE VALUES
# ============================================================

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


# ============================================================
# CONTINUE TO ANALYSIS
# ============================================================

if st.button(
    "Continue to Analysis →",
    type="primary",
    use_container_width=True
):

    # Create final PBD results
    results = design.copy()

    results[response_name] = response_values

    # Save results in session state
    st.session_state["pbd_results"] = results

    # --------------------------------------------------------
    # Save project data
    # --------------------------------------------------------
    project_data = {
        "variable_table": variable_table.to_dict(
            orient="records"
        ),
        "response_name": response_name,
        "design": design.to_dict(
            orient="records"
        ),
        "responses": response_values,
        "pbd_results": results.to_dict(
            orient="records"
        )
    }

    save_project(
        user_id=st.session_state["user"]["id"],
        project_id=st.session_state["project_id"],
        data=project_data,
        current_stage="pbd_analysis"
    )

    # Update current stage
    st.session_state["current_stage"] = "pbd_analysis"

    # Go to PBD Analysis
    st.switch_page("pages/PBD analysis.py")