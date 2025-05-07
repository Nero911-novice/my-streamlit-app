import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# --- Настройка страницы ---
st.set_page_config(page_title="Демоверсия вероятностных законов", layout="wide")
sns.set_theme(style="whitegrid")

st.title("📊 Демонстрация вероятностных законов")
tabs = st.tabs(["Закон трёх сигм", "ЦПТ", "ЗБЧ"])

# === 1. Закон трёх сигм ===
with tabs[0]:
    st.header("Закон трёх сигм (эмпирическое правило)")
    mu = st.slider("Среднее (μ)", 20, 80, 50)
    sigma = st.slider("Стандартное отклонение (σ)", 1, 30, 10)
    size = st.slider("Размер выборки", 1000, 50000, 10000, step=1000)

    data = np.random.normal(mu, sigma, size)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(data, bins=50, density=True, color='lightgray', edgecolor='black')

    # Заливки зон ±1σ, ±2σ, ±3σ и их границы
    colors = ['#b2df8a', '#fdbf6f', '#fb9a99']
    labels = ['±1σ (68%)', '±2σ (95%)', '±3σ (99.7%)']
    for i, color, label in zip([1, 2, 3], colors, labels):
        ax.axvspan(mu - i * sigma, mu + i * sigma, color=color, alpha=0.3, label=label)
        ax.axvline(mu - i * sigma, color='red', linestyle='--', linewidth=1)
        ax.axvline(mu + i * sigma, color='red', linestyle='--', linewidth=1)

    # Нижняя и верхняя границы по Y
    ymax = ax.get_ylim()[1]

    # Аннотации с фиксированным смещением
    ax.annotate(
        "68% значений\n(±1σ)", xy=(mu, ymax * 0.9), xycoords='data',
        xytext=(0, -40), textcoords='offset points', ha='center', va='top',
        arrowprops=dict(arrowstyle='->', color='black'), fontsize=9
    )
    ax.annotate(
        "95% значений\n(±2σ)", xy=(mu - 2 * sigma, ymax * 0.6), xycoords='data',
        xytext=(-40, -10), textcoords='offset points', ha='left', va='top',
        arrowprops=dict(arrowstyle='->', color='black'), fontsize=9
    )
    ax.annotate(
        "Почти все значения\nв пределах ±3σ", xy=(mu + 2.5 * sigma, ymax * 0.6), xycoords='data',
        xytext=(40, -10), textcoords='offset points', ha='right', va='top',
        arrowprops=dict(arrowstyle='->', color='black'), fontsize=9
    )

    ax.set_title(f"Закон трёх сигм (μ = {mu}, σ = {sigma})")
    ax.set_xlabel("Значение")
    ax.set_ylabel("Плотность вероятности")
    ax.legend()

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    # Кнопка скачивания
    buf1 = BytesIO()
    fig.savefig(buf1, format="png")
    st.download_button("📥 Скачать график (PNG)", buf1.getvalue(), "three_sigma.png", "image/png")

    st.markdown(f"""
**Пояснение**  
График демонстрирует _закон трёх сигм_, согласно которому:
- около **68%** значений попадают в диапазон ±1σ от среднего,
- около **95%** — в диапазон ±2σ,
- около **99.7%** — в диапазон ±3σ.
""")

# обычный абзац (без заголовков и без лишней жирности)
st.markdown("""
Здесь: распределение = {dist_type.lower()}, размер выборки = {sample_size}, число выборок = {num_samples}.")
""")

st.markdown("""
🔴 **Ограничения**:
- Работает только при приближении к нормальному распределению.
- Неприменим к мощно скошенным, мультипиковым, дискретным распределениям.
- На маленьких выборках может не соблюдаться — выборочная дисперсия ещё «прыгает».
- Выбросы и шум нарушают правило: в реальной жизни за 3 сигмы может выходить и 5% наблюдений.
""")

# === 2. Центральная предельная теорема ===
with tabs[1]:
    st.header("Центральная предельная теорема")
    dist_type = st.selectbox(
        "Выберите распределение",
        ["Нормальное", "Равномерное", "Экспоненциальное", "Бимодальное"]
    )
    sample_size = st.slider("Размер одной выборки", 2, 100, 30)
    num_samples = st.slider("Количество выборок", 100, 5000, 1000, step=100)

    def generate(dist, n):
        if dist == "Равномерное":
            return np.random.uniform(0, 1, n)
        if dist == "Экспоненциальное":
            return np.random.exponential(1.0, n)
        if dist == "Бимодальное":
            half = n // 2
            return np.concatenate([
                np.random.normal(-2, 1, half),
                np.random.normal(2, 1, n - half)
            ])
        return np.random.normal(0, 1, n)

    means = [np.mean(generate(dist_type, sample_size)) for _ in range(num_samples)]
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.histplot(means, bins=30, kde=True, ax=ax2, color="skyblue", edgecolor='black')

    ax2.set_title(f"ЦПТ: Средние {num_samples} выборок ({dist_type}, размер = {sample_size})")
    ax2.set_xlabel("Среднее значение выборки")
    ax2.set_ylabel("Частота")

    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)

    buf2 = BytesIO()
    fig2.savefig(buf2, format="png")
    st.download_button("📥 Скачать график (PNG)", buf2.getvalue(), "clt.png", "image/png")

    st.markdown(f"""
**Пояснение**  
_Центральная предельная теорема_ утверждает, что независимо от распределения исходных данных распределение **средних значений** будет стремиться к нормальному при увеличении размера выборки.

Здесь: распределение = {dist_type.lower()}, размер выборки = {sample_size}, число выборок = {num_samples}.
---  
🔴 **Ограничения**:
- Нужны независимые и одинаково распределённые данные (i.i.d.).
- Размер выборки должен быть достаточно большим. Для нормального случая 30+, но для тяжёлых хвостов может понадобиться 100+.
- Не работает на агрегатах нестационарных процессов (например, трендовых временных рядов).
- При бесконечной дисперсии (например, распределение Коши) ЦПТ не применяется.
""")

# === 3. Закон больших чисел ===
with tabs[2]:
    st.header("Закон больших чисел")
    dist_type_lln = st.selectbox(
        "Распределение данных",
        ["Нормальное", "Равномерное", "Экспоненциальное"],
        key="lln"
    )
    trials = st.slider("Количество испытаний", 100, 20000, 10000, step=100)

    def sample(dist, n):
        if dist == "Равномерное":
            return np.random.uniform(0, 1, n)
        if dist == "Экспоненциальное":
            return np.random.exponential(1.0, n)
        return np.random.normal(0, 1, n)

    data_lln = sample(dist_type_lln, trials)
    cumulative = np.cumsum(data_lln) / np.arange(1, trials + 1)
    expected = np.mean(data_lln)

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(cumulative, label="Накопленное среднее")
    ax3.axhline(expected, color='r', linestyle='--', label=f"Теоретическое среднее ({expected:.2f})")

    ax3.set_title("Закон больших чисел")
    ax3.set_xlabel("Количество испытаний")
    ax3.set_ylabel("Среднее значение")
    ax3.legend()

    fig3.tight_layout()
    st.pyplot(fig3, use_container_width=True)

    buf3 = BytesIO()
    fig3.savefig(buf3, format="png")
    st.download_button("📥 Скачать график (PNG)", buf3.getvalue(), "lln.png", "image/png")

    st.markdown(f"""
**Пояснение**  
_Закон больших чисел_ утверждает, что по мере увеличения количества наблюдений среднее значение будет сходиться к математическому ожиданию распределения. Здесь использовано **{trials}** испытаний из **{dist_type_lln.lower()} распределения**.
---  
🔴 **Ограничения**:
- Данные должны быть независимыми и одинаково распределёнными.
- Сходимость может быть медленной, особенно при высокой дисперсии.
- В реальности редко удаётся собрать действительно независимые данные.
- ЗБЧ не говорит ничего о скорости сходимости — можно не дождаться её в реальном проекте.
""")
