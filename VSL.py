# 1. 引入 streamlit
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# --- 設定網頁標題和版面 ---
st.set_page_config(layout="wide")  # 讓圖形使用更寬的頁面佈局
st.title('VSL 專項學習')

# --- 從 CSV 檔案讀取節點數據 ---
# (這部分和之前的腳本完全相同)
raw_node_texts = []
try:
    df = pd.read_csv("spiral_data.csv").fillna('')
    for column in df.columns:
        raw_node_texts.append(df[column].tolist())
except FileNotFoundError:
    st.error("錯誤：找不到 'spiral_data.csv' 檔案。請確保 CSV 檔案和 app.py 在同一個資料夾。")
    # 如果找不到檔案，則停止執行
    st.stop()

# --- 顏色主題 ---
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# --- 螺旋參數設定 ---
# (您可以保留這些參數，或者之後將它們變成 Streamlit 的互動元件)
num_spirals = 6
points_per_turn = 120
expansion_power = 2.5
num_turns = 7
spiral_height = 40
bottom_radius = 1.5
top_radius = 14.0
line_spacing_factor = 0.3
line_width = 4
marker_size = 8

# --- 生成圖形 (這部分和之前的腳本完全相同) ---
fig = go.Figure()

total_points = num_turns * points_per_turn
theta = np.linspace(0, num_turns * 2 * np.pi, total_points)
z = np.linspace(0, spiral_height, total_points)

base_growth = np.linspace(0, 1, total_points)
accelerated_growth = base_growth ** expansion_power
main_r_profile = bottom_radius + (top_radius - bottom_radius) * accelerated_growth

for i in range(num_spirals):
    angle_offset = (2 * np.pi / num_spirals) * i
    r_offset = line_spacing_factor * np.sin(theta + angle_offset * 2) * (main_r_profile / top_radius)
    r_i = main_r_profile + r_offset
    theta_i = theta + i * 0.3
    x_full, y_full, z_full = r_i * np.cos(theta_i), r_i * np.sin(theta_i), z
    fig.add_trace(go.Scatter3d(x=x_full, y=y_full, z=z_full, mode='lines', line=dict(color=colors[i], width=line_width),
                               hoverinfo='none'))

    spiral_data_with_blanks = raw_node_texts[i]
    total_slots = len(spiral_data_with_blanks)
    if total_slots > 0:
        all_slot_indices = np.linspace(0, total_points - 1, total_slots, dtype=int)
        x_nodes, y_nodes, z_nodes, text_nodes = [], [], [], []
        for j, text in enumerate(spiral_data_with_blanks):
            if text and isinstance(text, str) and text.strip():
                master_index = all_slot_indices[j]
                x_nodes.append(x_full[master_index])
                y_nodes.append(y_full[master_index])
                z_nodes.append(z_full[master_index])
                text_nodes.append(text)
        if text_nodes:
            fig.add_trace(go.Scatter3d(
                x=x_nodes, y=y_nodes, z=z_nodes,
                mode='markers+text',
                text=text_nodes,
                textposition="top center",
                textfont=dict(color='white', size=12),
                marker=dict(size=marker_size, color=colors[i], line=dict(width=1, color='white')),
                hoverinfo='text',
                hovertext=[f'<b>{text}</b>' for text in text_nodes]
            ))

# --- 美化與排版 (這部分和之前的腳本完全相同) ---
fig.update_layout(
    # title 已由 st.title() 取代
    width=900, height=900, showlegend=False, template='plotly_dark',
    scene=dict(
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        camera=dict(eye=dict(x=1.2, y=1.2, z=0.3)),
        aspectmode='manual', aspectratio=dict(x=1, y=1, z=1.0)
    ),
    margin=dict(r=10, l=10, b=10, t=10)  # 縮小邊界讓圖更大
)

# 2. ★★★ 將 fig.show() 替換為 st.plotly_chart() ★★★
st.plotly_chart(fig, use_container_width=True)

st.write("請稍後。")
