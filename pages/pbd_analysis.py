import streamlit as st

from calculations.pbd_analysis_ca import analyze_pbd


st.set_page_config(
    page_title="PBD Analysis - DOE Optimizer",
    page_icon="🧪",
    layout="wide"
)

st.title("PBD Analysis")
st.write("Plackett–Burman statistical analysis.")

# Get data from session state
results = st.session_state["pbd_results"]
variable_table = st.session_state["variable_table"]
response_name = st.session_state["response_name"]

factor_names = variable_table["variable_name"].tolist()


# Analyze PBD
analysis = analyze_pbd(
    results,
    response_name,
    factor_names
)


# Experimental Data
st.subheader("Experimental Data")

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)


st.divider()


# Summary Output
st.subheader("Regression Statistics")

st.dataframe(
    analysis["summary"],
    use_container_width=True
)


# ANOVA
st.subheader("ANOVA")

st.dataframe(
    analysis["anova"],
    use_container_width=True
)


# Coefficients
st.subheader("Coefficients")

st.dataframe(
    analysis["coefficients"],
    use_container_width=True
)
st.divider()

st.subheader("Factor Effects")

st.dataframe(
    analysis["effects"],
    use_container_width=True
)