import streamlit as st

from database.auth import create_user, authenticate_user
from database.projects import (
    create_project,
    list_projects,
    load_project,
    delete_project
)


st.set_page_config(
    page_title="DOE Optimizer",
    page_icon="🧪",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

if "user" not in st.session_state:
    st.session_state["user"] = None


# ============================================================
# LOGIN / REGISTER
# ============================================================

if st.session_state["user"] is None:

    st.title("🧪 DOE Optimizer")

    st.subheader("Welcome")

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    with login_tab:

        st.write("Login to your account")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "LOGIN",
            use_container_width=True
        ):

            if not username or not password:

                st.warning(
                    "Please enter your username and password."
                )

            else:

                user = authenticate_user(
                    username,
                    password
                )

                if user:

                    st.session_state["user"] = user

                    st.success(
                        f"Welcome back, {user['username']}!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    with register_tab:

        st.write("Create a new account")

        new_username = st.text_input(
            "Username",
            key="register_username"
        )

        new_email = st.text_input(
            "Email",
            key="register_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "CREATE ACCOUNT",
            use_container_width=True
        ):

            if not new_username or not new_email or not new_password:

                st.warning(
                    "Please fill in all fields."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(new_password) < 6:

                st.error(
                    "Password must be at least 6 characters."
                )

            else:

                success, message = create_user(
                    new_username,
                    new_email,
                    new_password
                )

                if success:

                    st.success(message)

                    st.info(
                        "Your account has been created. "
                        "Go to the Login tab."
                    )

                else:

                    st.error(message)

    st.stop()


# ============================================================
# LOGGED-IN HOME
# ============================================================

user = st.session_state["user"]


st.title("🧪 DOE Optimizer")

st.subheader("Design of Experiments & Optimization")

st.write(
    f"Welcome, {user['username']} 👋"
)
st.write(
    """
    A scientific tool for experimental design, statistical analysis,
    and optimization.
    """
)


# ============================================================
# LOGOUT
# ============================================================

if st.button(
    "LOGOUT",
    use_container_width=True
):

    st.session_state.clear()

    st.rerun()


st.divider()


# ============================================================
# NEW OPTIMIZATION
# ============================================================

st.subheader("Start a New Optimization")

if st.button(
    "NEW OPTIMIZATION",
    use_container_width=True
):

    st.session_state["creating_project"] = True


# ============================================================
# CREATE PROJECT
# ============================================================

if st.session_state.get("creating_project", False):

    st.divider()

    st.subheader("Create New Project")

    project_name = st.text_input(
        "Project Name",
        placeholder="e.g. Reactor Optimization"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "CREATE PROJECT",
            use_container_width=True
        ):

            if not project_name.strip():

                st.warning(
                    "Please enter a project name."
                )

            else:

                project_id = create_project(
                    user["id"],
                    project_name.strip()
                )

                st.session_state["project_id"] = project_id
                st.session_state["project_name"] = project_name.strip()
                st.session_state["current_stage"] = "setup"
                st.session_state["creating_project"] = False

                st.success(
                    "Project created successfully!"
                )

                st.switch_page(
                    "pages/set_up.py"
                )

    with col2:

        if st.button(
            "CANCEL",
            use_container_width=True
        ):

            st.session_state["creating_project"] = False

            st.rerun()


st.divider()


# ============================================================
# MY PROJECTS
# ============================================================

st.subheader("My Projects")

projects = list_projects(user["id"])


if not projects:

    st.info(
        "You don't have any projects yet. "
        "Create a new optimization to get started."
    )

else:

    for project in projects:

        st.markdown(
            f"### 🧪 {project['project_name']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.caption(
                f"Stage: {project['current_stage']}"
            )

        with col2:

            st.caption(
                f"Updated: {project['updated_at']}"
            )

        # ----------------------------------------------------
        # PROJECT BUTTONS
        # ----------------------------------------------------

        col_resume, col_delete = st.columns(2)

        # ----------------------------------------------------
        # RESUME
        # ----------------------------------------------------

        with col_resume:

            if st.button(
                "▶️ RESUME",
                key=f"resume_{project['id']}",
                use_container_width=True
            ):

                loaded_project = load_project(
                    user["id"],
                    project["id"]
                )

                if loaded_project:

                    st.session_state["project_id"] = (
                        loaded_project["id"]
                    )

                    st.session_state["project_name"] = (
                        loaded_project["project_name"]
                    )

                    st.session_state["current_stage"] = (
                        loaded_project["current_stage"]
                    )

                    st.session_state["project_data"] = (
                        loaded_project["data"]
                    )
                    stage = loaded_project["current_stage"]

                    # ----------------------------------------
                    # ROUTE TO CURRENT PROJECT STAGE
                    # ----------------------------------------

                    if stage == "setup":

                        st.switch_page(
                            "pages/set_up.py"
                        )

                    elif stage == "screening":

                        st.switch_page(
                            "pages/screening.py"
                        )

                    elif stage == "pbd_analysis":

                        st.switch_page(
                            "pages/PBD analysis.py"
                        )

                    elif stage == "bbd":

                        st.switch_page(
                            "pages/BBD.py"
                        )

                    elif stage == "rsm":

                        st.switch_page(
                            "pages/RSM analysis.py"
                        )

                    else:

                        st.error(
                            f"Unknown project stage: {stage}"
                        )

                else:

                    st.error(
                        "Unable to load this project."
                    )

        # ----------------------------------------------------
        # DELETE
        # ----------------------------------------------------

        with col_delete:

            if st.button(
                "🗑️ DELETE",
                key=f"delete_{project['id']}",
                use_container_width=True
            ):

                st.session_state[
                    f"confirm_delete_{project['id']}"
                ] = True

        # ----------------------------------------------------
        # DELETE CONFIRMATION
        # ----------------------------------------------------

        if st.session_state.get(
            f"confirm_delete_{project['id']}",
            False
        ):

            st.warning(
                f"Are you sure you want to delete "
                f"{project['project_name']}?"
            )

            confirm_col, cancel_col = st.columns(2)

            with confirm_col:

                if st.button(
                    "YES, DELETE",
                    key=f"confirm_yes_{project['id']}",
                    use_container_width=True
                ):

                    delete_project(
                        user["id"],
                        project["id"]
                    )

                    st.session_state.pop(
                        f"confirm_delete_{project['id']}",
                        None
                    )

                    st.success(
                        "Project deleted successfully."
                    )

                    st.rerun()

            with cancel_col:

                if st.button(
                    "CANCEL",
                    key=f"confirm_cancel_{project['id']}",
                    use_container_width=True
                ):

                    st.session_state.pop(
                        f"confirm_delete_{project['id']}",
                        None
                    )

                    st.rerun()

        st.divider()