# to create the csv file for loading CO2RR data
# use dict to store key and item
# 0 stands for no obvious impact
# 1 stands for suppress HER
# 2 stands for suppress HER and CO
# 3 stands for MOSTLY Liquid Prod.
mole_dic = {
    "Pyridine": {
        'SMILES': 'C1=CC=NC=C1',
        'General effects': 0
    },
    "2,2'-Bipyridyl": {
        'SMILES': 'C1=CC=NC(=C1)C2=CC=CC=N2',
        'General effects': 1
    },
    "2,2':6',2\"-Terpyridine": {
        'SMILES': 'C1=CC=NC(=C1)C2=NC(=CC=C2)C3=CC=CC=N3',
        'General effects': 0
    },
    "2,4,6-Tris(2-pyridyl)-s-triazine": {
        'SMILES': 'C1=CC=NC(=C1)C2=NC(=NC(=N2)C3=CC=CC=N3)C4=CC=CC=N4',
        'General effects': 0
    },
    "Dichloro(1,10-phenanthroline) Copper (II)": {
        'SMILES': 'C1=CC2=C(C3=C(C=CC=N3)C=C2)N=C1.Cl[Cu]Cl',
        'General effects': 0
    },
    "4,7-Phenanthroline": {
        'SMILES': 'C1=CC2=C(C=CC3=C2C=CC=N3)N=C1',
        'General effects': 0
    },
    "Neocuproine": {
        'SMILES': 'CC1=NC2=C(C=C1)C=CC3=C2N=C(C=C3)C',
        'General effects': 2
    },
    "1,7-Phenanthroline": {
        'SMILES': 'C1=CC2=C(C3=C(C=C2)N=CC=C3)N=C1',
        'General effects': 2
    },
    "1,10-Phenanathroline": {
        'SMILES': 'C1=CC2=C(C3=C(C=CC=N3)C=C2)N=C1',
        'General effects': 2
    },
    "1,10-Phenanthrolin-5-amine": {
        'SMILES': 'C1=CC2=CC(=C3C=CC=NC3=C2N=C1)N',
        'General effects': 2
    },
    "Adenine": {
        'SMILES': 'C1=NC2=NC=NC(=C2N1)N',
        'General effects': 1
    },
    "Benzotriazole": {
        'SMILES': 'C1=CC2=NNN=C2C=C1',
        'General effects': 1
    },
    "1,8-Naphthyridine": {
        'SMILES': 'C1=CC2=C(N=C1)N=CC=C2',
        'General effects': 1
    },
    "2,4-Diamino-6-(hydroxymethyl)pteridine": {
        'SMILES': 'C1=C(N=C2C(=NC(=NC2=N1)N)N)CO',
        'General effects': 1
    },
    "6,7-Dimethyl-4-hydroxy-2-mercaptopteridine": {
        'SMILES': 'CC1=C(N=C2C(=N1)C(=O)NC(=S)N2)C',
        'General effects': 3
    },
    "4-Tert-butylcalix[6]arene": {
        'SMILES': 'CC(C)(C)C1=CC2=C(C(=C1)CC3=CC(=CC(=C3O)CC4=CC(=CC(=C4O)CC5=CC(=CC(=C5O)CC6=C(C(=CC(=C6)C(C)(C)C)CC7=C(C(=CC(=C7)C(C)(C)C)C2)O)O)C(C)(C)C)C(C)(C)C)C(C)(C)C)O',
        'General effects': 0
    },
    "Calix[8]arene": {
        'SMILES': 'C1C2=C(C(=CC=C2)CC3=C(C(=CC=C3)CC4=C(C(=CC=C4)CC5=C(C(=CC=C5)CC6=CC=CC(=C6O)CC7=CC=CC(=C7O)CC8=CC=CC(=C8O)CC9=CC=CC1=C9O)O)O)O)O',
        'General effects': 0
    }
}

# store them into a csv file
import csv
with open('CO2RR.csv', 'w', newline='') as csvfile:
    fieldnames = ['SMILES', 'General effects']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for key in mole_dic:
        writer.writerow({'SMILES': mole_dic[key]['SMILES'], 'General effects': mole_dic[key]['General effects']})