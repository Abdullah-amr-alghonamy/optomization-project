import streamlit as st
import matplotlib.pyplot as plt

from calculations.pbd_analysis_ca import analyze_pbd


st.set_page_config(
    page_title="PBD Analysis - DOE Optimizer",
    page_icon="🧪",
    layout="wide"
)



# Page Title


st.title("PBD Analysis")

st.write(
    "Statistical analysis of the Plackett–Burman screening experiment."
)



# Load Data


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


st.subheader("🧪 Experimental Data")

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)


st.divider()



# Regression Statistics


st.subheader("📈 Regression Statistics")

st.dataframe(
    analysis["summary"],
    use_container_width=True,
    hide_index=True
)



# ANOVA


st.subheader("📊 ANOVA")

st.dataframe(
    analysis["anova"],
    use_container_width=True
)



# Coefficients


st.subheader("📐 Coefficients")

st.dataframe(
    analysis["coefficients"],
    use_container_width=True
)


st.divider()



# Main Effects


st.subheader("📉 Main Effects")

st.dataframe(
    analysis["main_effects"],
    use_container_width=True,
    hide_index=True
)



# Main Effects Chart


main_effects = analysis["main_effects"].sort_values(
    "Main Effect",
    ascending=True
)

fig, ax = plt.subplots(figsize=(15, 6))

ax.bar(
    main_effects["Factor"],
    main_effects["Main Effect"]
)

ax.axvline(
    0,
    linewidth=1
)

ax.set_xlabel("Main Effect")
ax.set_ylabel("Factor")
ax.set_title("Main Effects")

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


st.divider()



# Pareto Chart


st.subheader("📊 Pareto Chart")

pareto = analysis["pareto"]

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(
    pareto["Factor"],
    pareto["Absolute Effect"]
)

ax.set_xlabel("Factor")
ax.set_ylabel("Absolute Main Effect")
ax.set_title("Pareto Chart of Factor Effects")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

st.divider()



# Top 3 Factors


st.subheader("🏆 Top 3 Factors")

top_3 = analysis["top_3"]
st.session_state['top_3_factors'] = top_3

for i, factor in enumerate(top_3, start=1):

    st.write(
        f"{i}. {factor}"
    )

st.divider ()

if st.button(
    "Continue to BBD →",
    type="primary",
    use_container_width=True
):
    st.switch_page("pages/BBD.py")