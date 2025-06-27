import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

@st.cache_data
def load_data():
    return pd.read_csv("LAB3/all.csv")

data = load_data()

if "selected_area" not in st.session_state:
    st.session_state.selected_area = "Донецька область"
if "year_range" not in st.session_state:
    st.session_state.year_range = 2000
if "week_range" not in st.session_state:
    st.session_state.week_range = (1, 10)

regions = {
    "Вінницька область": 1, "Волинська область": 2, "Дніпропетровська область": 3, "Донецька область": 4,
    "Житомирська область": 5, "Закарпатська область": 6, "Запоріжська область": 7, "Івано-Франківська область": 8,
    "Київська область": 9, "Кіровоградська область": 10, "Луганська область": 11, "Львівська область": 12,
    "Миколаївська область": 13, "Одеська область": 14, "Полтавська область": 15, "Рівненська область": 16,
    "Сумська область": 17, "Тернопільська область": 18, "Харківська область": 19, "Херсонська область": 20,
    "Хмельницька область": 21, "Черкаська область": 22, "Чернівецька область": 23, "Чернігівська область": 24,
    "Крим область": 25
}

st.title("Visualization")
coefficient = st.selectbox("Оберіть коефіцієнт", ["VCI", "TCI", "VHI"])
st.session_state.selected_area = st.selectbox(
    "Оберіть область", options=list(regions.keys()), index=list(regions.keys()).index(st.session_state.selected_area)
)
region_id = regions[st.session_state.selected_area]
st.session_state.week_range = st.slider("Виберіть інтервал тижнів", 1, 52, st.session_state.week_range)
st.session_state.year_range = st.slider("Виберіть рік", 1982, 2024, st.session_state.year_range)

if st.button("Скинути фільтри"):
    st.session_state.selected_area = "Донецька область"
    st.session_state.year_range = 2000
    st.session_state.week_range = (1, 10)
    st.experimental_rerun()

filtered_data = data[
    (data["Area"] == region_id) &
    (data["Year"] == st.session_state.year_range) &
    (data["Week"] >= st.session_state.week_range[0]) &
    (data["Week"] <= st.session_state.week_range[1])
]

tab1, tab2 = st.tabs(["Таблиця", "Графік"])

with tab1:
    st.subheader("Відібрані дані")
    st.dataframe(filtered_data[["Year", "Week", coefficient, "Area"]])

    st.subheader("Статистика")
    st.markdown(f"- **Мінімум**: {filtered_data[coefficient].min():.2f}")
    st.markdown(f"- **Максимум**: {filtered_data[coefficient].max():.2f}")
    st.markdown(f"- **Середнє**: {filtered_data[coefficient].mean():.2f}")
    st.markdown(f"- **Медіана**: {filtered_data[coefficient].median():.2f}")

with tab2:
    st.subheader("Графік")
    fig, ax = plt.subplots()
    ax.plot(filtered_data["Week"], filtered_data[coefficient], marker='o')
    ax.set_xlabel("Тиждень")
    ax.set_ylabel("Значення")
    ax.set_title(f"{coefficient} для {st.session_state.selected_area} у {st.session_state.year_range} році")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True)
    st.pyplot(fig)
