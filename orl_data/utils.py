from .constants import DIR_ORL_DATA, PATH_BAD_PATIENTS

import logging.config
import numpy as np
import logging
import os


def get_logger(name: str) -> logging.Logger:

    logging.getLogger('numexpr.utils').setLevel(logging.CRITICAL)
    # Silence the 'matplotlib.font_manager' logger
    logging.getLogger('matplotlib.font_manager').setLevel(logging.CRITICAL)

    path_logging_config = os.path.join(os.path.dirname(__file__), 'logging.ini')
    logging.config.fileConfig(path_logging_config)
    logger = logging.getLogger(name)
    return logger


def get_list_bad_patients() -> list[str]:

    if not PATH_BAD_PATIENTS.exists():

        with open(PATH_BAD_PATIENTS, 'w') as file:
            pass
        return []

    with open(PATH_BAD_PATIENTS, 'r') as file:
        list_bad_patients = file.readlines()

    return list_bad_patients


def get_list_patients() -> list[str]:

    list_bad_patients = get_list_bad_patients()

    list_patients = list(set(os.listdir(DIR_ORL_DATA)) - set(list_bad_patients))
    list_patients = [list_patients[i] for i in np.argsort([int(p.strip("AGORL_P")) for p in list_patients])]

    return list_patients


def add_bad_patient(patient: str) -> None:

    list_bad_patients = get_list_bad_patients()

    if patient not in list_bad_patients:

        with open(PATH_BAD_PATIENTS, 'a') as file:
            file.write(patient + '\n')


def remove_bad_patient(patient: str) -> None:

    list_bad_patients = get_list_bad_patients()

    if patient in list_bad_patients:

        list_bad_patients.remove(patient)

        with open(PATH_BAD_PATIENTS, 'w') as file:
            for patient in list_bad_patients:
                file.write(patient + '\n')
