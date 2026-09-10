import numpy as np
import pandas as pd
import statsmodels.api as sm


# PBD Analysis
def analyze_pbd(df, response_name, factor_names):

    # 1) Regression

    X = df[factor_names]
    y = df[response_name]

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()


    # 2) SUMMARY OUTPUT

    multiple_r = np.sqrt(model.rsquared)

    summary = {
        "Multiple R": multiple_r,
        "R Square": model.rsquared,
        "Adjusted R Square": model.rsquared_adj,
        "Standard Error": np.sqrt(model.mse_resid),
        "Observations": int(model.nobs)
    }


    # 3) ANOVA

    df_reg = model.df_model
    df_resid = model.df_resid
    df_total = df_reg + df_resid

    ss_reg = model.ess
    ss_resid = model.ssr
    ss_total = model.centered_tss

    ms_reg = ss_reg / df_reg
    ms_resid = ss_resid / df_resid

    f_stat = model.fvalue
    significance_f = model.f_pvalue

    anova_table = pd.DataFrame({
        "df": [df_reg, df_resid, df_total],
        "SS": [ss_reg, ss_resid, ss_total],
        "MS": [ms_reg, ms_resid, np.nan],
        "F": [f_stat, np.nan, np.nan],
        "Significance F": [
            significance_f,
            np.nan,
            np.nan
        ]
    }, index=[
        "Regression",
        "Residual",
        "Total"
    ]).round(5)


    # 4) COEFFICIENTS

    results_table = pd.DataFrame({
        "Coefficients": model.params,
        "Standard Error": model.bse,
        "t Stat": model.tvalues,
        "P-value": model.pvalues,
        "Lower 95%": model.conf_int()[0],
        "Upper 95%": model.conf_int()[1]
    }).round(5)


    # 5) Return results

    return {
        "model": model,
        "summary": summary,
        "anova": anova_table,
        "coefficients": results_table
    }