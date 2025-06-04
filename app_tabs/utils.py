import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from io import BytesIO
from typing import Tuple, List, Dict, Any

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
            st.write(f"{key.capitalize()}: {value:.4f}")
        else:
            st.write(f"{key.capitalize()}: невозможно вычислить")
