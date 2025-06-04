import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from .utils import generate_distribution_data, create_download_button


def theoretical_mean(dist_type: str) -> float:
    """Возвращает теоретическое среднее для распределения"""
    means = {
        "Нормальное": 0.0,
        "Равномерное": 0.5,
        "Экспоненциальное": 1.0
    }
    return means.get(dist_type, 0.0)


def law_of_large_numbers_tab():
    """Вкладка закона больших чисел"""
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("ЗБЧ")

    st.header("Закон больших чисел")

    col1, col2 = st.columns(2)
    with col1:
        dist_type_lln = st.selectbox("Распределение данных",
                                    ["Нормальное", "Равномерное", "Экспоненциальное"], key="lln")
    with col2:
        trials = st.slider("Количество испытаний", 100, 20000, 10000, step=100)

    data_lln = generate_distribution_data(dist_type_lln, trials)
    cumulative = np.cumsum(data_lln) / np.arange(1, trials + 1)
    expected = theoretical_mean(dist_type_lln)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(cumulative, label="Накопленное среднее", linewidth=2)
    ax.axhline(expected, color='r', linestyle='--', linewidth=2,
              label=f"Теоретическое среднее ({expected:.3f})")

    ax.set_title("Закон больших чисел", fontsize=14)
    ax.set_xlabel("Количество испытаний")
    ax.set_ylabel("Среднее значение")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    create_download_button(fig, "lln.png")

    st.markdown(
        f"""
    **Пояснение**

    Закон больших чисел показывает, что среднее значение выборки сходится к истинному
    среднему популяции при увеличении размера выборки.

    Здесь: распределение = {dist_type_lln.lower()}, испытаний = {trials}
    """
    )
