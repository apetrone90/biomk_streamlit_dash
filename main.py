import pandas as pd
import sqlite3
import os
import glob
from Class_Definitions.py import DataHandler
from Function_Rep.py import find_most_recent_csv_file


# Example usage #
fp1 = r'C:\Users\AdamPetrone\Repare Therapeutics\Repare-R&D - Clinical-Team\RP-6306-03 MINOTAUR\RP-6306-03_Patient Status Update\RP6306-03 Patient Tracker.xlsx'
fp2 = r'C:\Users\AdamPetrone\Repare Therapeutics\Repare-R&D - Clinical-Team\Biomarkers and Diagnostics Team\RP-6306\RP-6306-03\PD Data Summaries\Archived Data\RP-6306-03 PKPD data summary.xlsx'
fp3 = r'C:\Users\AdamPetrone\Repare Therapeutics\Repare-R&D - ClinicalBioinformatics\shared\RP6306\RP6306-03\ctDNA\processing\Tempus\reports'

# Now we will call the function and print the result
# Please replace 'directory_path' with the actual directory path you want to search
fp3 = most_recent_csv = find_most_recent_csv_file(fp3)  # Example directory path

data_file_path_list = [fp1,fp2,fp3]

#########################################################################
for fp in data_file_path_list:
    data_file_path = fp
    db_name = r'C:\Users\AdamPetrone\Repare Therapeutics\Repare Collab - Manchester IND\Biomarkers and Diagnostics\RP-6306-03 MINOTAUR\MINOTAUR Data Updates\local_data_storage.db'

    data_handler = DataHandler(db_name)
    data_handler.create_database()
    data_handler.read_and_write_data(data_file_path)