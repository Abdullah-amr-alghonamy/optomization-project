import numpy as np
import pandas as pd
from pyDOE3 import bbdesign


def generate_bbd(factor_names, center_points=3):

    
    # Validate input
    

    if len(factor_names) != 3:
        raise ValueError(
            "Box-Behnken Design currently requires exactly 3 factors."
        )

    if center_points < 1:
        raise ValueError(
            "Number of center points must be at least 1."
        )

    
    # Generate BBD
    

    design = bbdesign(
        3,
        center=center_points
    )

    design = np.asarray(design, dtype=int)

    
    # Validate design
    

    if not np.all(np.isin(design, [-1, 0, 1])):
        raise ValueError(
            "BBD contains values other than -1, 0, and +1."
        )

    if design.shape[1] != 3:
        raise ValueError(
            "BBD must contain exactly 3 factors."
        )

    
    # Create DataFrame
    

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