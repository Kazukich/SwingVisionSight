import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# テニスコートを描画する関数
@st.cache
def make_tennis_court():
    
    # figを作成
    fig = go.Figure()
    fig.update_layout(
        width=500, height=350,
        margin=dict(l=10, r=10, t=20, b=20),
        autosize=True,
        )

    fig.update_xaxes(range=[-10.97/2-1.5, 10.97/2+1.5])
    fig.update_yaxes(range=[23.77/2-1.5, 23.77-3])

    # ベースライン
    fig.add_shape(type='rect', x0=-10.97/2, x1=10.97/2, y0=0, y1=0, line=dict(color='white', width=0.5), layer='above')
    fig.add_shape(type='rect', x0=-10.97/2, x1=10.97/2, y0=23.77, y1=23.77, line=dict(color='white', width=0.5), layer='above')

    # サービスライン
    fig.add_shape(type='rect', x0=-8.23/2, x1=8.23/2, y0=23.77/2-6.40, y1=23.77/2-6.40, line=dict(color='white', width=0.5), layer='above')
    fig.add_shape(type='rect', x0=-8.23/2, x1=8.23/2, y0=23.77/2+6.40, y1=23.77/2+6.40, line=dict(color='white', width=0.5), layer='above')

    # ネット
    fig.add_shape(type='rect', x0=-10.97/2-0.914, x1=10.97/2+0.914, y0=23.77/2, y1=23.77/2, line=dict(color='white', width=0.5), layer='above')

    # ダブルスサイドライン
    fig.add_shape(type='rect', x0=-10.97/2, x1=-10.97/2, y0=0, y1=23.77, line=dict(color='white', width=0.5), layer='above')
    fig.add_shape(type='rect', x0=10.97/2, x1=10.97/2, y0=0, y1=23.77, line=dict(color='white', width=0.5), layer='above')

    # シングルスサイドライン
    fig.add_shape(type='rect', x0=-8.23/2, x1=-8.23/2, y0=0, y1=23.77, line=dict(color='white', width=0.5), layer='above')
    fig.add_shape(type='rect', x0=8.23/2, x1=8.23/2, y0=0, y1=23.77, line=dict(color='white', width=0.5), layer='above')

    # センターライン
    fig.add_shape(type='rect', x0=0, x1=0, y0=23.77/2-6.40, y1=23.77/2+6.40, line=dict(color='white', width=0.5), layer='above')

    # センターマーク
    fig.add_shape(type='rect', x0=0, x1=0, y0=0, y1=0.5, line=dict(color='white', width=0.5), layer='above')
    fig.add_shape(type='rect', x0=0, x1=0, y0=23.77-0.5, y1=23.77, line=dict(color='white', width=0.5), layer='above')

    # サービスボックス分割線
    fig.add_shape(type='line', x0=-8.23/2/3, x1=-8.23/2/3, y0=23.77/2-6.40, y1=23.77/2+6.40, line=dict(dash='dash', color='white', width=0.5), layer='above')
    fig.add_shape(type='line', x0=8.23/2/3, x1=8.23/2/3, y0=23.77/2-6.40, y1=23.77/2+6.40, line=dict(dash='dash', color='white', width=0.5), layer='above')
    fig.add_shape(type='line', x0=-8.23/3, x1=-8.23/3, y0=23.77/2-6.40, y1=23.77/2+6.40, line=dict(dash='dash', color='white', width=0.5), layer='above')
    fig.add_shape(type='line', x0=8.23/3, x1=8.23/3, y0=23.77/2-6.40, y1=23.77/2+6.40, line=dict(dash='dash', color='white', width=0.5), layer='above')

    fig.update_shapes(dict(xref='x', yref='y'))
    fig.update_layout(plot_bgcolor='black')
    fig.update_xaxes(showgrid=False,showticklabels=False,visible=False)
    fig.update_yaxes(showgrid=False,showticklabels=False,visible=False)
    
    return fig



# サーブイン率を計算する関数
def calc_serve_in_rate(df, player, first_second=None, deuce_ad=None, spin=None):
    if first_second is None:
        if deuce_ad is None:
            if spin is None:
                total_serve = len(df[(df['Player']==player) & (df["Stroke"]=="Serve")])
                total_serve_in = len(df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Result"]=="In")])
                if total_serve == 0:
                    return total_serve, total_serve_in, '---'
                else:
                    serve_in_rate = total_serve_in / total_serve
                    return total_serve, total_serve_in, round(serve_in_rate*100, 1)
            else:
                total_serve = len(df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Spin"]==spin)])
                total_serve_in = len(df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Spin"]==spin) & (df["Result"]=="In")])
                if total_serve == 0:
                    return total_serve, total_serve_in, '---'
                else:
                    serve_in_rate = total_serve_in / total_serve
                    return total_serve, total_serve_in, round(serve_in_rate*100, 1)
        else:
            if spin is None:
                total_serve = len(df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad)])
                if total_serve == 0:
                    return total_serve, total_serve_in, '---'
                else:
                    total_serve_in = len(df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad) & (df["Result"]=="In")])
                    serve_in_rate = total_serve_in / total_serve
                    return total_serve, total_serve_in, round(serve_in_rate*100, 1)
            else:
                total_serve = len(df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad) & (df["Spin"]==spin)])
                if total_serve == 0:
                    return total_serve, total_serve_in, '---'
                else:
                    total_serve_in = len(df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad) & (df["Spin"]==spin) & (df["Result"]=="In")])
                    serve_in_rate = total_serve_in / total_serve
                    return total_serve, total_serve_in, round(serve_in_rate*100, 1)
    
    else:
        if deuce_ad is None:
            if spin is None:
                total_serve = len(df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve")])
                total_serve_in = len(df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Result"]=="In")])
                if total_serve == 0:
                    return total_serve, total_serve_in, '---'
                else:
                    serve_in_rate = total_serve_in / total_serve
                    return total_serve, total_serve_in, round(serve_in_rate*100, 1)
            else:
                total_serve = len(df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Spin"]==spin)])
                total_serve_in = len(df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Spin"]==spin) & (df["Result"]=="In")])
                if total_serve == 0:
                    return total_serve, total_serve_in, '---'
                else:
                    serve_in_rate = total_serve_in / total_serve
                    return total_serve, total_serve_in, round(serve_in_rate*100, 1)
        else:
            if spin is None:
                total_serve = len(df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad)])
                if total_serve == 0:
                    return total_serve, total_serve_in, '---'
                else:
                    total_serve_in = len(df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad) & (df["Result"]=="In")])
                    serve_in_rate = total_serve_in / total_serve
                    return total_serve, total_serve_in, round(serve_in_rate*100, 1)
            else:
                total_serve = len(df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad) & (df["Spin"]==spin)])
                if total_serve == 0:
                    return total_serve, total_serve_in, '---'
                else:
                    total_serve_in = len(df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad) & (df["Spin"]==spin) & (df["Result"]=="In")])
                    serve_in_rate = total_serve_in / total_serve
                    return total_serve, total_serve_in, round(serve_in_rate*100, 1)
    



# 平均サーブスピードを計算する関数
def calc_average_serve_speed(df, player, first_second=None, deuce_ad=None, spin=None):
    if first_second is None:
        if deuce_ad is None:
            if spin is None:
                average_serve_speed = df[(df['Player']==player) & (df["Stroke"]=="Serve")]["Speed (KM/H)"].mean()
                
            else:
                average_serve_speed = df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Spin"]==spin)]["Speed (KM/H)"].mean()
        
        else:
            if spin is None:
                average_serve_speed = df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad)]["Speed (KM/H)"].mean()
                
            else:
                average_serve_speed = df[(df['Player']==player) & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad) & (df["Spin"]==spin)]["Speed (KM/H)"].mean()
                
    else:
        if deuce_ad is None:
            if spin is None:
                average_serve_speed = df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve")]["Speed (KM/H)"].mean()
                
            else:
                average_serve_speed = df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Spin"]==spin)]["Speed (KM/H)"].mean()
        
        else:
            if spin is None:
                average_serve_speed = df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad)]["Speed (KM/H)"].mean()
                
            else:
                average_serve_speed = df[(df['Player']==player) & (df["Type"]==f"{first_second}_serve") & (df["Stroke"]=="Serve") & (df["Hit Zone"]==deuce_ad) & (df["Spin"]==spin)]["Speed (KM/H)"].mean()

            
    return round(average_serve_speed, 1)

