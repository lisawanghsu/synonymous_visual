import pandas as pd
import numpy as np
import streamlit as st

st.title('Visual Analysis of Synonymous Muations in Cancer')

st.header('Synonymous Mutations in COSMIC v98')

syn_mut_infos = pd.read_csv('COSMIC-V98-syns/syn_mut_COSMIC_v98_infos.zip')

st.write(f'There are **{syn_mut_infos.shape[0]:,}** synonymous mutations in COSMIC v98. The first five rows:', syn_mut_infos.head())


st.subheader('Choice 3: Select from sample counts')

min_sample_count = st.slider('Minimum sample count', 
                            min_value=1, 
                            max_value=10, 
                            value=10)
filtered_by_sample_count = syn_mut_infos[syn_mut_infos['SAMPLE_COUNT'] >= min_sample_count]
st.write(f'There are **{filtered_by_sample_count.shape[0]:,}** mutations with sample count >= {min_sample_count}.')
st.dataframe(filtered_by_sample_count)

# 下载筛选后的数据
st.download_button(
    label=f"Download data (sample count >= {min_sample_count})",
    data=filtered_by_sample_count.to_csv(index=False).encode('utf-8'),
    file_name=f'syn_mut_COSMIC_v98_infos_sample_count_ge_{min_sample_count}.csv',
)

