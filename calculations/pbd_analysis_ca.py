import numpy as np
import pandas as pd
import statsmodels.api as sm


# PBD Analysis
def analyze_pbd(df, response_name, factor_names):

    # -------------------------
    # 1) Regression
    # -------------------------
    X = df[factor_names]
    y = df[response_name]

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    # -------------------------
    # 2) Check residual degrees
    # -------------------------
    df_resid = model.df_resid
    saturated = df_resid <= 0

    # -------------------------
    # 3) Summary Output
    # -------------------------
    multiple_r = np.sqrt(model.rsquared)

    summary = {
        "Multiple R": multiple_r,
        "R Square": model.rsquared,
        "Adjusted R Square": None if saturated else model.rsquared_adj,
        "Standard Error": None if saturated else np.sqrt(model.mse_resid),
        "Observations": int(model.nobs)
    }

    # -------------------------
    # 4) ANOVA
    # -------------------------
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

    anova_table = pd.DataFrame({
        "df": [df_reg, df_resid, df_total],
        "SS": [ss_reg, ss_resid, ss_total],
        "MS": [ms_reg, ms_resid, None],
        "F": [f_stat, None, None],
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

    # -------------------------
    # 5) Coefficients
    # -------------------------
    if saturated:

        results_table = pd.DataFrame({
            "Coefficients": model.params,
            "Standard Error": None,
            "t Stat": None,
            "P-value": None,
            "Lower 95%": None,
            "Upper 95%": None
        })

    else:

        results_table = pd.DataFrame({
            "Coefficients": model.params,
            "Standard Error": model.bse,
            "t Stat": model.tvalues,
            "P-value": model.pvalues,
            "Lower 95%": model.conf_int()[0],
            "Upper 95%": model.conf_int()[1]
        })

    results_table = results_table.round(5)

    # -------------------------
    # 6) Factor Effects
    # -------------------------
    effects = model.params[factor_names] * 2

    effect_table = pd.DataFrame({
        "Effect": effects,
        "Absolute Effect": effects.abs()
    })

    effect_table["Rank"] = (
        effect_table["Absolute Effect"]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    effect_table = effect_table.sort_values(
        "Absolute Effect",
        ascending=False
    ).round(5)

    # -------------------------
    # 7) Return Results
    # -------------------------
    return {
        "model": model,
        "summary": summary,
        "anova": anova_table,
        "coefficients": results_table,
        "effects": effect_table,
        "saturated": saturated
    }