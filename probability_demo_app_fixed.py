import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_pdf import PdfPages

st.set_page_config(page_title="Демо вероятностей", layout="wide")

# --- Стили ---
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}
h1, h2 {
    color: #4F8BF9;
}
.sidebar .sidebar-content {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

st.title("🔬 Демонстрация вероятностных законов")

# --- Основные вкладки ---
tabs = st.tabs(["📊 Закон трёх сигм", "🎲 Центральная предельная теорема", "📈 Закон больших чисел"])

# === Вкладка 1: Закон трёх сигм ===
with tabs[0]:
    st.header("Закон трёх сигм (эмпирическое правило 68–95–99.7%)")
    mu = st.slider("Среднее (μ)", 20, 80, 50)
    sigma = st.slider("Стандартное отклонение (σ)", 1, 30, 10)
    sample_size = st.slider("Размер выборки", 1000, 20000, 10000)

    data = np.random.normal(mu, sigma, sample_size)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(data, bins=50, density=True, color='lightgray', edgecolor='black')

    colors = ['#a0e8af', '#ffd580', '#f28e8e']
    labels = ['±1σ (68%)', '±2σ (95%)', '±3σ (99.7%)']
    for i in range(3, 0, -1):
        ax.axvspan(mu - i * sigma, mu + i * sigma, color=colors[i - 1], alpha=0.3, label=labels[i - 1])
        ax.axvline(mu - i * sigma, color='red', linestyle='--', linewidth=1)
        ax.axvline(mu + i * sigma, color='red', linestyle='--', linewidth=1)

    ax.set_title(f"Закон трёх сигм (μ = {mu}, σ = {sigma})")
    ax.set_xlabel("Значение")
    ax.set_ylabel("Плотность вероятности")
    ax.legend()
    st.pyplot(fig)

    # Сохранение графика
    if st.button("💾 Скачать график (PDF)"):
        buf = io.BytesIO()
        with PdfPages(buf) as pdf:
            pdf.savefig(fig)
        b64 = base64.b64encode(buf.getvalue()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="three_sigma.pdf">Скачать PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

# === Вкладка 2: ЦПТ ===
with tabs[1]:
    st.header("Центральная предельная теорема")
    dist_type = st.selectbox("Тип распределения", ["Нормальное", "Равномерное", "Экспоненциальное", "Бимодальное"])
    sample_size = st.slider("Размер выборки", 2, 100, 30, key='clt_size')
    num_samples = st.slider("Количество выборок", 100, 5000, 1000, step=100, key='clt_count')

    def generate_distribution(dist_type, size):
        if dist_type == "Нормальное":
            return np.random.normal(0, 1, size)
        elif dist_type == "Равномерное":
            return np.random.uniform(-1, 1, size)
        elif dist_type == "Экспоненциальное":
            return np.random.exponential(scale=1, size=size)
        elif dist_type == "Бимодальное":
            d1 = np.random.normal(-2, 0.5, size // 2)
            d2 = np.random.normal(2, 0.5, size // 2)
            return np.concatenate([d1, d2])
        else:
            return np.random.normal(0, 1, size)

    means = [np.mean(generate_distribution(dist_type, sample_size)) for _ in range(num_samples)]
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.hist(means, bins=30, density=True, alpha=0.6, color='skyblue')
    ax2.set_title(f"ЦПТ: Средние из {num_samples} выборок по {sample_size} из {dist_type} распределения")
    ax2.set_xlabel("Среднее значение выборки")
    ax2.set_ylabel("Плотность")
    st.pyplot(fig2)

# === Вкладка 3: Закон больших чисел ===
with tabs[2]:
    st.header("Закон больших чисел")
    dist = st.selectbox("Тип распределения", ["Нормальное", "Равномерное"], key="lln_dist")
    trials = st.slider("Количество испытаний", 100, 20000, 10000, step=100)

    if dist == "Нормальное":
        data = np.random.normal(0, 1, trials)
        expected = 0
    else:
        data = np.random.uniform(-1, 1, trials)
        expected = 0

    cumulative_avg = np.cumsum(data) / np.arange(1, trials + 1)
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(cumulative_avg, label="Накопленное среднее")
    ax3.axhline(expected, color='red', linestyle='--', label=f"Теоретическое среднее ({expected})")
    ax3.set_title("ЗБЧ: Сходимость к математическому ожиданию")
    ax3.set_xlabel("Количество испытаний")
    ax3.set_ylabel("Среднее значение")
    ax3.legend()
    st.pyplot(fig3)
