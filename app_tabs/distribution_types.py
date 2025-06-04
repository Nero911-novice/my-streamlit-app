import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from .utils import create_download_button


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
        ax.axvline(lam, color='red', linestyle='--', linewidth=2, label=f'μ = {lam}')
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
        ax.set_title("Логнормальное распределение", fontsize=14)
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
        st.markdown("**📝 Описание:**")
        st.write(dist_info['description'])
        st.markdown(f"**⚙️ Параметры:** {dist_info['parameters']}")
        if 'formula' in dist_info:
            st.markdown("**🧮 Формула:**")
            st.code(dist_info['formula'])
        st.markdown("**🎯 Применения:**")
        for app in dist_info['applications']:
            st.write(f"• {app}")
        if dist_name == "Нормальное (Гауссово)":
            st.markdown("""**🔑 Ключевые свойства:**\n• Симметрично относительно среднего\n• 68-95-99.7 правило (закон трёх сигм)\n• Основа для ЦПТ и многих статистических тестов""")
        elif dist_name == "Экспоненциальное":
            st.markdown("""**🔑 Ключевые свойства:**\n• Отсутствие памяти (memoryless property)\n• Тяжелый правый хвост\n• Связано с распределением Пуассона""")


def distribution_types_tab():
    """Вкладка типов распределений"""
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Типы распределений")

    st.header("Типы вероятностных распределений")
    st.markdown("Интерактивное изучение основных вероятностных распределений, их свойств и применений.")

    chosen_dist = st.selectbox(
        "Выберите распределение для изучения:",
        [
            "Нормальное (Гауссово)", "Равномерное", "Биномиальное", "Пуассона",
            "Экспоненциальное", "Логнормальное", "Хи-квадрат", "Стьюдента (t)"
        ]
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = create_distribution_plot(chosen_dist)
        st.pyplot(fig, use_container_width=True)
        create_download_button(fig, f"{chosen_dist.lower().replace(' ', '_')}.png")
    with col2:
        display_distribution_info(chosen_dist)

    st.markdown("---")
    st.subheader("📊 Сравнение распределений")
    comparison_type = st.radio("Тип сравнения:", ["Таблица характеристик", "Визуальное сравнение"])
    if comparison_type == "Таблица характеристик":
        comparison_data = {
            "Распределение": ["Нормальное", "Равномерное", "Биномиальное", "Пуассона", "Экспоненциальное"],
            "Тип": ["Непрерывное", "Непрерывное", "Дискретное", "Дискретное", "Непрерывное"],
            "Параметры": ["μ, σ", "a, b", "n, p", "λ", "λ"],
            "Среднее": ["μ", "(a+b)/2", "n·p", "λ", "1/λ"],
            "Дисперсия": ["σ²", "(b-a)²/12", "n·p·(1-p)", "λ", "1/λ²"]
        }
        st.table(comparison_data)
    else:
        comparison_mode = st.selectbox("Выберите группу для сравнения:", ["Непрерывные распределения", "Дискретные распределения"])
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
            ax.bar(x-0.2, stats.binom.pmf(x, 20, 0.25), width=0.4, alpha=0.7, label="Биномиальное B(20,0.25)")
            ax.bar(x+0.2, stats.poisson.pmf(x, 5), width=0.4, alpha=0.7, label="Пуассона λ=5")
            ax.set_title("Сравнение дискретных распределений")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x) или P(X=x)")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        create_download_button(fig, f"comparison_{comparison_mode.lower().replace(' ', '_')}.png")

    st.markdown("---")
    st.subheader("🎯 Как выбрать подходящее распределение?")
    with st.expander("Пошаговый гид по выбору распределения"):
        st.markdown(
            """**Шаг 1: Определите тип данных**
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
        - 🎲 **Суммы случайных величин** → стремятся к нормальному"""
        )
    st.markdown("---")
    st.subheader("📚 Полезные ресурсы для изучения")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """**Интерактивные ресурсы:**
        - [Seeing Theory](https://seeing-theory.brown.edu/) - визуальная теория вероятностей
        - [Distribution Calculator](https://stattrek.com/online-calculator) - онлайн калькуляторы
        - [Wolfram Alpha](https://wolframalpha.com/) - для вычислений и графиков"""
        )
    with col2:
        st.markdown(
            """**Теоретические материалы:**
        - [Wikipedia: List of distributions](https://en.wikipedia.org/wiki/List_of_probability_distributions)
        - [Khan Academy: Statistics](https://www.khanacademy.org/math/statistics-probability)
        - [MIT OpenCourseWare](https://ocw.mit.edu/) - курсы по статистике"""
        )
