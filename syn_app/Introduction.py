from pathlib import Path

import streamlit as st

from st_pages import add_page_title, get_nav_from_toml


st.title("Visual analysis of Cancer synonymous mutations")
st.header("Contents:")

st.markdown(
    '''
- **Cancer synonymous mutations in COSMIC v98**
    - By choromosomes
    - By genes 
    - By sample counts 
    - By primary sites  
- **Trainging data of five methods for cancer driver synonymous mutation prediction**
    - CS    
    - PredDSMC
    - EPEL
    - epSMic
    - MFDSMC
- **Predictions of five methods for cancer driver synonymous mutation in COSMIC v98** 
    - CS
    - CSS
    - PredDSMC
    - MFDSMC
    - EPEL
    '''   )
st.write('**Note:** all the mutations are based on GRCh37. Moreover, the GRCh38 coordinates of the mutations were included in the `Predictions` via the `vid_38` column.')
st.write('---')
st.write("""
The references are as follows:
- CS   
` ROGERS M F, SHIHAB H A, GAUNT T R, et al. CScape: a tool for predicting oncogenic single-point mutations in the cancer genome [J]. Sci Rep, 2017, 7(1): 11597.`
- CSS   
`ROGERS M F, GAUNT T R, CAMPBELL C. CScape-somatic: distinguishing driver and passenger point mutations in the cancer genome [J]. Bioinformatics, 2020, 36(12): 3637-44.`         
- PredDSMC   
`WANG L, SUN J, MA S, et al. PredDSMC: A predictor for driver synonymous mutations in human cancers [J]. Front Genet, 2023, 14: 1164593.                  `
- epSMic   
`CHENG N, BI C, SHI Y, et al. Effect Predictor of Driver Synonymous Mutations Based on Multi-Feature Fusion and Iterative Feature Representation Learning [J]. IEEE Journal of Biomedical and Health Informatics, 2024, 28(2): 1144-51.`         
- EPEL   
`BI C, SHI Y, XIA J, et al. Ensemble learning-based predictor for driver synonymous mutation with sequence representation [J]. PLOS Computational Biology, 2025, 21(1): e1012744.`         
         
                  """
)

# Initialize use_sections if it doesn't exist
if 'use_sections' not in st.session_state:
    st.session_state['use_sections'] = True  # or False, depending on your default

location = "pages_sections.toml" if st.session_state["use_sections"] else "pages.toml"
