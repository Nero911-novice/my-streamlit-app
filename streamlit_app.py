import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats  # Важно импортировать stats именно так
from io import BytesIO
import time  # Для использования в модуле регрессии к среднему

@st.cache_data
def generate_data(dist_type, size, mu=0, sigma=1):
    """Генерирует данные с кэшированием для ускорения работы приложения"""
    if dist_type == "Нормальное":
        return np.random.normal(mu, sigma, size)
    elif dist_type == "Равномерное":
        return np.random.uniform(0, 1, size)
    elif dist_type == "Экспоненциальное":
        return np.random.exponential(1.0, size)
    elif dist_type == "Бимодальное":
        h = size // 2
        return np.concatenate([np.random.normal(-2, 1, h), np.random.normal(2, 1, size-h)])
    elif dist_type == "Хи-квадрат":
        df = 4  # Степени свободы
        return np.random.chisquare(df, size)
    elif dist_type == "Биномиальное":
        return np.random.binomial(20, 0.5, size)
    elif dist_type == "Пуассона":
        return np.random.poisson(5, size)
    else:
        # Возвращаем нормальное распределение по умолчанию
        return np.random.normal(mu, sigma, size)

# Функция для кэширования параметров распределений
@st.cache_data
def generate_with_params(_dist_type, size, **params):
    """Генерирует данные с параметрами и кэшированием"""
    if _dist_type == "Нормальное":
        return np.random.normal(params.get('mean', 0), params.get('sd', 1), size)
    elif _dist_type == "Равномерное":
        return np.random.uniform(params.get('a', 0), params.get('b', 1), size)
    elif _dist_type == "Экспоненциальное":
        return np.random.exponential(1/params.get('lambda', 1), size)
    elif _dist_type == "Биномиальное":
        return np.random.binomial(params.get('n', 20), params.get('p', 0.5), size)
    elif _dist_type == "Пуассона":
        return np.random.poisson(params.get('mu', 5), size)
    elif _dist_type == "Бимодальное":
        h = size // 2
        return np.concatenate([
            np.random.normal(params.get('mean1', -2), params.get('sd1', 1), h),
            np.random.normal(params.get('mean2', 2), params.get('sd2', 1), size-h)
        ])
    else:
        return np.random.normal(0, 1, size)

# Функция для кэширования малых выборок
@st.cache_data
def generate_small_samples(dist_type, n_small, num_sim):
    """Генерирует малые выборки с кэшированием"""
    samples = np.zeros((num_sim, n_small))
    for i in range(num_sim):
        if dist_type == "Нормальное":
            samples[i] = np.random.normal(0, 1, n_small)
        elif dist_type == "Равномерное":
            samples[i] = np.random.uniform(0, 1, n_small)
        elif dist_type == "Экспоненциальное":
            samples[i] = np.random.exponential(1.0, n_small)
        elif dist_type == "Бимодальное":
            h = n_small // 2
            samples[i] = np.concatenate([np.random.normal(-2, 1, h), np.random.normal(2, 1, n_small-h)])
    return samples

# Функция для безопасных вычислений статистик
def safe_stats(data, func_name):
    """Безопасно вычисляет статистические метрики с обработкой ошибок"""
    try:
        if func_name == "mean":
            return np.mean(data)
        elif func_name == "median":
            return np.median(data)
        elif func_name == "std":
            return np.std(data)
        elif func_name == "min":
            return np.min(data)
        elif func_name == "max":
            return np.max(data)
        elif func_name == "skew":
            return stats.skew(data)
        elif func_name == "kurtosis":
            return stats.kurtosis(data)
        else:
            return None
    except Exception as e:
        if "debug_mode" in st.session_state and st.session_state.debug_mode:
            st.write(f"Ошибка при вычислении {func_name}: {str(e)}")
        return None

# Функция для форматирования статистик
def format_stat(data, func_name, label, precision=4):
    """Форматирует статистику для вывода с обработкой ошибок"""
    value = safe_stats(data, func_name)
    if value is not None:
        return f"{label}: {value:.{precision}f}"
    else:
        return f"{label}: невозможно вычислить"

# Кэшируем вычисление кумулятивных средних для закона больших чисел
@st.cache_data
def calculate_cumulative_mean(data):
    """Кэширует расчет кумулятивных средних"""
    return np.cumsum(data) / np.arange(1, len(data)+1)
# --- Настройка страницы и боковой панели с документацией ---
sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Демоверсия вероятностных законов", layout="wide")

# Сайдбар: интерактивная документация и помощь
with st.sidebar:
    st.header("📖 Справка и формулы")
    st.markdown("""
    **Закон трёх сигм**  
    [Статья на Wikipedia](https://en.wikipedia.org/wiki/68–95–99.7_rule)
    """, unsafe_allow_html=True)
    st.markdown("""
    **Центральная предельная теорема**  
    При больших n распределение средних стремится к нормальному (среднее μ, σ/√n)  
    [Статья на Wikipedia](https://ru.wikipedia.org/wiki/Центральная_предельная_теорема)
    """, unsafe_allow_html=True)
    st.markdown("""
    **Закон больших чисел**  
    Среднее сходится к математическому ожиданию при n→∞  
    [Статья на Wikipedia](https://ru.wikipedia.org/wiki/Закон_больших_чисел)
    """, unsafe_allow_html=True)
    st.markdown("""
    **Закон малых чисел**  
    Ошибки при обобщении малых выборок  
    [Статья на Wikipedia](https://ru.wikipedia.org/wiki/Закон_малых_чисел_(психология))
    """, unsafe_allow_html=True)
    st.markdown("""
    **Регрессия к среднему**  
    Ошибки из-за экстремальных выбросов
    [Статья на Wikipedia](https://ru.wikipedia.org/wiki/Регрессия_к_среднему)
    """, unsafe_allow_html=True)

   
st.title("📊 Демонстрация вероятностных законов")
tabs = st.tabs(["Закон трёх сигм", "ЦПТ", "ЗБЧ", "Малые выборки","Сравнение распределений","Регрессия к среднему","Проверь свои знания"])

# === 1. Закон трёх сигм ===
with tabs[0]:
    st.header("Закон трёх сигм (эмпирическое правило)")
    mu = st.slider("Среднее (μ)", 20, 80, 50)
    sigma = st.slider("Стандартное отклонение (σ)", 1, 30, 10)
    size = st.slider("Размер выборки", 1000, 50000, 10000, step=1000)

    data = generate_data("Нормальное", size, mu, sigma)
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
        "68% значений\n(±1σ)", xy=(mu, ymax * 0.9), xycoords='data',
        xytext=(0, -40), textcoords='offset points', ha='center', va='top',
        arrowprops=dict(arrowstyle='->', color='black'), fontsize=9
    )
    ax.annotate(
        "95% значений\n(±2σ)", xy=(mu - 2*sigma, ymax * 0.6), xycoords='data',
        xytext=(-40, -10), textcoords='offset points', ha='left', va='top',
        arrowprops=dict(arrowstyle='->', color='black'), fontsize=9
    )
    ax.annotate(
        "Почти все значения\nв пределах ±3σ", xy=(mu + 2.5*sigma, ymax * 0.6), xycoords='data',
        xytext=(40, -10), textcoords='offset points', ha='right', va='top',
        arrowprops=dict(arrowstyle='->', color='black'), fontsize=9
    )

    ax.set_title(f"Закон трёх сигм (μ = {mu}, σ = {sigma})")
    ax.set_xlabel("Значение")
    ax.set_ylabel("Плотность вероятности")
    ax.legend()

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    # Скачать
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📥 Скачать график (PNG)", buf.getvalue(), "three_sigma.png", "image/png")

    # Описание и ограничения
    st.markdown(f"""
**Пояснение**  
График демонстрирует _закон трёх сигм_, согласно которому:
- около **68%** значений попадают в диапазон ±1σ от среднего,
- около **95%** — в диапазон ±2σ,
- около **99.7%** — в диапазон ±3σ.

Здесь: μ = {mu}, σ = {sigma}, n = {size}.

---  
🔴 **Ограничения**:
- Работает только при приближении к нормальному распределению.
- Неприменим к мощно скошенным, мультипиковым, дискретным распределениям.
- На маленьких выборках может не соблюдаться — выборочная дисперсия ещё «прыгает».
- Выбросы и шум нарушают правило: в реальной жизни за 3 сигмы может выходить и 5% наблюдений.

🔵 **Преимущества**:
- Простой эвристический метод оценки разброса.
- Основа контроля качества (Six Sigma).
- Легко визуализируется и воспринимается.
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
        if dist == "Равномерное": return np.random.uniform(0, 1, n)
        if dist == "Экспоненциальное": return np.random.exponential(1.0, n)
        if dist == "Бимодальное":
            h = n // 2
            return np.concatenate([np.random.normal(-2, 1, h), np.random.normal(2, 1, n-h)])
        return np.random.normal(0, 1, n)

    @st.cache_data
    def generate_clt_means(dist_type, sample_size, num_samples):
       """Кэширует вычисление выборочных средних для ЦПТ"""
       return [np.mean(generate_data(dist_type, sample_size)) for _ in range(num_samples)]

    means = generate_clt_means(dist_type, sample_size, num_samples)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.histplot(means, bins=30, kde=True, ax=ax2, color="skyblue", edgecolor='black')

    ax2.set_title(f"ЦПТ: Средние {num_samples} выборок ({dist_type}, n = {sample_size})")
    ax2.set_xlabel("Среднее значение выборки")
    ax2.set_ylabel("Частота")

    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)

    buf = BytesIO()
    fig2.savefig(buf, format="png")
    st.download_button("📥 Скачать график (PNG)", buf.getvalue(), "clt.png", "image/png")

# Анимация ЦПТ
    animate_clt = st.checkbox("Анимировать эффект увеличения размера выборки")
    
    if animate_clt:
        # Создаем единый контейнер для графика
        animation_container = st.container()
        chart_placeholder = animation_container.empty()
        info_placeholder = animation_container.empty()
        
        # Создаем слайдеры для контроля анимации
        animation_speed = st.slider("Скорость анимации", 0.1, 2.0, 0.5, 0.1)
        display_progress = st.checkbox("Показывать прогрессбар", value=True)
        
        # Определяем размеры выборок для анимации
        sample_sizes = [2, 5, 10, 20, 30, 50, 100]
        
        # Создаем прогрессбар, если включен
        if display_progress:
            progress_bar = st.progress(0)
        
        # Запускаем анимацию
        for i, n in enumerate(sample_sizes):
            # Обновляем прогресс
            if display_progress:
                progress_bar.progress((i + 1) / len(sample_sizes))
            
            # Генерация данных для текущего размера выборки
            @st.cache_data
            def generate_clt_animation_means(dist_type, n, num_samples):
                return [np.mean(generate_data(dist_type, n)) for _ in range(num_samples)]

            means = generate_clt_animation_means(dist_type, n, num_samples)
            
            # Создание нового графика
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(means, bins=30, kde=True, ax=ax, color="skyblue", edgecolor='black')
            
            # Настраиваем график
            ax.set_title(f"Распределение выборочных средних (n = {n})")
            ax.set_xlabel("Среднее значение выборки")
            ax.set_ylabel("Частота")
            fig.tight_layout()
            
            # Добавляем теоретические статистики
            std_dev = np.std(means)
            ax.axvline(np.mean(means), color='red', linestyle='--', 
                      label=f'Среднее: {np.mean(means):.3f}, σ: {std_dev:.3f}')
            ax.legend()
            
            # Обновляем один и тот же контейнер
            with chart_placeholder:
                st.pyplot(fig)
            
            # Обновляем информацию о текущем шаге
            with info_placeholder:
                st.info(f"Размер выборки: {n}. Обратите внимание, как распределение становится более нормальным, а разброс уменьшается с увеличением n.")
            
            plt.close(fig)  # Закрываем фигуру для освобождения памяти
            
            # Ждем перед показом следующего графика
            time.sleep(1/animation_speed)
        
        if display_progress:
            # Заполняем прогрессбар до конца
            progress_bar.progress(1.0)
        
        # Итоговое сообщение после анимации
        st.success("""
        🎉 **Анимация завершена!** 
        
        Вы наблюдали практическую демонстрацию Центральной предельной теоремы:
        1. С увеличением размера выборки (n) распределение выборочных средних становится ближе к нормальному
        2. Стандартное отклонение уменьшается пропорционально √n
        3. Даже для распределений, далеких от нормального, средние значения распределяются нормально
        
        Это одна из причин, почему нормальное распределение так часто встречается в статистике!
        """)


    st.markdown(f"""
**Пояснение**  
_Центральная предельная теорема_ утверждает, что независимо от распределения исходных данных распределение **средних значений** будет стремиться к нормальному при увеличении n.

Здесь: распределение = {dist_type.lower()}, размер n = {sample_size}, число выборок = {num_samples}.

---  
🔴 **Ограничения**:
- Нужны независимые и одинаково распределённые данные (i.i.d.).
- Для нестационарных процессов (с трендом) не работает.
- Для тяжёлых хвостов может понадобиться n ≥ 100.
- При бесконечной дисперсии (напр. распределение Коши) неприменима.

🔵 **Преимущества**:
- Основа большинства статистических тестов и доверительных интервалов.
- Обосновывает приближение к нормали при агрегации.
- Универсальна для разных типов данных.
""")

# === 3. Закон больших чисел ===
with tabs[2]:
    st.header("Закон больших чисел")
    dist_type_lln = st.selectbox(
        "Распределение данных",
        ["Нормальное", "Равномерное", "Экспоненциальное"], key="lln"
    )
    trials = st.slider("Количество испытаний", 100, 20000, 10000, step=100)

    def sample(dist, n):
        if dist == "Равномерное": return np.random.uniform(0, 1, n)
        if dist == "Экспоненциальное": return np.random.exponential(1.0, n)
        return np.random.normal(0, 1, n)

    data_lln = generate_data(dist_type_lln, trials)
   cumulative = calculate_cumulative_mean(data_lln)
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
_Закон больших чисел_ утверждает, что среднее по n независимым наблюдениям сходится к математическому ожиданию.

Здесь: распределение = {dist_type_lln.lower()}, испытаний = {trials}.

---  
🔴 **Ограничения**:
- Данные должны быть независимыми и одинаково распределёнными.
- Сходимость может быть медленной при высокой вариабельности.
- Ничего не говорит о скорости сходимости.

🔵 **Преимущества**:
- Обеспечивает консистентность оценки среднего при больших n.
- Обосновывает надежность долгосрочных прогнозов.
- Широко используется в экономике и страховании.
""")

# === 4. Закон малых выборок ===
with tabs[3]:
    st.header("Закон малых выборок")
    st.markdown("""
Закон малых чисел — неформальный термин из психологии: люди переоценивают надежность выводов при малых выборках.
Например, при n=10 наблюдений статистическая нестабильность может давать сильно ошибочные результаты.
""")
    
    # Параметры
    dist_small = st.selectbox(
        "Исходное распределение",
        ["Нормальное","Равномерное","Экспоненциальное","Бимодальное"]
    )
    n_small = st.slider("Размер маленькой выборки (n)", 2, 30, 5)
    num_sim = st.slider("Количество симуляций", 100, 2000, 500, step=100)
    show_mean = st.checkbox("Показать теоретическое среднее", value=True)

    # Кэшируем с помощью lru_cache можно было бы, но для простоты
    # Генерация и расчет
    samples = generate_small_samples(dist_small, n_small, num_sim)
    # Здесь для биномиального пример; аналогично можно менять распределение
    means_small = samples.mean(axis=1)

    # Гистограмма
    fig4, ax4 = plt.subplots(figsize=(10,5))
    ax4.hist(means_small, bins=20, density=True, alpha=0.7, edgecolor='black')
    if show_mean:
        ax4.axvline(np.mean(means_small), color='green', linestyle='--', label='Эмпирическое среднее')
    ax4.set_title(f"Закон малых выборок (n={n_small}, симуляций={num_sim})")
    ax4.set_xlabel("Среднее значение")
    ax4.set_ylabel("Плотность")
    if show_mean:
        ax4.legend()
    fig4.tight_layout()
    st.pyplot(fig4, use_container_width=True)

    # Скачать
    buf4 = BytesIO()
    fig4.savefig(buf4, format="png")
    st.download_button("📥 Скачать гистограмму (PNG)", buf4.getvalue(), "small_law.png", "image/png")

    # Описание и метрики
    st.markdown(f"""
**Пояснение**  
При малом n ({n_small}) распределение выборочных средних остаётся широким и нестабильным.

Среднее по симуляциям: {means_small.mean():.3f}, σ эмпирическое: {means_small.std(ddof=1):.3f}.

---  
🔴 **Ограничения и риски**:
- Высокая дисперсия оценок среднего.
- n < 30 — ЦПТ ещё не действует полностью.
- Для тяжелых хвостов требуются большие n.

🔵 **Преимущества**:
- Демонстрирует важность объема выборки.
- Помогает понять, когда результаты малой выборки ненадежны.
""")

# === 5. Сравнение распределений ===
with tabs[4]:
    st.header("Сравнение распределений")
    st.markdown("Сравнение различных вероятностных распределений и их характеристик.")
    
    # Выбор распределений для сравнения
    col1, col2 = st.columns(2)
    with col1:
        dist1 = st.selectbox(
            "Первое распределение", 
            ["Нормальное", "Равномерное", "Экспоненциальное", "Биномиальное", "Пуассона"]
        )
        
        # Параметры для первого распределения
        if dist1 == "Нормальное":
            mean1 = st.slider("Среднее μ (1)", -10.0, 10.0, 0.0)
            sd1 = st.slider("Стандартное отклонение σ (1)", 0.1, 5.0, 1.0)
        elif dist1 == "Равномерное":
            a1 = st.slider("Минимум a (1)", -10.0, 10.0, 0.0)
            b1 = st.slider("Максимум b (1)", a1+0.1, a1+20.0, a1+1.0)
        elif dist1 == "Экспоненциальное":
            lambda1 = st.slider("Лямбда λ (1)", 0.1, 5.0, 1.0)
        elif dist1 == "Биномиальное":
            n1 = st.slider("Количество испытаний n (1)", 1, 100, 20)
            p1 = st.slider("Вероятность успеха p (1)", 0.0, 1.0, 0.5)
        elif dist1 == "Пуассона":
            mu1 = st.slider("Интенсивность λ (1)", 0.1, 20.0, 5.0)

    with col2:
        dist2 = st.selectbox(
            "Второе распределение", 
            ["Нормальное", "Равномерное", "Экспоненциальное", "Биномиальное", "Пуассона"],
            index=1
        )
        
        # Параметры для второго распределения
        if dist2 == "Нормальное":
            mean2 = st.slider("Среднее μ (2)", -10.0, 10.0, 0.0)
            sd2 = st.slider("Стандартное отклонение σ (2)", 0.1, 5.0, 1.0)
        elif dist2 == "Равномерное":
            a2 = st.slider("Минимум a (2)", -10.0, 10.0, 0.0)
            b2 = st.slider("Максимум b (2)", a2+0.1, a2+20.0, a2+1.0)
        elif dist2 == "Экспоненциальное":
            lambda2 = st.slider("Лямбда λ (2)", 0.1, 5.0, 1.0)
        elif dist2 == "Биномиальное":
            n2 = st.slider("Количество испытаний n (2)", 1, 100, 20)
            p2 = st.slider("Вероятность успеха p (2)", 0.0, 1.0, 0.5)
        elif dist2 == "Пуассона":
            mu2 = st.slider("Интенсивность λ (2)", 0.1, 20.0, 5.0)
    
    # Размер выборки
    sample_size = st.slider("Размер выборки", 1000, 10000, 5000)
    
    # Генерация данных
    def generate_dist_data(dist_type, sample_size, params):
        if dist_type == "Нормальное":
            return np.random.normal(params.get('mean', 0), params.get('sd', 1), sample_size)
        elif dist_type == "Равномерное":
            return np.random.uniform(params.get('a', 0), params.get('b', 1), sample_size)
        elif dist_type == "Экспоненциальное":
            return np.random.exponential(1/params.get('lambda', 1), sample_size)
        elif dist_type == "Биномиальное":
            return np.random.binomial(params.get('n', 20), params.get('p', 0.5), sample_size)
        elif dist_type == "Пуассона":
            return np.random.poisson(params.get('mu', 5), sample_size)
    
    # Параметры для распределений
    params1 = {}
    if dist1 == "Нормальное":
        params1 = {'mean': mean1, 'sd': sd1}
    elif dist1 == "Равномерное":
        params1 = {'a': a1, 'b': b1}
    elif dist1 == "Экспоненциальное":
        params1 = {'lambda': lambda1}
    elif dist1 == "Биномиальное":
        params1 = {'n': n1, 'p': p1}
    elif dist1 == "Пуассона":
        params1 = {'mu': mu1}
    
    params2 = {}
    if dist2 == "Нормальное":
        params2 = {'mean': mean2, 'sd': sd2}
    elif dist2 == "Равномерное":
        params2 = {'a': a2, 'b': b2}
    elif dist2 == "Экспоненциальное":
        params2 = {'lambda': lambda2}
    elif dist2 == "Биномиальное":
        params2 = {'n': n2, 'p': p2}
    elif dist2 == "Пуассона":
        params2 = {'mu': mu2}
    
    # Генерация данных
    @st.cache_data
    def generate_comparison_data(dist1, dist2, params1, params2, sample_size):
    """Кэширует генерацию данных для сравнения распределений"""
    data1 = generate_with_params(dist1, sample_size, **params1)
    data2 = generate_with_params(dist2, sample_size, **params2)
    return data1, data2

data1, data2 = generate_comparison_data(dist1, dist2, params1, params2, sample_size)
    
    # Построение графика
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Гистограммы с прозрачностью
    sns.histplot(data1, bins=30, alpha=0.5, label=f"{dist1}", color="blue", kde=True, ax=ax)
    sns.histplot(data2, bins=30, alpha=0.5, label=f"{dist2}", color="red", kde=True, ax=ax)
    
    # Настройка графика
    ax.set_title(f"Сравнение распределений: {dist1} vs {dist2}")
    ax.set_xlabel("Значение")
    ax.set_ylabel("Частота")
    ax.legend()
    
    # Отображение графика
    st.pyplot(fig, use_container_width=True)
    
    # Добавление статистических характеристик
    stats_col1, stats_col2 = st.columns(2)
    
    # Безопасный расчет статистики с обработкой ошибок
    try:
        with stats_col1:
            st.subheader(f"Статистика: {dist1}")
            st.write(f"Среднее: {np.mean(data1):.4f}")
            st.write(f"Медиана: {np.median(data1):.4f}")
            st.write(f"Стандартное отклонение: {np.std(data1):.4f}")
            st.write(f"Минимум: {np.min(data1):.4f}")
            st.write(f"Максимум: {np.max(data1):.4f}")
            
            # Используем try-except для асимметрии и эксцесса, так как они могут вызывать ошибки
            try:
                skewness = stats.skew(data1)
                st.write(f"Асимметрия: {skewness:.4f}")
            except:
                st.write("Асимметрия: невозможно вычислить")
                
            try:
                kurtosis = stats.kurtosis(data1)
                st.write(f"Эксцесс: {kurtosis:.4f}")
            except:
                st.write("Эксцесс: невозможно вычислить")
        
        with stats_col2:
            st.subheader(f"Статистика: {dist2}")
            st.write(f"Среднее: {np.mean(data2):.4f}")
            st.write(f"Медиана: {np.median(data2):.4f}")
            st.write(f"Стандартное отклонение: {np.std(data2):.4f}")
            st.write(f"Минимум: {np.min(data2):.4f}")
            st.write(f"Максимум: {np.max(data2):.4f}")
            
            try:
                skewness = stats.skew(data2)
                st.write(f"Асимметрия: {skewness:.4f}")
            except:
                st.write("Асимметрия: невозможно вычислить")
                
            try:
                kurtosis = stats.kurtosis(data2)
                st.write(f"Эксцесс: {kurtosis:.4f}")
            except:
                st.write("Эксцесс: невозможно вычислить")
    except Exception as e:
        st.error(f"Произошла ошибка при расчете статистики: {str(e)}")
    
    # Кнопка для скачивания
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    st.download_button("📥 Скачать график сравнения (PNG)", buf.getvalue(), "comparison.png", "image/png")
    
    # Информационный блок
    st.markdown("""
    **Пояснение**
    Это сравнение позволяет визуально наблюдать различия между вероятностными распределениями и их статистическими характеристиками.
    
    Особое внимание обратите на:
    - Форму распределения (симметричность, пики)
    - Хвосты распределения (тяжесть, скорость убывания)
    - Диапазон значений
    - Статистические метрики (среднее, медиана, стандартное отклонение)
    """)

# === 6. Регрессия к среднему ===
with tabs[5]:
    st.header("Регрессия к среднему")
    st.markdown("""
    **Регрессия к среднему** — статистический феномен, когда переменная с экстремальным значением 
    при повторном измерении стремится ближе к среднему значению. Этот феномен часто ошибочно 
    принимают за реальный эффект вмешательства.
    """)
    
    # Параметры симуляции
    col1, col2 = st.columns(2)
    with col1:
        mu_reg = st.slider("Истинное среднее популяции", 0, 100, 50)
        sigma_reg = st.slider("Стандартное отклонение", 5, 30, 15)
    
    with col2:
        n_subjects = st.slider("Количество субъектов", 20, 500, 100)
        threshold_percentile = st.slider("Порог отбора (процентиль)", 70, 95, 80)
    
    # Генерация данных для первого и второго измерений
    # Зафиксируем начальное состояние для воспроизводимости, но добавим вариативность на разных запусках
    import time
    seed_value = int(time.time()) % 1000  # Используем время как источник случайности
    np.random.seed(seed_value)
    
    try:
        # Истинные способности (неизвестны наблюдателю)
        true_abilities = np.random.normal(mu_reg, sigma_reg/2, n_subjects)
        
        # Первое измерение (тест 1): истинная способность + случайный шум
        test1_scores = true_abilities + np.random.normal(0, sigma_reg/2, n_subjects)
        
        # Второе измерение (тест 2): также истинная способность + новый случайный шум
        test2_scores = true_abilities + np.random.normal(0, sigma_reg/2, n_subjects)
        
        # Находим порог для выбора "лучших" субъектов
        threshold = np.percentile(test1_scores, threshold_percentile)
        
        # Выбираем "лучших" субъектов по первому тесту
        best_subjects_mask = test1_scores >= threshold
        
        # Проверка, что есть хотя бы один "лучший" субъект
        if np.sum(best_subjects_mask) > 0:
            best_subjects_test1 = test1_scores[best_subjects_mask]
            best_subjects_test2 = test2_scores[best_subjects_mask]
            
            # Средние значения
            all_mean_test1 = np.mean(test1_scores)
            all_mean_test2 = np.mean(test2_scores)
            best_mean_test1 = np.mean(best_subjects_test1)
            best_mean_test2 = np.mean(best_subjects_test2)
            
            # Создаем график
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Разброс всех точек
            ax.scatter(test1_scores, test2_scores, alpha=0.4, label="Все субъекты", color="gray")
            
            # Выделяем лучших субъектов
            ax.scatter(best_subjects_test1, best_subjects_test2, alpha=0.6, 
                       label=f"Лучшие субъекты (>{threshold_percentile}%)", color="red")
            
            # Линия y=x для сравнения
            min_val = min(np.min(test1_scores), np.min(test2_scores))
            max_val = max(np.max(test1_scores), np.max(test2_scores))
            ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, label="Линия y=x")
            
            # Средние линии
            ax.axvline(all_mean_test1, color='blue', linestyle=':', alpha=0.5, 
                      label=f"Среднее Тест 1 (все): {all_mean_test1:.1f}")
            ax.axhline(all_mean_test2, color='green', linestyle=':', alpha=0.5, 
                      label=f"Среднее Тест 2 (все): {all_mean_test2:.1f}")
            
            # Средние для лучших
            ax.axvline(best_mean_test1, color='red', linestyle='--', alpha=0.5, 
                      label=f"Среднее Тест 1 (лучшие): {best_mean_test1:.1f}")
            ax.axhline(best_mean_test2, color='orange', linestyle='--', alpha=0.5, 
                      label=f"Среднее Тест 2 (лучшие): {best_mean_test2:.1f}")
            
            # Настройка графика
            ax.set_title("Регрессия к среднему")
            ax.set_xlabel("Результаты первого теста")
            ax.set_ylabel("Результаты второго теста")
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper left')
            
            # Отображение
            st.pyplot(fig, use_container_width=True)
            
            # Разница в средних для лучших субъектов
            diff = best_mean_test1 - best_mean_test2
            pct_diff = (diff / best_mean_test1) * 100 if best_mean_test1 != 0 else 0
            
            # Результаты анализа
            st.markdown(f"""
            ### Результаты анализа
            
            **Наблюдения:**
            - Среднее значение первого теста (все субъекты): {all_mean_test1:.2f}
            - Среднее значение второго теста (все субъекты): {all_mean_test2:.2f}
            - Среднее значение первого теста (лучшие субъекты): {best_mean_test1:.2f}
            - Среднее значение второго теста (лучшие субъекты): {best_mean_test2:.2f}
            - **Регрессия к среднему**: {diff:.2f} пунктов ({pct_diff:.1f}%)
            """)
            
            # Кнопка для скачивания
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=300)
            st.download_button("📥 Скачать график (PNG)", buf.getvalue(), "regression_to_mean.png", "image/png")
        else:
            st.warning("Не найдено ни одного субъекта, удовлетворяющего критерию отбора. Попробуйте снизить порог.")
    
    except Exception as e:
        st.error(f"Произошла ошибка при построении графика: {str(e)}")
    
    # Объяснение эффекта
    st.markdown("""
    ### Объяснение эффекта
    
    📊 **Суть регрессии к среднему:**  
    Если мы отбираем субъектов по высоким результатам первого измерения, во втором измерении 
    они в среднем показывают результаты ближе к среднему значению популяции. Это **не** означает, что 
    навыки ухудшились, а является статистическим артефактом.
    
    🔍 **Практические последствия:**
    - Этот эффект часто принимают за действие вмешательства
    - "Проклятие обложки Sports Illustrated": спортсмены часто снижают результаты после попадания на обложку
    - "Эффект лечения" при обращении с крайними симптомами: пациенты часто "улучшаются" без лечения
    - Оценка эффективности тренингов, начатых после провальных результатов
    """)
    
    # Дополнительная теоретическая информация
    with st.expander("Теоретическое обоснование"):
        st.markdown("""
        **Математическая основа регрессии к среднему:**
        
        Корреляция между двумя измерениями одной и той же величины обычно меньше 1 из-за случайной вариации. 
        При отборе по крайним значениям (высоким или низким) в первом измерении, второе измерение будет иметь 
        меньшее отклонение от среднего значения популяции.
        
        Если X и Y - два измерения с одинаковым средним μ и стандартным отклонением σ, и корреляцией ρ, то:
        
        E[Y|X=x] = μ + ρ(x-μ)
        
        Где E[Y|X=x] - ожидаемое значение Y при условии X=x. Так как |ρ| < 1 для реальных измерений с шумом,
        разница между x и μ сокращается на множитель ρ.
        
        Чем больше случайной вариации в измерениях (меньше надежность теста), тем сильнее проявляется эффект регрессии к среднему.
        """)

with tabs[6]:
    st.header("📝 Проверь свои знания")
    
    # Выбор темы квиза
    quiz_topic = st.selectbox(
        "Выберите тему", 
        ["Закон трёх сигм", "Центральная предельная теорема", "Закон больших чисел"]
    )
    
    # Вопросы и ответы
    questions = {
        "Закон трёх сигм": [
            {
                "question": "Какой процент значений находится в пределах ±1σ от среднего в нормальном распределении?",
                "options": ["50%", "68%", "95%", "99.7%"],
                "correct": 1,
                "explanation": "По закону трёх сигм, около 68% значений находятся в пределах ±1σ от среднего."
            },
            # Другие вопросы
        ],
        # Другие темы
    }
    
    # Отображение вопросов
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
        
    for i, q in enumerate(questions[quiz_topic]):
        st.subheader(f"Вопрос {i+1}")
        st.write(q["question"])
        answer = st.radio("Выберите ответ:", q["options"], key=f"q_{quiz_topic}_{i}")
        
        if st.button("Проверить", key=f"check_{quiz_topic}_{i}"):
            if q["options"].index(answer) == q["correct"]:
                st.success("Правильно! " + q["explanation"])
                st.session_state.quiz_score += 1
            else:
                st.error("Неверно. " + q["explanation"])
    
    # Общий результат
    if st.button("Показать результат"):
        st.metric("Правильных ответов", f"{st.session_state.quiz_score}/{len(questions[quiz_topic])}")

       # Обработка ошибок и предупреждения
try:
    # Проверка наличия ошибок в графиках
    plt.close('all')  # Закрываем все открытые фигуры для предотвращения утечек памяти
except Exception as e:
    st.error(f"Произошла ошибка при обработке графиков: {str(e)}")

# Метрики и статистика использования
if "page_views" not in st.session_state:
    st.session_state.page_views = 0
st.session_state.page_views += 1

# Подвал с дополнительной информацией
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Дополнительные ресурсы")
    st.markdown("""
    - [Khan Academy: Статистика и теория вероятностей](https://www.khanacademy.org/math/statistics-probability)
    - [StatQuest with Josh Starmer](https://www.youtube.com/c/joshstarmer)
    - [Seeing Theory](https://seeing-theory.brown.edu/)
    - [Онлайн-калькуляторы вероятностных распределений](https://stattrek.com/online-calculator)
    """)

with col2:
    st.markdown("### О проекте")
    st.markdown("""
    Это приложение создано для интерактивного изучения статистических и вероятностных концепций. 
    
    Оно сочетает в себе теоретические принципы с практическими демонстрациями и симуляциями.
    
    Использование интерактивных элементов позволяет лучше понять, как работают статистические законы.
    """)

with col3:
    st.markdown("### Статистика использования")
    st.metric("Просмотров этой сессии", st.session_state.page_views)
    
    if st.button("📝 Оставить отзыв"):
        feedback = st.text_area("Ваши предложения по улучшению приложения:")
        if feedback:
            st.success("Спасибо за ваш отзыв! Мы учтем ваши предложения в будущих обновлениях.")

# Добавление шкалы времени изменений и обновлений
with st.expander("📅 История обновлений"):
    st.markdown("""
    **v2.0 (июнь 2025)**
    - Добавлены новые модули: Сравнение распределений, Регрессия к среднему, Распределение выборочного среднего, Доверительные интервалы
    - Улучшена производительность через кэширование данных
    - Добавлена обработка ошибок и оптимизированы вычисления
    
    **v1.1 (май 2025)**
    - Улучшены визуализации и аннотации графиков
    - Исправлены ошибки в модуле закона малых выборок
    
    **v1.0 (апрель 2025)**
    - Первоначальный релиз
    - Базовые модули: Закон трёх сигм, ЦПТ, ЗБЧ, Малые выборки
    """)

# Добавление справочного режима и гида для начинающих
with st.sidebar:
    st.markdown("### 🔰 Для начинающих")
    if st.checkbox("Включить справочный режим"):
        st.info("""
        **Как пользоваться приложением:**
        
        1. Выберите интересующую вкладку вверху страницы
        2. Настройте параметры с помощью слайдеров и выпадающих списков
        3. Изучите результаты симуляции и прочитайте объяснения
        4. Используйте кнопки "Скачать график" для сохранения визуализаций
        
        Экспериментируйте с разными параметрами, чтобы увидеть, как они влияют на результаты!
        """)

# Полезные советы по использованию
with st.sidebar:
    with st.expander("💡 Советы"):
        st.markdown("""
        **Советы по использованию:**
        
        * Используйте вкладки для переключения между разными вероятностными законами
        * Экспериментируйте с параметрами для наблюдения их влияния
        * Обратите внимание на аннотации на графиках - они объясняют ключевые моменты
        * Для анимации ЦПТ используйте чекбокс на вкладке ЦПТ
        * Проверьте свои знания в разделе "Проверь свои знания"
        * График можно увеличить, наведя курсор и используя инструменты просмотра
        
        При медленной работе приложения попробуйте:
        * Уменьшить размеры выборок
        * Уменьшить количество симуляций
        * Обновить страницу
        """)
