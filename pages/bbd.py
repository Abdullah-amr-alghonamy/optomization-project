import streamlit as st
import pandas as pd

from calculations.box_behnken import generate_bbd
from database.projects import save_project, load_project


st.set_page_config(
    page_title="BBD - DOE Optimizer",
    page_icon="🧪",
    layout="wide"
)


st.title("🧪 Box–Behnken Design")
st.write(
    "Response Surface Methodology using the three most influential factors."
)


# ============================================================
# Restore project data if this page was opened through Resume
# ============================================================

if (
    "project_data" in st.session_state
    and st.session_state["project_data"]
):

    project_data = st.session_state["project_data"]

    if "top_3_factors" not in st.session_state:
        if "top_3_factors" in project_data:
            st.session_state["top_3_factors"] = (
                project_data["top_3_factors"]
            )

    if "variable_table" not in st.session_state:
        if "variable_table" in project_data:
            st.session_state["variable_table"] = pd.DataFrame(
                project_data["variable_table"]
            )

    if "response_name" not in st.session_state:
        if "response_name" in project_data:
            st.session_state["response_name"] = (
                project_data["response_name"]
            )


# ============================================================
# Get data from session state
# ============================================================

top_3 = st.session_state["top_3_factors"]
variable_table = st.session_state["variable_table"]
response_name = st.session_state["response_name"]


# Make sure variable_table is a DataFrame
if not isinstance(variable_table, pd.DataFrame):
    variable_table = pd.DataFrame(variable_table)


# ============================================================
# Selected Factors
# ============================================================

st.subheader("🏆 Selected Factors")

for i, factor in enumerate(top_3, start=1):

    factor_info = variable_table[
        variable_table["variable_name"] == factor
    ].iloc[0]

    st.write(
        f"X{i} — {factor}  "
        f"(Low: {factor_info['low_level']}, "
        f"High: {factor_info['high_level']})"
    )


st.divider()


# ============================================================
# Generate BBD
# ============================================================

design = generate_bbd(top_3)


# ============================================================
# Actual Experimental Levels
# ============================================================

actual_design = design.copy()

for factor in top_3:

    factor_info = variable_table[
        variable_table["variable_name"] == factor
    ].iloc[0]

    low = factor_info["low_level"]
    high = factor_info["high_level"]

    center = (low + high) / 2
    half_range = (high - low) / 2

    actual_design[factor] = (
        center
        + design[factor] * half_range
    )


# ============================================================
# Coded BBD Design
# ============================================================

st.subheader("📋 Box–Behnken Design")

st.write("Coded experimental levels:")

st.dataframe(
    design,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# Actual Design
# ============================================================

st.write("Actual experimental levels:")

st.dataframe(
    actual_design,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# Restore previously entered responses
# ============================================================

saved_responses = {}

if "project_data" in st.session_state:

    project_data = st.session_state["project_data"]

    if "bbd_responses" in project_data:
        saved_responses = project_data["bbd_responses"]


# ============================================================
# Enter Responses
# ============================================================
st.subheader(f"🧪 Enter {response_name}")

st.write(
    "Enter the experimental response obtained for each run."
)


response_values = []

for run in design["Run"]:

    default_value = saved_responses.get(str(run), 0.0)

    response = st.number_input(
        f"Run {run}",
        value=float(default_value),
        key=f"bbd_response_{run}",
        format="%.4f"
    )

    response_values.append(response)


st.divider()


# ============================================================
# Auto-save BBD responses
# ============================================================

if "project_id" in st.session_state:

    auto_save_data = {
        "variable_table": variable_table.to_dict(
            orient="records"
        ),
        "response_name": response_name,
        "top_3_factors": top_3,
        "bbd_design": design.to_dict(
            orient="records"
        ),
        "actual_bbd_design": actual_design.to_dict(
            orient="records"
        ),
        "bbd_responses": {
            str(run): value
            for run, value in zip(
                design["Run"],
                response_values
            )
        }
    }

    save_project(
        user_id=st.session_state["user"]["id"],
        project_id=st.session_state["project_id"],
        data=auto_save_data,
        current_stage="bbd"
    )

    st.session_state["project_data"] = auto_save_data
    st.session_state["current_stage"] = "bbd"


# ============================================================
# Continue to RSM Analysis
# ============================================================

if st.button(
    "Continue to RSM Analysis →",
    type="primary",
    use_container_width=True
):

    # Attach the entered response values to the design
    bbd_results = design.copy()
    bbd_results[response_name] = response_values

    # Keep actual (uncoded) values with responses
    actual_results = actual_design.copy()
    actual_results[response_name] = response_values

    # Save to session state
    st.session_state["bbd_results"] = bbd_results
    st.session_state["actual_bbd_results"] = actual_results

    # ========================================================
    # Save complete BBD results to project
    # ========================================================

    project_data = {
        "variable_table": variable_table.to_dict(
            orient="records"
        ),
        "response_name": response_name,
        "top_3_factors": top_3,

        "bbd_design": design.to_dict(
            orient="records"
        ),

        "actual_bbd_design": actual_design.to_dict(
            orient="records"
        ),

        "bbd_responses": {
            str(run): value
            for run, value in zip(
                design["Run"],
                response_values
            )
        },

        "bbd_results": bbd_results.to_dict(
            orient="records"
        ),

        "actual_bbd_results": actual_results.to_dict(
            orient="records"
        )
    }

    save_project(
        user_id=st.session_state["user"]["id"],
        project_id=st.session_state["project_id"],
        data=project_data,
        current_stage="rsm"
    )

    st.session_state["project_data"] = project_data
    st.session_state["current_stage"] = "rsm"

    st.switch_page("pages/RSM analysis.py")