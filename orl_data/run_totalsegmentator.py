from .utils import get_logger, add_bad_patient
from .constants import DIR_WORKSPACE


import dicom2nifti
import traceback
import shutil
import time
import os

# Set the logger :
logger = get_logger('run_totalsegmentator')


def convert_dicom_to_nifti(patient):
    logger.debug(f"Convert DICOM CT to NIFTI for patient {patient}...")
    start_time = time.time()

    dir_dicom_ct = DIR_WORKSPACE / patient / "CT_TO_TOTALSEGMENTATOR"

    path_nifti_ct = DIR_WORKSPACE / patient / "temp" / "CT.nii.gz"
    path_nifti_ct.parent.mkdir(exist_ok=True, parents=True)

    # convert the CT directory :
    try:
        dicom2nifti.dicom_series_to_nifti(dir_dicom_ct, path_nifti_ct, reorient_nifti=True)

        time_taken = time.time() - start_time
        logger.debug(f"DICOM CT to NIFTI for patient {patient} converted successfully in {time_taken:.2f} seconds")

    except Exception as e:
        add_bad_patient(patient)
        logger.error(f"Failed to convert DICOM CT to NIFTI for patient {patient} !")
        logger.error(e)
        logger.error(traceback.format_exc())


def run_totalsegmentator_for_total_task(patient):

    from totalsegmentator.python_api import totalsegmentator

    logger.debug(f"Run TotalSegmentator task=total for patient {patient}...")
    start_time = time.time()

    path_nifti_ct = DIR_WORKSPACE / patient / "temp" / "CT.nii.gz"
    if not path_nifti_ct.exists():
        add_bad_patient(patient)
        logger.error(fr"Failed to run TotalSegmentator  task=total for patient {patient} !")
        logger.error("The NIFTI CT file doesn't exist !")
        return

    dir_nifti_total = DIR_WORKSPACE / patient / "NIFTI_FROM_CT"
    dir_nifti_total.mkdir(exist_ok=True, parents=True)

    # run TotalSegmentator :
    try:
        totalsegmentator(path_nifti_ct, dir_nifti_total, task="total", body_seg=False, output_type="nifti")

        time_taken = time.time() - start_time
        logger.debug(f"TotalSegmentator task=total for patient {patient} ran successfully in {time_taken:.2f} seconds")

    except Exception as e:
        add_bad_patient(patient)
        logger.error(fr"Failed to run TotalSegmentator  task=total for patient {patient} !")
        logger.error(e)
        logger.error(traceback.format_exc())


def run_totalsegmentator_for_body_task(patient):

    from totalsegmentator.python_api import totalsegmentator

    logger.debug(f"Run TotalSegmentator task=body for patient {patient}...")
    start_time = time.time()

    path_nifti_ct = DIR_WORKSPACE / patient / "temp" / "CT.nii.gz"
    if not path_nifti_ct.exists():
        add_bad_patient(patient)
        logger.error(fr"Failed to run TotalSegmentator  task=total for patient {patient} !")
        logger.error("The NIFTI CT file doesn't exist !")
        return

    dir_nifti_body = DIR_WORKSPACE / patient / "temp" / "body"
    dir_nifti_body.mkdir(exist_ok=True, parents=True)

    # run TotalSegmentator :
    try:
        totalsegmentator(path_nifti_ct, dir_nifti_body, task="body", body_seg=False, output_type="nifti")

        # Copy the body segmentations to the workspace :
        for file in os.listdir(dir_nifti_body):
            shutil.copy(dir_nifti_body / file, DIR_WORKSPACE / patient / "NIFTI_FROM_CT" / file)

        time_taken = time.time() - start_time
        logger.debug(f"TotalSegmentator task=body for patient {patient} ran successfully in {time_taken:.2f} seconds")

    except Exception as e:
        add_bad_patient(patient)
        logger.error(fr"Failed to run TotalSegmentator  task=body for patient {patient} !")
        logger.error(e)
        logger.error(traceback.format_exc())
