import pandas as pd
import numpy as np
import streamlit as st

st.title('Visual Analysis of Synonymous Muations in Cancer')

st.header('Synonymous Mutations in COSMIC v98')

syn_mut_infos = pd.read_csv('syn_mut_COSMIC_v98_infos.zip')

st.write(f'There are **{syn_mut_infos.shape[0]:,}** synonymous mutations in COSMIC v98. The first five rows:', syn_mut_infos.head())


# 根据基因名称筛选突变
st.subheader('Choice 2: Select from genes')
st.write('The top 10 genes with the most synonymous mutations:')
# st.write(syn_mut_infos['GENE'].value_counts(ascending=False)[:10])
st.bar_chart(syn_mut_infos['GENE'].value_counts(ascending=False)[:10],
             x_label='Gene',
             y_label='Number of synonymous mutations',
             use_container_width=True)
st.write('Genes with only one synonymous mutation:')

# 获取仅包含一个突变的基因信息
single_mutation_genes = syn_mut_infos[syn_mut_infos['GENE'].map(syn_mut_infos['GENE'].value_counts()) == 1]
st.dataframe(single_mutation_genes)

genes = st.multiselect('Gene', sorted(syn_mut_infos['GENE'].unique()))
total = pd.DataFrame()
for gene in genes:
    syn_mut_infos_gene = syn_mut_infos[syn_mut_infos['GENE'] == gene]
    st.write(syn_mut_infos_gene)
    st.write(f'There are {syn_mut_infos_gene.shape[0]:,} synonymous mutations in Gene {gene} in COSMIC v98.')
    total = pd.concat([total, syn_mut_infos_gene])

# 下载当前基因下的突变数据
st.download_button(
    label=f"Download data",
    data=total.to_csv(index=False).encode('utf-8'),
    file_name=f'syn_mut_COSMIC_v98_infos_gene_{"_".join(genes)}.csv', 
)
