import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Демоверсия вероятностных законов", layout="wide")

st.title("📊 Демонстрация вероятностных законов")
tabs = st.tabs(["Закон трёх сигм", "ЦПТ", "ЗБЧ"])

# === Вкладка 1: Закон трёх сигм ===
with tabs[0]:
    st.header("Закон трёх сигм (эмпирическое правило)")
    mu = st.slider("Среднее (μ)", 20, 80, 50)
    sigma = st.slider("Стандартное отклонение (σ)", 1, 30, 10)
    size = st.slider("Размер выборки", 1000, 50000, 10000, step=1000)

    data = np.random.normal(mu, sigma, size)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=50,
        histnorm="probability density",
        marker_color="lightgray",
        name="Данные",
        opacity=0.75
    ))

    colors = [
        "rgba(178,223,138,0.3)",
        "rgba(253,191,111,0.3)",
        "rgba(251,154,153,0.3)"
    ]
    labels = ["±1σ (68%)", "±2σ (95%)", "±3σ (99.7%)"]

    for i, color, label in zip([1, 2, 3], colors, labels):
        fig.add_vrect(
            x0=mu - i * sigma, x1=mu + i * sigma,
            fillcolor=color, line_width=0,
            annotation_text=label, annotation_position="top left"
        )
        fig.add_vline(x=mu - i * sigma, line_dash="dash", line_color="red")
        fig.add_vline(x=mu + i * sigma, line_dash="dash", line_color="red")

    fig.update_layout(
        title=f"Закон трёх сигм (μ = {mu}, σ = {sigma})",
        xaxis_title="Значение",
        yaxis_title="Плотность вероятности",
        bargap=0.1,
        hovermode="x",
        autosize=True,
        margin=dict(l=30, r=30, t=50, b=30)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"responsive": True, "displaylogo": False}
    )

    st.markdown(f"""
    **Пояснение**  
    График демонстрирует _закон трёх сигм_, согласно которому:
    - около **68%** значений попадают в диапазон ±1σ от среднего,
    - около **95%** — в диапазон ±2σ,
    - около **99.7%** — в диапазон ±3σ.

    Здесь μ = {mu}, σ = {sigma}, n = {size}.
    """)

# === Вкладка 2: Центральная предельная теорема ===
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
            h = n // 2
            return np.concatenate([
                np.random.normal(-2, 1, h),
                np.random.normal(2, 1, n - h)
            ])
        return np.random.normal(0, 1, n)

    means = [np.mean(generate(dist_type, sample_size)) for _ in range(num_samples)]

    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(
        x=means,
        nbinsx=30,
        marker_color="skyblue",
        name="Средние выборки",
        opacity=0.75
    ))
    fig2.update_layout(
        title=f"ЦПТ: Средние {num_samples} выборок ({dist_type}, размер = {sample_size})",
        xaxis_title="Среднее значение выборки",
        yaxis_title="Частота",
        hovermode="x",
        height=700,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    **Пояснение**  
    _Центральная предельная теорема_ утверждает, что независимо от распределения исходных данных
    распределение **средних значений** будет стремиться к нормальному при увеличении размера выборки.

    Здесь: распределение = {dist_type.lower()}, размер выборки = {sample_size}, число выборок = {num_samples}.
    """)

# === Вкладка 3: Закон больших чисел ===
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

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        y=cumulative,
        mode="lines",
        name="Накопленное среднее"
    ))
    fig3.add_hline(
        y=expected,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Теоретическое среднее ({expected:.2f})",
        annotation_position="bottom right"
    )
    fig3.update_layout(
        title="Закон больших чисел",
        xaxis_title="Количество испытаний",
        yaxis_title="Среднее значение",
        hovermode="x",
        height=500,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f"""
    **Пояснение**  
    _Закон больших чисел_ утверждает, что по мере увеличения количества наблюдений среднее значение будет сходиться
    к математическому ожиданию распределения. Здесь использовано **{trials}** испытаний из **{dist_type_lln.lower()} распределения**.
    """)
