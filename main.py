import pandas as pd

class File():
    def __init__(self, filepath):
        self.filepath = filepath

    def readfile(self):
        try:
            print(pd.read_excel(self.url))
        except:
            raise ImportError('File type not in .xlsx format')
        

File(r'C:\Users\AdamPetrone\OneDrive - Repare Therapeutics\Desktop')