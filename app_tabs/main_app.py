import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from .three_sigma import three_sigma_law_tab
from .central_limit import central_limit_theorem_tab
from .law_of_large_numbers import law_of_large_numbers_tab
from .small_samples import small_samples_tab
from .comparison import comparison_distributions_tab
from .regression import regression_to_mean_tab
from .knowledge_test import knowledge_test_tab
from .distribution_types import distribution_types_tab
from .utils import generate_distribution_data, safe_statistics, create_download_button, format_stat_display

sns.set_theme(style="whitegrid")


def main():
    setup_sidebar()
    st.title("📊 Демонстрация вероятностных законов")
    tabs = st.tabs([
        "Закон трёх сигм", "ЦПТ", "ЗБЧ", "Малые выборки",
        "Сравнение распределений", "Регрессия к среднему",
        "Проверь свои знания", "Типы распределений"
    ])
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
    setup_footer()


def setup_sidebar():
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
            st.markdown(f"**{name}**\n{descriptions[name]}\n[Статья на Wikipedia]({url})", unsafe_allow_html=True)
        st.markdown("### 🔰 Для начинающих")
        if st.checkbox("Включить справочный режим"):
            st.info(
                """**Как пользоваться приложением:**
                1. Выберите интересующую вкладку вверху страницы
                2. Настройте параметры с помощью слайдеров и выпадающих списков
                3. Изучите результаты симуляции и прочитайте объяснения
                4. Используйте кнопки \"Скачать график\" для сохранения визуализаций
                Экспериментируйте с разными параметрами, чтобы увидеть, как они влияют на результаты!"""
            )
        with st.expander("💡 Советы"):
            st.markdown(
                """**Советы по использованию:**
                * Используйте вкладки для переключения между разными вероятностными законами
                * Экспериментируйте с параметрами для наблюдения их влияния
                * Обратите внимание на аннотации на графиках - они объясняют ключевые моменты
                * Для анимации ЦПТ используйте чекбокс на вкладке ЦПТ
                * График можно увеличить, наведя курсор и используя инструменты просмотра
                При медленной работе приложения попробуйте:
                * Уменьшить размеры выборок
                * Уменьшить количество симуляций
                * Обновить страницу"""
            )


def setup_footer():
    try:
        plt.close('all')
    except Exception as e:
        st.error(f"Ошибка при обработке графиков: {str(e)}")
    if "page_views" not in st.session_state:
        st.session_state.page_views = 0
    st.session_state.page_views += 1
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📚 Дополнительные ресурсы")
        st.markdown(
            """- [Khan Academy: Статистика](https://www.khanacademy.org/math/statistics-probability)
- [StatQuest YouTube](https://www.youtube.com/c/joshstarmer)
- [Seeing Theory](https://seeing-theory.brown.edu/)
- [Stattrek Calculators](https://stattrek.com/online-calculator)
- [Coursera: Statistics Courses](https://www.coursera.org/courses?query=statistics)"""
        )
    with col2:
        st.markdown("### ℹ️ О проекте")
        st.markdown(
            """**Интерактивное приложение для изучения статистических и вероятностных концепций.**
            
🎯 **Цель:** Сделать статистику понятной и доступной через интерактивные визуализации

🔧 **Технологии:** Python, Streamlit, NumPy, Matplotlib, SciPy

📧 **Обратная связь:** Используйте форму ниже для предложений"""
        )
    with col3:
        st.markdown("### 📊 Статистика использования")
        st.metric("Просмотров сессии", st.session_state.page_views)
        if "visited_tabs" not in st.session_state:
            st.session_state.visited_tabs = set()
        visited_count = len(st.session_state.visited_tabs)
        total_tabs = 8
        progress = visited_count / total_tabs
        st.metric("Изучено разделов", f"{visited_count}/{total_tabs}")
        st.progress(progress)
        with st.expander("📝 Оставить отзыв"):
            feedback_type = st.selectbox("Тип отзыва:", ["💡 Предложение", "🐛 Сообщить об ошибке", "👍 Похвалить", "❓ Задать вопрос"])
            feedback = st.text_area("Ваш отзыв:")
            if st.button("Отправить отзыв") and feedback:
                st.success("Спасибо за отзыв! Мы учтем ваши предложения в будущих обновлениях.")
    with st.expander("📅 История обновлений"):
        st.markdown(
            """**v3.0 (Декабрь 2025) - Оптимизированная версия**
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
- 📊 Базовые модули: Закон трёх сигм, ЦПТ, ЗБЧ, Малые выборки"""
        )
    st.markdown("---")
    st.markdown(
        """<div style='text-align: center; color: #666666; font-size: 12px;'>
💡 Создано для образовательных целей | 🔬 Основано на научных принципах статистики |
🎯 Помогает понять сложные концепции через интерактивность
</div>""",
        unsafe_allow_html=True,
    )
