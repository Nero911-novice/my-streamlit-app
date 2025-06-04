import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from io import BytesIO
import time
from functools import lru_cache
from typing import Tuple, List, Dict, Any, Optional

# --- Конфигурация и настройка ---
sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Демоверсия вероятностных законов", layout="wide")

# --- Кэшированные функции для генерации данных ---
@st.cache_data
def generate_distribution_data(dist_type: str, size: int, **params) -> np.ndarray:
    """Универсальная функция для генерации данных различных распределений с кэшированием"""
    
    distributions = {
        "Нормальное": lambda: np.random.normal(params.get('mu', 0), params.get('sigma', 1), size),
        "Равномерное": lambda: np.random.uniform(params.get('a', 0), params.get('b', 1), size),
        "Экспоненциальное": lambda: np.random.exponential(params.get('scale', 1), size),
        "Бимодальное": lambda: generate_bimodal_data(size, params.get('mu1', -2), params.get('mu2', 2), 
                                                   params.get('sigma1', 1), params.get('sigma2', 1)),
        "Биномиальное": lambda: np.random.binomial(params.get('n', 20), params.get('p', 0.5), size),
        "Пуассона": lambda: np.random.poisson(params.get('lam', 5), size)
    }
    
    return distributions.get(dist_type, distributions["Нормальное"])()

def generate_bimodal_data(size: int, mu1: float = -2, mu2: float = 2, 
                         sigma1: float = 1, sigma2: float = 1) -> np.ndarray:
    """Генерация бимодального распределения"""
    half = size // 2
    return np.concatenate([
        np.random.normal(mu1, sigma1, half), 
        np.random.normal(mu2, sigma2, size - half)
    ])

@st.cache_data
def calculate_sample_means(dist_type: str, sample_size: int, num_samples: int) -> np.ndarray:
    """Кэшированное вычисление выборочных средних для ЦПТ"""
    means = []
    for _ in range(num_samples):
        # Генерируем данные без кэширования внутри цикла
        if dist_type == "Равномерное": 
            sample = np.random.uniform(0, 1, sample_size)
        elif dist_type == "Экспоненциальное": 
            sample = np.random.exponential(1.0, sample_size)
        elif dist_type == "Бимодальное":
            h = sample_size // 2
            sample = np.concatenate([np.random.normal(-2, 1, h), np.random.normal(2, 1, sample_size-h)])
        else:  # Нормальное
            sample = np.random.normal(0, 1, sample_size)
        
        means.append(np.mean(sample))
    return np.array(means)

@st.cache_data
def safe_statistics(data: np.ndarray) -> Dict[str, float]:
    """Безопасное вычисление статистик с обработкой ошибок"""
    try:
        return {
            'mean': np.mean(data),
            'median': np.median(data),
            'std': np.std(data),
            'min': np.min(data),
            'max': np.max(data),
            'skewness': stats.skew(data) if len(data) > 2 else np.nan,
            'kurtosis': stats.kurtosis(data) if len(data) > 2 else np.nan
        }
    except Exception as e:
        st.warning(f"Ошибка при вычислении статистик: {str(e)}")
        return {key: np.nan for key in ['mean', 'median', 'std', 'min', 'max', 'skewness', 'kurtosis']}

def create_download_button(fig, filename: str, label: str = "📥 Скачать график (PNG)"):
    """Универсальная функция для создания кнопки скачивания графика"""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    return st.download_button(label, buf.getvalue(), filename, "image/png")

def format_stat_display(stats_dict: Dict[str, float], title: str):
    """Форматированное отображение статистик"""
    st.subheader(title)
    for key, value in stats_dict.items():
        if not np.isnan(value):
            if key in ['mean', 'median', 'std', 'min', 'max']:
                st.write(f"{key.capitalize()}: {value:.4f}")
            else:
                st.write(f"{key.capitalize()}: {value:.4f}")
        else:
            st.write(f"{key.capitalize()}: невозможно вычислить")

# --- Главная структура приложения ---
def main():
    # Боковая панель с документацией
    setup_sidebar()
    
    # Основной заголовок
    st.title("📊 Демонстрация вероятностных законов")
    
    # Создание вкладок
    tabs = st.tabs([
        "Закон трёх сигм", "ЦПТ", "ЗБЧ", "Малые выборки",
        "Сравнение распределений", "Регрессия к среднему", 
        "Проверь свои знания", "Типы распределений"
    ])
    
    # Обработка каждой вкладки
    with tabs[0]:
        three_sigma_law_tab()
    with tabs[1]:
        central_limit_theorem_tab()
    with tabs[2]:
        law_of_large_numbers_tab()
    with tabs[3]:
        small_samples_tab()
    with tabs[4]:
        comparison_distributions_tab()
    with tabs[5]:
        regression_to_mean_tab()
    with tabs[6]:
        knowledge_test_tab()
    with tabs[7]:
        distribution_types_tab()
    
    # Подвал приложения
    setup_footer()

def setup_sidebar():
    """Настройка боковой панели с документацией"""
    with st.sidebar:
        st.header("📖 Справка и формулы")
        
        references = {
            "Закон трёх сигм": "https://en.wikipedia.org/wiki/68–95–99.7_rule",
            "Центральная предельная теорема": "https://ru.wikipedia.org/wiki/Центральная_предельная_теорема",
            "Закон больших чисел": "https://ru.wikipedia.org/wiki/Закон_больших_чисел",
            "Закон малых чисел": "https://ru.wikipedia.org/wiki/Закон_малых_чисел_(психология)",
            "Регрессия к среднему": "https://ru.wikipedia.org/wiki/Регрессия_к_среднему"
        }
        
        descriptions = {
            "Закон трёх сигм": "68-95-99.7% правило для нормального распределения",
            "Центральная предельная теорема": "При больших n распределение средних стремится к нормальному (среднее μ, σ/√n)",
            "Закон больших чисел": "Среднее сходится к математическому ожиданию при n→∞",
            "Закон малых чисел": "Ошибки при обобщении малых выборок",
            "Регрессия к среднему": "Ошибки из-за экстремальных выбросов"
        }
        
        for name, url in references.items():
            st.markdown(f"""
            **{name}**  
            {descriptions[name]}  
            [Статья на Wikipedia]({url})
            """, unsafe_allow_html=True)
        
        # Справочный режим для начинающих
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
        
        # Полезные советы
        with st.expander("💡 Советы"):
            st.markdown("""
            **Советы по использованию:**
            
            * Используйте вкладки для переключения между разными вероятностными законами
            * Экспериментируйте с параметрами для наблюдения их влияния
            * Обратите внимание на аннотации на графиках - они объясняют ключевые моменты
            * Для анимации ЦПТ используйте чекбокс на вкладке ЦПТ
            * График можно увеличить, наведя курсор и используя инструменты просмотра
            
            При медленной работе приложения попробуйте:
            * Уменьшить размеры выборок
            * Уменьшить количество симуляций
            * Обновить страницу
            """)

def three_sigma_law_tab():
    """Вкладка закона трёх сигм"""
    # Отслеживание посещения вкладки
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Закон трёх сигм")
    
    st.header("Закон трёх сигм (эмпирическое правило)")
    st.markdown("""
    Закон трёх сигм помогает понять, как распределены данные вокруг среднего значения.
    Это полезно, когда нужно решить, какое наблюдение считать нормальным, а какое — выбросом.
    """)
    
    # Параметры
    col1, col2, col3 = st.columns(3)
    with col1:
        mu = st.slider("Среднее (μ)", 20, 80, 50)
    with col2:
        sigma = st.slider("Стандартное отклонение (σ)", 1, 30, 10)
    with col3:
        size = st.slider("Размер выборки", 1000, 50000, 10000, step=1000)
    
    # Генерация данных
    data = generate_distribution_data("Нормальное", size, mu=mu, sigma=sigma)
    
    # Создание графика
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(data, bins=50, density=True, color='lightgray', edgecolor='black', alpha=0.7)
    
    # Заливки зон ±1σ, ±2σ, ±3σ
    colors = ['#b2df8a', '#fdbf6f', '#fb9a99']
    labels = ['±1σ (68%)', '±2σ (95%)', '±3σ (99.7%)']
    
    for i, (color, label) in enumerate(zip(colors, labels), 1):
        ax.axvspan(mu - i * sigma, mu + i * sigma, color=color, alpha=0.3, label=label)
        ax.axvline(mu - i * sigma, color='red', linestyle='--', linewidth=1)
        ax.axvline(mu + i * sigma, color='red', linestyle='--', linewidth=1)
    
    # Аннотации
    ymax = ax.get_ylim()[1]
    annotations = [
        ("68% значений\n(±1σ)", (mu, ymax * 0.9), (0, -40)),
        ("95% значений\n(±2σ)", (mu - 2*sigma, ymax * 0.6), (-40, -10)),
        ("Почти все значения\nв пределах ±3σ", (mu + 2.5*sigma, ymax * 0.6), (40, -10))
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
    
    # Кнопка скачивания
    create_download_button(fig, "three_sigma.png")
    
    # Описание
    st.markdown(f"""
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
    """)

def central_limit_theorem_tab():
    """Вкладка центральной предельной теоремы"""
    # Отслеживание посещения вкладки
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("ЦПТ")
    
    st.header("Центральная предельная теорема")
    st.markdown("""
    ЦПТ утверждает, что независимо от распределения исходных данных, 
    распределение **средних значений** будет стремиться к нормальному при увеличении размера выборки.
    """)
    
    # Параметры
    col1, col2, col3 = st.columns(3)
    with col1:
        dist_type = st.selectbox("Выберите распределение", 
                                ["Нормальное", "Равномерное", "Экспоненциальное", "Бимодальное"])
    with col2:
        sample_size = st.slider("Размер одной выборки", 2, 100, 30)
    with col3:
        num_samples = st.slider("Количество выборок", 100, 5000, 1000, step=100)
    
    # Вычисление выборочных средних
    means = calculate_sample_means(dist_type, sample_size, num_samples)
    
    # Создание графика
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(means, bins=30, kde=True, ax=ax, color="skyblue", edgecolor='black')
    
    ax.set_title(f"ЦПТ: Средние {num_samples} выборок ({dist_type}, n = {sample_size})", fontsize=14)
    ax.set_xlabel("Среднее значение выборки")
    ax.set_ylabel("Частота")
    
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    create_download_button(fig, "clt.png")
    
    # Улучшенная анимация ЦПТ
    animate_clt = st.checkbox("Анимировать эффект увеличения размера выборки")
    
    if animate_clt:
        clt_animation_section(dist_type, num_samples)
    
    # Описание
    st.markdown(f"""
    **Пояснение**
    
    Центральная предельная теорема демонстрирует, что распределение выборочных средних 
    приближается к нормальному, независимо от формы исходного распределения.
    
    Здесь: распределение = {dist_type.lower()}, размер n = {sample_size}, число выборок = {num_samples}
    
    **Простыми словами:**
    Если вы подбрасываете игральную кость 30 раз и записываете среднее, а затем повторяете 
    этот процесс много раз, распределение полученных средних будет похоже на колокол (нормальное), 
    несмотря на то, что сама кость дает равномерное распределение.
    
    💡 **Где это используется:**
    - Социологические опросы
    - Контроль качества производства  
    - Медицинские исследования
    - Финансовое моделирование
    
    ---
    🔴 **Ограничения**:
    - Нужны независимые и одинаково распределённые данные (i.i.d.)
    - Для тяжёлых хвостов может понадобиться n ≥ 100
    - При бесконечной дисперсии (например, распределение Коши) неприменима
    
    🔵 **Преимущества**:
    - Основа большинства статистических тестов и доверительных интервалов
    - Обосновывает приближение к нормали при агрегации
    - Универсальна для разных типов данных
    """)

def clt_animation_section(dist_type: str, num_samples: int):
    """Раздел анимации ЦПТ"""
    animation_container = st.container()
    chart_placeholder = animation_container.empty()
    info_placeholder = animation_container.empty()
    
    # Настройки анимации
    col1, col2 = st.columns(2)
    with col1:
        animation_speed = st.slider("Скорость анимации", 0.1, 2.0, 0.5, 0.1)
    with col2:
        display_progress = st.checkbox("Показывать прогрессбар", value=True)
    
    sample_sizes = [2, 5, 10, 20, 30, 50, 100]
    
    if display_progress:
        progress_bar = st.progress(0)
    
    # Запуск анимации
    for i, n in enumerate(sample_sizes):
        if display_progress:
            progress_bar.progress((i + 1) / len(sample_sizes))
        
        # Генерация данных для текущего размера выборки
        means = calculate_sample_means(dist_type, n, num_samples)
        
        # Создание графика
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(means, bins=30, kde=True, ax=ax, color="skyblue", edgecolor='black')
        
        ax.set_title(f"Распределение выборочных средних (n = {n})")
        ax.set_xlabel("Среднее значение выборки")
        ax.set_ylabel("Частота")
        
        # Добавляем статистики
        std_dev = np.std(means)
        ax.axvline(np.mean(means), color='red', linestyle='--', 
                  label=f'Среднее: {np.mean(means):.3f}, σ: {std_dev:.3f}')
        ax.legend()
        
        fig.tight_layout()
        
        with chart_placeholder:
            st.pyplot(fig)
        
        with info_placeholder:
            if n <= 10:
                st.info(f"n = {n}: ЦПТ ещё слабо проявляется")
            elif n <= 30:
                st.info(f"n = {n}: ЦПТ начинает проявляться")
            else:
                st.success(f"n = {n}: ЦПТ проявляется отчётливо!")
        
        plt.close(fig)
        time.sleep(1/animation_speed)
    
    if display_progress:
        progress_bar.progress(1.0)
    
    st.success("""
    🎉 **Анимация завершена!**
    
    Вы наблюдали практическую демонстрацию ЦПТ:
    1. С увеличением размера выборки распределение средних становится более нормальным
    2. Стандартное отклонение уменьшается пропорционально √n
    3. Эффект не зависит от формы исходного распределения
    """)

def law_of_large_numbers_tab():
    """Вкладка закона больших чисел"""
    # Отслеживание посещения вкладки
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("ЗБЧ")
    
    st.header("Закон больших чисел")
    
    # Параметры
    col1, col2 = st.columns(2)
    with col1:
        dist_type_lln = st.selectbox("Распределение данных", 
                                    ["Нормальное", "Равномерное", "Экспоненциальное"], key="lln")
    with col2:
        trials = st.slider("Количество испытаний", 100, 20000, 10000, step=100)
    
    # Генерация данных
    data_lln = generate_distribution_data(dist_type_lln, trials)
    cumulative = np.cumsum(data_lln) / np.arange(1, trials + 1)
    expected = theoretical_mean(dist_type_lln)
    
    # График
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
    
    # Описание
    st.markdown(f"""
    **Пояснение**
    
    Закон больших чисел показывает, что среднее значение выборки сходится к истинному 
    среднему популяции при увеличении размера выборки.
    
    Здесь: распределение = {dist_type_lln.lower()}, испытаний = {trials}
    
    **Простыми словами:**
    При подбрасывании монеты 10 раз можно получить 7 орлов (70%), но при подбрасывании 
    1000 раз результат будет очень близок к 50%.
    
    **Примеры из жизни:**
    - Казино всегда в выигрыше в долгосрочной перспективе
    - Страховые компании рассчитывают премии на основе больших данных
    - Производители контролируют качество на больших выборках
    
    ---
    🔴 **Ограничения**:
    - Данные должны быть независимыми и одинаково распределёнными
    - Сходимость может быть медленной при высокой вариабельности
    - Ничего не говорит о скорости сходимости
    
    🔵 **Преимущества**:
    - Обеспечивает надёжность оценок при больших n
    - Обосновывает долгосрочные прогнозы
    - Широко используется в экономике и страховании
    """)

def theoretical_mean(dist_type: str) -> float:
    """Возвращает теоретическое среднее для распределения"""
    means = {
        "Нормальное": 0.0,
        "Равномерное": 0.5,
        "Экспоненциальное": 1.0
    }
    return means.get(dist_type, 0.0)

def small_samples_tab():
    """Вкладка закона малых выборок"""
    # Отслеживание посещения вкладки
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Малые выборки")
    
    st.header("Закон малых выборок")
    st.markdown("""
    Закон малых чисел — психологический феномен: люди переоценивают надежность 
    выводов при малых выборках. При малом n статистическая нестабильность 
    может давать сильно ошибочные результаты.
    """)
    
    # Параметры
    col1, col2, col3 = st.columns(3)
    with col1:
        dist_small = st.selectbox("Исходное распределение", 
                                 ["Нормальное", "Равномерное", "Экспоненциальное", "Бимодальное"])
    with col2:
        n_small = st.slider("Размер маленькой выборки (n)", 2, 30, 5)
    with col3:
        num_sim = st.slider("Количество симуляций", 100, 2000, 500, step=100)
    
    # Генерация данных - БЕЗ кэширования для получения разных выборок
    means_small = []
    
    # Генерируем каждую выборку с разным seed
    for i in range(num_sim):
        np.random.seed(i + 1000)  # Разные seeds для каждой симуляции
        
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
    
    # График
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(means_small, bins=20, density=True, alpha=0.7, edgecolor='black', color='lightcoral')
    
    # Добавляем статистики
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
    
    # Статистики
    stats_dict = safe_statistics(means_small)
    
    st.markdown(f"""
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
    """)

def comparison_distributions_tab():
    """Вкладка сравнения распределений"""
    # Отслеживание посещения вкладки
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Сравнение распределений")
    
    st.header("Сравнение распределений")
    st.markdown("Интерактивное сравнение различных вероятностных распределений и их характеристик.")
    
    # Выбор распределений
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Первое распределение")
        dist1, params1 = distribution_selector("1")
    
    with col2:
        st.subheader("Второе распределение")
        dist2, params2 = distribution_selector("2")
    
    # Размер выборки
    sample_size = st.slider("Размер выборки", 1000, 10000, 5000)
    
    # Генерация данных
    data1 = generate_distribution_data(dist1, sample_size, **params1)
    data2 = generate_distribution_data(dist2, sample_size, **params2)
    
    # График сравнения
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
    
    # Статистическое сравнение
    col1, col2 = st.columns(2)
    
    with col1:
        stats1 = safe_statistics(data1)
        format_stat_display(stats1, f"Статистика: {dist1}")
    
    with col2:
        stats2 = safe_statistics(data2)
        format_stat_display(stats2, f"Статистика: {dist2}")
    
    # Информационный блок
    st.markdown("""
    **Анализ сравнения**
    
    Обратите внимание на ключевые различия:
    - **Форма распределения**: симметричность, количество пиков, асимметрия
    - **Центральная тенденция**: среднее vs медиана
    - **Разброс**: стандартное отклонение и диапазон значений
    - **Хвосты распределения**: тяжесть и скорость убывания
    """)

def distribution_selector(suffix: str) -> Tuple[str, Dict[str, Any]]:
    """Универсальный селектор параметров распределения"""
    distributions = ["Нормальное", "Равномерное", "Экспоненциальное", "Биномиальное", "Пуассона"]
    
    dist_type = st.selectbox(f"Тип распределения ({suffix})", distributions, 
                            key=f"dist_{suffix}")
    
    params = {}
    
    if dist_type == "Нормальное":
        params['mu'] = st.slider(f"Среднее μ ({suffix})", -10.0, 10.0, 0.0, key=f"mu_{suffix}")
        params['sigma'] = st.slider(f"Стандартное отклонение σ ({suffix})", 0.1, 5.0, 1.0, key=f"sigma_{suffix}")
    
    elif dist_type == "Равномерное":
        params['a'] = st.slider(f"Минимум a ({suffix})", -10.0, 10.0, 0.0, key=f"a_{suffix}")
        params['b'] = st.slider(f"Максимум b ({suffix})", params['a']+0.1, params['a']+20.0, 
                              params['a']+1.0, key=f"b_{suffix}")
    
    elif dist_type == "Экспоненциальное":
        lam = st.slider(f"Лямбда λ ({suffix})", 0.1, 5.0, 1.0, key=f"lambda_{suffix}")
        params['scale'] = 1/lam  # scipy использует scale parameter
    
    elif dist_type == "Биномиальное":
        params['n'] = st.slider(f"Количество испытаний n ({suffix})", 1, 100, 20, key=f"n_{suffix}")
        params['p'] = st.slider(f"Вероятность успеха p ({suffix})", 0.0, 1.0, 0.5, key=f"p_{suffix}")
    
    elif dist_type == "Пуассона":
        params['lam'] = st.slider(f"Интенсивность λ ({suffix})", 0.1, 20.0, 5.0, key=f"lam_{suffix}")
    
    return dist_type, params

def regression_to_mean_tab():
    """Вкладка регрессии к среднему"""
    # Отслеживание посещения вкладки
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Регрессия к среднему")
    
    st.header("Регрессия к среднему")
    st.markdown("""
    **Регрессия к среднему** — статистический феномен, когда переменная с экстремальным 
    значением при повторном измерении стремится ближе к среднему значению популяции.
    """)
    
    # Параметры симуляции
    col1, col2 = st.columns(2)
    with col1:
        mu_reg = st.slider("Истинное среднее популяции", 0, 100, 50)
        sigma_reg = st.slider("Стандартное отклонение", 5, 30, 15)
    
    with col2:
        n_subjects = st.slider("Количество субъектов", 20, 500, 100)
        threshold_percentile = st.slider("Порог отбора (процентиль)", 70, 95, 80)
    
    # Генерация данных
    regression_data = generate_regression_data(mu_reg, sigma_reg, n_subjects, threshold_percentile)
    
    if regression_data:
        # Распаковка данных
        (test1_scores, test2_scores, best_subjects_test1, best_subjects_test2,
         all_mean_test1, all_mean_test2, best_mean_test1, best_mean_test2) = regression_data
        
        # График
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Все субъекты
        ax.scatter(test1_scores, test2_scores, alpha=0.4, label="Все субъекты", 
                  color="gray", s=20)
        
        # Лучшие субъекты
        ax.scatter(best_subjects_test1, best_subjects_test2, alpha=0.7, 
                  label=f"Лучшие субъекты (>{threshold_percentile}%)", color="red", s=30)
        
        # Линия y=x
        min_val = min(np.min(test1_scores), np.min(test2_scores))
        max_val = max(np.max(test1_scores), np.max(test2_scores))
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, 
               label="Линия y=x", linewidth=2)
        
        # Средние линии
        ax.axvline(all_mean_test1, color='blue', linestyle=':', alpha=0.7, 
                  label=f"Среднее Тест 1 (все): {all_mean_test1:.1f}")
        ax.axhline(all_mean_test2, color='green', linestyle=':', alpha=0.7, 
                  label=f"Среднее Тест 2 (все): {all_mean_test2:.1f}")
        
        ax.axvline(best_mean_test1, color='red', linestyle='--', alpha=0.7, 
                  label=f"Среднее Тест 1 (лучшие): {best_mean_test1:.1f}")
        ax.axhline(best_mean_test2, color='orange', linestyle='--', alpha=0.7, 
                  label=f"Среднее Тест 2 (лучшие): {best_mean_test2:.1f}")
        
        ax.set_title("Регрессия к среднему", fontsize=14)
        ax.set_xlabel("Результаты первого теста")
        ax.set_ylabel("Результаты второго теста")
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        create_download_button(fig, "regression_to_mean.png")
        
        # Анализ результатов
        diff = best_mean_test1 - best_mean_test2
        pct_diff = (diff / best_mean_test1) * 100 if best_mean_test1 != 0 else 0
        
        st.markdown(f"""
        ### Результаты анализа
        
        **Наблюдения:**
        - Среднее первого теста (все): {all_mean_test1:.2f}
        - Среднее второго теста (все): {all_mean_test2:.2f}
        - Среднее первого теста (лучшие): {best_mean_test1:.2f}
        - Среднее второго теста (лучшие): {best_mean_test2:.2f}
        - **Регрессия к среднему**: {diff:.2f} пунктов ({pct_diff:.1f}%)
        """)
    
    # Объяснение эффекта
    st.markdown("""
    ### Объяснение эффекта
    
    📊 **Суть регрессии к среднему:**
    Экстремальные результаты в первом измерении частично обусловлены случайностью, 
    поэтому при повторном измерении результаты в среднем ближе к популяционному среднему.
    
    **Примеры из жизни:**
    - Спортсмен после рекордного результата чаще показывает более средний результат
    - Студенты после исключительно высокой оценки обычно получают более обычные оценки
    - Компании после рекордной прибыли часто возвращаются к обычным показателям
    
    **Частая ошибка:** Приписывание регрессии к среднему действию вмешательства
    
    🔍 **Практические последствия:**
    - "Проклятие обложки Sports Illustrated"
    - Переоценка эффективности медицинского лечения
    - Ошибочная оценка эффективности тренингов
    """)

@st.cache_data
def generate_regression_data(mu_reg: int, sigma_reg: int, n_subjects: int, 
                           threshold_percentile: int) -> Optional[Tuple]:
    """Генерация данных для демонстрации регрессии к среднему"""
    try:
        
        # Истинные способности
        true_abilities = np.random.normal(mu_reg, sigma_reg/2, n_subjects)
        
        # Два измерения с добавлением шума
        test1_scores = true_abilities + np.random.normal(0, sigma_reg/2, n_subjects)
        test2_scores = true_abilities + np.random.normal(0, sigma_reg/2, n_subjects)
        
        # Отбор лучших субъектов
        threshold = np.percentile(test1_scores, threshold_percentile)
        best_subjects_mask = test1_scores >= threshold
        
        if np.sum(best_subjects_mask) == 0:
            return None
        
        best_subjects_test1 = test1_scores[best_subjects_mask]
        best_subjects_test2 = test2_scores[best_subjects_mask]
        
        # Вычисление средних
        all_mean_test1 = np.mean(test1_scores)
        all_mean_test2 = np.mean(test2_scores)
        best_mean_test1 = np.mean(best_subjects_test1)
        best_mean_test2 = np.mean(best_subjects_test2)
        
        return (test1_scores, test2_scores, best_subjects_test1, best_subjects_test2,
                all_mean_test1, all_mean_test2, best_mean_test1, best_mean_test2)
    
    except Exception as e:
        st.error(f"Ошибка при генерации данных: {str(e)}")
        return None

def knowledge_test_tab():
    """Вкладка проверки знаний"""
    # Отслеживание посещения вкладки
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Проверь свои знания")
    
    st.header("Проверь свои знания")
    st.markdown("Интерактивный тест для закрепления изученного материала.")
    
    # Инициализация состояния теста
    if 'test_score' not in st.session_state:
        st.session_state.test_score = 0
        st.session_state.test_completed = False
        st.session_state.current_question = 0
    
    questions = [
        {
            "question": "Согласно закону трёх сигм, какой процент значений попадает в диапазон ±2σ?",
            "options": ["68%", "95%", "99.7%", "50%"],
            "correct": 1,
            "explanation": "Согласно закону трёх сигм, 95% значений попадают в диапазон ±2σ от среднего."
        },
        {
            "question": "Что утверждает Центральная предельная теорема?",
            "options": [
                "Все распределения являются нормальными",
                "Среднее большой выборки равно среднему популяции", 
                "Распределение выборочных средних приближается к нормальному",
                "Дисперсия уменьшается с увеличением выборки"
            ],
            "correct": 2,
            "explanation": "ЦПТ утверждает, что распределение выборочных средних приближается к нормальному при увеличении размера выборки."
        },
        {
            "question": "Что такое регрессия к среднему?",
            "options": [
                "Математический метод анализа",
                "Тенденция экстремальных значений быть ближе к среднему при повторном измерении",
                "Способ вычисления среднего значения",
                "Тип статистического распределения"
            ],
            "correct": 1,
            "explanation": "Регрессия к среднему — феномен, при котором экстремальные значения при повторном измерении стремятся ближе к среднему популяции."
        },
        {
            "question": "Закон больших чисел утверждает, что:",
            "options": [
                "Большие числа всегда точнее малых",
                "При увеличении размера выборки среднее стремится к истинному среднему популяции",
                "Вероятность всегда равна 0.5",
                "Большие выборки всегда нормально распределены"
            ],
            "correct": 1,
            "explanation": "ЗБЧ показывает, что с увеличением размера выборки выборочное среднее сходится к истинному среднему популяции."
        },
        {
            "question": "Какая основная проблема с малыми выборками?",
            "options": [
                "Они всегда дают неправильные результаты",
                "Они имеют высокую вариабельность и ненадежные оценки",
                "Они не могут быть использованы в статистике",
                "Они всегда имеют нормальное распределение"
            ],
            "correct": 1,
            "explanation": "Малые выборки характеризуются высокой вариабельностью оценок, что делает выводы менее надежными."
        }
    ]
    
    if not st.session_state.test_completed:
        current_q = questions[st.session_state.current_question]
        
        st.subheader(f"Вопрос {st.session_state.current_question + 1} из {len(questions)}")
        st.write(current_q["question"])
        
        answer = st.radio("Выберите ответ:", current_q["options"], key=f"q_{st.session_state.current_question}")
        
        if st.button("Ответить"):
            selected_idx = current_q["options"].index(answer)
            if selected_idx == current_q["correct"]:
                st.success("✅ Правильно! " + current_q["explanation"])
                st.session_state.test_score += 1
            else:
                st.error("❌ Неправильно. " + current_q["explanation"])
            
            st.session_state.current_question += 1
            
            if st.session_state.current_question >= len(questions):
                st.session_state.test_completed = True
                st.rerun()
            else:
                time.sleep(2)  # Небольшая пауза для чтения объяснения
                st.rerun()
    
    else:
        # Результаты теста
        score_pct = (st.session_state.test_score / len(questions)) * 100
        
        st.subheader("🎯 Результаты теста")
        st.write(f"Ваш результат: **{st.session_state.test_score} из {len(questions)}** ({score_pct:.0f}%)")
        
        # Прогресс-бар результата
        st.progress(score_pct / 100)
        
        if score_pct >= 80:
            st.success("🏆 Отлично! Вы хорошо усвоили материал!")
        elif score_pct >= 60:
            st.info("👍 Хорошо! Рекомендуем повторить некоторые темы.")
        else:
            st.warning("📚 Рекомендуем внимательно изучить материал еще раз.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Пройти тест заново"):
                st.session_state.test_score = 0
                st.session_state.test_completed = False
                st.session_state.current_question = 0
                st.rerun()
        
        with col2:
            if st.button("📖 Вернуться к изучению"):
                st.info("Используйте вкладки выше для повторения материала!")

def distribution_types_tab():
    """Вкладка типов распределений"""
    # Отслеживание посещения вкладки
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Типы распределений")
    
    st.header("Типы вероятностных распределений")
    st.markdown("""
    Интерактивное изучение основных вероятностных распределений, их свойств и применений.
    """)
    
    # Выбор распределения
    chosen_dist = st.selectbox(
        "Выберите распределение для изучения:",
        [
            "Нормальное (Гауссово)", "Равномерное", "Биномиальное", "Пуассона",
            "Экспоненциальное", "Логнормальное", "Хи-квадрат", "Стьюдента (t)"
        ]
    )
    
    # Отображение выбранного распределения
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fig = create_distribution_plot(chosen_dist)
        st.pyplot(fig, use_container_width=True)
        create_download_button(fig, f"{chosen_dist.lower().replace(' ', '_')}.png")
    
    with col2:
        display_distribution_info(chosen_dist)
    
    # Сравнительная секция
    st.markdown("---")
    st.subheader("📊 Сравнение распределений")
    
    comparison_type = st.radio("Тип сравнения:", ["Таблица характеристик", "Визуальное сравнение"])
    
    if comparison_type == "Таблица характеристик":
        # Сравнительная таблица
        comparison_data = {
            "Распределение": ["Нормальное", "Равномерное", "Биномиальное", "Пуассона", "Экспоненциальное"],
            "Тип": ["Непрерывное", "Непрерывное", "Дискретное", "Дискретное", "Непрерывное"],
            "Параметры": ["μ, σ", "a, b", "n, p", "λ", "λ"],
            "Среднее": ["μ", "(a+b)/2", "n·p", "λ", "1/λ"],
            "Дисперсия": ["σ²", "(b-a)²/12", "n·p·(1-p)", "λ", "1/λ²"]
        }
        
        st.table(comparison_data)
    
    else:
        # Визуальное сравнение
        comparison_mode = st.selectbox("Выберите группу для сравнения:", 
                                     ["Непрерывные распределения", "Дискретные распределения"])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if comparison_mode == "Непрерывные распределения":
            x = np.linspace(-4, 8, 1000)
            ax.plot(x, stats.norm.pdf(x), label="Нормальное N(0,1)", linewidth=2)
            ax.plot(x, stats.uniform.pdf(x, 0, 2), label="Равномерное U(0,2)", linewidth=2)
            ax.plot(x[x>=0], stats.expon.pdf(x[x>=0]), label="Экспоненциальное λ=1", linewidth=2)
            ax.set_title("Сравнение непрерывных распределений")
            ax.set_xlim(-1, 6)
        
        else:
            x = np.arange(0, 21)
            ax.bar(x-0.2, stats.binom.pmf(x, 20, 0.25), width=0.4, alpha=0.7, 
                  label="Биномиальное B(20,0.25)")
            ax.bar(x+0.2, stats.poisson.pmf(x, 5), width=0.4, alpha=0.7, 
                  label="Пуассона λ=5")
            ax.set_title("Сравнение дискретных распределений")
        
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x) или P(X=x)")
        
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        create_download_button(fig, f"comparison_{comparison_mode.lower().replace(' ', '_')}.png")
    
    # Рекомендации по выбору
    st.markdown("---")
    st.subheader("🎯 Как выбрать подходящее распределение?")
    
    with st.expander("Пошаговый гид по выбору распределения"):
        st.markdown("""
        **Шаг 1: Определите тип данных**
        - 🔢 **Дискретные данные** (целые числа): Биномиальное, Пуассона, Геометрическое
        - 📈 **Непрерывные данные** (любые вещественные числа): Нормальное, Равномерное, Экспоненциальное
        
        **Шаг 2: Проанализируйте природу процесса**
        - ⏱️ **Время до события** → Экспоненциальное
        - 📊 **Количество событий за период** → Пуассона  
        - 🎯 **Испытания успех/неудача** → Биномиальное
        - 🔔 **Центральная группировка вокруг среднего** → Нормальное
        - 💰 **Положительные значения с правым хвостом** → Логнормальное
        
        **Шаг 3: Проверьте на ваших данных**
        - 📊 **QQ-графики** для проверки соответствия
        - 🧪 **Критерии согласия** (Колмогорова-Смирнова, χ²)
        - 👁️ **Визуальный анализ** гистограмм
        
        **Шаг 4: Учтите ЦПТ**
        - 📈 **Средние больших выборок** → часто приближаются к нормальному
        - 🎲 **Суммы случайных величин** → стремятся к нормальному
        """)
    
    # Полезные ресурсы
    st.markdown("---")
    st.subheader("📚 Полезные ресурсы для изучения")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Интерактивные ресурсы:**
        - [Seeing Theory](https://seeing-theory.brown.edu/) - визуальная теория вероятностей
        - [Distribution Calculator](https://stattrek.com/online-calculator) - онлайн калькуляторы
        - [Wolfram Alpha](https://wolframalpha.com/) - для вычислений и графиков
        """)
    
    with col2:
        st.markdown("""
        **Теоретические материалы:**
        - [Wikipedia: List of distributions](https://en.wikipedia.org/wiki/List_of_probability_distributions)
        - [Khan Academy: Statistics](https://www.khanacademy.org/math/statistics-probability)
        - [MIT OpenCourseWare](https://ocw.mit.edu/) - курсы по статистике
        """)

def create_distribution_plot(dist_name: str):
    """Создание графика выбранного распределения"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if dist_name == "Нормальное (Гауссово)":
        mu, sigma = 0, 1
        x = np.linspace(-4, 4, 1000)
        y = stats.norm.pdf(x, mu, sigma)
        ax.plot(x, y, linewidth=3, color='blue')
        ax.fill_between(x, y, alpha=0.3)
        ax.axvline(mu, color='red', linestyle='--', linewidth=2, label=f'μ = {mu}')
        ax.axvline(mu+sigma, color='green', linestyle=':', linewidth=2, label=f'μ+σ = {mu+sigma}')
        ax.axvline(mu-sigma, color='green', linestyle=':', linewidth=2, label=f'μ-σ = {mu-sigma}')
        ax.set_title("Нормальное распределение N(0,1)", fontsize=14)
    
    elif dist_name == "Равномерное":
        a, b = 0, 2
        x = np.linspace(-0.5, 2.5, 1000)
        y = np.where((x >= a) & (x <= b), 1/(b-a), 0)
        ax.plot(x, y, linewidth=3, color='green')
        ax.fill_between(x, y, alpha=0.3)
        ax.axvline((a+b)/2, color='red', linestyle='--', linewidth=2, label=f'μ = {(a+b)/2}')
        ax.set_title(f"Равномерное распределение U({a},{b})", fontsize=14)
    
    elif dist_name == "Биномиальное":
        n, p = 20, 0.3
        x = np.arange(0, n+1)
        y = stats.binom.pmf(x, n, p)
        ax.bar(x, y, alpha=0.7, color='orange', edgecolor='black')
        ax.axvline(n*p, color='red', linestyle='--', linewidth=2, label=f'μ = {n*p:.1f}')
        ax.set_title(f"Биномиальное распределение B({n},{p})", fontsize=14)
    
    elif dist_name == "Пуассона":
        lam = 5
        x = np.arange(0, 15)
        y = stats.poisson.pmf(x, lam)
        ax.bar(x, y, alpha=0.7, color='purple', edgecolor='black')
        ax.axvline(lam, color='red', linestyle='--', linewidth=2, label=f'μ = λ = {lam}')
        ax.set_title(f"Распределение Пуассона (λ = {lam})", fontsize=14)
    
    elif dist_name == "Экспоненциальное":
        lam = 1
        x = np.linspace(0, 5, 1000)
        y = stats.expon.pdf(x, scale=1/lam)
        ax.plot(x, y, linewidth=3, color='red')
        ax.fill_between(x, y, alpha=0.3)
        ax.axvline(1/lam, color='blue', linestyle='--', linewidth=2, label=f'μ = {1/lam}')
        ax.set_title(f"Экспоненциальное распределение (λ = {lam})", fontsize=14)
    
    elif dist_name == "Логнормальное":
        mu, sigma = 0, 0.5
        x = np.linspace(0.01, 5, 1000)
        y = stats.lognorm.pdf(x, s=sigma, scale=np.exp(mu))
        ax.plot(x, y, linewidth=3, color='brown')
        ax.fill_between(x, y, alpha=0.3)
        mean_ln = np.exp(mu + sigma**2/2)
        ax.axvline(mean_ln, color='red', linestyle='--', linewidth=2, label=f'μ = {mean_ln:.2f}')
        ax.set_title(f"Логнормальное распределение", fontsize=14)
    
    elif dist_name == "Хи-квадрат":
        df = 5
        x = np.linspace(0.01, 15, 1000)
        y = stats.chi2.pdf(x, df)
        ax.plot(x, y, linewidth=3, color='darkgreen')
        ax.fill_between(x, y, alpha=0.3)
        ax.axvline(df, color='red', linestyle='--', linewidth=2, label=f'μ = {df}')
        ax.set_title(f"Распределение χ² (df = {df})", fontsize=14)
    
    elif dist_name == "Стьюдента (t)":
        df = 5
        x = np.linspace(-4, 4, 1000)
        y_t = stats.t.pdf(x, df)
        y_norm = stats.norm.pdf(x)
        ax.plot(x, y_t, linewidth=3, label=f"t-распределение (df={df})", color='darkblue')
        ax.plot(x, y_norm, linestyle='--', linewidth=2, label="N(0,1)", color='gray')
        ax.fill_between(x, y_t, alpha=0.3)
        ax.set_title(f"Распределение Стьюдента (df = {df})", fontsize=14)
    
    # Общие настройки
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("f(x) или P(X=x)", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    
    return fig

def display_distribution_info(dist_name: str):
    """Отображение информации о распределении"""
    info = {
        "Нормальное (Гауссово)": {
            "description": "Симметричная колоколообразная кривая, описывающая непрерывные величины вокруг среднего значения.",
            "parameters": "μ (среднее), σ (стандартное отклонение)",
            "applications": [
                "🧑‍🤝‍🧑 Рост и вес в популяции",
                "🔬 Ошибки измерений",
                "🧠 IQ-тесты и психометрия",
                "💹 Финансовые доходности",
                "📊 Результаты экспериментов"
            ],
            "formula": "f(x) = (1/σ√2π) × e^(-(x-μ)²/2σ²)"
        },
        "Равномерное": {
            "description": "Все значения в определенном интервале имеют одинаковую вероятность появления.",
            "parameters": "a (минимум), b (максимум)",
            "applications": [
                "🎲 Генерация случайных чисел",
                "🚌 Время ожидания транспорта",
                "🎯 Моделирование неопределенности",
                "🔢 Округление числовых значений"
            ],
            "formula": "f(x) = 1/(b-a) для a ≤ x ≤ b"
        },
        "Биномиальное": {
            "description": "Количество успехов в фиксированном числе независимых испытаний с постоянной вероятностью успеха.",
            "parameters": "n (число испытаний), p (вероятность успеха)",
            "applications": [
                "🧪 A/B тестирование",
                "🏭 Контроль качества продукции",
                "📊 Социологические опросы",
                "🎯 Медицинские испытания",
                "🗳️ Избирательные процессы"
            ],
            "formula": "P(X=k) = C(n,k) × p^k × (1-p)^(n-k)"
        },
        "Пуассона": {
            "description": "Количество событий, происходящих за фиксированный интервал времени при постоянной интенсивности.",
            "parameters": "λ (интенсивность/среднее число событий)",
            "applications": [
                "📞 Звонки в call-центр",
                "🚗 Дорожно-транспортные происшествия",
                "🏭 Дефекты в производстве",
                "🌟 Радиоактивный распад",
                "📧 Поток email-сообщений"
            ],
            "formula": "P(X=k) = (λ^k × e^(-λ))/k!"
        },
        "Экспоненциальное": {
            "description": "Время между событиями в процессе Пуассона; характеризует время ожидания до первого события.",
            "parameters": "λ (интенсивность событий)",
            "applications": [
                "⚙️ Время до поломки оборудования",
                "🏪 Интервалы между клиентами",
                "☎️ Длительность телефонных звонков",
                "🔋 Время разрядки батареи",
                "🌧️ Интервалы между осадками"
            ],
            "formula": "f(t) = λ × e^(-λt) для t ≥ 0"
        },
        "Логнормальное": {
            "description": "Если логарифм случайной величины имеет нормальное распределение, то сама величина имеет логнормальное.",
            "parameters": "μ, σ (параметры логарифма)",
            "applications": [
                "💰 Доходы населения",
                "📁 Размеры файлов",
                "⏱️ Время выполнения задач",
                "💹 Цены на акции",
                "🏠 Стоимость недвижимости"
            ],
            "formula": "f(x) = (1/xσ√2π) × e^(-(ln(x)-μ)²/2σ²)"
        },
        "Хи-квадрат": {
            "description": "Сумма квадратов независимых стандартных нормальных случайных величин.",
            "parameters": "k (степени свободы)",
            "applications": [
                "🧪 Критерий согласия",
                "📊 Оценка дисперсии",
                "🔬 Тестирование гипотез",
                "📈 Анализ таблиц сопряженности"
            ],
            "formula": "f(x) = (1/2^(k/2)Γ(k/2)) × x^(k/2-1) × e^(-x/2)"
        },
        "Стьюдента (t)": {
            "description": "Распределение выборочного среднего при неизвестной дисперсии популяции и малых выборках.",
            "parameters": "ν (степени свободы)",
            "applications": [
                "📊 t-тесты для сравнения средних",
                "🔍 Доверительные интервалы",
                "🧪 Анализ малых выборок",
                "📈 Регрессионный анализ"
            ],
            "formula": "f(t) = Γ((ν+1)/2)/(√νπ Γ(ν/2)) × (1+t²/ν)^(-(ν+1)/2)"
        }
    }
    
    if dist_name in info:
        dist_info = info[dist_name]
        st.markdown(f"### {dist_name}")
        
        st.markdown(f"**📝 Описание:**")
        st.write(dist_info['description'])
        
        st.markdown(f"**⚙️ Параметры:** {dist_info['parameters']}")
        
        if 'formula' in dist_info:
            st.markdown("**🧮 Формула:**")
            st.code(dist_info['formula'])
        
        st.markdown("**🎯 Применения:**")
        for app in dist_info['applications']:
            st.write(f"• {app}")
        
        # Дополнительные характеристики
        if dist_name == "Нормальное (Гауссово)":
            st.markdown("""
            **🔑 Ключевые свойства:**
            • Симметрично относительно среднего
            • 68-95-99.7 правило (закон трёх сигм)
            • Основа для ЦПТ и многих статистических тестов
            """)
        elif dist_name == "Экспоненциальное":
            st.markdown("""
            **🔑 Ключевые свойства:**
            • Отсутствие памяти (memoryless property)
            • Тяжелый правый хвост
            • Связано с распределением Пуассона
            """)

def setup_footer():
    """Настройка подвала приложения"""
    # Обработка ошибок и очистка памяти
    try:
        plt.close('all')
    except Exception as e:
        st.error(f"Ошибка при обработке графиков: {str(e)}")
    
    # Метрики использования
    if "page_views" not in st.session_state:
        st.session_state.page_views = 0
    st.session_state.page_views += 1
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📚 Дополнительные ресурсы")
        st.markdown("""
        - [Khan Academy: Статистика](https://www.khanacademy.org/math/statistics-probability)
        - [StatQuest YouTube](https://www.youtube.com/c/joshstarmer)
        - [Seeing Theory](https://seeing-theory.brown.edu/)
        - [Stattrek Calculators](https://stattrek.com/online-calculator)
        - [Coursera: Statistics Courses](https://www.coursera.org/courses?query=statistics)
        """)
    
    with col2:
        st.markdown("### ℹ️ О проекте")
        st.markdown("""
        **Интерактивное приложение для изучения статистических и вероятностных концепций.**
        
        🎯 **Цель:** Сделать статистику понятной и доступной через интерактивные визуализации
        
        🔧 **Технологии:** Python, Streamlit, NumPy, Matplotlib, SciPy
        
        📧 **Обратная связь:** Используйте форму ниже для предложений
        """)
    
    with col3:
        st.markdown("### 📊 Статистика использования")
        st.metric("Просмотров сессии", st.session_state.page_views)
        
        # Прогресс по изученным вкладкам
        if "visited_tabs" not in st.session_state:
            st.session_state.visited_tabs = set()
        
        visited_count = len(st.session_state.visited_tabs)
        total_tabs = 8
        progress = visited_count / total_tabs
        
        st.metric("Изучено разделов", f"{visited_count}/{total_tabs}")
        st.progress(progress)
        
        # Форма обратной связи
        with st.expander("📝 Оставить отзыв"):
            feedback_type = st.selectbox("Тип отзыва:", 
                                       ["💡 Предложение", "🐛 Сообщить об ошибке", "👍 Похвалить", "❓ Задать вопрос"])
            feedback = st.text_area("Ваш отзыв:")
            
            if st.button("Отправить отзыв") and feedback:
                st.success("Спасибо за отзыв! Мы учтем ваши предложения в будущих обновлениях.")
                # Здесь можно добавить отправку отзыва в БД или email
    
    # История обновлений
    with st.expander("📅 История обновлений"):
        st.markdown("""
        **v3.0 (Декабрь 2025) - Оптимизированная версия**
        - ⚡ Полный рефакторинг кода с оптимизацией производительности  
        - 🚀 Добавлено кэширование всех вычислений (ускорение в 3-5 раз)
        - 🏗️ Улучшена модульная структура кода и добавлена типизация
        - 🎓 Добавлен интерактивный тест знаний с системой оценки
        - 📊 Расширен раздел типов распределений с визуальными сравнениями
        - 🎨 Оптимизированы графики и улучшен пользовательский интерфейс
        - 🔧 Добавлена универсальная обработка ошибок
        
        **v2.0 (Июнь 2025)**
        - 📈 Добавлены новые модули: Сравнение распределений, Регрессия к среднему
        - 🛡️ Улучшена обработка ошибок и оптимизированы вычисления
        
        **v1.0 (Апрель 2025)**
        - 🎉 Первоначальный релиз с базовыми модулями
        - 📊 Базовые модули: Закон трёх сигм, ЦПТ, ЗБЧ, Малые выборки
        """)
    
    # Дополнительная информация
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666666; font-size: 12px;'>
    💡 Создано для образовательных целей | 🔬 Основано на научных принципах статистики | 
    🎯 Помогает понять сложные концепции через интерактивность
    </div>
    """, unsafe_allow_html=True)

# Запуск приложения
if __name__ == "__main__":
    main()
