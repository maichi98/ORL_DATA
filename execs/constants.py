from pathlib import Path
import numpy as np
import os

__all__ = [
    'DIR_ORL_DATA',
    'DIR_WORKSPACE',
    'LIST_PATIENTS'
]

# patients ORL data Directory :
DIR_ORL_DATA = Path("/media/maichi/T7/ORL Dataset Lyon")

# Workspace directory :
DIR_WORKSPACE = Path("/media/maichi/T7/workspace")

# Patients list :
LIST_PATIENTS = os.listdir(DIR_ORL_DATA)
LIST_PATIENTS = [LIST_PATIENTS[i] for i in np.argsort([int(p.strip("AGORL_P")) for p in LIST_PATIENTS])]
