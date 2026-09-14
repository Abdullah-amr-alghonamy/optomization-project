import streamlit as st
import numpy as np
import pandas as pd
import statsmodels.api as sm
import plotly.graph_objects as go

from scipy.optimize import minimize


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Optimization - DOE Optimizer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 RSM Optimization")

st.write(
    "Optimization of the response using the fitted second-order "
    "Response Surface Methodology model."
)


# =========================================================
# Check Required Data
# =========================================================

required_keys = [
    "rsm_analysis",
    "variable_table",
    "top_3_factors",
    "response_name"
]

missing_keys = [
    key for key in required_keys
    if key not in st.session_state
]

if missing_keys:

    st.warning(
        "Required RSM analysis data is not available. "
        "Please complete the RSM Analysis first."
    )

    if st.button("← Back to RSM Analysis"):

        st.switch_page("pages/rsm.analysis.py")

    st.stop()


# =========================================================
# Get Data
# =========================================================

analysis = st.session_state["rsm_analysis"]

variable_table = st.session_state["variable_table"]

factor_names = st.session_state["top_3_factors"]

response_name = st.session_state["response_name"]

model = analysis["model"]


# =========================================================
# Exactly Three Factors
# =========================================================

if len(factor_names) != 3:

    st.error(
        "Optimization currently requires exactly three factors."
    )

    st.stop()


x1, x2, x3 = factor_names


# =========================================================
# Factor Information
# =========================================================

factor_info = {}

for factor in factor_names:

    row = variable_table[
        variable_table["variable_name"] == factor
    ]

    if row.empty:

        st.error(
            f"Factor information for '{factor}' was not found."
        )

        st.stop()

    row = row.iloc[0]

    factor_info[factor] = {

        "low": float(row["low_level"]),

        "high": float(row["high_level"])
    }


# =========================================================
# Actual / Coded Conversion
# =========================================================

def coded_to_actual(
    factor,
    coded_value
):

    low = factor_info[factor]["low"]

    high = factor_info[factor]["high"]

    center = (low + high) / 2

    half_range = (high - low) / 2

    return (
        center
        + np.asarray(coded_value) * half_range
    )


def actual_to_coded(
    factor,
    actual_value
):

    low = factor_info[factor]["low"]

    high = factor_info[factor]["high"]

    center = (low + high) / 2

    half_range = (high - low) / 2

    return (
        np.asarray(actual_value) - center
    ) / half_range


# =========================================================
# Model Prediction Function
# =========================================================

def predict_response(
    coded_x1,
    coded_x2,
    coded_x3
):

    # Convert inputs to 1D arrays

    x1_values = np.asarray(
        coded_x1
    ).ravel()

    x2_values = np.asarray(
        coded_x2
    ).ravel()

    x3_values = np.asarray(
        coded_x3
    ).ravel()


    # -----------------------------------------------------
    # Build EXACTLY the same quadratic features
    # used during model fitting
    # -----------------------------------------------------

    prediction_data = pd.DataFrame({

        x1: x1_values,

        x2: x2_values,

        x3: x3_values,

        f"{x1}²":
            x1_values ** 2,

        f"{x2}²":
            x2_values ** 2,

        f"{x3}²":
            x3_values ** 2,

        f"{x1}×{x2}":
            x1_values * x2_values,

        f"{x1}×{x3}":
            x1_values * x3_values,
            f"{x2}×{x3}":
            x2_values * x3_values,
    })


    # -----------------------------------------------------
    # Add intercept
    # -----------------------------------------------------

    prediction_data = sm.add_constant(
        prediction_data,
        has_constant="add"
    )


    # -----------------------------------------------------
    # Make columns EXACTLY match training model
    # -----------------------------------------------------

    prediction_data = prediction_data.reindex(
        columns=model.model.exog_names,
        fill_value=0
    )


    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    predictions = model.predict(
        prediction_data
    )

    return np.asarray(predictions)


# =========================================================
# Page Information
# =========================================================

st.subheader("📌 Selected Factors")


factor_display = pd.DataFrame({

    "Factor": factor_names,

    "Low Level": [
        factor_info[x]["low"]
        for x in factor_names
    ],

    "High Level": [
        factor_info[x]["high"]
        for x in factor_names
    ]
})


st.dataframe(
    factor_display,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# Model Equation
# =========================================================

st.subheader("🧮 Fitted Quadratic Model")


st.code(
    analysis["equation"],
    language="text"
)


st.divider()


# =========================================================
# Experimental Results
# =========================================================

st.subheader("🧪 Experimental Runs")


if "actual_bbd_results" in st.session_state:

    actual_results = (
        st.session_state[
            "actual_bbd_results"
        ].copy()
    )

    coded_results = (
        st.session_state[
            "bbd_results"
        ].copy()
    )


    # Predicted response

    actual_results["Predicted"] = (
        predict_response(

            coded_results[x1],

            coded_results[x2],

            coded_results[x3]
        )
    )


    actual_results["Predicted"] = (
        actual_results[
            "Predicted"
        ].round(5)
    )


    columns_to_show = (
        factor_names
        + [
            response_name,
            "Predicted"
        ]
    )


    st.dataframe(

        actual_results[
            columns_to_show
        ],

        use_container_width=True,

        hide_index=True
    )


else:

    st.warning(
        "Actual BBD results were not found."
    )


st.divider()


# =========================================================
# Create 3D Surface Plot
# =========================================================

def create_surface_plot(
    factor_a,
    factor_b,
    fixed_factor
):

    grid_size = 40


    # -----------------------------------------------------
    # Coded grid
    # -----------------------------------------------------

    a_values = np.linspace(
        -1,
        1,
        grid_size
    )

    b_values = np.linspace(
        -1,
        1,
        grid_size
    )


    A, B = np.meshgrid(
        a_values,
        b_values
    )


    fixed_values = np.zeros_like(A)


    # -----------------------------------------------------
    # Assign factors
    # -----------------------------------------------------

    if fixed_factor == x1:

        X1 = fixed_values
        X2 = A
        X3 = B

    elif fixed_factor == x2:

        X1 = A
        X2 = fixed_values
        X3 = B

    else:

        X1 = A
        X2 = B
        X3 = fixed_values


    # -----------------------------------------------------
    # Predict response
    # -----------------------------------------------------

    Z = predict_response(
        X1,
        X2,
        X3
    ).reshape(A.shape)
    # -----------------------------------------------------
    # Convert axes to actual values
    # -----------------------------------------------------

    actual_a = coded_to_actual(
        factor_a,
        A
    )

    actual_b = coded_to_actual(
        factor_b,
        B
    )


    # -----------------------------------------------------
    # Create Surface
    # -----------------------------------------------------

    fig = go.Figure(

        data=[

            go.Surface(

                x=actual_a,

                y=actual_b,

                z=Z,

                colorscale="Viridis",

                colorbar=dict(
                    title=response_name
                )
            )
        ]
    )


    fig.update_layout(

        title=(
            f"{response_name} Surface: "
            f"{factor_a} × {factor_b}"
        ),

        scene=dict(

            xaxis_title=factor_a,

            yaxis_title=factor_b,

            zaxis_title=response_name
        ),

        height=650,

        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50
        )
    )


    return fig


# =========================================================
# Create 2D Contour Plot
# =========================================================

def create_contour_plot(
    factor_a,
    factor_b,
    fixed_factor
):

    grid_size = 60

    a_values = np.linspace(-1, 1, grid_size)
    b_values = np.linspace(-1, 1, grid_size)

    A, B = np.meshgrid(a_values, b_values)

    fixed_values = np.zeros_like(A)

    if fixed_factor == x1:
        X1 = fixed_values
        X2 = A
        X3 = B

    elif fixed_factor == x2:
        X1 = A
        X2 = fixed_values
        X3 = B

    else:
        X1 = A
        X2 = B
        X3 = fixed_values

    Z = predict_response(
        X1,
        X2,
        X3
    ).reshape(A.shape)

    actual_a = coded_to_actual(
        factor_a,
        a_values
    )

    actual_b = coded_to_actual(
        factor_b,
        b_values
    )

    fig = go.Figure(
        data=[
            go.Contour(
                x=actual_a,
                y=actual_b,
                z=Z,
                colorscale="Viridis",

                contours=dict(
                    coloring="fill",
                    showlabels=True
                ),

                colorbar=dict(
                    title=response_name
                ),

                hovertemplate=(
                    f"{factor_a}: %{{x:.3f}}<br>"
                    f"{factor_b}: %{{y:.3f}}<br>"
                    f"{response_name}: %{{z:.3f}}"
                    "<extra></extra>"
                )
            )
        ]
    )

    fig.update_layout(
        title=(
            f"{response_name} Contour: "
            f"{factor_a} × {factor_b}"
        ),

        xaxis=dict(
            title=factor_a,
            fixedrange=False
        ),

        yaxis=dict(
            title=factor_b,
            fixedrange=False
        ),

        height=600,

        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50
        ),

        dragmode="zoom"
    )

    return fig


# =========================================================
# Response Surface & Contour Models
# =========================================================

st.subheader(
    "🌐 Response Surface & Contour Models"
)

st.write(
    "The third factor is fixed at its center level "
    "(coded value = 0)."
)


# =========================================================
# X1 × X2
# =========================================================

st.markdown(
    f"### {x1} × {x2}"
)
st.markdown(
    "#### 🌐 3D Response Surface"
)


st.plotly_chart(

    create_surface_plot(
        x1,
        x2,
        x3
    ),

    use_container_width=True
)


st.markdown(
    "#### 🗺️ Contour Plot"
)


st.plotly_chart(

    create_contour_plot(
        x1,
        x2,
        x3
    ),

    use_container_width=True
)


st.divider()


# =========================================================
# X1 × X3
# =========================================================

st.markdown(
    f"### {x1} × {x3}"
)


st.markdown(
    "#### 🌐 3D Response Surface"
)


st.plotly_chart(

    create_surface_plot(
        x1,
        x3,
        x2
    ),

    use_container_width=True
)


st.markdown(
    "#### 🗺️ Contour Plot"
)


st.plotly_chart(

    create_contour_plot(
        x1,
        x3,
        x2
    ),

    use_container_width=True
)


st.divider()


# =========================================================
# X2 × X3
# =========================================================

st.markdown(
    f"### {x2} × {x3}"
)


st.markdown(
    "#### 🌐 3D Response Surface"
)


st.plotly_chart(

    create_surface_plot(
        x2,
        x3,
        x1
    ),

    use_container_width=True
)


st.markdown(
    "#### 🗺️ Contour Plot"
)


st.plotly_chart(

    create_contour_plot(
        x2,
        x3,
        x1
    ),

    use_container_width=True
)


st.divider()


# =========================================================
# Numerical Optimization
# =========================================================

st.subheader("🎯 Response Optimization")


st.write(
    "A numerical optimization is performed inside the "
    "experimental design region (coded values −1 to +1)."
)


# =========================================================
# Objective Function
# =========================================================

def objective_function(
    values,
    maximize=False
):

    coded_x1 = values[0]
    coded_x2 = values[1]
    coded_x3 = values[2]


    prediction = predict_response(

        [coded_x1],

        [coded_x2],

        [coded_x3]
    )[0]


    # scipy.optimize.minimize performs minimization.
    #
    # Therefore:
    #
    # Maximum → minimize negative response
    #
    # Minimum → minimize response

    if maximize:

        return -prediction

    return prediction


# =========================================================
# Numerical Optimization Function
# =========================================================

def run_optimization(
    maximize=False
):

    bounds = [

        (-1, 1),

        (-1, 1),

        (-1, 1)
    ]


    # -----------------------------------------------------
    # Multiple starting points
    # -----------------------------------------------------

    starting_points = [

        [0, 0, 0],

        [1, 1, 1],

        [1, 1, -1],

        [1, -1, 1],

        [1, -1, -1],

        [-1, 1, 1],

        [-1, 1, -1],

        [-1, -1, 1],

        [-1, -1, -1]
    ]


    results = []


    # -----------------------------------------------------
    # Run optimization from each starting point
    # -----------------------------------------------------

    for start in starting_points:

        result = minimize(

            objective_function,

            x0=np.array(
                start,
                dtype=float
            ),

            args=(maximize,),

            method="L-BFGS-B",

            bounds=bounds,

            options={
                "ftol": 1e-12,
                "gtol": 1e-10,
                "maxiter": 1000
            }
        )


        if result.success:

            results.append(result)


    # -----------------------------------------------------
    # If no successful result
    # -----------------------------------------------------

    if not results:

        return None


    # -----------------------------------------------------
    # Select best result
    # -----------------------------------------------------

    if maximize:
        best_result = min(
            results,
            key=lambda r: r.fun
        )

    else:

        best_result = min(
            results,
            key=lambda r: r.fun
        )


    return best_result


# =========================================================
# Find Maximum
# =========================================================

max_result = run_optimization(
    maximize=True
)


if max_result is not None:

    max_coded = {

        x1: max_result.x[0],

        x2: max_result.x[1],

        x3: max_result.x[2]
    }


    max_predicted = predict_response(

        [max_result.x[0]],

        [max_result.x[1]],

        [max_result.x[2]]
    )[0]


    max_actual = {

        x1: coded_to_actual(
            x1,
            max_coded[x1]
        ),

        x2: coded_to_actual(
            x2,
            max_coded[x2]
        ),

        x3: coded_to_actual(
            x3,
            max_coded[x3]
        )
    }


else:

    max_coded = None
    max_actual = None
    max_predicted = None


# =========================================================
# Find Minimum
# =========================================================

min_result = run_optimization(
    maximize=False
)


if min_result is not None:

    min_coded = {

        x1: min_result.x[0],

        x2: min_result.x[1],

        x3: min_result.x[2]
    }


    min_predicted = predict_response(

        [min_result.x[0]],

        [min_result.x[1]],

        [min_result.x[2]]
    )[0]


    min_actual = {

        x1: coded_to_actual(
            x1,
            min_coded[x1]
        ),

        x2: coded_to_actual(
            x2,
            min_coded[x2]
        ),

        x3: coded_to_actual(
            x3,
            min_coded[x3]
        )
    }


else:

    min_coded = None
    min_actual = None
    min_predicted = None


# =========================================================
# Maximum Response
# =========================================================

st.markdown(
    "### 🔼 Maximum Predicted Response"
)


if max_predicted is not None:

    max_col1, max_col2 = st.columns(2)


    with max_col1:

        st.metric(

            "Predicted Response",

            f"{max_predicted:.5f}"
        )


    with max_col2:

        st.write(
            "Optimal Actual Factor Values"
        )


        max_actual_table = pd.DataFrame({

            "Factor": factor_names,

            "Actual Value": [

                max_actual[factor]

                for factor in factor_names
            ],

            "Coded Value": [

                max_coded[factor]

                for factor in factor_names
            ]
        })


        max_actual_table[
            "Actual Value"
        ] = (
            max_actual_table[
                "Actual Value"
            ].round(5)
        )


        max_actual_table[
            "Coded Value"
        ] = (
            max_actual_table[
                "Coded Value"
            ].round(5)
        )


        st.dataframe(

            max_actual_table,

            use_container_width=True,

            hide_index=True
        )


else:

    st.error(
        "Maximum response optimization failed."
    )


st.divider()


# =========================================================
# Minimum Response
# =========================================================

st.markdown(
    "### 🔽 Minimum Predicted Response"
)


if min_predicted is not None:

    min_col1, min_col2 = st.columns(2)


    with min_col1:

        st.metric(

            "Predicted Response",

            f"{min_predicted:.5f}"
        )


    with min_col2:

        st.write(
            "Optimal Actual Factor Values"
        )


        min_actual_table = pd.DataFrame({

            "Factor": factor_names,

            "Actual Value": [

                min_actual[factor]

                for factor in factor_names
            ],

            "Coded Value": [

                min_coded[factor]

                for factor in factor_names
            ]
        })
        min_actual_table[
            "Actual Value"
        ] = (
            min_actual_table[
                "Actual Value"
            ].round(5)
        )


        min_actual_table[
            "Coded Value"
        ] = (
            min_actual_table[
                "Coded Value"
            ].round(5)
        )


        st.dataframe(

            min_actual_table,

            use_container_width=True,

            hide_index=True
        )


else:

    st.error(
        "Minimum response optimization failed."
    )


st.divider()


# =========================================================
# Optimization Summary
# =========================================================

st.subheader(
    "📊 Optimization Summary"
)


if (
    max_predicted is not None
    and min_predicted is not None
):

    optimization_summary = pd.DataFrame({

        "Optimization": [

            "Maximum Response",

            "Minimum Response"
        ],

        "Predicted Response": [

            max_predicted,

            min_predicted
        ],

        f"{x1}": [

            max_actual[x1],

            min_actual[x1]
        ],

        f"{x2}": [

            max_actual[x2],

            min_actual[x2]
        ],

        f"{x3}": [

            max_actual[x3],

            min_actual[x3]
        ]
    })


    optimization_summary = (
        optimization_summary.round(5)
    )


    st.dataframe(

        optimization_summary,

        use_container_width=True,

        hide_index=True
    )


else:

    st.warning(
        "Optimization summary is not available."
    )


st.divider()


# =========================================================
# Navigation
# =========================================================

if st.button(
    "← Back to RSM Analysis",
    use_container_width=True
):

    st.switch_page(
        "pages/rsm.analysis.py"
    )