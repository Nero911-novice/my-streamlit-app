import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from .utils import generate_distribution_data, create_download_button


def three_sigma_law_tab():
    """Вкладка закона трёх сигм"""
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Закон трёх сигм")

    st.header("Закон трёх сигм (эмпирическое правило)")
    st.markdown(
        """Закон трёх сигм помогает понять, как распределены данные вокруг среднего значения.
    Это полезно, когда нужно решить, какое наблюдение считать нормальным, а какое — выбросом."""
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        mu = st.slider("Среднее (μ)", 20, 80, 50)
    with col2:
        sigma = st.slider("Стандартное отклонение (σ)", 1, 30, 10)
    with col3:
        size = st.slider("Размер выборки", 1000, 50000, 10000, step=1000)

    data = generate_distribution_data("Нормальное", size, mu=mu, sigma=sigma)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(data, bins=50, density=True, color='lightgray', edgecolor='black', alpha=0.7)

    colors = ['#b2df8a', '#fdbf6f', '#fb9a99']
    labels = ['±1σ (68%)', '±2σ (95%)', '±3σ (99.7%)']
    for i, (color, label) in enumerate(zip(colors, labels), 1):
        ax.axvspan(mu - i * sigma, mu + i * sigma, color=color, alpha=0.3, label=label)
        ax.axvline(mu - i * sigma, color='red', linestyle='--', linewidth=1)
        ax.axvline(mu + i * sigma, color='red', linestyle='--', linewidth=1)

    ymax = ax.get_ylim()[1]
    annotations = [
        ("68% значений\n(±1σ)", (mu, ymax * 0.9), (0, -40)),
        ("95% значений\n(±2σ)", (mu - 2 * sigma, ymax * 0.6), (-40, -10)),
        ("Почти все значения\nв пределах ±3σ", (mu + 2.5 * sigma, ymax * 0.6), (40, -10))
    ]

    for text, xy, xytext in annotations:
        ax.annotate(text, xy=xy, xycoords='data', xytext=xytext,
                    textcoords='offset points', ha='center', va='top',
                    arrowprops=dict(arrowstyle='->', color='black'), fontsize=9)

    ax.set_title(f"Закон трёх сигм (μ = {mu}, σ = {sigma})", fontsize=14)
    ax.set_xlabel("Значение")
    ax.set_ylabel("Плотность вероятности")
    ax.legend()

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    create_download_button(fig, "three_sigma.png")

    st.markdown(
        f"""
    **Пояснение**
    График демонстрирует _закон трёх сигм_, согласно которому:
    - около **68%** значений попадают в диапазон ±1σ от среднего
    - около **95%** — в диапазон ±2σ
    - около **99.7%** — в диапазон ±3σ

    Здесь: μ = {mu}, σ = {sigma}, n = {size}

    **Простыми словами:**
    Представьте школьный класс, где средний рост детей 140 см, а стандартное отклонение 5 см:
    - Около 68% детей имеют рост от 135 до 145 см (±1σ)
    - Примерно 95% детей имеют рост от 130 до 150 см (±2σ)
    - Практически все дети (99.7%) имеют рост от 125 до 155 см (±3σ)

    ---
    🔴 **Ограничения**:
    - Работает только при приближении к нормальному распределению
    - Неприменим к сильно скошенным, мультипиковым, дискретным распределениям
    - На маленьких выборках может не соблюдаться

    🔵 **Преимущества**:
    - Простой эвристический метод оценки разброса
    - Основа контроля качества (Six Sigma)
    - Легко визуализируется и воспринимается
    """
    )
