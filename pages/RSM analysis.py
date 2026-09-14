import streamlit as st

from calculations.rsm_analysis import analyze_rsm


st.set_page_config(
    page_title="RSM Analysis - DOE Optimizer",
    page_icon="🧪",
    layout="wide"
)


st.title("📈 RSM Analysis")

st.write(
    "Response Surface Methodology using a second-order quadratic model."
)

if "bbd_results" not in st.session_state:
    st.warning(
        "No BBD experiment data found. "
        "Please complete the BBD experiment first."
    )

    if st.button("← Back to BBD"):
        st.switch_page("pages/bbd.py")

    st.stop()


# ---------------------------------------------------------
# Get data from session state
# ---------------------------------------------------------

bbd_results = st.session_state["bbd_results"]
variable_table = st.session_state["variable_table"]
response_name = st.session_state["response_name"]
factor_names = st.session_state["top_3_factors"]


# ---------------------------------------------------------
# Analyze RSM
# ---------------------------------------------------------

analysis = analyze_rsm(
    bbd_results,
    response_name,
    factor_names
)


# ---------------------------------------------------------
# Experimental Data
# ---------------------------------------------------------

st.subheader("🧪 Experimental Data")

st.dataframe(
    bbd_results,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ---------------------------------------------------------
# Regression Statistics
# ---------------------------------------------------------

st.subheader("📈 Regression Statistics")

st.dataframe(
    analysis["summary"],
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# ANOVA
# ---------------------------------------------------------

st.subheader("📊 ANOVA")

st.dataframe(
    analysis["anova"],
    use_container_width=True
)


# ---------------------------------------------------------
# Coefficients
# ---------------------------------------------------------

st.subheader("📐 Coefficients")

st.dataframe(
    analysis["coefficients"],
    use_container_width=True
)


st.divider()


# ---------------------------------------------------------
# Quadratic Model
# ---------------------------------------------------------

st.subheader("🧮 Quadratic Model")

st.code(
    analysis["equation"],
    language="text"
)


st.divider()


# ---------------------------------------------------------
# Measured vs Predicted
# ---------------------------------------------------------

st.subheader("📋 Measured vs Predicted")

st.dataframe(
    analysis["measured_vs_predicted"],
    use_container_width=True,
    hide_index=True
)


st.divider()


# ---------------------------------------------------------
# Continue to Optimization
# ---------------------------------------------------------

if st.button(
    "Continue to Optimization →",
    type="primary",
    use_container_width=True
):

    st.session_state["rsm_analysis"] = analysis

    st.switch_page("pages/Optimization.py")