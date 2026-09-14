import streamlit as st
import pandas as pd

from calculations.draft import list_drafts, load_draft


st.set_page_config(
    page_title="DOE Optimizer",
    page_icon="🧪",
    layout="centered"
)


st.title("DOE Optimizer")

st.subheader("Design of Experiments & Optimization")

st.write(
    """
    A scientific tool for experimental design, statistical analysis,
    and optimization.
    """
)

st.divider()


# New Optimization
if st.button(
    "NEW OPTIMIZATION",
    use_container_width=True
):
    st.switch_page("pages/set_up.py")


st.divider()


# Load Existing Draft
st.subheader("Load Existing Draft")

drafts = list_drafts()

if drafts:

    selected_draft = st.selectbox(
        "Select an experiment",
        drafts
    )

    if st.button(
    "LOAD DRAFT",
    use_container_width=True):
        data = load_draft(selected_draft)

        st.session_state["draft_data"] = data

        st.session_state["variable_table"] = pd.DataFrame(data["variable_table"])

        st.session_state["response_name"] = data["response_name"]

        if data["stage"] == "screening":
            st.switch_page("pages/screening.py")
else:

    st.info("No saved experiments found.")