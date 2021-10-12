import pandas as pd
z=0
data = pd.read_csv('seq.csv')
dna=data['sequence'].to_list()
label=data['label'].to_list()
for i, x in zip(label, range(len(label))):
    if len(i)!=500:
        label[x]=i[:500]

for i in label:
    if len(i)!=500:
        z+=1
print(z)

train_dataframe = {
    'sequence': dna,
    'label': label
}

tr_df = pd.DataFrame(train_dataframe)

tr_df.to_csv('seq1.csv')



