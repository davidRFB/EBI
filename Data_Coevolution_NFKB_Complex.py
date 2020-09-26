#!/usr/bin/env python
# coding: utf-8
## Execute this code as $python Data_Coevolution_NFKB_Complex.py > output.txt to get all information
## separeted by character | 
## the for extract information by columns it is possible to execute : 
##  head -2 output | awk -F '|' '{print $6}' varing $6
# # Extract orthologes gen Id from human NF-KB

# ## implemented for reading orthoXML files of orthologs. 
# Obtain genId of all orthologs

# In[147]:
'''

with open("./Human_NFKB1_orthologues.xml","r") as orthologs :
    text=orthologs.readlines()
name_gen=dict()
for i in range(len(text)):
	
    if("<species" in text[i]):
        name=text[i].split("name")[-1][2:-3]
        genId=text[i+3].split("=")[-2][1:-8]
        #protID=text[i+3].split("=")[-1][1:-5]   
        name_gen[name]=genId


# In[ ]:


with open("./Human_NFKB2_orthologues.xml","r") as orthologs :
    text=orthologs.readlines()
name_gen2=dict()
for i in range(len(text)):
    if("<species" in text[i]):
        name=text[i].split("name")[-1][2:-3]
        genId=text[i+3].split("=")[-2][1:-8]
        #protID=text[i+3].split("=")[-1][1:-5]   
        name_gen2[name]=genId

'''
# # Use of programatic access (REST/API : ENSEMBL) to find orthologs 

# In[149]:


'''
list of 5 genes in humans
'''
Human_NFKBComplex=dict()
Human_NFKBComplex["NKFB1"]="ENSG00000109320"
Human_NFKBComplex["NFKB2"]="ENSG00000077150"
Human_NFKBComplex["REL-A"]="ENSG00000173039"
Human_NFKBComplex["REL-B"]="ENSG00000104856"
Human_NFKBComplex["C-REL"]="ENSG00000162924"


# # Send Request  function 
# ## based on server and request its possible to find different information 
# ### Example : 
#        -orthologs
#        -phenotypes
#        -gen_basic or complete information 
# 
# all information in 
# http://rest.ensembl.org/

# In[151]:


import requests, sys, json
from pprint import pprint
import pandas as pd 
import numpy as np 
import time


def fetch_endpoint(server, request, content_type):
    '''
    input: server ,request (genId)  and optional parameters, content_type = json or xml 
    make a request in ensamble to look for gen basic information
    output r.json or r.txt objetc wiht gen information 
    
    '''
    r = requests.get(server+request, headers={ "Content-Type" : content_type}) 
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    if content_type == 'application/json':
        return r.json()
    else:
        return r.text
server_basicId = "http://rest.ensembl.org/lookup/id/"
server_homologs="http://rest.ensembl.org/homology/id/"
ext_homolgs = "?type=orthologues;format=condensed"
json = "application/json"
xml="text/xml"


# # Example of gen basic id info 

# In[152]:


#look for basic information of genes in humans.
'''
keys=["species","id"]
for i in Human_NFKBComplex.values():
    r=fetch_endpoint(server_basicId,i+"?",json)
    print(r["species"],r["id"],i)
'''

# In[ ]:


organism=["phascolarctos_cinereus","ornithorhynchus_anatinus","erinaceus_europaeus","sorex_araneus","myotis_lucifugus","pteropus_vampyrus","equus_caballus","panthera_leo","panthera_tigris_altaica","lynx_canadensis","vulpes_vulpes","canis_lupus_familiaris","ursus_americanus","ailuropoda_melanoleuca","mustela_putorius_furo","neovison_vison","balaenoptera_musculus","tursiops_truncatus","delphinapterus_leucas","camelus_dromedarius","bos_taurus","capra_hircus","cervus_hanglu_yarkandensis","aotus_nancymaae","macaca_fascicularis","mandrillus_leucophaeus","gorilla_gorilla","homo_sapiens","chinchilla_lanigera","cavia_porcellus","sciurus_vulgaris","urocitellus_parryii","meriones_unguiculatus","mus_musculus","rattus_norvegicus","nannospalax_galili","cricetulus_griseus"
]


# # Orthologs 

# In[60]:

#example
#r=fetch_endpoint(server_homologs,Human_NFKBComplex["NFKB2"]+ext_homolgs,json)


# In[68]:


def OrthologsPrintGenId(request):
    '''
    input request from server_homologs,gendID+ext_homolos fetch  in JSON format
    output dictionary with species name and gen ID
    '''
    ortholog_dict=dict()

    for ortholog in request['data'][0]['homologies']:

        #print(ortholog['species'],ortholog['id'],ortholog['protein_id'])
        ortholog_dict[ortholog['species']]=[]
        ortholog_dict[ortholog['species']].append(ortholog['id'])

    return ortholog_dict


# In[69]:

#example
#Orth_dic =OrthologsPrintGenId(r)


# # Nucleotide Sequence

# In[159]:


def ObtainNucleotideSeq(genId):
    '''
    input : genID
    output : nucleotide seq in plain text 
    
    if content type is x-fasta print also gen location 
    
    '''
    server = "http://rest.ensembl.org"
    ext = "/sequence/id/{}?type=genomic".format(genId)
    
    r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})
    

    if not r.ok:
      #r.raise_for_status()
      return "NaN"
      #sys.exit()
        
    return(r.text)


# # Protein seq and Uniprot Link

# In[167]:


def UniprotByGen(genid):
    '''
    make a request in ensamble to look for gen basic information
    output r.json or r.txt objetc wiht gen information 
    
    '''
    requestURL = "https://www.ebi.ac.uk/proteins/api/proteins/Ensembl:{}?offset=0&size=100".format(genid)

    r = requests.get(requestURL, headers={ "Accept" : "application/json"})

    if not r.ok:
        r.raise_for_status()
        
        sys.exit()
    responseBody = r.json()
    if(len(responseBody)<1):
        #print("genId {} not found in Uniprot".format(genid))
        return "NaN"
        
    return (responseBody[0])


# In[168]:

#example
###b=UniprotByGen("ENSGGOG00000006971")


# In[ ]:





# In[ ]:


##b['sequence']['sequence']


# # Data for NFKB complex 

# In[169]:


NFKBComplex_Data = dict()


# In[170]:


for i in Human_NFKBComplex.keys():
    NFKBComplex_Data[i]=[]


# In[171]:


#for key,val in NFKBComplex_Data.items():
#    print(key,val)   


# # Data Extraction. 
# ## takes around 1 s per organisms. total of 189 x5 = 15 min.  
# ### Steps :
#        - request orthologs
#        - get Nucleotide sequence
#        - get protein information (Acession code,  AA lenght, Prot Seq)
# ### Output : 
#       dict{([Protein in complex])= dict(species,[genID,NuclSeq,AA lenght,AA seq])}
#       where [Protein in complex] is NFKB1,NFKB2,REL-A,REL-B,C-REL
# #### ( this script could be used for data extraction of other proteins. Only needs lists with genes Id)

# In[175]:


t0 = time.time()
for key,val in NFKBComplex_Data.items():
    print("Getting information of {}".format(key))
    otholog_json=fetch_endpoint(server_homologs,Human_NFKBComplex[key]+ext_homolgs,json) ## orthologs of NFKB protein
    Orth_dic =OrthologsPrintGenId(otholog_json) ## create dictionary with {specie, genID}

    for species,gen in Orth_dic.items():
        #count= 0
        #print(count)
        #if(count==1):
        #    break 
        genId=gen[0]
        '''
        Obtain nucleotide seq from genId in plain text. use list.split(\n) to obtain each read
        ''' 
       
        seq = ObtainNucleotideSeq(genId)
        if(seq !="NaN"):
            gen.append(seq)
        else:
            gen.append("NaN") ## add this nucleotide seq to genId in list
        proteinSeq = UniprotByGen(genId) # obtain AA sequence
        
        if(proteinSeq !="NaN"): 
            '''
            if protein existe in Uniprot. then add 
            0. tuple(String,int) = (Acession,Uniprot Code)
            1. tuple(String,int) = (AA_length,len(protinSeq))
            2. String = AA sequence
            '''
            gen.append(("accesion",proteinSeq['accession']))
            gen.append(("AA length",proteinSeq['sequence']['length']))
            gen.append(proteinSeq['sequence']['sequence'])
        else: ## protein sequence doesnt exist in uniprot. 
            gen.append(("NaN","NaN"))
            gen.append(("AA length","NaN"))
            gen.append("NaN")
        Orth_dic[species]=gen
        #count+= 1  
    for name,data in Orth_dic.items():
        print(name,end=" | ")
        for eachdata in data:
            print(eachdata,end=" | ")
        print()
             
        
    '''
    add a dictionary as a value for dict{([Protein in complex])= dict(species,[genID,NuclSeq,AA lenght,AA seq])}
    where [Protein in complex] is NFKB1,NFKB2,REL-A,REL-B,C-REL
    '''
    NFKBComplex_Data[key]=Orth_dic 
    print("All data of {} uptdated".format(key))
    
tf=time.time()
print("total time of execution {} s".format(tf-t0))


# # Creation of data frame

# In[174]:


NFKB_DataFrame = pd.DataFrame.from_dict(NFKBComplex_Data)
#NFKB_DataFrame


# In[136]:


NFKB_DataFrame.to_csv("Data_NFKBComplex.csv")


# 

# In[137]:





# In[ ]:




