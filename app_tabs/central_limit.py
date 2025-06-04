import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import calculate_sample_means, create_download_button


def central_limit_theorem_tab():
    """Вкладка центральной предельной теоремы"""
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("ЦПТ")

    st.header("Центральная предельная теорема")
    st.markdown(
        """ЦПТ утверждает, что независимо от распределения исходных данных,
    распределение **средних значений** будет стремиться к нормальному при увеличении размера выборки."""
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        dist_type = st.selectbox("Выберите распределение",
                                 ["Нормальное", "Равномерное", "Экспоненциальное", "Бимодальное"])
    with col2:
        sample_size = st.slider("Размер одной выборки", 2, 100, 30)
    with col3:
        num_samples = st.slider("Количество выборок", 100, 5000, 1000, step=100)

    means = calculate_sample_means(dist_type, sample_size, num_samples)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(means, bins=30, kde=True, ax=ax, color="skyblue", edgecolor='black')

    ax.set_title(f"ЦПТ: Средние {num_samples} выборок ({dist_type}, n = {sample_size})", fontsize=14)
    ax.set_xlabel("Среднее значение выборки")
    ax.set_ylabel("Частота")

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    create_download_button(fig, "clt.png")

    animate_clt = st.checkbox("Анимировать эффект увеличения размера выборки")
    if animate_clt:
        clt_animation_section(dist_type, num_samples)

    st.markdown(
        f"""
    **Пояснение**

    Центральная предельная теорема демонстрирует, что распределение выборочных средних
    приближается к нормальному, независимо от формы исходного распределения.

    Здесь: распределение = {dist_type.lower()}, размер n = {sample_size}, число выборок = {num_samples}
    """
    )


def clt_animation_section(dist_type: str, num_samples: int):
    """Раздел анимации ЦПТ"""
    animation_container = st.container()
    chart_placeholder = animation_container.empty()
    info_placeholder = animation_container.empty()

    col1, col2 = st.columns(2)
    with col1:
        animation_speed = st.slider("Скорость анимации", 0.1, 2.0, 0.5, 0.1)
    with col2:
        display_progress = st.checkbox("Показывать прогрессбар", value=True)

    sample_sizes = [2, 5, 10, 20, 30, 50, 100]
    if display_progress:
        progress_bar = st.progress(0)

    for i, n in enumerate(sample_sizes):
        if display_progress:
            progress_bar.progress((i + 1) / len(sample_sizes))

        means = calculate_sample_means(dist_type, n, num_samples)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(means, bins=30, kde=True, ax=ax, color="skyblue", edgecolor='black')

        ax.set_title(f"Распределение выборочных средних (n = {n})")
        ax.set_xlabel("Среднее значение выборки")
        ax.set_ylabel("Частота")

        std_dev = np.std(means)
        ax.axvline(np.mean(means), color='red', linestyle='--',
                   label=f'Среднее: {np.mean(means):.3f}, σ: {std_dev:.3f}')
        ax.legend()

        fig.tight_layout()
        chart_placeholder.pyplot(fig)

        if n <= 10:
            info_placeholder.info(f"n = {n}: ЦПТ ещё слабо проявляется")
        elif n <= 30:
            info_placeholder.info(f"n = {n}: ЦПТ начинает проявляться")
        else:
            info_placeholder.success(f"n = {n}: ЦПТ проявляется отчётливо!")

        plt.close(fig)
        time.sleep(1 / animation_speed)

    if display_progress:
        progress_bar.progress(1.0)

    st.success(
        """🎉 **Анимация завершена!**

    Вы наблюдали практическую демонстрацию ЦПТ:
    1. С увеличением размера выборки распределение средних становится более нормальным
    2. Стандартное отклонение уменьшается пропорционально √n
    3. Эффект не зависит от формы исходного распределения
    """
    )
