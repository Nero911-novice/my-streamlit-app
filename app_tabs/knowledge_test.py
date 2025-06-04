import streamlit as st
import time


def knowledge_test_tab():
    """Вкладка проверки знаний"""
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Проверь свои знания")

    st.header("Проверь свои знания")
    st.markdown("Интерактивный тест для закрепления изученного материала.")

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
                time.sleep(2)
                st.rerun()
    else:
        score_pct = (st.session_state.test_score / len(questions)) * 100
        st.subheader("🎯 Результаты теста")
        st.write(f"Ваш результат: **{st.session_state.test_score} из {len(questions)}** ({score_pct:.0f}%)")
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
