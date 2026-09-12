from calculations.box_behnken import generate_bbd


factors = [
    "Glucose",
    "FeSO4.7H2O",
    "pH"
]

design = generate_bbd(factors)

print(design)