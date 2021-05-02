import sys
import os
import numpy as np
import re
import math

def input_file(xyzfile, functional, charge_eda, charge_f1, charge_f2, frag1_a, frag1_b, frag2_a, frag2_b):
    filename = xyzfile
    input = open(filename,'r')
    filebase = os.path.splitext(filename)[0]
    #outputs section
    eda_file = open(filebase+'-eda.in', 'a')
    frag1_file = open(filebase+'-f1.in', 'a')
    frag2_file = open(filebase+'-f2.in', 'a')
    eda_file.write(f'title {filebase}\n\nXC\nHYBRID FUNCTIONAL {functional}\nDISPERSION Grimme3 BJDAMP\n'
                   f'END\n\nBASIS\ntype TZ2P\ncore none\nEND\n'
                   f'\nSAVE  TAPE21\n\nscf\nIterations 1500\nconverge 0.00000100 0.0010000\nend\n '
                   f'\nSYMMETRY NOSYM\nETSNOCV RHOKMIN=1.e-3 EKMIN=0.5 ENOCV=0.01\nPRINT ETSLOWDIN\n'
                   f'\ncharge {charge_eda}\n')
    frag1_file.write(f'title {filebase}\n\nXC\n HYBRID FUNCTIONAL {functional}\nDISPERSION Grimme3 BJDAMP\n'
                     f'END\n\nBASIS\ntype TZ2P\ncore none\nEND\n '
                     f'\nSAVE  TAPE21\n\nscf\nIterations 1500\nconverge 0.00000100 0.0010000\nend\n'
                     f'\nSYMMETRY NOSYM\nETSNOCV RHOKMIN=1.e-3 EKMIN=0.5 ENOCV=0.01\nPRINT ETSLOWDIN\n'
                     f'\ncharge {charge_f1}\n')
    frag2_file.write(f'title {filebase}\n\nXC\nHYBRID FUNCTIONAL {functional}\nDISPERSION Grimme3 BJDAMP\n'
                     f'END\n\nBASIS\ntype TZ2P\ncore none\nEND\n'
                     f'\nSAVE  TAPE21\n\nscf\nIterations 1500\nconverge 0.00000100 0.0010000\nend\n'
                     f'\nSYMMETRY NOSYM\nETSNOCV RHOKMIN=1.e-3 EKMIN=0.5 ENOCV=0.01\nPRINT ETSLOWDIN\n'
                     f'\ncharge {charge_f2}\n')

    coordinates = []
    frag1 = []
    fragment_1 = []

    frag2 = []
    fragment_2 = []

    for line in input.readlines():
        coordinates.append(line)
    del coordinates[0], coordinates[0]

    for p, e in enumerate(coordinates):
        if frag1_a <= p <= frag1_b:
            frag1.append(f'{e.rstrip().strip()} f=1\n')
            fragment_1.append(f'{e.strip()}\n')
        if frag2_a <= p <= frag2_b:
            frag2.append(f'{e.rstrip().strip()} f=2\n')
            fragment_2.append(f'{e.rstrip().strip()}\n')

    eda_file.write(f'\natoms\n')
    frag1_file.write(f'\natoms\n')
    frag2_file.write(f'\natoms\n')
    eda_file.writelines(frag1)
    frag1_file.writelines(fragment_1)
    eda_file.writelines(frag2)
    frag2_file.writelines(fragment_2)
    eda_file.write(f'end\n \nfragments\n 1 {filebase}-f1.t21\n '
                   f'2 {filebase}-f2.t21\nend\nend input')
    frag1_file.write(f'end\nend input')
    frag2_file.write(f'end\nend input')


    input.close()
    eda_file.close()
    frag1_file.close()
    frag2_file.close()
    return eda_file, frag1_file, frag2_file



