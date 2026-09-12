# 🧬 Experimental Design & Optimization Platform

A Python-based platform for Design of Experiments (DoE), statistical analysis, factor screening, and experimental optimization.

The platform provides a structured workflow for researchers and experimental scientists to investigate how multiple experimental factors affect a target response, identify the most influential factors, and determine experimental conditions that lead to an optimized outcome.

---

# 🔬 Project Overview

Experimental processes are often influenced by many variables at the same time.

For example, in a biological or chemical process, the final outcome may depend on factors such as:

- Temperature
- pH
- Incubation time
- Nutrient concentrations
- Inoculum size
- Agitation speed
- Carbon and nitrogen sources
- And many other experimental parameters

Studying these factors individually can require a large number of experiments and may not provide an efficient understanding of the overall system.

This project addresses this challenge by providing a systematic, statistical, and data-driven approach to experimental design and optimization.

Instead of changing one factor at a time, the platform uses statistically designed experiments to investigate multiple factors simultaneously, determine which variables have the greatest influence on the target response, and then focus the optimization process on the most important factors.

---

## 🎯 Complete Workflow

The platform follows a sequential experimental optimization workflow:

                    Experimental Problem
                            │
                            ▼
                  Define Experimental
                       Factors
                            │
                            ▼
                   Set Factor Levels
                            │
                            ▼
                 Design of Experiments
                            │
                            ▼
                  Conduct Experiments
                            │
                            ▼
                   Measure Response
                            │
                            ▼
                  Statistical Analysis
                            │
                            ▼
                 Factor Screening &
                      Ranking
                            │
                            ▼
                 Select Important
                       Factors
                            │
                            ▼
                 Optimization Design
                            │
                            ▼
                 Response Modeling
                            │
                            ▼
                 Find Optimal Conditions
                            │
                            ▼
                Experimental Validation

The main idea is to progressively reduce a potentially large experimental search space into a smaller and more manageable optimization problem.

---

## 🧪 Experimental Setup

The process starts by defining the experimental factors that may influence the target response.

Each factor can be assigned appropriate experimental levels or a defined operating range.

For example:

Factor| Low Level| High Level
Temperature| 25| 35
pH| 5| 8
Agitation Speed| 100| 200
Incubation Time| 24| 72

The platform uses these values to construct the experimental design.

This allows the same methodology to be applied to different experimental systems and scientific applications.

---

## 📐 Design of Experiments

The platform uses Design of Experiments (DoE) methodologies to determine efficient combinations of experimental factors.

A major component of the platform is the Plackett–Burman Design (PBD).

Plackett–Burman Design is particularly useful during the screening stage, when many factors may potentially influence the response.

Instead of testing every possible combination, PBD generates a statistically structured set of experimental runs that allows multiple factors to be investigated simultaneously.

Conceptually:

Multiple Experimental Factors
                         │
                         ▼
               Plackett–Burman Design
                         │
                         ▼
                 Experimental Runs
                         │
                         ▼
                  Measured Response

This makes the initial screening process significantly more efficient than testing all possible combinations.

---

## 📊 Experimental Response

After carrying out the designed experiments, the measured response from each run is entered into the platform.

The response represents the experimental outcome that the researcher wants to understand and eventually optimize.

Depending on the application, the response could represent:

- Product concentration
- Yield
- Enzyme activity
- Biomass
- Productivity
- Conversion
- Growth rate
- Reaction efficiency
- Or any other quantitative experimental measurement

For example, in a biological production experiment, the response could be the final product concentration obtained from each experimental run.

The response is then analyzed together with the corresponding factor levels.

---

## 📈 Statistical Analysis

The platform applies statistical modeling to determine how the experimental factors influence the measured response.

A simplified linear model can be represented as:

Y = β₀ + β₁X₁ + β₂X₂ + ... + βₙXₙ + ε

Where:

- "Y" = measured experimental response
- "X₁ ... Xₙ" = experimental factors
- "β₀" = model intercept
- "β₁ ... βₙ" = estimated factor effects
- "ε" = experimental error

The statistical analysis helps quantify the contribution of each factor and determine which variables are most relevant to the response.

---

 ## 🔎 Factor Screening & Ranking

One of the main objectives of the platform is to convert experimental results into an interpretable ranking of the investigated factors.

The analysis can provide statistical information including:

- Estimated factor effects
- Regression coefficients
- p-values
- Confidence intervals
- R²
- Adjusted R²
- Standard error
- ANOVA
- F-statistic
- Significance F
- Factor ranking

The results allow researchers to distinguish between factors with relatively strong effects and factors with relatively small effects.

For example:

Factor A ─────────────────► Strong Influence
Factor B ────────────────► Moderate Influence
Factor C ───────────────► Weak Influence
Factor D ──────────────► Weak Influence
Factor E ─────────────► Strong Influence

This information provides the basis for selecting the variables that should receive further experimental attention.

---

# ⚙️ From Screening to Optimization

Screening and optimization have different objectives.

Screening asks:

«Which factors have the greatest influence on the response?»

Optimization asks:

«What combination of the important factors produces the best response?»

After the influential factors have been identified, the experimental problem can be reduced from a large number of variables to a smaller set of important ones.

The optimization stage can then investigate these factors in greater detail.

Many Experimental Factors
          │
          ▼
   Screening Design
          │
          ▼
 Important Factors
          │
          ▼
 Optimization Design
          │
          ▼
 Response Modeling
          │
          ▼
 Optimal Conditions

This sequential strategy reduces unnecessary experimentation and concentrates resources on the variables that are most likely to affect the desired outcome.

---

🧠 Optimization Strategy

The platform is designed around a sequential optimization philosophy.

1. Screening

Investigate a large number of potential factors and identify the variables that have the strongest influence on the response.

2. Factor Selection

Use the statistical results to determine which factors should be carried forward to the optimization stage.

3. Optimization Design

Generate a more detailed experimental design around the selected factors.

4. Response Modeling

Develop a statistical model describing the relationship between the important factors and the response.

5. Optimization

Search the experimental space to identify conditions associated with the desired response.

6. Validation

Perform an experiment using the predicted optimal conditions and compare the experimental result with the model prediction.

---

# 📋 Platform Capabilities

The platform is designed to support a complete experimental optimization workflow.

Experimental Design

- Define multiple experimental factors
- Specify factor levels and experimental ranges
- Generate structured experimental designs
- Create efficient experimental runs
- Reduce the number of experiments required during screening

Factor Screening

- Perform Plackett–Burman screening
- Investigate multiple factors simultaneously
- Estimate factor effects
- Identify potentially influential variables
- Rank factors based on their statistical contribution

Statistical Analysis

- Perform OLS regression
- Calculate regression coefficients
- Calculate factor effects
- Calculate p-values
- Calculate confidence intervals
- Perform ANOVA
- Calculate R² and adjusted R²
- Calculate model error statistics
- Evaluate F-statistics and statistical significance

Optimization

- Select important factors
- Build optimization-focused experimental designs
- Model factor-response relationships
- Search the experimental space
- Determine predicted optimal conditions
- Support experimental validation

---

## 🖥️ Interactive Application

The platform provides an interactive interface built with Streamlit, allowing users to perform the workflow through a graphical interface rather than interacting directly with the underlying statistical code.

The application is organized around the major stages of the experimental process:

Setup
  │
  ▼
Screening
  │
  ▼
Experimental Runs
  │
  ▼
Response Data
  │
  ▼
PBD Analysis
  │
  ▼
Factor Selection
  │
  ▼
Optimization

This structure is intended to make experimental design and statistical optimization easier to use for researchers who may not want to manually implement the underlying mathematical procedures.

---

# 🏗️ Project Structure

optomization-project/
│
├── calculations/
│   ├── plackett_burman.py
│   ├── pbd_analysis_ca.py
│   └── ...
│
├── pages/
│   ├── set_up.py
│   ├── screening.py
│   ├── pbd_analysis.py
│   └── ...
│
├── drafts/
│
├── app.py
│
├── requirements.txt
│
└── README.md

"calculations/"

Contains the mathematical, statistical, and experimental-design logic of the platform.

"pages/"

Contains the different stages of the interactive Streamlit application.

"app.py"

The main entry point of the application.

---

# 🛠️ Technology Stack

Technology| Purpose
Python| Core programming language
Pandas| Data manipulation and analysis
NumPy| Numerical computation
Statsmodels| Statistical modeling and regression
PyDOE3| Design of Experiments
Streamlit| Interactive web application

---

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/Abdullah-amr-alghonamy/optomization-project.git
cd optomization-project

2. Install Dependencies

pip install -r requirements.txt

3. Run the Application

streamlit run app.py

The application will open through the Streamlit interface in your browser.

---

# 🌱 Example Application

Consider an experimental process containing 14 potential factors that may affect a target response.

Testing every possible combination of these factors would require a very large number of experiments.

The platform approaches the problem systematically:

14 Potential Factors
        │
        ▼
Plackett–Burman Screening
        │
        ▼
Experimental Runs
        │
        ▼
Measured Response
        │
        ▼
Statistical Analysis
        │
        ▼
Factor Ranking
        │
        ▼
Important Factors
        │
        ▼
Optimization
        │
        ▼
Predicted Optimal Conditions
        │
        ▼
Experimental Validation

This approach transforms a high-dimensional experimental problem into a more focused optimization problem.

---

# 📌 Why Design of Experiments?

A traditional One-Factor-at-a-Time (OFAT) approach changes one variable while keeping the other variables fixed.

Although this method is straightforward, it can become inefficient when many factors are involved.

A Design of Experiments approach provides a more systematic framework for investigating multiple variables within the same experimental study.

The objective is not simply to perform fewer experiments, but to obtain more useful information from each experiment.

---

# 🔮 Project Vision

The ultimate vision of this project is to provide a unified platform for data-driven experimental design and optimization.

The platform brings together:

Experimental Design
        +
Statistical Analysis
        +
Factor Screening
        +
Optimization
        +
Experimental Validation

into a single workflow.

The goal is to help researchers move from a large and complex experimental search space toward a scientifically informed set of optimal experimental conditions.

---

# 👨‍💻 Author

Abdullah Amr Alghonamy

Built with Python, statistics, and Design of Experiments to develop a practical platform for experimental screening and optimization.