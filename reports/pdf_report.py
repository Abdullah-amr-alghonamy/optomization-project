from io import BytesIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)


# =========================================================
# Helpers
# =========================================================

def format_number(value, decimals=5):
    try:
        if pd.isna(value):
            return ""
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


def dataframe_to_table(data, font_size=7):
    if data is None:
        return None

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    if data.empty:
        return None

    data = data.copy()

    for column in data.columns:
        data[column] = data[column].apply(
            lambda x: format_number(x)
            if isinstance(x, (int, float, np.number))
            else str(x)
        )

    table_data = [list(data.columns)] + data.values.tolist()

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F4E78")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                font_size
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                7
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, 0),
                7
            ),
        ])
    )

    return table


def dataframe_from_project(project_data, key):
    value = project_data.get(key)

    if value is None:
        return None

    try:
        return pd.DataFrame(value)
    except Exception:
        return None


# =========================================================
# Matplotlib Chart Helpers
# =========================================================

def create_main_effects_chart(main_effects):
    if main_effects is None or main_effects.empty:
        return None

    data = main_effects.copy()

    if "Factor" not in data.columns:
        return None

    if "Main Effect" not in data.columns:
        return None

    data = data.sort_values(
        "Main Effect",
        ascending=True
    )

    fig, ax = plt.subplots(
        figsize=(9, 4.8)
    )

    ax.barh(
        data["Factor"],
        data["Main Effect"]
    )

    ax.axvline(
        0,
        linewidth=1
    )

    ax.set_xlabel("Main Effect")
    ax.set_ylabel("Factor")
    ax.set_title("Main Effects")

    plt.tight_layout()

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(fig)

    buffer.seek(0)

    return buffer


def create_pareto_chart(pareto):
    if pareto is None or pareto.empty:
        return None

    data = pareto.copy()

    if "Factor" not in data.columns:
        return None
    if "Absolute Effect" not in data.columns:
        return None

    fig, ax = plt.subplots(
        figsize=(9, 4.8)
    )

    ax.bar(
        data["Factor"],
        data["Absolute Effect"]
    )

    ax.set_xlabel("Factor")
    ax.set_ylabel("Absolute Main Effect")
    ax.set_title("Pareto Chart of Factor Effects")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(fig)

    buffer.seek(0)

    return buffer


# =========================================================
# RSM Prediction
# =========================================================

def create_prediction_function(
    model,
    factor_names
):
    x1, x2, x3 = factor_names

    def predict(
        coded_x1,
        coded_x2,
        coded_x3
    ):
        x1_values = np.asarray(
            coded_x1
        ).ravel()

        x2_values = np.asarray(
            coded_x2
        ).ravel()

        x3_values = np.asarray(
            coded_x3
        ).ravel()

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

        import statsmodels.api as sm

        prediction_data = sm.add_constant(
            prediction_data,
            has_constant="add"
        )

        prediction_data = prediction_data.reindex(
            columns=model.model.exog_names,
            fill_value=0
        )

        predictions = model.predict(
            prediction_data
        )

        return np.asarray(predictions)

    return predict


# =========================================================
# Actual / Coded Conversion
# =========================================================

def coded_to_actual(
    factor,
    coded_value,
    factor_info
):
    low = factor_info[factor]["low"]
    high = factor_info[factor]["high"]

    center = (low + high) / 2
    half_range = (high - low) / 2

    return (
        center
        + np.asarray(coded_value) * half_range
    )


# =========================================================
# 3D Surface Chart
# =========================================================

def create_3d_surface_chart(
    factor_a,
    factor_b,
    fixed_factor,
    factor_names,
    factor_info,
    model,
    response_name
):
    x1, x2, x3 = factor_names

    predict = create_prediction_function(
        model,
        factor_names
    )

    grid_size = 35

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

    Z = predict(
        X1,
        X2,
        X3
    ).reshape(A.shape)

    actual_a = coded_to_actual(
        factor_a,
        A,
        factor_info
    )

    actual_b = coded_to_actual(
        factor_b,
        B,
        factor_info
    )

    fig = plt.figure(
        figsize=(8, 6)
    )

    ax = fig.add_subplot(
        111,
        projection="3d"
    )

    surface = ax.plot_surface(
        actual_a,
        actual_b,
        Z,
        cmap="viridis",
        edgecolor="none"
    )

    ax.set_xlabel(
        factor_a
    )

    ax.set_ylabel(
        factor_b
    )

    ax.set_zlabel(
        response_name
    )
    ax.set_title(
        f"{response_name} Surface: "
        f"{factor_a} × {factor_b}"
    )

    fig.colorbar(
        surface,
        ax=ax,
        shrink=0.65,
        pad=0.1,
        label=response_name
    )

    plt.tight_layout()

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(fig)

    buffer.seek(0)

    return buffer


# =========================================================
# 2D Contour Chart
# =========================================================

def create_contour_chart(
    factor_a,
    factor_b,
    fixed_factor,
    factor_names,
    factor_info,
    model,
    response_name
):
    x1, x2, x3 = factor_names

    predict = create_prediction_function(
        model,
        factor_names
    )

    grid_size = 50

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

    Z = predict(
        X1,
        X2,
        X3
    ).reshape(A.shape)

    actual_a = coded_to_actual(
        factor_a,
        a_values,
        factor_info
    )

    actual_b = coded_to_actual(
        factor_b,
        b_values,
        factor_info
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    contour = ax.contourf(
        actual_a,
        actual_b,
        Z,
        levels=20,
        cmap="viridis"
    )

    ax.set_xlabel(
        factor_a
    )

    ax.set_ylabel(
        factor_b
    )

    ax.set_title(
        f"{response_name} Contour: "
        f"{factor_a} × {factor_b}"
    )

    fig.colorbar(
        contour,
        ax=ax,
        label=response_name
    )

    plt.tight_layout()

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(fig)

    buffer.seek(0)

    return buffer


# =========================================================
# Main PDF Generator
# =========================================================

def generate_pdf_report(
    project_name,
    response_name,
    variable_table,
    factor_names,
    equation=None,
    experimental_results=None,
    max_predicted=None,
    max_actual=None,
    max_coded=None,
    min_predicted=None,
    min_actual=None,
    min_coded=None,
    rsm_analysis=None,
    pbd_data=None
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.3 * cm,
        leftMargin=1.3 * cm,
        topMargin=1.3 * cm,
        bottomMargin=1.3 * cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        leading=28,
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=19,
        spaceBefore=12,
        spaceAfter=10,
        textColor=colors.HexColor("#1F4E78")
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=7,
        textColor=colors.HexColor("#1F4E78")
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=14,
        spaceAfter=8
    )
    equation_style = ParagraphStyle(
        "Equation",
        parent=styles["Code"],
        fontSize=8,
        leading=11,
        backColor=colors.HexColor("#F2F2F2"),
        borderColor=colors.lightgrey,
        borderWidth=0.5,
        borderPadding=8
    )

    story = []

    # =====================================================
    # Cover
    # =====================================================

    story.append(
        Spacer(
            1,
            1.5 * cm
        )
    )

    story.append(
        Paragraph(
            "DOE Optimization Report",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Design of Experiments & "
            "Response Surface Methodology",
            subtitle_style
        )
    )

    project_info = pd.DataFrame({
        "Item": [
            "Project Name",
            "Response",
            "Selected Factors"
        ],
        "Value": [
            project_name,
            response_name,
            ", ".join(factor_names)
        ]
    })

    project_table = dataframe_to_table(
        project_info
    )

    if project_table:
        story.append(project_table)

    story.append(
        Spacer(
            1,
            1 * cm
        )
    )

    story.append(
        Paragraph(
            "This report summarizes the complete DOE "
            "optimization workflow including Plackett–Burman "
            "screening, Box–Behnken Design, Response Surface "
            "Methodology, response surface visualization, "
            "and numerical optimization.",
            normal_style
        )
    )

    story.append(PageBreak())

    # =====================================================
    # 1. Selected Factors
    # =====================================================

    story.append(
        Paragraph(
            "1. Selected Factors",
            heading_style
        )
    )

    factor_rows = []

    for factor in factor_names:

        row = variable_table[
            variable_table["variable_name"] == factor
        ]

        if row.empty:
            continue

        row = row.iloc[0]

        factor_rows.append({
            "Factor": factor,
            "Low Level": row["low_level"],
            "High Level": row["high_level"]
        })

    factor_df = pd.DataFrame(
        factor_rows
    )

    factor_table = dataframe_to_table(
        factor_df
    )

    if factor_table:
        story.append(factor_table)

    story.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    # =====================================================
    # 2. PBD Screening
    # =====================================================

    story.append(
        Paragraph(
            "2. Plackett–Burman Screening",
            heading_style
        )
    )

    if pbd_data:

        pbd_results = pbd_data.get(
            "pbd_results"
        )

        if pbd_results is not None:

            story.append(
                Paragraph(
                    "2.1 Experimental Data",
                    subheading_style
                )
            )

            table = dataframe_to_table(
                pd.DataFrame(pbd_results)
            )

            if table:
                story.append(table)

            story.append(
                Spacer(1, 0.4 * cm)
            )

        pbd_summary = pbd_data.get(
            "pbd_summary"
        )

        if pbd_summary is not None:

            story.append(
                Paragraph(
                    "2.2 Regression Statistics",
                    subheading_style
                )

            )

            table = dataframe_to_table(
                pd.DataFrame(pbd_summary)
            )

            if table:
                story.append(table)

        pbd_anova = pbd_data.get(
            "pbd_anova"
        )

        if pbd_anova is not None:

            story.append(
                Paragraph(
                    "2.3 ANOVA",
                    subheading_style
                )
            )
            table = dataframe_to_table(
                pd.DataFrame(pbd_anova)
            )

            if table:
                story.append(table)

        pbd_coefficients = pbd_data.get(
            "pbd_coefficients"
        )

        if pbd_coefficients is not None:

            story.append(
                Paragraph(
                    "2.4 Coefficients",
                    subheading_style
                )
            )

            table = dataframe_to_table(
                pd.DataFrame(pbd_coefficients)
            )

            if table:
                story.append(table)

        pbd_main_effects = pbd_data.get(
            "pbd_main_effects"
        )

        if pbd_main_effects is not None:

            main_effects_df = pd.DataFrame(
                pbd_main_effects
            )

            story.append(
                Paragraph(
                    "2.5 Main Effects",
                    subheading_style
                )
            )

            table = dataframe_to_table(
                main_effects_df
            )

            if table:
                story.append(table)

            chart = create_main_effects_chart(
                main_effects_df
            )

            if chart:
                story.append(
                    Spacer(
                        1,
                        0.3 * cm
                    )
                )

                story.append(
                    Image(
                        chart,
                        width=16 * cm,
                        height=8.5 * cm
                    )
                )

        pbd_pareto = pbd_data.get(
            "pbd_pareto"
        )

        if pbd_pareto is not None:

            pareto_df = pd.DataFrame(
                pbd_pareto
            )

            story.append(
                Paragraph(
                    "2.6 Pareto Analysis",
                    subheading_style
                )
            )

            table = dataframe_to_table(
                pareto_df
            )

            if table:
                story.append(table)

            chart = create_pareto_chart(
                pareto_df
            )

            if chart:
                story.append(
                    Spacer(
                        1,
                        0.3 * cm
                    )
                )

                story.append(
                    Image(
                        chart,
                        width=16 * cm,
                        height=8.5 * cm
                    )
                )

        top_3 = pbd_data.get(
            "top_3_factors"
        )

        if top_3:

            story.append(
                Paragraph(
                    "2.7 Selected Top 3 Factors",
                    subheading_style
                )
            )

            top_df = pd.DataFrame({
                "Rank": range(
                    1,
                    len(top_3) + 1
                ),
                "Factor": top_3
            })

            table = dataframe_to_table(
                top_df
            )

            if table:
                story.append(table)

    else:

        story.append(
            Paragraph(
                "PBD screening data is not available.",
                normal_style
            )
        )

    story.append(PageBreak())

    # =====================================================
    # 3. RSM Analysis
    # =====================================================

    story.append(
        Paragraph(
            "3. Response Surface Methodology",
            heading_style
        )
    )

    if rsm_analysis:

        summary = rsm_analysis.get(
            "summary"
        )

        if summary is not None:

            story.append(
                Paragraph(
                    "3.1 Regression Statistics",
                    subheading_style
                )
            )

            table = dataframe_to_table(
                summary
            )

            if table:
                story.append(table)
                anova = rsm_analysis.get(
            "anova"
        )

        if anova is not None:

            story.append(
                Paragraph(
                    "3.2 ANOVA",
                    subheading_style
                )
            )

            table = dataframe_to_table(
                anova
            )

            if table:
                story.append(table)

        coefficients = rsm_analysis.get(
            "coefficients"
        )

        if coefficients is not None:

            story.append(
                Paragraph(
                    "3.3 Coefficients",
                    subheading_style
                )
            )

            table = dataframe_to_table(
                coefficients
            )

            if table:
                story.append(table)

    # =====================================================
    # Quadratic Model
    # =====================================================

    story.append(
        Paragraph(
            "3.4 Fitted Quadratic Model",
            subheading_style
        )
    )

    if equation:

        story.append(
            Paragraph(
                equation.replace(
                    "\n",
                    "<br/>"
                ),
                equation_style
            )
        )

    else:

        story.append(
            Paragraph(
                "The fitted model equation "
                "is not available.",
                normal_style
            )
        )

    # =====================================================
    # Experimental Results
    # =====================================================

    story.append(
        Paragraph(
            "3.5 Measured vs Predicted",
            subheading_style
        )
    )

    if experimental_results is not None:

        results_df = experimental_results.copy()

        columns_to_keep = [
            factor
            for factor in factor_names
            if factor in results_df.columns
        ]

        if response_name in results_df.columns:
            columns_to_keep.append(
                response_name
            )

        if "Predicted" in results_df.columns:
            columns_to_keep.append(
                "Predicted"
            )

        results_df = results_df[
            columns_to_keep
        ]

        table = dataframe_to_table(
            results_df
        )

        if table:
            story.append(table)

    else:

        story.append(
            Paragraph(
                "Experimental results are not available.",
                normal_style
            )
        )

    story.append(PageBreak())

    # =====================================================
    # 4. Response Surface & Contour Models
    # =====================================================

    story.append(
        Paragraph(
            "4. Response Surface & Contour Models",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "The third factor is fixed at its center "
            "level (coded value = 0).",
            normal_style
        )
    )

    try:

        model = rsm_analysis["model"]

        factor_info = {}

        for factor in factor_names:

            row = variable_table[
                variable_table["variable_name"]
                == factor
            ]

            if not row.empty:

                row = row.iloc[0]

                factor_info[factor] = {
                    "low": float(
                        row["low_level"]
                    ),
                    "high": float(
                        row["high_level"]
                    )
                }

        pairs = [
            (
                factor_names[0],
                factor_names[1],
                factor_names[2]
            ),
            (
                factor_names[0],
                factor_names[2],
                factor_names[1]
            ),
            (
                factor_names[1],
                factor_names[2],
                factor_names[0]
            )
        ]
        for factor_a, factor_b, fixed_factor in pairs:

            story.append(
                Paragraph(
                    f"{factor_a} × {factor_b}",
                    subheading_style
                )
            )

            story.append(
                Paragraph(
                    "3D Response Surface",
                    normal_style
                )
            )

            surface = create_3d_surface_chart(
                factor_a,
                factor_b,
                fixed_factor,
                factor_names,
                factor_info,
                model,
                response_name
            )

            if surface:

                story.append(
                    Image(
                        surface,
                        width=16 * cm,
                        height=11 * cm
                    )
                )

            story.append(
                Paragraph(
                    "Contour Plot",
                    normal_style
                )
            )

            contour = create_contour_chart(
                factor_a,
                factor_b,
                fixed_factor,
                factor_names,
                factor_info,
                model,
                response_name
            )

            if contour:

                story.append(
                    Image(
                        contour,
                        width=16 * cm,
                        height=9.5 * cm
                    )
                )

            story.append(
                PageBreak()
            )

    except Exception as exc:

        story.append(
            Paragraph(
                "Response surface charts could not be "
                "included in the PDF.",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"Chart generation error: {exc}",
                normal_style
            )
        )

    # =====================================================
    # 5. Maximum Response
    # =====================================================

    story.append(
        Paragraph(
            "5. Maximum Predicted Response",
            heading_style
        )
    )

    if max_predicted is not None:

        story.append(
            Paragraph(
                f"<b>Predicted Response:</b> "
                f"{format_number(max_predicted)}",
                normal_style
            )
        )

        if max_actual is not None:

            max_rows = []

            for factor in factor_names:

                max_rows.append({
                    "Factor": factor,
                    "Actual Value":
                        max_actual[factor],
                    "Coded Value":
                        max_coded[factor]
                        if max_coded
                        else None
                })

            max_df = pd.DataFrame(
                max_rows
            )

            table = dataframe_to_table(
                max_df
            )

            if table:
                story.append(table)

    else:

        story.append(
            Paragraph(
                "Maximum response optimization failed.",
                normal_style
            )
        )

    story.append(
        Spacer(
            1,
            0.7 * cm
        )
    )

    # =====================================================
    # 6. Minimum Response
    # =====================================================

    story.append(
        Paragraph(
            "6. Minimum Predicted Response",
            heading_style
        )
    )

    if min_predicted is not None:

        story.append(
            Paragraph(
                f"<b>Predicted Response:</b> "
                f"{format_number(min_predicted)}",
                normal_style
            )
        )

        if min_actual is not None:

            min_rows = []

            for factor in factor_names:
                min_rows.append({
                    "Factor": factor,
                    "Actual Value":
                        min_actual[factor],
                    "Coded Value":
                        min_coded[factor]
                        if min_coded
                        else None
                })

            min_df = pd.DataFrame(
                min_rows
            )

            table = dataframe_to_table(
                min_df
            )

            if table:
                story.append(table)

    else:

        story.append(
            Paragraph(
                "Minimum response optimization failed.",
                normal_style
            )
        )

    story.append(
        Spacer(
            1,
            0.7 * cm
        )
    )

    # =====================================================
    # 7. Optimization Summary
    # =====================================================

    story.append(
        Paragraph(
            "7. Optimization Summary",
            heading_style
        )
    )

    if (
        max_predicted is not None
        and min_predicted is not None
        and max_actual is not None
        and min_actual is not None
    ):

        summary_data = {
            "Optimization": [
                "Maximum Response",
                "Minimum Response"
            ],
            "Predicted Response": [
                max_predicted,
                min_predicted
            ]
        }

        for factor in factor_names:

            summary_data[factor] = [
                max_actual[factor],
                min_actual[factor]
            ]

        summary_df = pd.DataFrame(
            summary_data
        )

        table = dataframe_to_table(
            summary_df
        )

        if table:
            story.append(table)

    else:

        story.append(
            Paragraph(
                "Optimization summary is not available.",
                normal_style
            )
        )

    story.append(
        Spacer(
            1,
            1 * cm
        )
    )

    story.append(
        Paragraph(
            "Report generated by DOE Optimizer.",
            subtitle_style
        )
    )

    # =====================================================
    # Build PDF
    # =====================================================

    document.build(
        story
    )

    buffer.seek(0)

    return buffer.getvalue()