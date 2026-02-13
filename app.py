import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from engine import ReadinessEngine, TELC_B1_TOTAL_POINTS, TELC_B1_PASSING_POINTS

st.set_page_config(layout="wide", page_title="Exam Prep Analytics Pro")

# --- ФУНКЦИЯ ГРАДИЕНТА (Твое пожелание) ---
def get_color_gradient(percentage):
    """Возвращает цвет от красного до зеленого в зависимости от %"""
    if percentage >= 70: return "#10b981" # Зеленый (Успех)
    if percentage >= 60: return "#eab308" # Желтый (На грани)
    if percentage >= 50: return "#f59e0b" # Оранжевый (Риск)
    return "#ef4444" # Красный (Критично)

# --- ДАННЫЕ ИЗ MOCK-DATA.TS ---
scenarios = {
    "Успевает (216 баллов)": {
        "score": 216, 
        "parts": [
            {"name": "Lesen", "score": 59, "max": 75},
            {"name": "Hören", "score": 47, "max": 75},
            {"name": "Sprechen", "score": 21, "max": 30},
            {"name": "Schreiben", "score": 35, "max": 45}
        ]
    },
    "Под риском (174 балла)": {
        "score": 174, 
        "parts": [
            {"name": "Lesen", "score": 48, "max": 75},
            {"name": "Hören", "score": 38, "max": 75},
            {"name": "Sprechen", "score": 18, "max": 30},
            {"name": "Schreiben", "score": 24, "max": 45}
        ]
    }
}

st.sidebar.title("Настройки прототипа")
selected_name = st.sidebar.selectbox("Выберите сценарий:", list(scenarios.keys()))
data = scenarios[selected_name]

# Расчеты через ReadinessEngine
perc = (data['score'] / TELC_B1_TOTAL_POINTS) * 100
points_above = ReadinessEngine.calculate_points_above_target(data['score'])
main_color = get_color_gradient(perc)

# --- ВИЗУАЛИЗАЦИЯ (Верхний ряд) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Прогноз готовности (Индивидуально)")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = data['score'],
        gauge = {
            'axis': {'range': [0, 300]},
            'bar': {'color': main_color},
            'threshold': {'line': {'color': "red", 'width': 4}, 'value': TELC_B1_PASSING_POINTS}
        }
    ))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"<h2 style='text-align: center; color: {main_color};'>{points_above:+} к минимуму</h2>", unsafe_allow_html=True)

with col2:
    st.subheader("Точки роста (Градиент по частям)")
    df_parts = pd.DataFrame(data['parts'])
    df_parts['perc'] = (df_parts['score'] / df_parts['max']) * 100
    df_parts['color'] = df_parts['perc'].apply(get_color_gradient)
    
    # Строим график, где каждый столбик имеет свой цвет
    fig_bar = px.bar(df_parts, x='name', y='score', text='score',
                     color='perc', 
                     color_continuous_scale=[(0, "#ef4444"), (0.6, "#eab308"), (1, "#10b981")],
                     range_color=[40, 80])
    fig_bar.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.write("Чем 'краснее' столбик, тем больше внимания нужно уделить этой части.")

st.divider()

# --- СПИСОК ГРУППЫ (Нижний ряд) ---
st.subheader("Список группы и порог 60%")
group_data = [
    {"name": "Ученик 1 (On Track)", "score": 216, "perc": 72},
    {"name": "Ученик 2 (At Risk)", "score": 174, "perc": 58},
    {"name": "Ученик 3 (Not Ready)", "score": 135, "perc": 45},
]

for student in group_data:
    c_name, c_progress = st.columns([1, 3])
    with c_name:
        st.write(f"**{student['name']}**")
    with c_progress:
        # Цвет полоски зависит от прохождения порога 60%
        bar_color = "green" if student['perc'] >= 60 else "orange"
        st.progress(student['perc'] / 100)
        if student['perc'] < 60:
            st.caption(f"⚠️ Ниже порога: {student['score']} баллов (нужно 180)")