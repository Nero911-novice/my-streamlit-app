import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, Any
from .utils import generate_distribution_data, safe_statistics, format_stat_display, create_download_button


def distribution_selector(suffix: str) -> Tuple[str, Dict[str, Any]]:
    """Универсальный селектор параметров распределения"""
    distributions = ["Нормальное", "Равномерное", "Экспоненциальное", "Биномиальное", "Пуассона"]
    dist_type = st.selectbox(f"Тип распределения ({suffix})", distributions, key=f"dist_{suffix}")
    params: Dict[str, Any] = {}

    if dist_type == "Нормальное":
        params['mu'] = st.slider(f"Среднее μ ({suffix})", -10.0, 10.0, 0.0, key=f"mu_{suffix}")
        params['sigma'] = st.slider(f"Стандартное отклонение σ ({suffix})", 0.1, 5.0, 1.0, key=f"sigma_{suffix}")
    elif dist_type == "Равномерное":
        params['a'] = st.slider(f"Минимум a ({suffix})", -10.0, 10.0, 0.0, key=f"a_{suffix}")
        params['b'] = st.slider(f"Максимум b ({suffix})", params['a']+0.1, params['a']+20.0, params['a']+1.0, key=f"b_{suffix}")
    elif dist_type == "Экспоненциальное":
        lam = st.slider(f"Лямбда λ ({suffix})", 0.1, 5.0, 1.0, key=f"lambda_{suffix}")
        params['scale'] = 1/lam
    elif dist_type == "Биномиальное":
        params['n'] = st.slider(f"Количество испытаний n ({suffix})", 1, 100, 20, key=f"n_{suffix}")
        params['p'] = st.slider(f"Вероятность успеха p ({suffix})", 0.0, 1.0, 0.5, key=f"p_{suffix}")
    elif dist_type == "Пуассона":
        params['lam'] = st.slider(f"Интенсивность λ ({suffix})", 0.1, 20.0, 5.0, key=f"lam_{suffix}")
    return dist_type, params


def comparison_distributions_tab():
    """Вкладка сравнения распределений"""
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Сравнение распределений")

    st.header("Сравнение распределений")
    st.markdown("Интерактивное сравнение различных вероятностных распределений и их характеристик.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Первое распределение")
        dist1, params1 = distribution_selector("1")
    with col2:
        st.subheader("Второе распределение")
        dist2, params2 = distribution_selector("2")

    sample_size = st.slider("Размер выборки", 1000, 10000, 5000)

    data1 = generate_distribution_data(dist1, sample_size, **params1)
    data2 = generate_distribution_data(dist2, sample_size, **params2)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data1, bins=30, alpha=0.6, label=f"{dist1}", color="blue", kde=True, ax=ax)
    sns.histplot(data2, bins=30, alpha=0.6, label=f"{dist2}", color="red", kde=True, ax=ax)

    ax.set_title(f"Сравнение распределений: {dist1} vs {dist2}", fontsize=14)
    ax.set_xlabel("Значение")
    ax.set_ylabel("Частота")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    create_download_button(fig, "comparison.png")

    col1, col2 = st.columns(2)
    with col1:
        stats1 = safe_statistics(data1)
        format_stat_display(stats1, f"Статистика: {dist1}")
    with col2:
        stats2 = safe_statistics(data2)
        format_stat_display(stats2, f"Статистика: {dist2}")

    st.markdown(
        """**Анализ сравнения**
    
    Обратите внимание на ключевые различия:
    - **Форма распределения**: симметричность, количество пиков, асимметрия
    - **Центральная тенденция**: среднее vs медиана
    - **Разброс**: стандартное отклонение и диапазон значений
    - **Хвосты распределения**: тяжесть и скорость убывания
    """
    )
