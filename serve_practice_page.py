import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import SwingVisionSight.functions as functions

def app(uploaded_file):
    
    # Streamlitアプリのタイトルを設定する
    st.title('SwingVisionSight - Serve Practice')
    
    st.header('SERVE PLACEMENT')

    fig = functions.make_tennis_court()
    
    # アップロードされたファイルをdataFrameとして読み込む
    df = pd.read_excel(uploaded_file, sheet_name='Shots')
    
    
    col1, col2, col3 = st.columns(3)
    with col1:
        player = st.selectbox('PLAYER', (df['Player'].unique()))
    with col2:
        deuce_ad = st.selectbox('COURT', ('DEUCE', 'AD'))
    with col3:
        st.write('')
        st.write('')
        check = st.checkbox(label='Hide Miss Shots.')
    
    # 中心座標
    center = np.array([0, 23.77/2])

    # 座標変換行列
    R = np.array([[np.cos(np.pi), -np.sin(np.pi)], [np.sin(np.pi), np.cos(np.pi)]])

    # 座標変換
    df[['Transformed_Bounce (x)', 'Transformed_Bounce (y)']] = df.apply(lambda row: np.dot(R, np.array([row['Bounce (x)'], row['Bounce (y)']]) - center) + center if row['Hit Side'] == 'far' else [row['Bounce (x)'], row['Bounce (y)']], axis=1, result_type='expand')
    
    
    # マーカーの形と色の設定用の辞書
    marker_dict = {'Kick': 'circle', 'Slice': 'diamond', 'Flat': 'square'}
    miss_marker_dict = {'Kick': 'circle-open', 'Slice': 'diamond-open', 'Flat': 'square-open'}
    
    if deuce_ad == 'DEUCE':
        hit_zone = 'deuce'
    else:
        hit_zone = 'ad'
        
    if check:
        # Result = In
        fig.add_trace(
            go.Scatter(
                x=df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Transformed_Bounce (x)'],
                y=df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Transformed_Bounce (y)'],
                showlegend=False,
                mode='markers',
                marker=dict(
                    symbol=[marker_dict[spin] for spin in df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Spin']],
                    color='blue',
                    size=10,
                    ),
                text=[f"Spin: {spin}, Speed: {speed:.1f} km/h" for spin, speed, direction in zip(df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Spin'], df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Speed (KM/H)'], df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Direction'])],
                hoverinfo='text',
                )
            )
        
        
    else:
        # Result = In
        fig.add_trace(
            go.Scatter(
                x=df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Transformed_Bounce (x)'],
                showlegend=False,
                y=df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Transformed_Bounce (y)'],
                mode='markers',
                marker=dict(
                    symbol=[marker_dict[spin] for spin in df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Spin']],
                    color='blue',
                    size=10,
                    ),
                text=[f"Spin: {spin}, Speed: {speed:.1f} km/h" for spin, speed, direction in zip(df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Spin'], df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Speed (KM/H)'], df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Hit Zone']==hit_zone)]['Direction'])],
                hoverinfo='text',
                )
            )
        
        # Result != In
        fig.add_trace(
            go.Scatter(
                x=df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']!='In') & (df['Hit Zone']==hit_zone)]['Transformed_Bounce (x)'],
                y=df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']!='In') & (df['Hit Zone']==hit_zone)]['Transformed_Bounce (y)'],
                showlegend=False,
                mode='markers',
                marker=dict(
                    symbol=[miss_marker_dict[spin] for spin in df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']!='In') & (df['Hit Zone']==hit_zone)]['Spin']],
                    color='blue',
                    size=10,
                    ),
                text=[f"Spin: {spin}, Speed: {speed:.1f} km/h" for spin, speed, direction in zip(df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']!='In') & (df['Hit Zone']==hit_zone)]['Spin'], df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']!='In') & (df['Hit Zone']==hit_zone)]['Speed (KM/H)'], df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']!='In') & (df['Hit Zone']==hit_zone)]['Direction'])],
                hoverinfo='text',
                )
            )
    
    with st.container():
        # グラフを描画
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write('● IN')
        
        with col2:
            st.write('○ OUT')
        
        st.write('VIEW SERVE SPIN')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('● KICK')
            
        with col2:
            st.write('◆ SLICE')
            
        with col3:
            st.write('■ FLAT')
    

    # ダッシュボードに要素を表示
    with st.container():
        st.header('DASHBOARD')
        
        st.subheader(player)
        
        st.metric(
            'FASTEST SERVE', 
            f"{df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In')]['Speed (KM/H)'].max():.1f}km/h", 
            # 個人の過去データと比較を表示させる？
            # f"{df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In')]['Speed (KM/H)'].max() - df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In')]['Speed (KM/H)'].max():.1f} km/h"
            )
            
        st.metric(
            'AVERAGE SERVE', 
            f"{df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In')]['Speed (KM/H)'].mean():.1f}km/h", 
            # f"{df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In')]['Speed (KM/H)'].mean() - df[(df['Player']==player) & (df['Stroke']=='Serve') & (df['Result']=='In')]['Speed (KM/H)'].mean():.1f}km/h"
            )
        
        st.subheader('PLACEMENT RATE(%)')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('DEUCE')
            
            deuce_wide = len(df[(df['Player']==player) & (df['Hit Zone']=='deuce') & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Transformed_Bounce (x)'] > -8.23/2) & (df['Transformed_Bounce (x)'] < -8.23/2/3)])
            deuce_body = len(df[(df['Player']==player) & (df['Hit Zone']=='deuce') & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Transformed_Bounce (x)'] > -8.23/2/3) & (df['Transformed_Bounce (x)'] < -8.23/3)])
            deuce_t = len(df[(df['Player']==player) & (df['Hit Zone']=='deuce') & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Transformed_Bounce (x)'] > -8.23/3) & (df['Transformed_Bounce (x)'] < 0)])
            deuce_total = deuce_wide + deuce_body + deuce_t
            
            if deuce_total == 0:
                deuce_wide_rate, deuce_body_rate, deuce_t_rate = [0, 0, 0]
            else:
                deuce_wide_rate = deuce_wide/deuce_total*100
                deuce_body_rate = deuce_body/deuce_total*100
                deuce_t_rate = deuce_t/deuce_total*100
            
            deuce_graph = px.bar(x=['Wide', 'body', 'T'], y=[deuce_wide_rate, deuce_body_rate, deuce_t_rate])
            deuce_graph.update_yaxes(range=[0, 110])
            deuce_graph.update_layout(xaxis_title='', yaxis_title='Placement rate(%)')
            
            
            st.plotly_chart(deuce_graph, use_container_width=True)
            
            if deuce_total == 0:
                st.markdown('### NO DATA')
            
        
        with col2:
            st.subheader('AD')
            
            ad_t = len(df[(df['Player']==player) & (df['Hit Zone']=='ad') & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Transformed_Bounce (x)'] > 0) & (df['Transformed_Bounce (x)'] < 8.23/3)])
            ad_body = len(df[(df['Player']==player) & (df['Hit Zone']=='ad') & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Transformed_Bounce (x)'] > 8.23/3) & (df['Transformed_Bounce (x)'] < 8.23/2/3)])
            ad_wide = len(df[(df['Player']==player) & (df['Hit Zone']=='ad') & (df['Stroke']=='Serve') & (df['Result']=='In') & (df['Transformed_Bounce (x)'] > 8.23/2/3) & (df['Transformed_Bounce (x)'] < 8.23/2)])
            ad_total = ad_t + ad_body + ad_wide
            
            if ad_total == 0:
                ad_wide_rate, ad_body_rate, ad_t_rate = [0, 0, 0]
            else:
                ad_wide_rate = ad_wide/ad_total*100
                ad_body_rate = ad_body/ad_total*100
                ad_t_rate = ad_t/ad_total*100
            
            ad_graph = px.bar(x=['T', 'body', 'Wide'], y=[ad_wide_rate, ad_body_rate, ad_t_rate])
            ad_graph.update_yaxes(range=[0, 110])
            ad_graph.update_layout(xaxis_title='', yaxis_title='Placement rate(%)')
    
            st.plotly_chart(ad_graph, use_container_width=True)
            
            if ad_total == 0:
                st.markdown('### NO DATA')
        
    
    
    
    # 詳細データ
    expander = st.expander('Show detail data')
    
    # ダッシュボードに表示する要素を定義
    total_serve, total_serve_in, serve_in_rate = functions.calc_serve_in_rate(df, player)
    total_serve_deuce, total_serve_in_deuce, serve_in_rate_deuce = functions.calc_serve_in_rate(df, player, deuce_ad="deuce")
    total_serve_ad, total_serve_in_ad, serve_in_rate_ad = functions.calc_serve_in_rate(df, player, deuce_ad="ad")
    total_serve_kick, total_serve_in_kick, serve_in_rate_kick = functions.calc_serve_in_rate(df, player, spin="Kick")
    total_serve_slice, total_serve_in_slice, serve_in_rate_slice = functions.calc_serve_in_rate(df, player, spin="Slice")
    total_serve_flat, total_serve_in_flat, serve_in_rate_flat = functions.calc_serve_in_rate(df, player, spin="Flat")
    average_serve_speed = functions.calc_average_serve_speed(df, player)
    average_serve_speed_deuce = functions.calc_average_serve_speed(df, player, deuce_ad="deuce")
    average_serve_speed_ad = functions.calc_average_serve_speed(df, player, deuce_ad="ad")
    average_serve_speed_kick = functions.calc_average_serve_speed(df, player, spin="Kick")
    average_serve_speed_slice = functions.calc_average_serve_speed(df, player, spin="Slice")
    average_serve_speed_flat = functions.calc_average_serve_speed(df, player, spin="Flat")
    
    with expander:
        st.subheader("Serve In %")
        st.metric("Serve In %", f"{serve_in_rate} % ({total_serve_in}/{total_serve})")
        
        col1, col2, col3 = st.columns(3)
        
        if serve_in_rate_deuce == '---':
            col1.metric("Serve In % (Deuce)", f"{serve_in_rate_deuce} % ({total_serve_in_deuce}/{total_serve_deuce})", '---')
        else:
            col1.metric("Serve In % (Deuce)", f"{serve_in_rate_deuce} % ({total_serve_in_deuce}/{total_serve_deuce})", f"{float(serve_in_rate_deuce) - float(serve_in_rate):.1f} %")
            
        if serve_in_rate_ad == '---':
            col2.metric("Serve In % (Ad)", f"{serve_in_rate_ad} % ({total_serve_in_ad}/{total_serve_ad})", '---')
        else:
            col2.metric("Serve In % (Ad)", f"{serve_in_rate_ad} % ({total_serve_in_ad}/{total_serve_ad})", f"{float(serve_in_rate_ad) - float(serve_in_rate):.1f} %")
            
        
        col1, col2, col3 = st.columns(3)
        if serve_in_rate_kick == '---':
            col1.metric("Serve In % (Kick)", f"{serve_in_rate_kick} % ({total_serve_in_kick}/{total_serve_kick})", '---')
        else:
            col1.metric("Serve In % (Kick)", f"{serve_in_rate_kick} % ({total_serve_in_kick}/{total_serve_kick})", f"{float(serve_in_rate_kick) - float(serve_in_rate):.1f} %")
        
        if serve_in_rate_slice == '---':
            col2.metric("Serve In % (Slice)", f"{serve_in_rate_slice} % ({total_serve_in_slice}/{total_serve_slice})", "---")
        else:
            col2.metric("Serve In % (Slice)", f"{serve_in_rate_slice} % ({total_serve_in_slice}/{total_serve_slice})", f"{float(serve_in_rate_slice) - float(serve_in_rate):.1f} %")
            
        if serve_in_rate_flat == '---':
            col3.metric("Serve In % (Flat)", f"{serve_in_rate_flat} % ({total_serve_in_flat}/{total_serve_flat})", "---")
        else:
            col3.metric("Serve In % (Flat)", f"{serve_in_rate_flat} % ({total_serve_in_flat}/{total_serve_flat})", f"{float(serve_in_rate_flat) - float(serve_in_rate):.1f} %")
        
        
        st.subheader("Average Serve Speed(km/h)")
        st.metric("Average Serve Speed", f"{average_serve_speed} km/h")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Serve Speed (Deuce)", f"{average_serve_speed_deuce} km/h", f"{float(average_serve_speed_deuce) - float(average_serve_speed):.1f} km/h")
        col2.metric("Average Serve Speed (Ad)", f"{average_serve_speed_ad} km/h", f"{float(average_serve_speed_ad) - float(average_serve_speed):.1f} km/h")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Serve Speed (Kick)", f"{average_serve_speed_kick} km/h", f"{float(average_serve_speed_kick) - float(average_serve_speed):.1f} km/h")
        col2.metric("Average Serve Speed (Slice)", f"{average_serve_speed_slice} km/h", f"{float(average_serve_speed_slice) - float(average_serve_speed):.1f} km/h")
        col3.metric("Average Serve Speed (Flat)", f"{average_serve_speed_flat} km/h", f"{float(average_serve_speed_flat) - float(average_serve_speed):.1f} km/h")



