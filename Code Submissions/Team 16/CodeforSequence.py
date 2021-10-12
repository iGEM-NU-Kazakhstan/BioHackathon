from tkinter import *
from tkinter import filedialog
from os import startfile
from PIL import ImageTk, Image
from Bio.Seq import *
from Bio.Restriction import *
from Bio.Data import CodonTable
from tkinter.filedialog import asksaveasfile
from Bio import SeqIO

def substitute(positions, codon_dict, sequence, acid_names):
    sequence = MutableSeq(sequence)
    for position in positions:
        current_codon = sequence[position[0] * 3:3 * position[0] + 3]
        for i in current_codon:
            if i == 'T':
                current_codon[current_codon.index(i)] = current_codon[current_codon.index(i)].replace('T', 'U')

        for keys, values in codon_dict.items():
            count = 0
            if current_codon[0] != keys[0]:
                count += 1
            if current_codon[1] != keys[1]:
                count += 1
            if current_codon[2] != keys[2]:
                count += 1
            if current_codon != keys and acid_names[positions.index(position)] == values and count == 1:
                sequence[position[0] * 3:3 * position[0] + 3] = keys

    for base in sequence:
        if base == 'U':
            sequence[sequence.index(base)] = sequence[sequence.index(base)].replace('U', 'T')

    return sequence

def mapping(input_seq, restriction_sites, restriction_batch, protein, codons):
    restriction_indexes = []
    acids = []
    indexes = []
    overlapping_pos = []
    overlapping_acids = []
    overlapping_codons = []
    for j in range(0, len(restriction_sites)):
        if restriction_batch.get(restriction_sites[j]).site in input_seq:
            temp = []

            for i in range(input_seq.index(restriction_batch.get(restriction_sites[j]).site),
                           input_seq.index(restriction_batch.get(restriction_sites[j]).site) + len(
                               restriction_batch.get(restriction_sites[j]).site)):

                temp.append(i)
            restriction_indexes.append(temp)

    # this part creates a list of index positions inside the sequence which showcases the limits of the restriction
    # sites.

    for i in protein:
        acids.append(i)

    for i in range(0, len(input_seq)):
        if i % 3 == 0:
            aa = [i, i + 1, i + 2]
            indexes.append(aa)

    for h in restriction_indexes:
        temp = []
        for i in h:
            for j in indexes:
                for k in j:
                    if i == k and indexes.index(j) not in temp:

                        temp.append(indexes.index(j))
        overlapping_pos.append(temp)

    # this part is IMPORTANT! As it creates a list of positions of aminoacids which anyhow overlaps with the restriction
    # sites in the aminoacid sequence, therefore aminoacids in these positions are to be changed (their codons,
    # not the acids themselves)

    for i in overlapping_pos:
        overlapping_acids.append(acids[i[0]])

    # THIS PART CREATES A LIST OF OVERLAPPING AMINOACID NAMES (THEIR FIRST LETTERS)

    for i in overlapping_acids:
        for k, v in codons.items():
            if v == i:
                overlapping_codons.append(k)

    # THIS IS THE LIST OF CODONS FROM THE DICTIONARY WHICH REPRESENT OVERLAPPING AMINOACIDS. IN OTHER WORDS, IF WE HAVE
    # 'X' AMINOACID WHICH OVERLAPS WITH RESTRICTION SITE, THIS LIST WOULD CONTAIN ALL OF THE POSSIBLE CODON COMBINATIONS
    # FOR THIS AMINOACID
    for i in range(0, len(overlapping_codons)):
        overlapping_codons[i] = overlapping_codons[i].replace('U', 'T')
    return overlapping_pos, overlapping_acids

root = Tk()
root.title("Sequence Analysis. High Steaks")
root.iconbitmap('Screenshot_7.ico')
root.resizable(False, False)
root.geometry('650x810')
bg = ImageTk.PhotoImage(file = "bg1.png")
img = Label(root, image = bg)
img.place(x=-500, y=-500)




myLabel = Label(root, text = "Please enter your sequence of interest:", bg = "#333333", fg = "#FFFFFF", font=("Futura, 14"))
myLabel.pack()
# scrollbar = Scrollbar(orient="vertical")
e = Text(width=60, height = 10, bg = "#333333", fg = "#FFFFFF", relief = FLAT)
e.pack()
def codingseq(seq):

    if len(seq) % 3 == 2:
        seq = seq[0:len(seq)-2]
    elif len(seq) % 3 == 1:
        seq = seq[0:len(seq)-1]

    #print(len(seq))
    protein_raw = Seq(seq).translate()
   # print(protein_raw)
    str = protein_raw
    Met = []
    Stopp = []

    for i in range(len(str)):
        if str[i] == "M":
            Met.append(i)
        elif str[i] == "*":
            Stopp.append(i)
    # print(Met)
    # print(Stopp)
    last = 0
    result = []

    for i in Met:
        curr = Stopp[0]
        if i < curr and i > last:
            temp = str[i:curr]
            print(temp)
            result.append([i, curr])
            last = curr
            Stopp.remove(curr)
            Met.remove(i)
    # print(result)

    control = ""
    for i in result:
        x = i[0] * 3 - 1
        y = i[1] * 3 - 1
        control += seq[x:y]

    return Seq(control)

def openFile():
    openFile.tfile = filedialog.askopenfilename(initialdir = "/Downloads", title = "Select FASTA file", filetypes = (("fasta files", "*.fna"), ("text files", "*.txt"), ("all files", "*.*")))

    # tfile = open(tfile, 'r')
    #e.insert(END, openFile.tfile)
    openFile.dataa = open(str(openFile.tfile)).read()
    e.insert(END, openFile.dataa)
    # print(openFile.tfile)
    # print("openFile.tfile")
    # print(openFile.dataa[:50])
    # myLabel = Label(root, text = "")
    # myLabel.pack()
    # tfile.close()
    #return dataa


def text_save():
    files = [ ('Text Document', '*.txt'), ('All Files', '*.*')]
    file = asksaveasfile(filetypes=files, defaultextension=".txt")
    file.write(str(myClick.final_sequence))
    file.close()

def myClick():
    # myLabel = Label(root, text = e.get(1.0, END))
    # myLabel.pack()
    seq = e.get(1.0, END)
    # remove first line for fata files
    if seq[0] != '>':
        seq1 = seq  # from new_line_index + 1 position till the end
    else:
        seq1 = SeqIO.read(openFile.tfile, 'fasta').seq
        # print(seq1)
        # print('seq1')
        if seq1 != '' and seq1 is not None:
            seq = seq1
    seq1 = seq1.upper()
    # print(seq1)
    # print(len(seq1))
    # seq1 = codingseq(seq1)
    # print(seq1)
    # print(len(seq1))


    check_vars = [var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get()]
    # outtext.insert(END, check_vars)

    enzymes = ['EcoRI', 'XbaI', 'SpeI', 'PstI', 'NotI', 'SapI', 'BsaI']
    change_enzymes(enzymes, check_vars)
    # print(enzymes)
    # AatII, AfeI, ApaI, FspI

    restriction_batch = RestrictionBatch(enzymes)
    protein = Seq(seq1).translate()
    codons = {
        "UUU": "F",
        "CUU": "L",
        "AUU": "I",
        "GUU": "V",
        "UUC": "F",
        "CUC": "L",
        "AUC": "I",
        "GUC": "V",
        "UUA": "L",
        "CUA": "L",
        "AUA": "I",
        "GUA": "V",
        "UUG": "L",
        "CUG": "L",
        "AUG": "M",
        "GUG": "V",
        "UCU": "S",
        "CCU": "P",
        "ACU": "T",
        "GCU": "A",
        "UCC": "S",
        "CCC": "P",
        "ACC": "T",
        "GCC": "A",
        "UCA": "S",
        "CCA": "P",
        "ACA": "T",
        "GCA": "A",
        "UCG": "S",
        "CCG": "P",
        "ACG": "T",
        "GCG": "A",
        "UAU": "Y",
        "CAU": "H",
        "AAU": "N",
        "GAU": "D",
        "UAC": "Y",
        "CAC": "H",
        "AAC": "N",
        "GAC": "D",
        "UAA": "*",
        "CAA": "Q",
        "AAA": "K",
        "GAA": "E",
        "UAG": "*",
        "CAG": "Q",
        "AAG": "K",
        "GAG": "E",
        "UGU": "C",
        "CGU": "R",
        "AGU": "S",
        "GGU": "G",
        "UGC": "C",
        "CGC": "R",
        "AGC": "S",
        "GGC": "G",
        "UGA": "*",
        "CGA": "R",
        "AGA": "R",
        "GGA": "G",
        "UGG": "W",
        "CGG": "R",
        "AGG": "R",
        "GGG": "G"
    }

    cod = clicked.get()

    if cod == "2. The Vertebrate Mitochondrial Code":
        codons["AGA"] = "*"
        codons["AGG"] = "*"
        codons["AUA"] = "M"
        codons["UGA"] = "W"
    if cod == "3. The Yeast Mitochondrial Code":
        codons["AUA"] = "M"
        codons["CUU"] = "T"
        codons["CUC"] = "T"
        codons["CUA"] = "T"
        codons["CUG"] = "T"
        codons["UGA"] = "W"
    if cod == "4. The Mold, Protozoan, and Coelenterate Mitochondrial Code and the Mycoplasma/Spiroplasma Code":
        codons["UGA"] = "W"
    if cod == "5. The Invertebrate Mitochondrial Code":
        codons["AGA"] = "S"
        codons["AGG"] = "S"
        codons["AUA"] = "M"
        codons["UGA"] = "W"
    if cod == "6. The Ciliate, Dasycladacean and Hexamita Nuclear Code":
        codons["UAA"] = "Q"
        codons["UAG"] = "Q"
    if cod == "9. The Echinoderm and Flatworm Mitochondrial Code":
        codons["AAA"] = "N"
        codons["AGA"] = "S"
        codons["AGG"] = "S"
        codons["UGA"] = "W"
    if cod == "10. The Euplotid Nuclear Code":
        codons["UGA"] = "C"
    if cod == "12. The Alternative Yeast Nuclear Code":
        codons["CUG"] = "S"
    if cod == "13. The Ascidian Mitochondrial Code":
        codons["AGA"] = "G"
        codons["AGG"] = "G"
        codons["AUA"] = "M"
        codons["UGA"] = "W"
    if cod == "14. The Alternative Flatworm Mitochondrial Code":
        codons["AAA"] = "N"
        codons["AGA"] = "S"
        codons["AGG"] = "S"
        codons["UAA"] = "Y"
        codons["UGA"] = "W"
    if cod == "16. Chlorophycean Mitochondrial Code":
        codons["UAG"] = "L"
    if cod == "21. Trematode Mitochondrial Code":
        codons["UGA"] = "W"
        codons["AUA"] = "M"
        codons["AGA"] = "S"
        codons["AGG"] = "S"
        codons["AAA"] = "N"
    if cod == "22. Scenedesmus obliquus Mitochondrial Code":
        codons["UCA"] = "*"
        codons["UAG"] = "L"
    if cod == "24. Rhabdopleuridae Mitochondrial Code":
        codons["AGA"] = "S"
        codons["AGG"] = "K"
        codons["UGA"] = "W"
    if cod == "25. Candidate Division SR1 and Gracilibacteria Code":
        codons["UGA"] = "G"
    if cod == "26. Pachysolen tannophilus Nuclear Code":
        codons["CUG"] = "A"
    if cod == "27. Karyorelict Nuclear Code":
        codons["UAG"] = "Q"
        codons["UAA"] = "Q"
        codons["UGA"] = "*"
    if cod == "28. Condylostoma Nuclear Code":
        codons["UAA"] = "Q"
        codons["UAG"] = "Q"
        codons["UGA"] = "W"
    if cod == "29. Mesodinium Nuclear Code":
        codons["UAA"] = "Y"
        codons["UAG"] = "Y"
    if cod == "30. Peritrich Nuclear Code":
        codons["UAA"] = "E"
        codons["UAG"] = "E"
    if cod == "31. Blastocrithidia Nuclear Code":
        codons["UGA"] = "W"
        codons["UAG"] = "E"
        codons["UAA"] = "E"
    if cod == "33. Cephalodiscidae Mitochondrial UAA-Tyr Code":
        codons["UAA"] = "Y"
        codons["UGA"] = "W"
        codons["AGA"] = "S"
        codons["AGG"] = "K"

    # codon_name = clicked.get()
    # if codon_name == "1. The Standard Code":
    #     myLabel = Label(root, text = "Standard Codon Table")
    #     myLabel.pack()
    # print(seq1)
    forMapping = mapping(seq1, enzymes, restriction_batch, protein, codons)
    overlapping_pos = forMapping[0]
    overlapping_acids = forMapping[1]
    final = substitute(overlapping_pos, codons, seq1, overlapping_acids)
    myClick.final_sequence = final
    protein2 = final.translate()

    # myLabel = Label(root, text = "Initial seuence:" + str(seq) +"\n" + "Output sequence: " + str(final) + "\n" + str(protein==protein2))
    # myLabel.pack()
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    outtext.insert(END, "Your sequence is ready to be saved")



def show():
    myLabel = Label(root, text=clicked.get()).pack()

fastaButton = Button(root, text = "Open FASTA file", command = openFile, bg = "#752092", fg = "#FFFFFF").pack()

coding = Label(root, text = "Choose your aminoacid alphabet", bg = "#333333", fg = "#FFFFFF", font=("Futura, 14"))
coding.pack()

options = [
    "1. The Standard Code",
    "2. The Vertebrate Mitochondrial Code",
    "3. The Yeast Mitochondrial Code",
    "4. The Mold, Protozoan, and Coelenterate Mitochondrial Code and the Mycoplasma/Spiroplasma Code",
    "5. The Invertebrate Mitochondrial Code",
    "6. The Ciliate, Dasycladacean and Hexamita Nuclear Code",
    "9. The Echinoderm and Flatworm Mitochondrial Code",
    "10. The Euplotid Nuclear Code",
    "11. The Bacterial, Archaeal and Plant Plastid Code",
    "12. The Alternative Yeast Nuclear Code",
    "13. The Ascidian Mitochondrial Code",
    "14. The Alternative Flatworm Mitochondrial Code",
    "16. Chlorophycean Mitochondrial Code",
    "21. Trematode Mitochondrial Code",
    "22. Scenedesmus obliquus Mitochondrial Code",
    "23. Thraustochytrium Mitochondrial Code",
    "24. Rhabdopleuridae Mitochondrial Code",
    "25. Candidate Division SR1 and Gracilibacteria Code",
    "26. Pachysolen tannophilus Nuclear Code",
    "27. Karyorelict Nuclear Code",
    "28. Condylostoma Nuclear Code",
    "29. Mesodinium Nuclear Code",
    "30. Peritrich Nuclear Code",
    "31. Blastocrithidia Nuclear Code",
    "33. Cephalodiscidae Mitochondrial UAA-Tyr Code"
]
clicked = StringVar()
clicked.set("1. The Standard Code")
drop = OptionMenu(root, clicked, *options)
drop.config(bg = "#333333", fg = "#FFFFFF", relief = FLAT, bd=0)
drop['menu'].config(bg = "#333333", fg = "#FFFFFF", relief = FLAT, bd=0)
drop.pack()
# myButton = Button(root, text="Show Selection", command=show).pack()

def change_enzymes(enz, check_vars):
    if check_vars[0] == 0:
        enz.remove('EcoRI')
    if check_vars[1] == 0:
        enz.remove('XbaI')
    if check_vars[2] == 0:
        enz.remove('SpeI')
    if check_vars[3] == 0:
        enz.remove('PstI')
    if check_vars[4] == 0:
        enz.remove('NotI')
    if check_vars[5] == 0:
        enz.remove('SapI')
    if check_vars[6] == 0:
        enz.remove('BsaI')
    if additional.get() != '':
        user_enzymes_str = additional.get().replace(' ', '')
        enzs = user_enzymes_str.split(',')
        for x in enzs:
            enz.append(x)
        print(enz)


var1 = BooleanVar()
var2 = BooleanVar()
var3 = BooleanVar()
var4 = BooleanVar()
var5 = BooleanVar()
var6 = BooleanVar()
var7 = BooleanVar()

EcoRI = Checkbutton(root, text = "EcoRI - (GAATTC)", variable = var1, onvalue = True, offvalue = False,  bg = "#333333", fg = "#EA46FF")
EcoRI.pack()
XbaI= Checkbutton(root, text = "XbaI - (TCTAGA)", variable = var2, onvalue = True, offvalue = False,  bg = "#333333", fg = "#EA46FF")
XbaI.pack()
SpeI = Checkbutton(root, text = "SpeI - (ACTAGT)", variable = var3, onvalue = True, offvalue = False, bg = "#333333", fg = "#EA46FF")
SpeI.pack()
PstI = Checkbutton(root, text = "PstI - (CTGCAG)", variable = var4,  onvalue = True, offvalue = False, bg = "#333333", fg = "#EA46FF")
PstI.pack()
NotI = Checkbutton(root, text = "NotI - (GCGGCCGC)", variable = var5, onvalue = True, offvalue = False,  bg = "#333333", fg = "#EA46FF")
NotI.pack()
SapI= Checkbutton(root, text = "SapI - (GCTCTTC)", variable = var6,  onvalue = True, offvalue = False, bg = "#333333", fg = "#EA46FF")
SapI.pack()
BsaI = Checkbutton(root, text = "BsaI - (GGTCTC)", variable = var7,  onvalue = True, offvalue = False, bg = "#333333", fg = "#EA46FF")
BsaI.pack()
# myButton2 = Button(root, text = "Show Selected enzymes", command=show2).pack()

add_label = Label(root, text="Please provide any additional restriction sites in the following format: XXXX, YYYY, ZZZZ", bg = "#333333", fg = "#FFFFFF").pack()
additional = Entry(root, width = 50, bg = "#333333", fg = "#FFFFFF", relief = FLAT)
additional.pack(pady=5)
# if you want to get value from inputbox, use additional.get()
#AatII, AcII, AfeI, ApaI, FspI, PI-PspI
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

myButton = Button(root, text = "Analyze sequence", command = myClick, bg = "#752092", fg = "#FFFFFF", relief = FLAT)
myButton.pack(padx=10, pady=10)

outtext = Text(width=60, height=10, bg = "#333333", fg = "#FFFFFF")
outtext.pack()

saving = Button(root, text = "Save Results As...", command=text_save, bg = "#752092", fg = "#FFFFFF", relief = FLAT).pack(padx=10, pady=10)

root.mainloop()

#Interface loop ends -------------------------------------------------------------

# я вставил если че табличный код
# from tkinter import *
#
#
# class Table:
#
#     def __init__(self, roo):
#
#         # code for creating table
#         for i in range(total_rows):
#             for j in range(total_columns):
#                 self.e = Entry(root, width=20, fg='blue',
#                                font=('Arial', 16, 'bold'))
#
#                 self.e.grid(row=i, column=j)
#                 self.e.insert(END, lst[i][j])
#
#
# # take the data
# lst = [(1, 'EcoRI', 'GAATTC'),
#        (2, 'XbaI', 'TCTAGA'),
#        (3, 'SpeI', 'ACTAGT'),
#        (4, 'PstI', 'CTGCAG'),
#        (5, 'NotI', 'GCGGCCGC'),
#        (6, 'SapI', 'GCTCTTC'),
#        (7, 'BsaI', 'GGTCTC'),
#        (8, 'Enter Enzyme', 'formula'),
#        (9, 'Enter Enzyme', 'formula'),
#        (10, 'Enter Enzyme', 'formula'),
#        ]
#
# # find total number of rows and
# # columns in list
# a = Entry('Enter enzyme')
# b = Entry('Enter formula of enzyme')
# for i, j in a, b:
#     while a == "":
#         a = Entry('Enter enzyme')
#     while b == "":
#         b= input('Enter formula of enzyme')
# total_rows = len(lst)
# total_columns = len(lst[0])
#
# # create root window
# root = Tk()
# t = Table(root)
# root.mainloop()


