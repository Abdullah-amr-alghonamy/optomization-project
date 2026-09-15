import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from calculations.pbd_analysis_ca import analyze_pbd
from database.projects import save_project


st.set_page_config(
    page_title="PBD Analysis - DOE Optimizer",
    page_icon="🧪",
    layout="wide"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("PBD Analysis")

st.write(
    "Statistical analysis of the Plackett–Burman screening experiment."
)


# ============================================================
# LOAD PROJECT DATA
# ============================================================

# Normal workflow:
# data already exists in session_state.

# Resume workflow:
# restore the required data from the saved project.

if "pbd_results" not in st.session_state:

    project_data = st.session_state.get(
        "project_data",
        {}
    )

    if "pbd_results" in project_data:

        st.session_state["pbd_results"] = pd.DataFrame(
            project_data["pbd_results"]
        )

    elif "design" in project_data and "responses" in project_data:

        design = pd.DataFrame(
            project_data["design"]
        )

        response_name = project_data.get(
            "response_name"
        )

        responses = project_data["responses"]

        design[response_name] = responses

        st.session_state["pbd_results"] = design

    else:

        st.error(
            "No PBD results found for this project."
        )

        if st.button("← Back to Home"):

            st.switch_page("Home.py")

        st.stop()


# ============================================================
# LOAD VARIABLE DATA
# ============================================================

if "variable_table" not in st.session_state:

    project_data = st.session_state.get(
        "project_data",
        {}
    )

    if "variable_table" in project_data:

        st.session_state["variable_table"] = pd.DataFrame(
            project_data["variable_table"]
        )

    else:

        st.error(
            "No variable information found for this project."
        )

        if st.button("← Back to Home"):

            st.switch_page("Home.py")

        st.stop()


# ============================================================
# LOAD RESPONSE NAME
# ============================================================

if "response_name" not in st.session_state:

    project_data = st.session_state.get(
        "project_data",
        {}
    )

    if "response_name" in project_data:

        st.session_state["response_name"] = (
            project_data["response_name"]
        )

    else:

        st.error(
            "No response information found for this project."
        )

        if st.button("← Back to Home"):

            st.switch_page("Home.py")

        st.stop()


# ============================================================
# GET DATA
# ============================================================

results = st.session_state["pbd_results"]

variable_table = st.session_state["variable_table"]

response_name = st.session_state["response_name"]

factor_names = variable_table["variable_name"].tolist()


# ============================================================
# ANALYZE PBD
# ============================================================

analysis = analyze_pbd(
    results,
    response_name,
    factor_names
)


# ============================================================
# EXPERIMENTAL DATA
# ============================================================

st.subheader("🧪 Experimental Data")

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)

st.divider()


# ============================================================
# REGRESSION STATISTICS
# ============================================================

st.subheader("📈 Regression Statistics")

st.dataframe(
    analysis["summary"],
    use_container_width=True,
    hide_index=True
)
# ============================================================
# ANOVA
# ============================================================

st.subheader("📊 ANOVA")

st.dataframe(
    analysis["anova"],
    use_container_width=True
)


# ============================================================
# COEFFICIENTS
# ============================================================

st.subheader("📐 Coefficients")

st.dataframe(
    analysis["coefficients"],
    use_container_width=True
)

st.divider()


# ============================================================
# MAIN EFFECTS
# ============================================================

st.subheader("📉 Main Effects")

st.dataframe(
    analysis["main_effects"],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# MAIN EFFECTS CHART
# ============================================================

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


# ============================================================
# PARETO CHART
# ============================================================

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


# ============================================================
# TOP 3 FACTORS
# ============================================================

st.subheader("🏆 Top 3 Factors")

top_3 = analysis["top_3"]

st.session_state["top_3_factors"] = top_3

for i, factor in enumerate(top_3, start=1):

    st.write(
        f"{i}. {factor}"
    )

st.divider()


# ============================================================
# CONTINUE TO BBD
# ============================================================

if st.button(
    "Continue to BBD →",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # Save analysis results
    # --------------------------------------------------------

    project_data = {

        "variable_table":
            variable_table.to_dict(
                orient="records"
            ),

        "response_name":
            response_name,

        "pbd_results":
            results.to_dict(
                orient="records"
            ),

        "pbd_summary":
            analysis["summary"].to_dict(
                orient="records"
            ),

        "pbd_anova":
            analysis["anova"].reset_index().to_dict(
                orient="records"
            ),

        "pbd_coefficients":
            analysis["coefficients"].reset_index().to_dict(
                orient="records"
            ),

        "pbd_main_effects":
            analysis["main_effects"].to_dict(
                orient="records"
            ),

        "pbd_pareto":
            analysis["pareto"].to_dict(
                orient="records"
            ),

        "top_3_factors":
            top_3
    }

    # --------------------------------------------------------
    # Save project
    # --------------------------------------------------------

    save_project(
        user_id=st.session_state["user"]["id"],
        project_id=st.session_state["project_id"],
        data=project_data,
        current_stage="bbd"
    )

    # --------------------------------------------------------
    # Update session state
    # --------------------------------------------------------

    st.session_state["project_data"] = project_data
    st.session_state["current_stage"] = "bbd"

    # --------------------------------------------------------
    # Go to BBD
    # --------------------------------------------------------

    st.switch_page(
        "pages/bbd.py"
    )
    #