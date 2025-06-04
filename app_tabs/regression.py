import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Tuple
from .utils import create_download_button


@st.cache_data
def generate_regression_data(mu_reg: int, sigma_reg: int, n_subjects: int,
                           threshold_percentile: int) -> Optional[Tuple]:
    """Генерация данных для демонстрации регрессии к среднему"""
    try:
        true_abilities = np.random.normal(mu_reg, sigma_reg/2, n_subjects)
        test1_scores = true_abilities + np.random.normal(0, sigma_reg/2, n_subjects)
        test2_scores = true_abilities + np.random.normal(0, sigma_reg/2, n_subjects)
        threshold = np.percentile(test1_scores, threshold_percentile)
        best_subjects_mask = test1_scores >= threshold
        if np.sum(best_subjects_mask) == 0:
            return None
        best_subjects_test1 = test1_scores[best_subjects_mask]
        best_subjects_test2 = test2_scores[best_subjects_mask]
        all_mean_test1 = np.mean(test1_scores)
        all_mean_test2 = np.mean(test2_scores)
        best_mean_test1 = np.mean(best_subjects_test1)
        best_mean_test2 = np.mean(best_subjects_test2)
        return (
            test1_scores, test2_scores, best_subjects_test1, best_subjects_test2,
            all_mean_test1, all_mean_test2, best_mean_test1, best_mean_test2
        )
    except Exception as e:
        st.error(f"Ошибка при генерации данных: {str(e)}")
        return None


def regression_to_mean_tab():
    """Вкладка регрессии к среднему"""
    if "visited_tabs" not in st.session_state:
        st.session_state.visited_tabs = set()
    st.session_state.visited_tabs.add("Регрессия к среднему")

    st.header("Регрессия к среднему")
    st.markdown(
        """**Регрессия к среднему** — статистический феномен, когда переменная с экстремальным
    значением при повторном измерении стремится ближе к среднему значению популяции."""
    )

    col1, col2 = st.columns(2)
    with col1:
        mu_reg = st.slider("Истинное среднее популяции", 0, 100, 50)
        sigma_reg = st.slider("Стандартное отклонение", 5, 30, 15)
    with col2:
        n_subjects = st.slider("Количество субъектов", 20, 500, 100)
        threshold_percentile = st.slider("Порог отбора (процентиль)", 70, 95, 80)

    regression_data = generate_regression_data(mu_reg, sigma_reg, n_subjects, threshold_percentile)
    if regression_data:
        (
            test1_scores, test2_scores, best_subjects_test1, best_subjects_test2,
            all_mean_test1, all_mean_test2, best_mean_test1, best_mean_test2
        ) = regression_data

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.scatter(test1_scores, test2_scores, alpha=0.4, label="Все субъекты", color="gray", s=20)
        ax.scatter(best_subjects_test1, best_subjects_test2, alpha=0.7,
                   label=f"Лучшие субъекты (> {threshold_percentile}%)", color="red", s=30)
        min_val = min(np.min(test1_scores), np.min(test2_scores))
        max_val = max(np.max(test1_scores), np.max(test2_scores))
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, label="Линия y=x", linewidth=2)
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

        diff = best_mean_test1 - best_mean_test2
        pct_diff = (diff / best_mean_test1) * 100 if best_mean_test1 != 0 else 0
        st.markdown(
            f"""
        ### Результаты анализа
        - Среднее первого теста (все): {all_mean_test1:.2f}
        - Среднее второго теста (все): {all_mean_test2:.2f}
        - Среднее первого теста (лучшие): {best_mean_test1:.2f}
        - Среднее второго теста (лучшие): {best_mean_test2:.2f}
        - **Регрессия к среднему**: {diff:.2f} пунктов ({pct_diff:.1f}%)
        """
        )

    st.markdown(
        """### Объяснение эффекта
    
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
    """
    )
