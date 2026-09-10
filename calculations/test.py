from calculations.draft import load_draft
from calculations.pbd_analysis_ca import analyze_pbd
import pandas as pd


# Load saved experiment
data = load_draft("1ex")


# Convert saved data to DataFrame
df = pd.DataFrame(data["design"])


# Get factor names
factor_names = [
    item["variable_name"]
    for item in data["variable_table"]
]


# Add responses
df[data["response_name"]] = data["responses"]


# Run PBD analysis
analysis = analyze_pbd(
    df,
    data["response_name"],
    factor_names
)


print("\nSUMMARY")
print(analysis["summary"])

print("\nANOVA")
print(analysis["anova"])

print("\nCOEFFICIENTS")
print(analysis["coefficients"])

print("\nEFECTS")
print(analysis['effects'])