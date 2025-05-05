import pandas as pd
import numpy as np
import streamlit as st

st.title('Visual Analysis of Synonymous Muations in Cancer')

st.header('Synonymous Mutations in COSMIC v98')

syn_mut_infos = pd.read_csv('COSMIC-V98-syns/syn_primary_sites.zip')

st.write(f'There are **{syn_mut_infos.shape[0]:,}** synonymous mutation records in COSMIC v98. The first five rows:', syn_mut_infos.head())

st.bar_chart(syn_mut_infos['PRIMARY_SITE'].value_counts(),color='#FF5733')
st.subheader('Choice 4: Select from primary sites')

tissue = st.selectbox('Pirmary sites', 
                            options=syn_mut_infos['PRIMARY_SITE'].unique(),
                            )
# 根据tissue筛选数据
syn_mut_infos = syn_mut_infos[syn_mut_infos['PRIMARY_SITE'] == tissue]

st.write(f'There are **{syn_mut_infos.shape[0]:,}** synonymous mutation records in **{tissue}**.')

st.write(syn_mut_infos)

# 提供下载按钮
st.download_button(
    label="Download data as CSV",
    data=syn_mut_infos.to_csv().encode('utf-8'),
    file_name='syn_primary_sites.csv',  
)