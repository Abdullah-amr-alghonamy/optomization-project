import numpy as np
import pandas as pd
from pyDOE3 import pbdesign


def generate_pbd(number_of_factors):

    # Validate input    
    if number_of_factors < 1:
        raise ValueError(
            "Number of factors must be at least 1."
        )
    # Generate PBD
    design = pbdesign(number_of_factors)

    design = np.asarray(design, dtype=int)

    
    # Validate design
    
    if not np.all(np.isin(design, [-1, 1])):
        raise ValueError(
            "PBD contains values other than -1 and +1."
        )

    if design.shape[1] != number_of_factors:
        raise ValueError(
            "Number of factors does not match."
        )

    
    # Make the last run all -1
    
    reference_row = design[0]

    design = design * (-reference_row)

    # Move the reference row to the end
    design = np.vstack([
        design[1:],
        design[0]
    ])

    
    # Factor names
    
    factor_names = [
        f"X{i + 1}"
        for i in range(number_of_factors)
    ]

    
    # DataFrame
    
    design_df = pd.DataFrame(
        design,
        columns=factor_names
    )

    design_df.insert(
        0,
        "Run",
        range(1, len(design_df) + 1)
    )

    return design_df