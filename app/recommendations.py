import pandas as pd

def get_recommendations(df, crop):
    """Educational climate insights, not agronomic prescriptions."""
    recommendations = []

    if df.empty:
        return ["Insufficient data for recommendations."]

    # Historical measurements from merged NASA data
    avg_temp = df["temperature"].mean()
    avg_rain = df["rainfall"].mean()
    avg_ndvi = df["ndvi"].mean()

    if avg_temp > 30:
        recommendations.append(
            "🌡️ High average temperature observed. "
            "Consider reviewing heat-stress risks with "
            "local agricultural advisory services."
        )

    if avg_rain < 10:
        recommendations.append(
            "🌧️ Low average rainfall per observed 16-day period. "
            "Review seasonal rainfall distribution before "
            "making irrigation decisions."
        )

    if avg_ndvi < 0.3:
        recommendations.append(
            "🌿 Low average vegetation greenness. "
            "This can reflect crop cycles, bare soil or "
            "vegetation conditions; NDVI alone cannot "
            "diagnose crop stress."
        )

    if not recommendations:
        recommendations.append(
            "✅ No simple indicator thresholds were triggered. "
            "This does not guarantee low agricultural risk."
        )

    recommendations.append(
        f"Crop selected: {crop}. These preliminary indicators "
        "are not yet calibrated specifically for this crop."
    )

    return recommendations