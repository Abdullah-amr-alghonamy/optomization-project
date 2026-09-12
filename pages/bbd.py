import streamlit as st
from calculations.box_behnken import generate_bbd


st.set_page_config(
    page_title="BBD - DOE Optimizer",
    page_icon="🧪",
    layout="wide"
)


st.title("🧪 Box–Behnken Design")
st.write(
    "Response Surface Methodology using the three most influential factors."
)



# Get data from session state


top_3 = st.session_state["top_3_factors"]
variable_table = st.session_state["variable_table"]
response_name = st.session_state["response_name"]



# Selected Factors


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



# Generate BBD


design = generate_bbd(top_3)



# Actual Experimental Levels


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



# Coded BBD Design


st.subheader("📋 Box–Behnken Design")

st.write("Coded experimental levels:")

st.dataframe(
    design,
    use_container_width=True,
    hide_index=True
)



# Actual Design


st.write("Actual experimental levels:")

st.dataframe(
    actual_design,
    use_container_width=True,
    hide_index=True
)


st.divider()



# Enter Responses


st.subheader(f"🧪 Enter {response_name}")

st.write(
    "Enter the experimental response obtained for each run."
)


response_values = []

for run in design["Run"]:

    response = st.number_input(
        f"Run {run}",
        key=f"bbd_response_{run}",
        format="%.4f"
    )

    response_values.append(response)


st.divider()



# Continue to RSM Analysis


if st.button(
    "Continue to RSM Analysis →",
    type="primary",
    use_container_width=True
):

    # Keep coded values for RSM calculations
    bbd_results = design.copy()

    bbd_results