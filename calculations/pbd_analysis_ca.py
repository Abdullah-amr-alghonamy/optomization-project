import numpy as np
import pandas as pd
import statsmodels.api as sm


def analyze_pbd(df, response_name, factor_names):

    
    # Prepare data
    

    X = df[factor_names]
    y = df[response_name]

    # Add intercept
    X_model = sm.add_constant(X)

    # Fit linear model
    model = sm.OLS(y, X_model).fit()

    
    # Regression Statistics
    

    df_resid = model.df_resid
    saturated = df_resid <= 0

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
            None if saturated else model.rsquared_adj,
            None if saturated else np.sqrt(model.mse_resid),
            int(model.nobs)
        ]
    }).round(5)

    
    # ANOVA
    

    df_reg = model.df_model
    df_total = df_reg + df_resid

    ss_reg = model.ess
    ss_resid = model.ssr
    ss_total = model.centered_tss

    ms_reg = ss_reg / df_reg

    if saturated:

        ms_resid = None
        f_stat = None
        significance_f = None

    else:

        ms_resid = ss_resid / df_resid
        f_stat = model.fvalue
        significance_f = model.f_pvalue

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
            f_stat,
            None,
            None
        ],
        "Significance F": [
            significance_f,
            None,
            None
        ]
    }, index=[
        "Regression",
        "Residual",
        "Total"
    ]).round(5)

    
    # Coefficients
    

    if saturated:

        coefficients = pd.DataFrame({
            "Coefficient": model.params,
            "Standard Error": None,
            "t Stat": None,
            "P-value": None,
            "Lower 95%": None,
            "Upper 95%": None
        })

    else:

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

    
    # Main Effects
    

    main_effects = []

    for factor in factor_names:

        coefficient = model.params[factor]

        # Main Effect = 2 × coefficient
        effect = 2 * coefficient

        if saturated:
            confidence_level = None

        else:
            p_value = model.pvalues[factor]

            confidence_level = (1 - p_value) * 100

        main_effects.append({
            "Factor": factor,
            "Main Effect": effect,
            "Confidence Level": confidence_level
        })

    main_effects_table = pd.DataFrame(
        main_effects
    )

    main_effects_table["Main Effect"] = (
        main_effects_table["Main Effect"].round(5)
    )

    main_effects_table["Confidence Level"] = (
        main_effects_table["Confidence Level"].round(5)
    )

    
    # Top 3 Factors
    
    top_3 = (
        main_effects_table
        .head(3)["Factor"]
        .tolist()
    )

    
    # Pareto Data
    

    pareto = main_effects_table.copy()

    pareto["Absolute Effect"] = (
        pareto["Main Effect"].abs()
    )

    pareto = pareto.sort_values(
        "Absolute Effect",
        ascending=False
    ).reset_index(drop=True)

    pareto["Cumulative Percentage"] = (
        pareto["Absolute Effect"].cumsum()
        / pareto["Absolute Effect"].sum()
        * 100
    )

    
    # Return Results
    

    return {
        "model": model,
        "summary": summary,
        "anova": anova,
        "coefficients": coefficients,
        "main_effects": main_effects_table,
        "top_3": top_3,
        "pareto": pareto,
        "saturated": saturated
    }