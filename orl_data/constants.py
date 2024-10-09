from pathlib import Path


__all__ = [
    'DIR_ORL_DATA',
    'DIR_WORKSPACE',
    'PATH_BAD_PATIENTS'
]

# patients ORL data Directory :
DIR_ORL_DATA = Path("/media/maichi/SSD-IGR/PredictiveExtension/in vivo patients")

# Workspace directory :
DIR_WORKSPACE = Path("/media/maichi/SSD-IGR/PredictiveExtension/workspace")

# list of bad Patients directory :
PATH_BAD_PATIENTS = Path().cwd() / "bad_patients_in_vivo.txt"
