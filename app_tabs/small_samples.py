import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from .utils import safe_statistics, create_download_button


def small_samples_tab():
    """Вкладка закона малых выборок"""
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Малые выборки")

    st.header("Закон малых выборок")
    st.markdown(
        """Закон малых чисел — психологический феномен: люди переоценивают надежность
    выводов при малых выборках. При малом n статистическая нестабильность может давать сильно ошибочные результаты."""
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        dist_small = st.selectbox("Исходное распределение",
                                 ["Нормальное", "Равномерное", "Экспоненциальное", "Бимодальное"])
    with col2:
        n_small = st.slider("Размер маленькой выборки (n)", 2, 30, 5)
    with col3:
        num_sim = st.slider("Количество симуляций", 100, 2000, 500, step=100)

    means_small = []
    for i in range(num_sim):
        np.random.seed(i + 1000)
        if dist_small == "Нормальное":
            sample = np.random.normal(0, 1, n_small)
        elif dist_small == "Равномерное":
            sample = np.random.uniform(0, 1, n_small)
        elif dist_small == "Экспоненциальное":
            sample = np.random.exponential(1, n_small)
        elif dist_small == "Бимодальное":
            half = n_small // 2
            sample = np.concatenate([
                np.random.normal(-2, 1, half),
                np.random.normal(2, 1, n_small - half)
            ])
        means_small.append(np.mean(sample))

    means_small = np.array(means_small)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(means_small, bins=20, density=True, alpha=0.7, edgecolor='black', color='lightcoral')

    emp_mean = np.mean(means_small)
    ax.axvline(emp_mean, color='green', linestyle='--', linewidth=2,
              label=f'Эмпирическое среднее: {emp_mean:.3f}')

    ax.set_title(f"Закон малых выборок (n={n_small}, симуляций={num_sim})", fontsize=14)
    ax.set_xlabel("Среднее значение")
    ax.set_ylabel("Плотность")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    create_download_button(fig, "small_law.png")

    stats_dict = safe_statistics(means_small)
    st.markdown(
        f"""
    **Результаты анализа**

    При малом размере выборки n = {n_small}:
    - Среднее по симуляциям: {stats_dict['mean']:.4f}
    - Стандартное отклонение: {stats_dict['std']:.4f}
    - Диапазон значений: [{stats_dict['min']:.3f}, {stats_dict['max']:.3f}]

    **Вывод:** Распределение выборочных средних остается широким и нестабильным
    при малых размерах выборки.

    ---
    🔴 **Риски малых выборок**:
    - Высокая дисперсия оценок среднего
    - ЦПТ ещё не действует полностью при n < 30
    - Возможны серьёзные ошибки в выводах

    🔵 **Практическая польза**:
    - Демонстрирует важность объёма выборки
    - Помогает понять ненадёжность результатов малых выборок
    - Объясняет необходимость репликации исследований
    """
    )
