import numpy as np
import pandas as pd
import statsmodels.api as sm


def analyze_rsm(df, response_name, factor_names):

    if len(factor_names) != 3:
        raise ValueError(
            "RSM analysis currently requires exactly 3 factors."
        )

    x1, x2, x3 = factor_names

    # ---------------------------------------------------------
    # Build Quadratic Model
    # ---------------------------------------------------------

    X = pd.DataFrame({
        x1: df[x1],
        x2: df[x2],
        x3: df[x3],

        f"{x1}²": df[x1] ** 2,
        f"{x2}²": df[x2] ** 2,
        f"{x3}²": df[x3] ** 2,

        f"{x1}×{x2}": df[x1] * df[x2],
        f"{x1}×{x3}": df[x1] * df[x3],
        f"{x2}×{x3}": df[x2] * df[x3],
    })

    y = df[response_name]

    X_model = sm.add_constant(X)

    model = sm.OLS(y, X_model).fit()

    # ---------------------------------------------------------
    # Regression Statistics
    # ---------------------------------------------------------

    multiple_r = np.sqrt(model.rsquared)

    summary = pd.DataFrame({
        "Statistic": [
            "Multiple R",
            "R Square",
            "Adjusted R Square",
            "Standard Error",
            "Observations"
        ],
        "Value": [
            multiple_r,
            model.rsquared,
            model.rsquared_adj,
            np.sqrt(model.mse_resid),
            int(model.nobs)
        ]
    }).round(5)

    # ---------------------------------------------------------
    # ANOVA
    # ---------------------------------------------------------

    df_reg = model.df_model
    df_resid = model.df_resid
    df_total = df_reg + df_resid

    ss_reg = model.ess
    ss_resid = model.ssr
    ss_total = model.centered_tss

    ms_reg = ss_reg / df_reg
    ms_resid = ss_resid / df_resid

    anova = pd.DataFrame({
        "df": [
            df_reg,
            df_resid,
            df_total
        ],

        "SS": [
            ss_reg,
            ss_resid,
            ss_total
        ],

        "MS": [
            ms_reg,
            ms_resid,
            None
        ],

        "F": [
            model.fvalue,
            None,
            None
        ],

        "Significance F": [
            model.f_pvalue,
            None,
            None
        ]
    }, index=[
        "Regression",
        "Residual",
        "Total"
    ]).round(5)

    # ---------------------------------------------------------
    # Coefficients
    # ---------------------------------------------------------

    confidence_intervals = model.conf_int()

    coefficients = pd.DataFrame({
        "Coefficient": model.params,
        "Standard Error": model.bse,
        "t Stat": model.tvalues,
        "P-value": model.pvalues,
        "Lower 95%": confidence_intervals[0],
        "Upper 95%": confidence_intervals[1]
    })

    coefficients = coefficients.round(5)

    # ---------------------------------------------------------
    # Predicted Response
    # ---------------------------------------------------------

    predicted = model.predict(X_model)

    measured_vs_predicted = df.copy()

    measured_vs_predicted["Measured"] = y
    measured_vs_predicted["Predicted"] = predicted

    measured_vs_predicted = measured_vs_predicted[
        factor_names + ["Measured", "Predicted"]
    ]

    measured_vs_predicted = measured_vs_predicted.round(5)

    # ---------------------------------------------------------
    # Model Equation
    # ---------------------------------------------------------

    equation = (
        f"{response_name} = "
        f"{model.params['const']:.5f}"
    )

    for term in X.columns:

        coefficient = model.params[term]

        if coefficient >= 0:
            equation += (
                f" + {coefficient:.5f}({term})"
            )
        else:
            equation += (
                f" - {abs(coefficient):.5f}({term})"
            )
        return {
        "model": model,
        "summary": summary,
        "anova": anova,
        "coefficients": coefficients,
        "measured_vs_predicted": measured_vs_predicted,
        "equation": equation
    }