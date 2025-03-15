import streamlit as st
import pandas as pd


st.subheader('Prediction results of five methods of cancer driver synonymous mutation prediction')
pred = pd.read_csv('COSMIC-V98-driver-5predictors.zip')
st.write(pred)

#提供所有预测值的下载功能
st.download_button(
    label=f"Download all prediction results",
    data=pred.to_csv(index=False).encode('utf-8'),
    file_name=f'COSMIC-V98-driver-5predictors.csv')
   
# 添加突变查询功能
st.subheader('🔍️Choice 1: Query specific mutation')
col1, col2, col3, col4 = st.columns(4)
with col1:
    chrom_query = st.selectbox('Chromosome', ['X', 'Y'] + [str(i) for i in range(1, 23)])
with col2:
    pos_query = st.number_input('Position', min_value=1, step=1)
with col3:
    ref_query = st.selectbox('REF', list('ATCG'))
with col4:
    alt_query = st.selectbox('ALT', list('ATCG'))

syn_mut_infos = pd.read_csv('syn_mut_COSMIC_v98_infos.zip')
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
st.subheader('🔍️Choice 2: Query multiple mutations')
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
            st.write('Mutations found:')
            st.dataframe(query_result)
            # 执行预测查询
            query_pred_result = pd.merge(queries, pred, on=['#CHROM', 'POS', 'REF', 'ALT'], how='inner')
            st.write('Prediction results:')
            st.dataframe(query_pred_result)
        else:
            st.warning('No mutation found matching the query criteria.')
    except ValueError:
        st.error('Invalid input format. Please use: chrom\tpos\tref\talt')
