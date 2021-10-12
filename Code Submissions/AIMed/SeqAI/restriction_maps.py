from SeqProcessing import Slicer, RestrictionDeterminer
import numpy as np
import pandas as pd

data = pd.read_csv('data/seq.csv')

dna_data = data['sequence'].to_list()

ecoR1=[RestrictionDeterminer('GAATTC', i).CreateLabel() for i in dna_data]
Xba1=[RestrictionDeterminer('TCTAGA', i).CreateLabel() for i in dna_data]
Spe1=[RestrictionDeterminer('ACTAGT', i).CreateLabel() for i in dna_data]
Pst1=[RestrictionDeterminer('CTGCAG', i).CreateLabel() for i in dna_data]
Not1=[RestrictionDeterminer('GCGGCCGC', i).CreateLabel() for i in dna_data]
Sap1=[RestrictionDeterminer('GCTCTTC', i).CreateLabel() for i in dna_data]
Bsa1=[RestrictionDeterminer('GGTCTC', i).CreateLabel() for i in dna_data]

train_dataframe = {
    'sequence': dna_data,
    'ecoR1': ecoR1,
    'Xba1': Xba1,
    'Spe1': Spe1,
    'Pst1': Pst1,
    'Not1': Not1,
    'Sap1': Sap1,
    'Bsa1': Bsa1,
}

tr_df = pd.DataFrame(train_dataframe)

tr_df.to_csv('data/classic_restrict.csv')
