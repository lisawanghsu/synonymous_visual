import streamlit as st
import pandas as pd


st.subheader('Predictions of the five methods on COSMIC-V98 synonymous mutations')
st.markdown('''
- CS   
- CSS   
- PredDSMC   
- MFDSMC   
- EPEL              
   ''')
pred = pd.read_csv('pred-results-v98-syns/COSMIC-V98-driver-5predictors.zip')
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
    chrom_query = st.selectbox('Chromosome', ['X', 'Y'] + [str(i) for i in range(1, 23)], index=None)
with col2:
    pos_query = st.number_input('Position', min_value=1, step=1, value=None)
with col3:
    ref_query = st.selectbox('REF', list('ATCG'), index=None)
with col4:
    alt_query = st.selectbox('ALT', list('ATCG'), index=None)

syn_mut_infos = pd.read_csv('COSMIC-V98-syns/syn_mut_COSMIC_v98_infos.zip')
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
uploaded_file = st.file_uploader("Upload a file (txt/csv) which contains **four** columns.The four columns are `#CHROM, POS, REF, and ALT` in order. And the column separator is Tab.", type=["txt", "csv"])
query_input = st.text_area('Or enter a mutation query (format: chrom\tpos\tref\talt), each line indicates a mutation, the separator is Tab', 
                         placeholder='e.g., 1\t123456\tA\tT\n7\t66459316\tG\tA\n19\t45899666\tC\tT')

# 处理输入
input_data = None
if uploaded_file is not None:
    # 读取上传文件内容
    input_data = pd.read_csv(uploaded_file, sep='\t')

elif query_input.strip():
    # 使用文本输入内容
    input_data = query_input
# st.write(input_data)
if input_data is not None and ((isinstance(input_data, pd.DataFrame) and not input_data.empty) or 
                             (isinstance(input_data, str) and input_data.strip())):
    try:
         # 判断input_data类型
        if isinstance(input_data, pd.DataFrame):
            # 如果是DataFrame，直接使用
            queries = input_data
            st.write(f'You have entered **{queries.shape[0]}** mutations.')
        else:
            # 如果是字符串，按原有逻辑处理
            lines = len(input_data.split('\n'))
            st.write(f'You have entered **{lines}** mutations.')
            # 使用Tab键分割输入
            chrom_query = [item.split('\t')[0] for item in input_data.split('\n')]
            pos_query = [int(item.split('\t')[1]) for item in input_data.split('\n')]
            ref_query = [item.split('\t')[2] for item in input_data.split('\n')]
            alt_query = [item.split('\t')[3] for item in input_data.split('\n')]
            
            queries = pd.DataFrame({
                '#CHROM': chrom_query,
                'POS': pos_query,
                'REF': ref_query,
                'ALT': alt_query
            })
        # 执行查询
        query_result = pd.merge(queries, syn_mut_infos, on=['#CHROM', 'POS', 'REF', 'ALT'], how='inner')
        
        if not query_result.empty:
            st.write('😄Mutations found:',query_result.shape[0])
            st.dataframe(query_result)
            # 执行预测查询
            query_pred_result = pd.merge(queries, pred, on=['#CHROM', 'POS', 'REF', 'ALT'], how='inner')
            st.write('😄Prediction results:',query_pred_result.shape)
            st.dataframe(query_pred_result)
        else:
            st.warning('😓No mutation found matching the query criteria.')
    except ValueError:
        st.error('❔Invalid input format. Please use: chrom\tpos\tref\talt')
