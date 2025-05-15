import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# --- Настройка страницы ---
st.set_page_config(page_title="Демоверсия вероятностных законов", layout="wide")
sns.set_theme(style="whitegrid")

st.title("📊 Демонстрация вероятностных законов")
tabs = st.tabs(["Закон трёх сигм", "ЦПТ", "ЗБЧ","Малые выборки"])

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

    ymax = ax.get_ylim()[1]

    # Аннотации
    ax.annotate(
        "68% значений\n(±1σ)",
        xy=(mu, ymax * 0.9), xycoords='data',
        xytext=(0, -40), textcoords='offset points',
        ha='center', va='top',
        arrowprops=dict(arrowstyle='->', color='black'),
        fontsize=9
    )
    ax.annotate(
        "95% значений\n(±2σ)",
        xy=(mu - 2*sigma, ymax * 0.6), xycoords='data',
        xytext=(-40, -10), textcoords='offset points',
        ha='left', va='top',
        arrowprops=dict(arrowstyle='->', color='black'),
        fontsize=9
    )
    ax.annotate(
        "Почти все значения\nв пределах ±3σ",
        xy=(mu + 2.5*sigma, ymax * 0.6), xycoords='data',
        xytext=(40, -10), textcoords='offset points',
        ha='right', va='top',
        arrowprops=dict(arrowstyle='->', color='black'),
        fontsize=9
    )

    ax.set_title(f"Закон трёх сигм (μ = {mu}, σ = {sigma})")
    ax.set_xlabel("Значение")
    ax.set_ylabel("Плотность вероятности")
    ax.legend()

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📥 Скачать график (PNG)", buf.getvalue(), "three_sigma.png", "image/png")

    st.markdown(f"""
**Пояснение**  
График демонстрирует _закон трёх сигм_, согласно которому:
- около **68%** значений попадают в диапазон ±1σ от среднего,
- около **95%** — в диапазон ±2σ,
- около **99.7%** — в диапазон ±3σ.
""")
    st.write(f"Здесь: μ = {mu}, σ = {sigma}, n = {size}.")
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

    buf = BytesIO()
    fig2.savefig(buf, format="png")
    st.download_button("📥 Скачать график (PNG)", buf.getvalue(), "clt.png", "image/png")

    st.markdown(f"""
**Пояснение**  
_Центральная предельная теорема_ утверждает, что независимо от распределения исходных данных распределение **средних значений** будет стремиться к нормальному при увеличении размера выборки.
""")
    st.write(f"Здесь: распределение = {dist_type.lower()}, размер выборки = {sample_size}, число выборок = {num_samples}.")
    st.markdown("""
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

    buf = BytesIO()
    fig3.savefig(buf, format="png")
    st.download_button("📥 Скачать график (PNG)", buf.getvalue(), "lln.png", "image/png")

    st.markdown(f"""
**Пояснение**  
_Закон больших чисел_ утверждает, что по мере увеличения количества наблюдений среднее значение будет сходиться к математическому ожиданию распределения. Здесь использовано **{trials}** испытаний из **{dist_type_lln.lower()} распределения**.
""")
    st.write(f"Здесь: распределение = {dist_type_lln.lower()}, количество испытаний = {trials}.")
    st.markdown("""
🔴 **Ограничения**:
- Данные должны быть независимыми и одинаково распределёнными.
- Сходимость может быть медленной, особенно при высокой дисперсии.
- В реальности редко удаётся собрать действительно независимые данные.
- ЗБЧ не говорит ничего о скорости сходимости — можно не дождаться её в реальном проекте.
""")

# === 4. Закон малых выборок ===
with tabs[3]:
    st.header("Закон малых выборок")
    st.markdown(
        "Небольшие выборки дают сильно варьирующиеся оценки: "
        "распределение средних может быть далеким от нормального, "
        "а доверительные интервалы – слишком широкими."
    )

    dist_small = st.selectbox(
        "Исходное распределение",
        ["Нормальное", "Равномерное", "Экспоненциальное", "Бимодальное"]
    )
    n_small = st.slider("Размер маленькой выборки (n)", 2, 30, 5)
    k_trials = st.slider("Количество повторных выборок", 100, 2000, 500, step=100)

    # Функция генерации
    def gen(dist, m):
        if dist == "Равномерное":
            return np.random.uniform(0, 1, m)
        if dist == "Экспоненциальное":
            return np.random.exponential(1, m)
        if dist == "Бимодальное":
            h = m // 2
            return np.concatenate([
                np.random.normal(-2, 1, h),
                np.random.normal(2, 1, m - h)
            ])
        return np.random.normal(0, 1, m)

    # Считаем средние
    means_small = [np.mean(gen(dist_small, n_small)) for _ in range(k_trials)]

    # Рисуем гистограмму
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.histplot(means_small, bins=20, kde=True, ax=ax4, color="mediumpurple", edgecolor="black")
    ax4.set_title(f"Распределение средних из {k_trials} выборок по {n_small} элементов (из {dist_small})")
    ax4.set_xlabel("Среднее значение")
    ax4.set_ylabel("Частота")
    fig4.tight_layout()
    st.pyplot(fig4, use_container_width=True)

    # Скачивание
    buf4 = BytesIO()
    fig4.savefig(buf4, format="png")
    st.download_button("📥 Скачать график (PNG)", buf4.getvalue(), "small_sample.png", "image/png")

    # Текст
    st.markdown(f"""
**Пояснение**  
При **малых** n (= {n_small}) распределение выборочных средних остаётся широким и часто сильно отличается от нормали, даже если исходные данные нормальны.

🔴 **Ограничения и риски**:
- Высокая дисперсия оценок среднего – доверительный интервал слишком широк.
- Если n < 30, **ЦПТ** ещё не «развернута» в полную силу.
- Для скошенных или тяжёлохвостых распределений нужны **гораздо** большие n.
- Выводы по маленькой выборке могут быть **ненадежны** и легко сбить с толку.

 **Примеры проявления закона малых чисел в реальной жизни:**
    - Опросы общественного мнения с маленькой выборкой участников.
    - Медицинские исследования на небольших группах пациентов.
    - Прогнозы на основе малого количества наблюдений в бизнесе или спорте.
    - Ошибка игрока в азартных играх (ожидание компенсации потерь).
    
    Важно понимать ограничения выводов, сделанных на малых выборках, и стремиться к репликации результатов на больших объемах данных, чтобы получить надежные оценки.
    """)
