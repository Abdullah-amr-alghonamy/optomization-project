import streamlit as st

st.set_page_config(
    page_title="PBD Analysis - DOE Optimizer",
    page_icon="🧪",
    layout="wide"
)

st.title("PBD Analysis")

st.write("Plackett–Burman statistical analysis.")

results = st.session_state["pbd_results"]

st.subheader("Experimental Data")

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)