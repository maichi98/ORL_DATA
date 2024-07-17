from .utils import get_logger, add_bad_patient
from .constants import DIR_WORKSPACE

import pydicom as dcm
import traceback
import shutil
import time


# Set the logger :
logger = get_logger('separate_patient_data')


# Get the primary RTDOSE :
def get_primary_rtodse(patient):
    dir_rtdose = DIR_WORKSPACE / patient / "RD"
    assert dir_rtdose.exists(), fr"Patient {patient} RD Folder doesn't exist !"

    # Get the primary RTDOSE :
    list_primary_rtdose = [path_rtdose
                           for path_rtdose in dir_rtdose.glob("*.dcm")
                           if dcm.dcmread(str(path_rtdose)).get("DoseSummationType") == "PLAN"]

    if len(list_primary_rtdose) != 1:
        raise ValueError(fr"{len(list_primary_rtdose)} primary RTDOSE found for patient {patient} !")

    return list_primary_rtdose[0]


# Get the corresponding RTPLAN from an RTDOSE :
def get_corresponding_rtplan(path_rtdose, patient):

    # Read the RTDOSE :
    rtdose = dcm.dcmread(str(path_rtdose))

    # Get the Referenced RT Plan Sequence (300C,0002),
    # this sequence references the RT Plan that this RT Dose is related to.
    referenced_rtplan_sequence = rtdose.get("ReferencedRTPlanSequence", None)
    if referenced_rtplan_sequence is None:
        raise ValueError(fr"RTDOSE {rtdose.SOPInstanceUID} doesn't reference any RTPLAN !")
    referenced_rtplan_sequence = referenced_rtplan_sequence[0].get("ReferencedSOPInstanceUID")

    # Get the corresponding RTPLAN :
    dir_rtplan = DIR_WORKSPACE / patient / "RP"
    assert dir_rtplan.exists(), fr"Patient {patient} RP Folder doesn't exist !"

    # Get the list of RTPLANs that correspond to the RTDOSE :
    list_rtplans = [path_rtplan
                    for path_rtplan in dir_rtplan.glob("*.dcm")
                    if dcm.dcmread(str(path_rtplan)).get('SOPInstanceUID') == referenced_rtplan_sequence]

    if len(list_rtplans) != 1:
        raise ValueError(fr"{len(list_rtplans)} corresponding RTPLAN found for RTDOSE {rtdose.SOPInstanceUID} !")

    return list_rtplans[0]


# Get the corresponding RTSTRUCT from an RTPLAN :
def get_corresponding_rtstruct(path_rtplan, patient):
    # Read the RTPLAN :
    rtplan = dcm.dcmread(str(path_rtplan))

    # Get the Referenced Structure Set Sequence (300C,0060),
    # this sequence references the RT Structure Set that this RT Plan is related to.
    referenced_rtstruct_sequence = rtplan.get("ReferencedStructureSetSequence", None)
    if referenced_rtstruct_sequence is None:
        raise ValueError(fr"RTPLAN {rtplan.SOPInstanceUID} doesn't reference any RTSTRUCT !")

    referenced_rtstruct_sequence = referenced_rtstruct_sequence[0].get("ReferencedSOPInstanceUID")

    # Get the corresponding RTSTRUCT :
    dir_rtstruct = DIR_WORKSPACE / patient / "RS"
    assert dir_rtstruct.exists(), fr"Patient {patient} RS Folder doesn't exist !"

    # Get the list of RTSTRUCTs that correspond to the RTPLAN :
    list_rtstructs = [path_rtstruct
                      for path_rtstruct in dir_rtstruct.glob("*.dcm")
                      if dcm.dcmread(str(path_rtstruct)).get('SOPInstanceUID') == referenced_rtstruct_sequence]

    if len(list_rtstructs) != 1:
        raise ValueError(fr"{len(list_rtstructs)} corresponding RTSTRUCT found for RTPLAN {rtplan.SOPInstanceUID} !")

    return list_rtstructs[0]


# Get the corresponding CT from an RTSTRUCT :
def get_corresponding_ct(path_rtstruct, patient):
    # Read the RTSTRUCT :
    rtstruct = dcm.dcmread(str(path_rtstruct))

    # Get the SeriesInstanceUID of the corresponding CT :
    frame_of_reference_sequence = rtstruct.get("ReferencedFrameOfReferenceSequence", None)
    if frame_of_reference_sequence is None:
        raise ValueError(
            fr"RTSTRUCT {rtstruct.SOPInstanceUID} doesn't reference any CT ! Issue at Frame of Reference !")

    frame_of_reference_sequence = frame_of_reference_sequence[0].get("RTReferencedStudySequence", None)
    if frame_of_reference_sequence is None:
        raise ValueError(fr"RTSTRUCT {rtstruct.SOPInstanceUID} doesn't reference any CT ! Issue at Study !")

    series_sequence = frame_of_reference_sequence[0].get("RTReferencedSeriesSequence", None)
    if series_sequence is None:
        raise ValueError(fr"RTSTRUCT {rtstruct.SOPInstanceUID} doesn't reference any CT ! Issue at Series !")

    series_instance_uid = series_sequence[0].get("SeriesInstanceUID")

    # Get the corresponding CT :
    dir_ct = DIR_WORKSPACE / patient / "CT" / series_instance_uid
    assert dir_ct.exists(), fr"Patient {patient} CT Folder doesn't exist !"

    return dir_ct


def create_ct_to_totalsegmentator(patient):

    logger.debug(f"Creating CT_TO_TOTALSEGMENTATOR for patient {patient}...")
    start_time = time.time()

    # Get the primary RTDOSE :
    try:
        # Get the primary RTDOSE :
        path_rtdose = get_primary_rtodse(patient)

        # Get the corresponding RTPLAN :
        path_rtplan = get_corresponding_rtplan(path_rtdose, patient)

        # Get the corresponding RTSTRUCT :
        path_rtstruct = get_corresponding_rtstruct(path_rtplan, patient)

        # Get the corresponding CT :
        dir_ct = get_corresponding_ct(path_rtstruct, patient)

        # Move the CT to the TotalSegmentator folder :
        dir_totalsegmentator = DIR_WORKSPACE / patient / "CT_TO_TOTALSEGMENTATOR"
        if dir_totalsegmentator.exists():
            shutil.rmtree(dir_totalsegmentator)

        shutil.copytree(dir_ct, dir_totalsegmentator)

        time_taken = time.time() - start_time
        logger.debug(f"CT_TO_TOTALSEGMENTATOR for patient {patient} created successfully in {time_taken:.2f} seconds")

    except Exception as e:
        add_bad_patient(patient)
        logger.error(f"Failed to create CT_TO_TOTALSEGMENTATOR for patient {patient} !")
        logger.error(e)
        logger.error(traceback.format_exc())
