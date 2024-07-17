from pathlib import Path


__all__ = [
    'DIR_ORL_DATA',
    'DIR_WORKSPACE',
    'PATH_BAD_PATIENTS'
]

# patients ORL data Directory :
DIR_ORL_DATA = Path("/media/maichi/T7/ORL Dataset Lyon")

# Workspace directory :
DIR_WORKSPACE = Path("/media/maichi/T7/workspace")

# list of bad Patients directory :
PATH_BAD_PATIENTS = Path().cwd() / "bad_patients.txt"
