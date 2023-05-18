import streamlit as st
import SwingVisionSight.serve_practice_page as serve_practice_page
import SwingVisionSight.match_page as match_page

st.set_page_config(page_title="SwingVisionSight", page_icon=":tennis:",layout="wide")


# ファイルのアップロード
uploaded_file = st.sidebar.file_uploader('Upload File.', type=['xlsx'])


if uploaded_file is not None:
    file_name = uploaded_file.name
    
    if 'Serve Practice' in file_name:
        serve_practice_page.app(uploaded_file)
        
    if 'match' in file_name:
        match_page.app(uploaded_file)
        
else:
    # Streamlitアプリのタイトルを設定する
    st.title('SwingVisionSight - Home')
    st.write('SwingVisionSight will generate insightful visualizations of your tennis shots based on the data provided by SwingVision App. Analyzing your shots in detail can help you identify areas that need improvement and enable you to adjust your technique to enhance your performance. ')
            
    st.markdown('''
                ## How to use SwingVisionSight
                ### 1. "Export CSV" from SwingVision App
                ### 2. Upload file to SwingVisionSight(this app) from left sidebar
                ### 3. With SwingVisionSight, you can take your game to the next level!
                ''')
    
    

