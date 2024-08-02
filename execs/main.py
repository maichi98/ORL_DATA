from orl_data import run_totalsegmentator_for_total_task
from orl_data import run_totalsegmentator_for_body_task
from orl_data import generate_patient_characteristics
from orl_data import create_ct_to_totalsegmentator
from orl_data import convert_dicom_to_nifti
from orl_data import separate_patient_data
from orl_data import generate_contours
from orl_data import needed_junctions
from orl_data import filter_phantoms
from orl_data import utils


from tqdm import tqdm
import time


def main():

    # Set the Logger :
    logger = utils.get_logger(__name__)

    # get the list of patients :
    list_patients = utils.get_list_patients()

    for patient in tqdm(list_patients):

        logger.debug(f"{'-' * 35} iterating over Patient {patient.ljust(10)}{'-' * 35}")
        start_time = time.time()

        # # Separate the patient DICOM files into CET, PET, RTSTRUCT, RTPLAN and  RTDOSE directories :
        # separate_patient_data(patient)
        #
        # # Create CT_TO_TOTALSEGMENTATOR directory :
        # create_ct_to_totalsegmentator(patient)
        #
        # # Convert DICOM CT to NIFTI :
        # convert_dicom_to_nifti(patient)
        #
        # # run TotalSegmentator for total task :
        # run_totalsegmentator_for_total_task(patient)
        #
        # # run TotalSegmentator for body task :
        # run_totalsegmentator_for_body_task(patient)
        #
        # # Create the patient characteristics :
        # generate_patient_characteristics(patient)
        #
        # # Create the contours :
        # generate_contours(patient)
        #
        # # Filter the phantoms  :
        # filter_phantoms(patient)

        # Needed junctions :
        needed_junctions(patient)

        time_taken = (time.time() - start_time) / 60
        logger.debug(f"Time taken for patient {patient} : {time_taken:.2f} minutes.")
        logger.debug('-' * 104)


if __name__ == '__main__':
    main()
