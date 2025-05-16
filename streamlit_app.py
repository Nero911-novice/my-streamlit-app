import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats  # Важно импортировать stats именно так
from io import BytesIO
import time  # Для использования в модуле регрессии к среднему

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
    st.markdown("""
    Закон трёх сигм помогает понять, как распределены данные вокруг среднего значения
    Это полезно, когда нужно решить, какое наблюдение считать нормальным, а какое — выбросом. Например, если рост человека отклоняется от среднего больше чем на 3σ, это весьма необычно!
    """)
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

**Простыми словами:** 
Представьте школьный класс, где средний рост детей 140 см, а стандартное отклонение 5 см. Закон трёх сигм говорит нам, что:

- Около 68% детей (больше половины класса) имеют рост от 135 до 145 см (±1σ)
- Примерно 95% детей (почти весь класс) имеют рост от 130 до 150 см (±2σ) 
- Практически все дети (99.7%) имеют рост от 125 до 155 см (±3σ)

Если рост ребенка 160 см (отклонение больше 3σ), это действительно необычно для данного класса!

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
    st.markdown("""
Закон трёх сигм помогает понять, как распределены данные вокруг среднего значения
Это полезно, когда нужно решить, какое наблюдение считать нормальным, а какое — выбросом. Например, если рост человека отклоняется от среднего больше чем на 3σ, это весьма необычно!
""")
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

    means = [np.mean(generate(dist_type, sample_size)) for _ in range(num_samples)]
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
            means = [np.mean(generate(dist_type, n)) for _ in range(num_samples)]
            
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

**Простыми словами:**
Представьте, что вы подбрасываете игральную кость (результаты от 1 до 6). Распределение результатов равномерное — каждое число выпадает с одинаковой вероятностью.
Но если вы подбросите две кости и запишете среднее (результаты от 1 до 6 с шагом 0.5), распределение будет выглядеть как треугольник — крайние значения менее вероятны.
А если бросить 30 костей и записать их среднее? ЦПТ говорит, что это распределение будет похоже на колокол (нормальное), независимо от того, использовали вы кости, монеты или рулетку.

> 💡**Где это используется:**
> Когда социологи проводят опросы, они опрашивают не всех граждан, а лишь выборку. ЦПТ позволяет им делать обоснованные выводы даже с ограниченными данными.
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

    data_lln = sample(dist_type_lln, trials)
    cumulative = np.cumsum(data_lln) / np.arange(1, trials+1)
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

**Простыми словами:**
Подбрасывая монету 10 раз, вы можете получить 7 орлов и 3 решки (70% орлов!). Но если подбросить монету 1000 раз, вероятность получить сильное отклонение от 50% орлов очень мала.

**Пример из жизни:** 
- Казино всегда в выигрыше в долгосрочной перспективе, даже если отдельные игроки иногда выигрывают крупные суммы.
- Страховые компании могут точно рассчитывать стоимость страховки, основываясь на большом количестве случаев.

> 📊**Ключевая идея:**
Чем больше наблюдений, тем ближе среднее значение к истинному, но мы не можем предсказать, насколько быстро произойдет эта сходимость.
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

    # Кэшируем с помоью lru_cache можно было бы, но для простоты
    # Генерация и расчет
    samples = np.random.binomial(n_small, 0.5, size=(num_sim, n_small)) / n_small if dist_small == "Экспоненциальное" else np.random.binomial(n_small, 0.5, size=(num_sim, n_small)) / n_small
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
    data1 = generate_dist_data(dist1, sample_size, params1)
    data2 = generate_dist_data(dist2, sample_size, params2)
    
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
    **Простыми словами:**
    После исключительно хорошего или плохого результата следующий результат, скорее всего, будет ближе к среднему — не потому что что-то изменилось, а просто из-за случайности.

    > **Примеры из жизни:**
    - Спортсмен, установивший рекорд, вероятно, покажет более средний результат в следующий раз.
    - Студент, получивший неожиданно высокую оценку, скорее всего, получит более обычную оценку на следующем экзамене.
    - Компания, показавшая рекордную прибыль, вероятно, вернется к обычным показателям в следующем квартале.

    > **Частая ошибка:**
    Люди часто видят причинно-следственную связь там, где её нет: "После того, как мы отругали худших сотрудников, их производительность выросла!" Но это, скорее всего, просто регрессия к среднему, а не результат вмешательства.

    > 🔍 **Практические последствия:**
    - Этот эффект часто принимают за действие вмешательства
    - "Проклятие обложки Sports Illustrated": спортсмены часто снижают результаты после попадания на обложку
    - "Эффект лечения" при обращении с крайними симптомами: пациенты часто "улучшаются" без лечения
    - Оценка эффективности тренингов, начатых после провальных результатов
    """)

    # === Новый раздел: Типы распределений ===
    with tabs[7]:
    st.header("Типы вероятностных распределений")
    
    st.markdown("""
    # Основные вероятностные распределения
    
    Вероятностные распределения описывают, как распределены значения случайной величины. Разные типы 
    данных и явлений характеризуются разными распределениями. Ниже описаны основные распределения, 
    их свойства и примеры применения.
    """)
    
    # Выбор распределения для демонстрации
    chosen_dist = st.selectbox(
        "Выберите распределение для изучения:",
        ["Нормальное (Гауссово)", "Равномерное", "Биномиальное", "Пуассона", 
         "Экспоненциальное", "Логнормальное", "Хи-квадрат", "Стьюдента (t)"]
    )
    
    # Контейнер для визуализации
    visual_col1, visual_col2 = st.columns([3, 2])
    
    # Параметры распределений и их визуализация
    if chosen_dist == "Нормальное (Гауссово)":
        with visual_col1:
            mu = st.slider("Среднее (μ)", -10.0, 10.0, 0.0, 0.5)
            sigma = st.slider("Стандартное отклонение (σ)", 0.1, 5.0, 1.0, 0.1)
            
            # Генерация данных и построение графика
            x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
            y = stats.norm.pdf(x, mu, sigma)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, 'b-', linewidth=2)
            ax.fill_between(x, y, alpha=0.2)
            ax.set_title("Плотность нормального распределения")
            ax.set_xlabel("Значение")
            ax.set_ylabel("Плотность вероятности")
            ax.axvline(mu, color='r', linestyle='--', alpha=0.7, label=f'Среднее: {mu}')
            ax.axvline(mu + sigma, color='g', linestyle=':', alpha=0.7, label=f'μ+σ: {mu+sigma}')
            ax.axvline(mu - sigma, color='g', linestyle=':', alpha=0.7)
            ax.grid(alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
        with visual_col2:
            st.markdown(f"""
            ## Нормальное распределение
            
            **Суть:** Симметричная колоколообразная кривая, описывающая непрерывные величины, которые 
            группируются вокруг среднего значения.
            
            **Параметры:**
            - Среднее (μ): {mu} - центр распределения
            - Стандартное отклонение (σ): {sigma} - мера разброса
            
            **Формула плотности вероятности:**
            $$f(x) = \\frac{{1}}{{\\sigma\\sqrt{{2\\pi}}}} e^{{-\\frac{{(x-\\mu)^2}}{{2\\sigma^2}}}}$$
            
            **Примеры применения:**
            - Рост и вес в популяции
            - Ошибки измерений
            - IQ тесты
            - Множество естественных явлений
            
            **Особенности:**
            - Симметрично относительно среднего
            - ~68% значений лежат в пределах ±1σ
            - ~95% значений лежат в пределах ±2σ
            - ~99.7% значений лежат в пределах ±3σ
            """)
    
    elif chosen_dist == "Равномерное":
        with visual_col1:
            a = st.slider("Минимум (a)", -10.0, 10.0, 0.0, 0.5)
            b = st.slider("Максимум (b)", a + 0.5, a + 20.0, a + 5.0, 0.5)
            
            # Генерация данных и построение графика
            x = np.linspace(a - 1, b + 1, 1000)
            y = np.where((x >= a) & (x <= b), 1/(b-a), 0)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, 'b-', linewidth=2)
            ax.fill_between(x, y, alpha=0.2)
            ax.set_title("Плотность равномерного распределения")
            ax.set_xlabel("Значение")
            ax.set_ylabel("Плотность вероятности")
            ax.axvline((a+b)/2, color='r', linestyle='--', alpha=0.7, label=f'Среднее: {(a+b)/2}')
            ax.grid(alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
        with visual_col2:
            st.markdown(f"""
            ## Равномерное распределение
            
            **Суть:** Все значения в определенном интервале имеют одинаковую вероятность.
            
            **Параметры:**
            - Минимум (a): {a}
            - Максимум (b): {b}
            
            **Формула плотности вероятности:**
            $$f(x) = \\begin{{cases}} 
            \\frac{{1}}{{b-a}} & \\text{{если }} a \\leq x \\leq b \\\\
            0 & \\text{{в противном случае}}
            \\end{{cases}}$$
            
            **Примеры применения:**
            - Случайные числа в компьютерных программах
            - Время ожидания автобуса (если интервал движения точно соблюдается)
            - Округление чисел (ошибка округления)
            
            **Особенности:**
            - Все значения равновероятны
            - Среднее: (a+b)/2 = {(a+b)/2}
            - Стандартное отклонение: (b-a)/√12 = {(b-a)/np.sqrt(12):.4f}
            """)
            
    elif chosen_dist == "Биномиальное":
        with visual_col1:
            n = st.slider("Количество испытаний (n)", 1, 50, 20)
            p = st.slider("Вероятность успеха (p)", 0.0, 1.0, 0.5, 0.01)
            
            # Генерация данных и построение графика
            x = np.arange(0, n+1)
            y = stats.binom.pmf(x, n, p)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(x, y, alpha=0.7, width=0.8)
            ax.set_title("Функция вероятности биномиального распределения")
            ax.set_xlabel("Количество успехов")
            ax.set_ylabel("Вероятность")
            ax.axvline(n*p, color='r', linestyle='--', alpha=0.7, label=f'Среднее: {n*p}')
            ax.grid(alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
        with visual_col2:
            st.markdown(f"""
            ## Биномиальное распределение
            
            **Суть:** Описывает количество успехов в фиксированном числе независимых испытаний.
            
            **Параметры:**
            - Количество испытаний (n): {n}
            - Вероятность успеха (p): {p}
            
            **Формула вероятности:**
            $$P(X=k) = \\binom{{n}}{{k}} p^k (1-p)^{{n-k}}$$
            
            **Примеры применения:**
            - Подбрасывание монеты n раз (количество выпадений орла)
            - Результаты тестов с вариантами "да"/"нет"
            - Количество бракованных изделий в партии
            
            **Особенности:**
            - Дискретное распределение (целые числа от 0 до n)
            - Среднее: n·p = {n*p}
            - Стандартное отклонение: √(n·p·(1-p)) = {np.sqrt(n*p*(1-p)):.4f}
            - При больших n и p близких к 0.5, приближается к нормальному
            """)
            
    elif chosen_dist == "Пуассона":
        with visual_col1:
            lam = st.slider("Интенсивность (λ)", 0.1, 20.0, 5.0, 0.1)
            
            # Генерация данных и построение графика
            max_x = max(20, int(lam*3))
            x = np.arange(0, max_x+1)
            y = stats.poisson.pmf(x, lam)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(x, y, alpha=0.7, width=0.8)
            ax.set_title("Функция вероятности распределения Пуассона")
            ax.set_xlabel("Количество событий")
            ax.set_ylabel("Вероятность")
            ax.axvline(lam, color='r', linestyle='--', alpha=0.7, label=f'Среднее: {lam}')
            ax.grid(alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
        with visual_col2:
            st.markdown(f"""
            ## Распределение Пуассона
            
            **Суть:** Описывает количество событий, происходящих за фиксированный интервал времени 
            или пространства, если события происходят с постоянной средней интенсивностью.
            
            **Параметры:**
            - Интенсивность (λ): {lam} (среднее количество событий)
            
            **Формула вероятности:**
            $$P(X=k) = \\frac{{\\lambda^k e^{{-\\lambda}}}}{{k!}}$$
            
            **Примеры применения:**
            - Количество звонков в колл-центр за час
            - Количество опечаток на странице
            - Количество радиоактивных распадов за минуту
            - Количество клиентов в очереди
            
            **Особенности:**
            - Дискретное распределение (целые неотрицательные числа)
            - Среднее: λ = {lam}
            - Дисперсия: λ = {lam}
            - Стандартное отклонение: √λ = {np.sqrt(lam):.4f}
            - Подходит для редких событий в большом числе испытаний
            """)
            
    elif chosen_dist == "Экспоненциальное":
        with visual_col1:
            rate = st.slider("Интенсивность (λ)", 0.1, 5.0, 1.0, 0.1)
            
            # Генерация данных и построение графика
            x = np.linspace(0, 5/rate, 1000)
            y = rate * np.exp(-rate * x)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, 'b-', linewidth=2)
            ax.fill_between(x, y, alpha=0.2)
            ax.set_title("Плотность экспоненциального распределения")
            ax.set_xlabel("Значение")
            ax.set_ylabel("Плотность вероятности")
            ax.axvline(1/rate, color='r', linestyle='--', alpha=0.7, label=f'Среднее: {1/rate}')
            ax.grid(alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
        with visual_col2:
            st.markdown(f"""
            ## Экспоненциальное распределение
            
            **Суть:** Описывает время ожидания до наступления события в процессе Пуассона.
            
            **Параметры:**
            - Интенсивность (λ): {rate} (скорость наступления событий)
            
            **Формула плотности вероятности:**
            $$f(x) = \\lambda e^{{-\\lambda x}} \\quad \\text{{для }} x \\geq 0$$
            
            **Примеры применения:**
            - Время между звонками в колл-центр
            - Время работы электронного компонента до отказа
            - Время ожидания автобуса (если прибытие случайно)
            - Длительность обслуживания клиентов
            
            **Особенности:**
            - Непрерывное распределение (неотрицательные числа)
            - Среднее: 1/λ = {1/rate}
            - Стандартное отклонение: 1/λ = {1/rate}
            - "Безпамятное" распределение - вероятность наступления события 
              не зависит от того, сколько времени уже прошло
            """)
            
    elif chosen_dist == "Логнормальное":
        with visual_col1:
            mu_log = st.slider("μ логарифма", -1.0, 2.0, 0.0, 0.1)
            sigma_log = st.slider("σ логарифма", 0.1, 2.0, 0.5, 0.1)
            
            # Генерация данных и построение графика
            x = np.linspace(0.01, np.exp(mu_log + 4*sigma_log), 1000)
            y = stats.lognorm.pdf(x, s=sigma_log, scale=np.exp(mu_log))
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, 'b-', linewidth=2)
            ax.fill_between(x, y, alpha=0.2)
            ax.set_title("Плотность логнормального распределения")
            ax.set_xlabel("Значение")
            ax.set_ylabel("Плотность вероятности")
            mean = np.exp(mu_log + sigma_log**2/2)
            ax.axvline(mean, color='r', linestyle='--', alpha=0.7, label=f'Среднее: {mean:.4f}')
            ax.grid(alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
        with visual_col2:
            st.markdown(f"""
            ## Логнормальное распределение
            
            **Суть:** Если логарифм случайной величины имеет нормальное распределение, то сама 
            величина имеет логнормальное распределение.
            
            **Параметры:**
            - μ логарифма: {mu_log}
            - σ логарифма: {sigma_log}
            
            **Формула плотности вероятности:**
            $$f(x) = \\frac{{1}}{{x \\sigma \\sqrt{{2\\pi}}}} e^{{-\\frac{{(\\ln x - \\mu)^2}}{{2\\sigma^2}}}}$$
            
            **Примеры применения:**
            - Стоимость недвижимости
            - Доходы населения
            - Размеры частиц в природе
            - Цены акций и финансовые величины
            
            **Особенности:**
            - Непрерывное распределение (положительные числа)
            - Несимметричное, с "тяжелым" правым хвостом
            - Среднее: e^(μ+σ²/2) = {np.exp(mu_log + sigma_log**2/2):.4f}
            - Медиана: e^μ = {np.exp(mu_log):.4f}
            - Мода: e^(μ-σ²) = {np.exp(mu_log - sigma_log**2):.4f}
            """)
            
    elif chosen_dist == "Хи-квадрат":
        with visual_col1:
            df = st.slider("Степени свободы (k)", 1, 20, 5)
            
            # Генерация данных и построение графика
            x = np.linspace(0.01, max(20, df*3), 1000)
            y = stats.chi2.pdf(x, df)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, 'b-', linewidth=2)
            ax.fill_between(x, y, alpha=0.2)
            ax.set_title(f"Плотность распределения хи-квадрат (df={df})")
            ax.set_xlabel("Значение")
            ax.set_ylabel("Плотность вероятности")
            ax.axvline(df, color='r', linestyle='--', alpha=0.7, label=f'Среднее: {df}')
            ax.grid(alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
        with visual_col2:
            st.markdown(f"""
            ## Распределение хи-квадрат
            
            **Суть:** Сумма квадратов k независимых стандартных нормальных случайных величин.
            
            **Параметры:**
            - Степени свободы (k): {df}
            
            **Формула плотности вероятности:**
            $$f(x) = \\frac{{1}}{{2^{{k/2}}\\Gamma(k/2)}} x^{{k/2-1}} e^{{-x/2}}$$
            
            **Примеры применения:**
            - Проверка гипотез о дисперсиях
            - Критерий согласия хи-квадрат (goodness-of-fit)
            - Проверка независимости категориальных переменных
            - Доверительные интервалы для дисперсии
            
            **Особенности:**
            - Непрерывное распределение (положительные числа)
            - Несимметричное (при малых k), стремится к нормальному при больших k
            - Среднее: k = {df}
            - Дисперсия: 2k = {2*df}
            - Сумма независимых хи-квадрат также имеет распределение хи-квадрат
            """)
            
    elif chosen_dist == "Стьюдента (t)":
        with visual_col1:
            df_t = st.slider("Степени свободы (ν)", 1, 30, 5)
            
            # Генерация данных и построение графика
            x = np.linspace(-5, 5, 1000)
            y_t = stats.t.pdf(x, df_t)
            y_norm = stats.norm.pdf(x)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y_t, 'b-', linewidth=2, label=f't-распределение (ν={df_t})')
            ax.plot(x, y_norm, 'r--', linewidth=1.5, label='Нормальное распределение')
            ax.fill_between(x, y_t, alpha=0.2)
            ax.set_title(f"Плотность распределения Стьюдента (df={df_t})")
            ax.set_xlabel("Значение")
            ax.set_ylabel("Плотность вероятности")
            ax.grid(alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
        with visual_col2:
            st.markdown(f"""
            ## Распределение Стьюдента (t-распределение)
            
            **Суть:** Описывает выборочное среднее из нормально распределенной популяции, 
            когда истинная дисперсия неизвестна и оценивается по выборке.
            
            **Параметры:**
            - Степени свободы (ν): {df_t}
            
            **Формула плотности вероятности:**
            $$f(x) = \\frac{{\\Gamma((\\nu+1)/2)}}{{\\sqrt{{\\nu\\pi}}\\Gamma(\\nu/2)}}\\left(1+\\frac{{x^2}}{{\\nu}}\\right)^{{-(\\nu+1)/2}}$$
            
            **Примеры применения:**
            - t-тесты для проверки гипотез о средних
            - Доверительные интервалы для средних
            - Регрессионный анализ (t-тесты для коэффициентов)
            
            **Особенности:**
            - Непрерывное симметричное распределение
            - "Тяжелее" хвосты чем у нормального при малых ν
            - Среднее: 0 (при ν > 1)
            - Дисперсия: ν/(ν-2) (при ν > 2)
            - При ν → ∞ стремится к стандартному нормальному распределению
            """)
    
    # Секция "Сравнение распределений"
    st.markdown("---")
    st.subheader("Сравнение основных распределений")
    
    show_comparison = st.checkbox("Показать сравнение распределений", value=False)
    
    if show_comparison:
        # Параметры для сравнения
        compare_type = st.radio(
            "Выберите тип сравнения:",
            ["Непрерывные распределения", "Дискретные распределения"]
        )
        
        if compare_type == "Непрерывные распределения":
            # Генерация данных для сравнения непрерывных распределений
            x_norm = np.linspace(-4, 8, 1000)
            y_norm = stats.norm.pdf(x_norm, 0, 1)
            y_exp = stats.expon.pdf(x_norm, scale=1)
            y_lognorm = stats.lognorm.pdf(x_norm, s=0.5, scale=np.exp(0))
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_norm, y_norm, 'b-', linewidth=2, label='Нормальное (μ=0, σ=1)')
            ax.plot(x_norm, y_exp, 'r-', linewidth=2, label='Экспоненциальное (λ=1)')
            ax.plot(x_norm, y_lognorm, 'g-', linewidth=2, label='Логнормальное (μ=0, σ=0.5)')
            ax.set_title("Сравнение непрерывных распределений")
            ax.set_xlabel("Значение")
            ax.set_ylabel("Плотность вероятности")
            ax.grid(alpha=0.3)
            ax.legend()
            ax.set_ylim(0, 0.8)
            ax.set_xlim(-3, 5)
            
            st.pyplot(fig)
            
        else:  # Дискретные распределения
            # Генерация данных для сравнения дискретных распределений
            x_discrete = np.arange(0, 21)
            y_binom = stats.binom.pmf(x_discrete, 20, 0.25)
            y_poisson = stats.poisson.pmf(x_discrete, 5)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(x_discrete-0.2, y_binom, alpha=0.7, width=0.4, label='Биномиальное (n=20, p=0.25)')
            ax.bar(x_discrete+0.2, y_poisson, alpha=0.7, width=0.4, label='Пуассона (λ=5)')
            ax.set_title("Сравнение дискретных распределений")
            ax.set_xlabel("Значение")
            ax.set_ylabel("Вероятность")
            ax.grid(alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
    
    # Таблица сравнения распределений
    st.markdown("### Сводная таблица распределений")
    
    distributions_data = {
        "Распределение": ["Нормальное", "Равномерное", "Биномиальное", "Пуассона", "Экспоненциальное"],
        "Тип": ["Непрерывное", "Непрерывное", "Дискретное", "Дискретное", "Непрерывное"],
        "Параметры": ["μ, σ", "a, b", "n, p", "λ", "λ"],
        "Среднее": ["μ", "(a+b)/2", "n·p", "λ", "1/λ"],
        "Дисперсия": ["σ²", "(b-a)²/12", "n·p·(1-p)", "λ", "1/λ²"],
        "Типичное применение": ["Рост, вес, ошибки измерений", "Случайные числа, ошибки округления", 
                              "Подбрасывание монет, тесты", "Редкие события, очереди", 
                              "Время до наступления события"]
    }
    
    st.table(distributions_data)
    
    # Рекомендации по выбору распределения
    st.markdown("""
    ### Как выбрать подходящее распределение?
    
    1. **Непрерывные или дискретные данные?**
       - Дискретные (счетные): Биномиальное, Пуассона, Геометрическое...
       - Непрерывные: Нормальное, Равномерное, Экспоненциальное...
    
    2. **Какова природа данных?**
       - Симметричные данные с группировкой вокруг среднего → Нормальное
       - Время ожидания до события → Экспоненциальное
       - Количество редких событий → Пуассона
       - Испытания с исходами успех/неудача → Биномиальное
       - Положительные данные с тяжелым правым хвостом → Логнормальное
    
    3. **Проверка на данных:**
       - QQ-графики для оценки соответствия распределения
       - Критерии согласия (хи-квадрат, Колмогорова-Смирнова)
       - Визуальная оценка гистограммы
    
    4. **Центральная предельная теорема:**
       - Если ваши данные - средние значения из выборок, то они могут приближаться к 
         нормальному распределению, независимо от исходного распределения
    """)
    
    # Полезные ссылки
    st.markdown("""
    ### Полезные ресурсы
    
    - [Интерактивные визуализации распределений](https://seeing-theory.brown.edu/probability-distributions/index.html)
    - [Калькуляторы распределений вероятности](https://stattrek.com/probability-distributions/probability-distributions)
    - [Выбор подходящего распределения](https://stats.stackexchange.com/questions/132652)
    - [Виды распределений с примерами](https://en.wikipedia.org/wiki/List_of_probability_distributions)
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
