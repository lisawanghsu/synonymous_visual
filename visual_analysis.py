import pandas as pd
import numpy as np
import streamlit as st

st.title('Visual Analysis of Synonymous Muations in Cancer')

st.header('Synonymous Mutations in COSMIC v98')
# syn_mut_1 = pd.read_csv('SAMPLE_COUNT_1_syns.zip')
# st.write(syn_mut_1.head())
# print(syn_mut_1.columns)
# syn_mut_1['GENE'] = syn_mut_1['INFO'].apply(lambda x: x.split(';')[0].split('=')[1])
# # st.write(syn_mut_1['Gene'])

# syn_mut_over_1 = pd.read_csv('SAMPLE_COUNT_GT_1_syns.zip')
# st.write(syn_mut_over_1.head())
# syn_mut_over_1['GENE'] = syn_mut_over_1['INFO'].apply(lambda x: x.split(';')[0].split('=')[1])

# uscols = ['#CHROM', 'POS', 'REF', 'ALT', 'ID', 'GENE', 'SAMPLE_COUNT']
# pd.concat([syn_mut_1[uscols], syn_mut_over_1[uscols]]).to_csv('syn_mut_COSMIC_v98_infos.csv',index=False)
syn_mut_infos = pd.read_csv('syn_mut_COSMIC_v98_infos.zip')

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

# 根据基因名称筛选突变
st.subheader('Choice 2: Select from genes')
st.write('The top 10 genes with the most synonymous mutations:')
# st.write(syn_mut_infos['GENE'].value_counts(ascending=False)[:10])
st.bar_chart(syn_mut_infos['GENE'].value_counts(ascending=False)[:10],
             x_label='Gene',
             y_label='Number of synonymous mutations',
             use_container_width=True)
st.write('Genes with the only one synonymous mutations:')

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

st.subheader('Choice 3: Select from sample counts')

min_sample_count = st.slider('Minimum sample count', 
                            min_value=1, 
                            max_value=10, 
                            value=1)
filtered_by_sample_count = syn_mut_infos[syn_mut_infos['SAMPLE_COUNT'] >= min_sample_count]
st.write(f'There are **{filtered_by_sample_count.shape[0]:,}** mutations with sample count >= {min_sample_count}.')
st.dataframe(filtered_by_sample_count)

# 下载筛选后的数据
st.download_button(
    label=f"Download data (sample count >= {min_sample_count})",
    data=filtered_by_sample_count.to_csv(index=False).encode('utf-8'),
    file_name=f'syn_mut_COSMIC_v98_infos_sample_count_ge_{min_sample_count}.csv',
)

st.header('Training data of five methods of cancer driver synonymous mutation prediction')
cs_data = pd.read_csv(r'other_method_training_data\cscape_coding_training_examples.txt', sep='\t')
st.write('CS training data:', cs_data.shape, cs_data)
EPEL_data = pd.read_csv(r'other_method_training_data\EPEL_train_close7.txt', sep='\t')
st.write('EPEL training data:', EPEL_data.shape, EPEL_data)
epSMic_data = pd.read_csv(r'other_method_training_data\epSMic_training.vcf', sep='\t')
st.write('epSMic training data:', epSMic_data.shape, epSMic_data)
MFDSMC_data = pd.read_csv(r'other_method_training_data\MFDSMC_training.vcf', sep='\t', header=None)
st.write('MFDSMC training data:', MFDSMC_data.shape, MFDSMC_data)
PredDSMC_data = MFDSMC_data
st.write('PredDSMC training data are the same as MFDSMC:', PredDSMC_data.shape, PredDSMC_data)

st.header('Prediction results of five methods of cancer driver synonymous mutation prediction')
pred = pd.read_csv('COSMIC-V98-driver-5predictors.zip')
st.write(pred)

#提供所有预测值的下载功能
st.download_button(
    label=f"Download all prediction results",
    data=pred.to_csv(index=False).encode('utf-8'),
    file_name=f'COSMIC-V98-driver-5predictors.csv')
   
# 添加突变查询功能
st.subheader('Choice 1: Query specific mutation')
col1, col2, col3, col4 = st.columns(4)
with col1:
    chrom_query = st.text_input('Chromosome', placeholder='e.g., 1')
with col2:
    pos_query = st.number_input('Position', min_value=1, step=1)
with col3:
    ref_query = st.text_input('REF', placeholder='e.g., A')
with col4:
    alt_query = st.text_input('ALT', placeholder='e.g., T')

if chrom_query and pos_query and ref_query and alt_query:
    query_result = syn_mut_infos[
        (syn_mut_infos['#CHROM'] == chrom_query) &
        (syn_mut_infos['POS'] == pos_query) &
        (syn_mut_infos['REF'] == ref_query) &
        (syn_mut_infos['ALT'] == alt_query)
    ]
    query_pred_result = pred[
        (pred['#CHROM'] == chrom_query) &
        (pred['POS'] == pos_query) &
        (pred['REF'] == ref_query) &
        (pred['ALT'] == alt_query)
    ]
    
    if not query_result.empty:
        st.write('Mutation found:')
        st.dataframe(query_result)
        st.write('Prediction result:')
        st.dataframe(query_pred_result)
    else:
        st.warning('No mutation found matching the query criteria.')

# 添加批量查询突变功能
st.subheader('Choice 2: Query multiple mutations')
# uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv"])
query_input = st.text_area('Enter mutation query (format: chrom\tpos\tref\talt), the separator is Tab', 
                         placeholder='e.g., 1\t123456\tA\tT')

if query_input:
    try:
        lines = len(query_input.split('\n'))
        st.write(f'You have enterd **{lines}** mutations.')
        # 使用Tab键分割输入
        chrom_query = [item.split('\t')[0] for item in query_input.split('\n')]
        pos_query = [int(item.split('\t')[1]) for item in query_input.split('\n')]
        ref_query = [item.split('\t')[2] for item in query_input.split('\n')]
        alt_query = [item.split('\t')[3] for item in query_input.split('\n')]
        
        queries = pd.DataFrame({
            '#CHROM': chrom_query,
            'POS': pos_query,
            'REF': ref_query,
            'ALT': alt_query
        })
        # 执行查询
        query_result = pd.merge(queries, syn_mut_infos, on=['#CHROM', 'POS', 'REF', 'ALT'], how='inner')
        
        if not query_result.empty:
            st.write('Mutation found:')
            st.dataframe(query_result)
            # 执行预测查询
            query_pred_result = pd.merge(queries, pred, on=['#CHROM', 'POS', 'REF', 'ALT'], how='inner')
            st.write('Prediction result:')
            st.dataframe(query_pred_result)
        else:
            st.warning('No mutation found matching the query criteria.')
    except ValueError:
        st.error('Invalid input format. Please use: chrom\tpos\tref\talt')