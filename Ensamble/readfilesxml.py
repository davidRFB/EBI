#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 14:51:48 2020

@author: David Ricardo Figueora Blanco 
@email: dr.figueroa10@uniandes.edu.co 


   PROGRAM:   Read OrthoXML files with no processing xml structure.


   TODO:    Fix names as input ( .cvs file ) 

"""

import glob
files=glob.glob("./*.xml")

organism=["phascolarctos_cinereus","ornithorhynchus_anatinus","erinaceus_europaeus","sorex_araneus","myotis_lucifugus","pteropus_vampyrus","equus_caballus","panthera_leo","panthera_tigris_altaica","lynx_canadensis","vulpes_vulpes","canis_lupus_familiaris","ursus_americanus","ailuropoda_melanoleuca","mustela_putorius_furo","neovison_vison","balaenoptera_musculus","tursiops_truncatus","delphinapterus_leucas","camelus_dromedarius","bos_taurus","capra_hircus","cervus_hanglu_yarkandensis","aotus_nancymaae","macaca_fascicularis","mandrillus_leucophaeus","gorilla_gorilla","homo_sapiens","chinchilla_lanigera","cavia_porcellus","sciurus_vulgaris","urocitellus_parryii","meriones_unguiculatus","mus_musculus","rattus_norvegicus","nannospalax_galili","cricetulus_griseus"
]
count=0

def FindOrganismXML(data):
    '''
    read a orthoxml file and seach for a specific list of organism.
    organism name should be in lower case letter and separeted by _
    
    input = data name file othoXML file of orthologs.
    output = dictionary with name = (genID,protID)
    '''
    with open(data,"r") as orthologs : 
        text=orthologs.readlines()
    print()
    genprotDict=dict()
    for i in range(len(text)):
        if("<species" in text[i]):
            name=text[i].split("name")[-1][2:-3]
            if( name in organism):
                genId=text[i+3].split("=")[-2][1:-8]
                protID=text[i+3].split("=")[-1][1:-5]
                genprotDict[name]=((genId,protID))
                
    print("Organismos no encontrados:")
    for i in organism:
        if(i not in list(genprotDict.keys())):
            print(i)
                
    print()
    
    for name in organism:
        try:
            print(name,end=" , ")
            x=genprotDict.get(name)
            print(x[0])
        except:
            print()
    #for j,k in genprotDict.items():
    #    print(j,",",k[0])
    return genprotDict

for file in files:
    print(file)
    FindOrganismXML(file)















                       
                
