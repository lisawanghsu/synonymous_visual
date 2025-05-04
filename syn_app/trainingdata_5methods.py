import streamlit as st
import pandas as pd
st.subheader('Training data of five methods for prediction of cancer driver synonymous mutations ')
method = st.selectbox('Method', ['CS', 'EPEL', 'epSMic', 'MFDSMC', 'PredDSMC'])
if method == 'CS':
    cs_data = pd.read_csv(r'cscape_coding_training_examples.txt', sep='\t')
    st.write('CS training data:', cs_data.shape, cs_data)
elif method == 'EPEL':
    EPEL_data = pd.read_csv(r'EPEL_train_close7.txt', sep='\t')
    st.write('EPEL training data:', EPEL_data.shape, EPEL_data)
elif method == 'epSMic':
    epSMic_data = pd.read_csv(r'epSMic_training.vcf', sep='\t')
    st.write('epSMic training data:', epSMic_data.shape, epSMic_data)
elif method == 'MFDSMC':
    MFDSMC_data = pd.read_csv(r'MFDSMC_training.vcf', sep='\t', header=None)
    st.write('MFDSMC training data:', MFDSMC_data.shape, MFDSMC_data)
elif method == 'PredDSMC':
    PredDSMC_data = pd.read_csv(r'MFDSMC_training.vcf', sep='\t', header=None)
    st.write('PredDSMC training data are the same as MFDSMC:', PredDSMC_data.shape, PredDSMC_data)
