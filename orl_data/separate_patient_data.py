from .constants import DIR_ORL_DATA, DIR_WORKSPACE
from .utils import get_logger, add_bad_patient

import pydicom as dcm
import traceback
import shutil
import time


# Set the logger :
logger = get_logger('separate_patient_data')


# Get modality from dicom file :
def get_modality(dicom_slice):

    dict_modalities = {"RTDOSE": "RD", "RTPLAN": "RP", "RTSTRUCT": "RS"}
    modality = dicom_slice.Modality.upper()

    if modality in dict_modalities.keys():
        return dict_modalities[modality]

    if modality == "CT":

        code_meaning = dicom_slice.get('ProcedureCodeSequence')[0].get('CodeMeaning')

        if 'TDM' in code_meaning:
            return 'CT'
        elif 'TEP' or 'PET' in code_meaning:
            return 'PET'
        else:
            raise ValueError(fr"Not yet determined how to interpret {code_meaning} ! ")

    raise ValueError(fr"Not yet determined how to interpret {modality} !")


# Get map paths for all DICOM files in a patient's directory:
def get_mapped_paths(patient):

    dir_patient_data = DIR_ORL_DATA / patient
    assert dir_patient_data.exists(), fr"Patient {patient} Data Folder doesn't exist !"

    # Initialize the mapping directory :
    dict_mapping = {}

    for path_src_dicom in dir_patient_data.glob("*.dcm"):

        # read DICOM file :
        dicom_slice = dcm.dcmread(str(path_src_dicom))

        # Get the slice's modality :
        modality = get_modality(dicom_slice)

        if modality in ['CT', 'PET']:
            path_dst_dicom = DIR_WORKSPACE / patient / modality / dicom_slice.SeriesInstanceUID / path_src_dicom.name
        else:
            path_dst_dicom = DIR_WORKSPACE / patient / modality / path_src_dicom.name

        dict_mapping[path_src_dicom] = path_dst_dicom

    return dict_mapping


def separate_patient_data(patient):

    logger.debug(f"Separating patient DICOM files for patient {patient}...")
    start_time = time.time()

    try:
        # Get the mapping paths for all DICOM files in the patient's directory :
        dict_mapping = get_mapped_paths(patient)

        # Copy DICOM files to the workspace :
        for path_src_dicom, path_dst_dicom in dict_mapping.items():
            path_dst_dicom.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy(path_src_dicom, path_dst_dicom)

        time_taken = time.time() - start_time
        logger.debug(f"Patient DICOM files for patient {patient} separated successfully in {time_taken:.2f} seconds")

    except Exception as e:

        add_bad_patient(patient)
        logger.error(f"Failed to separate patient DICOM files for patient {patient} !")
        logger.error(traceback.format_exc())
        logger.error(e)
