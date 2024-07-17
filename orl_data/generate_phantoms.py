from .utils import get_logger, add_bad_patient
from .constants import DIR_WORKSPACE

import pydicom as dcm
import traceback
import shutil
import time


# Set the logger :
logger = get_logger('generate_phantoms')


def generate_patient_characteristics(patient: str):

    from phandose.patient import get_patient_characteristics

    logger.debug(f"Create patient characteristics for patient {patient}...")
    start_time = time.time()

    dir_patient = DIR_WORKSPACE / patient
    dir_ct = dir_patient / "CT_TO_TOTALSEGMENTATOR"

    try:
        df_patient_characteristics = get_patient_characteristics(dir_ct)

        path_patient_characteristics = dir_patient / "XYZ" / "patient_characteristics.csv"
        path_patient_characteristics.parent.mkdir(exist_ok=True, parents=True)
        df_patient_characteristics.to_csv(path_patient_characteristics, sep=";", index=False)

        time_taken = time.time() - start_time
        logger.debug(f"Patient characteristics for patient {patient} created successfully in {time_taken:.2f} seconds")

    except Exception as e:
        add_bad_patient(patient)
        logger.error(f"Failed to create patient characteristics for patient {patient} !")
        logger.error(e)
        logger.error(traceback.format_exc())


def generate_contours(patient: str):

    from phandose.patient import convert_nifti_segmentation_directory_to_contours_dataframe

    logger.debug(f"Convert segmentation to XYZ... for patient {patient}")
    start_time = time.time()

    dir_patient = DIR_WORKSPACE / patient
    dir_nifti_segmentations = dir_patient / "NIFTI_FROM_CT"

    if not dir_nifti_segmentations.exists() or not list(dir_nifti_segmentations.glob("*.nii.gz")):
        add_bad_patient(patient)
        logger.error(f"Failed to create contours for patient {patient} !")
        logger.error(f"No NIFTI segmentation found for patient {patient} !")
        return

    try:
        df_contours = convert_nifti_segmentation_directory_to_contours_dataframe(dir_nifti_segmentations)

        path_contours = dir_patient / "XYZ" / "contours.csv"
        path_contours.parent.mkdir(exist_ok=True, parents=True)
        df_contours.to_csv(path_contours, sep=";", index=False)

        time_taken = time.time() - start_time
        logger.debug(f"Segmentation to XYZ for patient {patient} created successfully in {time_taken:.2f} seconds")

    except Exception as e:
        add_bad_patient(patient)
        logger.error(f"Failed to create contours for patient {patient} !")
        logger.error(e)
