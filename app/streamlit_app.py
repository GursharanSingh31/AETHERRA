"""AETHERRA / Field Shift — premium Streamlit UI.

Run from your AETHERRA project root:
    python -m streamlit run app/streamlit_app.py

Required:
    data/processed/merged_dataset.csv

Optional:
    data/processed/model_predictions.csv
    app/recommendations.py
"""

from __future__ import annotations

import base64
import html
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =====================================================
# 1. APP CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AETHERRA · Field Shift",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
ASSETS = APP_DIR / "assets"
PROCESSED = ROOT / "data" / "processed"

sys.path.insert(0, str(APP_DIR))


# =====================================================
# 2. UTILITY FUNCTIONS
# =====================================================

def safe(value):
    return html.escape(str(value), quote=True)


def render_html(markup):
    st.markdown(markup.strip(), unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_asset(name):
    path = ASSETS / name

    if not path.is_file():
        return ""

    mime = (
        "image/png"
        if path.suffix.lower() == ".png"
        else "image/jpeg"
    )

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("ascii")

    return f"data:{mime};base64,{encoded}"


@st.cache_data(show_spinner=False)
def load_nasa_data():
    merged_file = PROCESSED / "merged_dataset.csv"

    if not merged_file.exists():
        return None, None

    merged = pd.read_csv(
        merged_file,
        parse_dates=["date"]
    )

    prediction_file = PROCESSED / "model_predictions.csv"

    predictions = None

    if prediction_file.exists():
        predictions = pd.read_csv(
            prediction_file,
            parse_dates=["date"]
        )

    return merged, predictions


def pretty_number(value, digits=1, unit=""):
    if pd.isna(value):
        return "—"
    return f"{value:,.{digits}f}{unit}"


def card_metric(label, value, note, symbol, accent="mint"):
    render_html(
        f'<div class="metric-card accent-{accent}">'
        '<div class="metric-top">'
        f'<span>{safe(label)}</span>'
        f'<span class="metric-symbol">{safe(symbol)}</span>'
        '</div>'
        f'<div class="metric-number">{safe(value)}</div>'
        f'<div class="metric-note">{safe(note)}</div>'
        '</div>'
    )


def feature_card(image, label, title, subtitle, icon):
    image_tag = (
        f'<img src="{image}" alt="{safe(title)}">'
        if image
        else '<div class="missing-image">🌿</div>'
    )

    render_html(
        '<div class="feature-card">'
        + image_tag
        + '<div class="feature-overlay">'
        f'<span class="feature-label">{safe(label)}</span>'
        f'<div class="feature-title">{safe(icon)} {safe(title)}</div>'
        f'<div class="feature-subtitle">{safe(subtitle)}</div>'
        '</div></div>'
    )


def section_head(kicker, title, explanation=""):
    render_html(
        '<div class="section-heading">'
        '<div>'
        f'<span class="section-kicker">{safe(kicker)}</span>'
        f'<h2>{safe(title)}</h2>'
        '</div>'
        f'<p>{safe(explanation)}</p>'
        '</div>'
    )


def plot_style(fig, height=390, y_title="", title=""):
    """Keep titles, legends and axis labels in separate spaces."""
    multiple_series = len(fig.data) > 1
    fig.update_layout(
        template="plotly_dark",
        title=dict(text=title, font=dict(size=16, color="#edf5e9"),
                   x=0.02, xanchor="left", y=0.98, yanchor="top"),
        height=max(height, 480) if multiple_series else height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b9cdbd", family="Inter, Segoe UI, sans-serif", size=12),
        margin=dict(l=65, r=25, t=80, b=105 if multiple_series else 55),
        hovermode="x unified",
        showlegend=multiple_series,
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,.065)",
                   zeroline=False, automargin=True, title=None),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,.065)",
                   zeroline=False, automargin=True, title=y_title),
        legend=dict(orientation="h", x=0, xanchor="left",
                    y=-0.25, yanchor="top", font=dict(size=11),
                    bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#143329", font_color="#f5f6ed"),
    )
    return fig


def plot_chart(fig):
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displaylogo": False}
    )


def label_year(data):
    result = data.copy()
    result["year"] = result["date"].dt.year
    return result


# =====================================================
# 3. LOAD PREMIUM CSS
# =====================================================

css_path = APP_DIR / "styles.css"

if css_path.is_file():
    css = css_path.read_text(encoding="utf-8")
    render_html(f"<style>{css}</style>")
else:
    st.warning(
        "styles.css is missing from app/. "
        "Copy the CSS file from your UI package."
    )


# =====================================================
# 4. LOAD VISUAL ASSETS
# =====================================================

hero_img = load_asset("hero_farm.jpg")
orbital_img = load_asset("satellite.jpg")
wheat_img = load_asset("wheat.jpg")
paddy_img = load_asset("paddy.jpg")
climate_img = load_asset("climate_bg.jpg")


# =====================================================
# 5. LOAD NASA DATASETS
# =====================================================

df, predictions = load_nasa_data()

if df is None:
    st.error(
        "Cannot find data/processed/merged_dataset.csv"
    )
    st.stop()

required = {
    "date",
    "district",
    "ndvi",
    "temperature",
    "rainfall",
    "humidity",
    "solar_radiation"
}

missing = sorted(required - set(df.columns))

if missing:
    st.error(
        "Missing columns: " + ", ".join(missing)
    )
    st.stop()

if df.empty:
    st.error("Your merged dataset is empty.")
    st.stop()

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["district"] = (
    df["district"]
    .astype(str)
    .str.strip()
    .str.lower()
)

numeric_columns = [
    "ndvi",
    "temperature",
    "rainfall",
    "humidity",
    "solar_radiation",
    "max_temperature"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

df = df.dropna(
    subset=["date", "district"]
).sort_values(["district", "date"])

if df.empty:
    st.error("No valid dated records found.")
    st.stop()

if predictions is not None:
    predictions["date"] = pd.to_datetime(
        predictions["date"],
        errors="coerce"
    )

    predictions["district"] = (
        predictions["district"]
        .astype(str)
        .str.strip()
        .str.lower()
    )


# =====================================================
# 6. SIDEBAR / MISSION CONTROL
# =====================================================

with st.sidebar:

    render_html(
        '<div class="brand">'
        '<div class="brand-mark">✳</div>'
        '<div>'
        '<div class="brand-name">AETHERRA</div>'
        '<div class="brand-sub">'
        'FIELD SHIFT · MISSION CONTROL'
        '</div>'
        '</div></div>'
    )

    render_html(
        '<div class="sidebar-group-label">'
        'EXPLORE THE REGION'
        '</div>'
    )

    locations = sorted(
        df["district"].dropna().unique().tolist()
    )

    district = st.selectbox(
        "District",
        locations,
        format_func=lambda value: str(value).title()
    )

    crop = st.selectbox(
        "Crop context",
        ["Wheat", "Paddy"],
        help=(
            "Crop selection changes visual context. "
            "The NASA data is not crop-specific."
        )
    )

    earliest = int(df["date"].dt.year.min())
    latest = int(df["date"].dt.year.max())

    if earliest < latest:
        start_year, end_year = st.slider(
            "Observation years",
            earliest,
            latest,
            (earliest, latest)
        )
    else:
        start_year = end_year = earliest

    st.divider()

    render_html(
        '<div class="sidebar-group-label">'
        'MISSION SYSTEMS'
        '</div>'
    )

    render_html(
        '<div class="side-nav">'
        '<div><i class="dot dot-green"></i>'
        ' Climate Observatory</div>'
        '<div><i class="dot dot-teal"></i>'
        ' Satellite Vegetation</div>'
        '<div><i class="dot dot-yellow"></i>'
        ' ML Evaluation</div>'
        '<div><i class="dot dot-purple"></i>'
        ' Explainable Insights</div>'
        '</div>'
    )

    st.divider()

    render_html(
        '<div class="sidebar-source">'
        '<span>DATA SOURCE STATUS</span>'
        '<strong>● NASA POWER + MODIS</strong>'
        '<small>Historical observations · '
        '2010–2025 target period</small>'
        '</div>'
    )

    st.caption(
        "Research prototype. Not a live forecast "
        "or validated farm-level advice."
    )


# =====================================================
# 7. FILTER DISTRICT DATA
# =====================================================

filtered = df.loc[
    (df["district"] == district)
    & df["date"].dt.year.between(
        start_year,
        end_year
    )
].sort_values("date").copy()

if filtered.empty:
    st.warning(
        "No observations found for this selection. "
        "Try widening the year range."
    )
    st.stop()


# =====================================================
# 8. CINEMATIC HERO
# =====================================================

if hero_img:
    background_css = (
        "linear-gradient("
        "90deg,"
        "rgba(5,22,17,.96) 1%,"
        "rgba(5,22,17,.78) 48%,"
        "rgba(4,19,15,.16) 100%"
        "),"
        f"url('{hero_img}')"
    )
else:
    background_css = (
        "linear-gradient(115deg,#102d23,#3c6951)"
    )

render_html(
    f'<div class="hero" style="background-image:{background_css}">'
    '<span class="hero-eyebrow">'
    '<i class="live-dot"></i>'
    ' NASA EARTH INTELLIGENCE · PUNJAB'
    '</span>'
    '<h1>THE FUTURE<br>OF FARMING<span>.</span></h1>'
    '<p>'
    'Understand what has changed above our fields '
    'and what the data can tell us about tomorrow. '
    'A transparent, NASA-powered climate intelligence prototype.'
    '</p>'
    '<div class="hero-chips">'
    '<span>◉ FIELD SHIFT</span>'
    '<span>NASA POWER</span>'
    '<span>MODIS NDVI</span>'
    '<span>EXPLAINABLE ML</span>'
    '</div>'
    '<div class="hero-watermark">AETHERRA / 01</div>'
    '</div>'
)


# =====================================================
# 9. CLIMATE OVERVIEW METRICS
# =====================================================

section_head(
    "01 / REGIONAL SNAPSHOT",
    "The earth, in numbers.",
    (
        f"{district.title()} · {crop} context · "
        f"{start_year}–{end_year}"
    )
)

metric_columns = st.columns(4)

with metric_columns[0]:
    card_metric(
        "MEAN TEMPERATURE",
        pretty_number(
            filtered["temperature"].mean(),
            1,
            " °C"
        ),
        "Matched observation windows",
        "↗",
        "orange"
    )

with metric_columns[1]:
    card_metric(
        "MEAN 16-DAY RAINFALL",
        pretty_number(
            filtered["rainfall"].mean(),
            1,
            " mm"
        ),
        "Not a whole-year rainfall total",
        "☂",
        "blue"
    )

with metric_columns[2]:
    card_metric(
        "MEAN NDVI",
        pretty_number(
            filtered["ndvi"].mean(),
            3
        ),
        "Satellite greenness index",
        "◈",
        "mint"
    )

with metric_columns[3]:
    card_metric(
        "OBSERVATIONS",
        f"{len(filtered):,}",
        "Quality-filtered periods",
        "▦",
        "purple"
    )


# =====================================================
# 10. VISUAL FEATURE CARDS
# =====================================================

section_head(
    "02 / LOOK CLOSER",
    "From space, to soil.",
    "Explore our satellite data and agricultural context"
)

image_columns = st.columns(3, gap="medium")

with image_columns[0]:
    feature_card(
        orbital_img,
        "01 · SATELLITE",
        "Above the fields",
        "MODIS vegetation observations",
        "✦"
    )

with image_columns[1]:
    crop_img = (
        wheat_img if crop == "Wheat"
        else paddy_img
    )

    feature_card(
        crop_img,
        "02 · AGRICULTURE",
        f"{crop} landscapes",
        "Illustrative crop imagery",
        "✦"
    )

with image_columns[2]:
    feature_card(
        climate_img,
        "03 · CLIMATE",
        "Patterns in motion",
        "Temperature, rainfall and solar signals",
        "✦"
    )

render_html(
    '<div class="art-note">'
    '✳ Decorative visuals are generated artwork. '
    'Analytical charts use processed NASA data.'
    '</div>'
)


# =====================================================
# 11. ANALYTICS WORKSPACE
# =====================================================

section_head(
    "03 / INTELLIGENCE WORKSPACE",
    "Explore the evidence.",
    "Choose a view and interact with the NASA data"
)

(
    tab_overview,
    tab_climate,
    tab_vegetation,
    tab_ai,
    tab_insights,
    tab_data
) = st.tabs([
    "◉ Overview",
    "☀ Climate",
    "◈ Vegetation",
    "✦ AI Lab",
    "✧ Insights",
    "▤ Source Data"
])


# =====================================================
# TAB 1 — OVERVIEW
# =====================================================

with tab_overview:

    left, right = st.columns(
        [1.4, 1],
        gap="large"
    )

    with left:
        st.markdown(
            "#### Vegetation observations over time"
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=filtered["date"],
                y=filtered["ndvi"],
                mode="lines+markers",
                name="Observed NDVI",
                line=dict(
                    color="#9ce6b1",
                    width=2.6
                ),
                marker=dict(size=4),
                fill="tozeroy",
                fillcolor="rgba(82,198,131,.10)"
            )
        )

        plot_chart(
            plot_style(
                fig,
                title="Vegetation greenness · MODIS NDVI",
                y_title="NDVI"
            )
        )

    with right:

        st.markdown("#### What we're measuring")

        render_html(
            '<div class="explainer">'
            '<b>01 Temperature</b>'
            '<p>Mean air temperature during '
            'matched weather periods.</p>'
            '<b>02 Rainfall</b>'
            '<p>Precipitation accumulated during '
            'matched observation windows.</p>'
            '<b>03 Vegetation</b>'
            '<p>MODIS-derived greenness with '
            'quality-filtered observations.</p>'
            '</div>'
        )

        if len(locations) > 1:

            st.markdown("#### Compare districts")

            other_district = st.selectbox(
                "Compare against",
                [
                    d for d in locations
                    if d != district
                ],
                format_func=str.title,
                key="district_comparison"
            )

            secondary = df.loc[
                (df["district"] == other_district)
                & df["date"].dt.year.between(
                    start_year,
                    end_year
                )
            ]

            comparison = go.Figure()

            for name, sample, color in [
                (district, filtered, "#9ce6b1"),
                (other_district, secondary, "#ecc78e")
            ]:

                annual = (
                    label_year(sample)
                    .groupby("year", as_index=False)["ndvi"]
                    .mean()
                )

                comparison.add_trace(
                    go.Scatter(
                        x=annual["year"],
                        y=annual["ndvi"],
                        name=name.title(),
                        mode="lines+markers",
                        line=dict(
                            color=color,
                            width=2.5
                        )
                    )
                )

            plot_chart(
                plot_style(
                    comparison,
                    height=270,
                    title="Mean available NDVI by year",
                    y_title="NDVI"
                )
            )

    st.caption(
        "Comparisons use available quality-filtered "
        "point observations, not district-wide crop measurements."
    )


# =====================================================
# TAB 2 — CLIMATE
# =====================================================

with tab_climate:

    st.markdown("#### Historical climate explorer")

    indicator = st.selectbox(
        "Choose climate indicator",
        [
            "Temperature",
            "Rainfall",
            "Humidity",
            "Solar radiation"
        ]
    )

    indicators = {
        "Temperature": (
            "temperature",
            "Temperature (°C)",
            "#f1b879"
        ),
        "Rainfall": (
            "rainfall",
            "Rainfall per matched period (mm)",
            "#6cc8e8"
        ),
        "Humidity": (
            "humidity",
            "Relative humidity (%)",
            "#8bd7c6"
        ),
        "Solar radiation": (
            "solar_radiation",
            "Solar radiation (MJ/m²/day)",
            "#cbb7f6"
        )
    }

    column, label, color = indicators[indicator]

    fig = go.Figure()

    if indicator == "Rainfall":

        fig.add_trace(
            go.Bar(
                x=filtered["date"],
                y=filtered[column],
                name=indicator,
                marker_color=color
            )
        )

    else:

        fig.add_trace(
            go.Scatter(
                x=filtered["date"],
                y=filtered[column],
                mode="lines+markers",
                name=indicator,
                line=dict(
                    color=color,
                    width=2.7
                ),
                marker=dict(size=4)
            )
        )

    plot_chart(
        plot_style(
            fig,
            height=450,
            title=f"{indicator} · {district.title()}",
            y_title=label
        )
    )

    st.info(
        "Weather is aggregated into MODIS-matched "
        "periods with usable NDVI observations. "
        "These are not complete calendar-year summaries."
    )


# =====================================================
# TAB 3 — VEGETATION
# =====================================================

with tab_vegetation:

    st.markdown(
        "#### Observing vegetation from space"
    )

    annual = (
        label_year(filtered)
        .groupby("year", as_index=False)
        .agg(
            ndvi=("ndvi", "mean"),
            count=("ndvi", "size")
        )
    )

    left, right = st.columns(
        [1.5, 1],
        gap="large"
    )

    with left:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=filtered["date"],
                y=filtered["ndvi"],
                mode="lines+markers",
                name="NDVI",
                line=dict(
                    color="#a7e3af",
                    width=2.7
                ),
                fill="tozeroy",
                fillcolor="rgba(116,206,136,.15)"
            )
        )

        plot_chart(
            plot_style(
                fig,
                title="Satellite vegetation signal",
                y_title="NDVI"
            )
        )

    with right:

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=annual["year"].astype(str),
                y=annual["ndvi"],
                marker_color="#6ec695",
                name="Mean NDVI"
            )
        )

        plot_chart(
            plot_style(
                fig,
                title="Annual mean of usable records",
                y_title="NDVI"
            )
        )

    render_html(
        '<div class="explainer compact">'
        '<b>What does NDVI mean?</b>'
        '<p>Normalized Difference Vegetation Index '
        'is a satellite-derived measure of vegetation '
        'greenness. It cannot, by itself, diagnose '
        'crop disease, yield loss or the cause '
        'of vegetation changes.</p>'
        '</div>'
    )


# =====================================================
# TAB 4 — AI / ML PREDICTIONS
# =====================================================

with tab_ai:

    st.markdown(
        "#### Model evaluation · historical test data"
    )

    if predictions is None:

        st.warning(
            "Missing model_predictions.csv. "
            "Run your existing ML training script."
        )

    else:

        selected = predictions.loc[
            (predictions["district"] == district)
            & predictions["date"].dt.year.between(
                start_year,
                end_year
            )
        ].sort_values("date").copy()

        required_pred = {
            "actual_ndvi",
            "predicted_ndvi",
            "baseline_ndvi"
        }

        missing_pred = (
            required_pred - set(selected.columns)
        )

        if missing_pred:

            st.error(
                "Prediction CSV is missing: "
                + ", ".join(sorted(missing_pred))
            )

        else:

            for name in required_pred:
                selected[name] = pd.to_numeric(
                    selected[name],
                    errors="coerce"
                )

            selected = selected.dropna(
                subset=list(required_pred) + ["date"]
            )

            if selected.empty:

                st.info(
                    "No held-out predictions for the selected "
                    "district and year range. Try a wider "
                    "or more recent period."
                )

            else:

                fig = go.Figure()

                series = [
                    (
                        "Actual NDVI",
                        "actual_ndvi",
                        "#a9e9b7",
                        "solid"
                    ),
                    (
                        "Random Forest",
                        "predicted_ndvi",
                        "#f4bf83",
                        "solid"
                    ),
                    (
                        "Persistence baseline",
                        "baseline_ndvi",
                        "#abb5ca",
                        "dash"
                    )
                ]

                for name, column, color, dash in series:

                    fig.add_trace(
                        go.Scatter(
                            x=selected["date"],
                            y=selected[column],
                            mode="lines+markers",
                            name=name,
                            line=dict(
                                color=color,
                                width=2.6,
                                dash=dash
                            ),
                            marker=dict(size=5)
                        )
                    )

                plot_chart(
                    plot_style(
                        fig,
                        height=450,
                        title="Observed vs predicted greenness",
                        y_title="NDVI"
                    )
                )

                model_mae = (
                    selected["actual_ndvi"]
                    - selected["predicted_ndvi"]
                ).abs().mean()

                baseline_mae = (
                    selected["actual_ndvi"]
                    - selected["baseline_ndvi"]
                ).abs().mean()

                metrics = st.columns(3)

                with metrics[0]:
                    card_metric(
                        "MODEL MAE",
                        pretty_number(model_mae, 4),
                        "Lower is better",
                        "✦",
                        "mint"
                    )

                with metrics[1]:
                    card_metric(
                        "BASELINE MAE",
                        pretty_number(baseline_mae, 4),
                        "Previous-observation prediction",
                        "≈",
                        "blue"
                    )

                with metrics[2]:
                    card_metric(
                        "TEST SAMPLES",
                        f"{len(selected):,}",
                        "Selected held-out records",
                        "▦",
                        "purple"
                    )

                if model_mae < baseline_mae:

                    st.success(
                        "Random Forest outperforms the "
                        "persistence baseline for this selection."
                    )

                else:

                    st.info(
                        "The baseline is as good as or better "
                        "than Random Forest for this selection."
                    )

                st.caption(
                    "This is a historical next-observation "
                    "experiment, not an operational future-season "
                    "or crop-yield forecast."
                )


# =====================================================
# TAB 5 — EXPLAINABLE INSIGHTS
# =====================================================

with tab_insights:

    st.markdown(
        "#### Explainable climate insights"
    )

    st.caption(
        "Transparent exploratory thresholds, not validated "
        "crop-specific farming recommendations."
    )

    try:

        from recommendations import get_recommendations

        insights = get_recommendations(
            filtered,
            crop
        )

        if isinstance(insights, str):
            insights = [insights]

        for index, insight in enumerate(insights, 1):

            render_html(
                '<div class="insight-card">'
                f'<span>INSIGHT / {index:02d}</span>'
                f'<p>{safe(insight)}</p>'
                '</div>'
            )

    except ImportError:

        st.info(
            "app/recommendations.py is missing. "
            "Keep your existing recommendation module "
            "inside the app folder."
        )

    except Exception as exc:

        st.error(
            f"Recommendation module error: {exc}"
        )

    with st.expander(
        "How are these insights created?"
    ):

        st.write(
            "Your existing recommendation function evaluates "
            "historical temperature, rainfall and NDVI "
            "observations against exploratory thresholds."
        )

        st.write(
            "It does not use live weather forecasts, "
            "field-specific soil measurements or "
            "crop-yield observations."
        )


# =====================================================
# TAB 6 — SOURCE DATA
# =====================================================

with tab_data:

    st.markdown(
        "#### The data behind every chart"
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "↓ Export selected NASA observations",
        data=filtered.to_csv(
            index=False
        ).encode("utf-8"),
        file_name=(
            f"aetherra_{district}_"
            f"{start_year}_{end_year}.csv"
        ),
        mime="text/csv"
    )

    with st.expander(
        "Source information and research limitations"
    ):

        st.markdown("""
**NASA POWER**

- Temperature
- Precipitation
- Relative humidity
- Solar radiation

**NASA MODIS MOD13Q1.061**

- Approximately 16-day vegetation index
- Nominal 250-metre spatial resolution
- Quality-filtered NDVI

**Processing**

- Filter unreliable MODIS observations
- Match weather records to vegetation observation periods
- Train and evaluate a historical Random Forest model

**Limitations**

- Representative geographic points, not entire districts
- Missing observation periods due to quality filtering
- Crop selection changes context only
- No validated crop-specific yield predictions
- No live weather forecast
        """)


# =====================================================
# 12. HOW FIELD SHIFT WORKS
# =====================================================

section_head(
    "04 / TRANSPARENT BY DESIGN",
    "From orbit to insight.",
    "Our four-step scientific workflow"
)

steps = [
    (
        "01",
        "OBSERVE",
        "NASA weather and MODIS satellite observations"
    ),
    (
        "02",
        "PREPARE",
        "Clean records and align measurement periods"
    ),
    (
        "03",
        "MODEL",
        "Estimate NDVI with a tested Random Forest"
    ),
    (
        "04",
        "EXPLAIN",
        "Present transparent, rule-based climate insights"
    )
]

for column, (number, title, description) in zip(
    st.columns(4),
    steps
):

    with column:

        render_html(
            '<div class="process-card">'
            f'<span>{number}</span>'
            f'<b>{safe(title)}</b>'
            f'<p>{safe(description)}</p>'
            '</div>'
        )


# =====================================================
# 13. FOOTER
# =====================================================

render_html(
    '<div class="site-footer">'
    '<strong>AETHERRA <span>✳</span> FIELD SHIFT</strong>'
    '<p>NASA-powered research prototype for Punjab agriculture. '
    'Built to explore historical climate and vegetation patterns.</p>'
    '<small>'
    'Educational prototype · No validated farm-level prescriptions, '
    'real-time forecasts or crop-yield guarantees.'
    '</small>'
    '</div>'
)