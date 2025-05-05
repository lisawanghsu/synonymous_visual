import pandas as pd
import numpy as np
import streamlit as st

st.title('Visual Analysis of Synonymous Muations in Cancer')

st.header('Synonymous Mutations in COSMIC v98')

syn_mut_infos = pd.read_csv('COSMIC-V98-syns/syn_mut_COSMIC_v98_infos.zip')

st.write(f'There are **{syn_mut_infos.shape[0]:,}** synonymous mutations in COSMIC v98. The first five rows:', syn_mut_infos.head())

st.header('Synonymous Mutations in choromsomes')
st.bar_chart(syn_mut_infos['#CHROM'].value_counts(),
             x_label='Chromosome',
             y_label='Number of synonymous mutations',
             use_container_width=True,
             color='#0000FF')
st.subheader('Choice 1: Select from chromosomes')
chroms = st.multiselect('Chromosome', sorted(syn_mut_infos['#CHROM'].unique()))
total = pd.DataFrame()
for chrom in chroms:
    syn_mut_infos_chrom = syn_mut_infos[syn_mut_infos['#CHROM'] == chrom]
    st.write(syn_mut_infos_chrom)
    st.write(f'There are **{syn_mut_infos_chrom.shape[0]:,}** synonymous mutations in Chromosome {chrom} in COSMIC v98.')
    total = pd.concat([total, syn_mut_infos_chrom])

# 下载当前染色体下的突变数据
st.download_button(
    label=f"Download data",
    data=total.to_csv(index=False).encode('utf-8'),
    file_name=f'syn_mut_COSMIC_v98_infos_chrom_{"_".join(chroms)}.csv',

)
