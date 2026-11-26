
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pathlib import Path
import base64

BASE = Path(r"C:\Users\AKRIT\Downloads\Flood")
DATA = BASE / "dataset" / "processed"
IMAGES = BASE / "visualizations"
APP = BASE / "streamlit_app"
MAP_FILE = APP / "upper_beas_interactive_map.html"

st.set_page_config(
    page_title="Upper Beas | Flood Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, #102b43 0%, transparent 38%),
        linear-gradient(145deg, #07111f 0%, #0a1626 55%, #101b2d 100%);
    color: #e7f0fa;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1728, #101e32);
    border-right: 1px solid rgba(56,189,248,0.18);
}

[data-testid="stSidebar"] * {
    color: #dceafa;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 11px 12px;
    border-radius: 10px;
    transition: all .25s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(34,211,238,.13);
    transform: translateX(4px);
}

.hero {
    padding: 30px 32px;
    border-radius: 20px;
    background: linear-gradient(115deg, rgba(13,45,72,.95), rgba(13,28,49,.88));
    border: 1px solid rgba(56,189,248,.25);
    box-shadow: 0 15px 45px rgba(0,0,0,.22);
    margin-bottom: 25px;
    animation: appear .7s ease;
}

.hero h1 {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #f0f9ff;
    margin: 0;
}

.hero p {
    color: #9db8d1;
    margin-top: 10px;
    font-size: 14px;
}

.eyebrow {
    color: #22d3ee;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 800;
    margin-bottom: 12px;
}

.metric-card {
    background: linear-gradient(145deg, rgba(20,43,68,.95), rgba(13,29,48,.95));
    border: 1px solid rgba(56,189,248,.20);
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
    transition: all .3s ease;
    animation: appear .6s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: #22d3ee;
    box-shadow: 0 10px 30px rgba(0,190,230,.12);
}

.metric-label {
    color: #91a9c2;
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    color: #f0f9ff;
    font-size: 30px;
    font-weight: 800;
    margin-top: 12px;
}

.metric-sub {
    color: #22d3ee;
    font-size: 11px;
    margin-top: 5px;
}

.panel {
    background: rgba(15,32,52,.85);
    border: 1px solid rgba(56,189,248,.17);
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 8px 28px rgba(0,0,0,.12);
}

.section-title {
    color: #e7f5ff;
    font-size: 21px;
    font-weight: 750;
    margin-bottom: 5px;
}

.section-sub {
    color: #91a9c2;
    font-size: 12px;
    margin-bottom: 18px;
}

.tag {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 20px;
    background: rgba(34,211,238,.12);
    color: #67e8f9;
    font-size: 11px;
    font-weight: 700;
    border: 1px solid rgba(34,211,238,.25);
}

div[data-testid="stImage"] img {
    border-radius: 13px;
    border: 1px solid rgba(56,189,248,.18);
}

.stButton button {
    background: linear-gradient(100deg,#0891b2,#2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

.stButton button:hover {
    border: 1px solid #67e8f9;
    transform: translateY(-2px);
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(56,189,248,.2);
    border-radius: 12px;
}

footer {visibility: hidden;}

@keyframes appear {
    from {opacity: 0; transform: translateY(12px);}
    to {opacity: 1; transform: translateY(0);}
}

@media (max-width: 700px) {
    .hero h1 {font-size: 25px;}
    .hero {padding: 22px;}
}
</style>
""", unsafe_allow_html=True)

def metric_card(label, value, subtitle):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def section_header(title, subtitle=""):
    st.markdown(f"""
    <div class="section-title">{title}</div>
    <div class="section-sub">{subtitle}</div>
    """, unsafe_allow_html=True)

def show_image(filename, caption=None):
    path = IMAGES / filename
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.warning(f"Visualization not found: {filename}")

def show_map():
    if MAP_FILE.exists():
        html = MAP_FILE.read_text(encoding="utf-8")
        components.html(html, height=730, scrolling=False)
    else:
        st.warning("Interactive map not found. Generate upper_beas_interactive_map.html first.")


def show_dynamic_map(day, selected_layer, selected_date):
    import folium
    from folium.plugins import MarkerCluster
    from branca.colormap import LinearColormap
    from html import escape

    boundary_file = DATA / "upper_beas_boundary.geojson"
    events_file = DATA / "historical_flood_events_final.csv"
    dbscan_file = DATA / "dbscan_single_day_test.csv"

    center = [31.80, 77.10]

    m = folium.Map(
        location=center,
        zoom_start=9,
        tiles=None,
        control_scale=True
    )

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite Imagery",
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        "OpenStreetMap",
        name="Street Map",
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attr="OpenTopoMap",
        name="Terrain",
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Place Names & Boundaries",
        overlay=True,
        control=True,
        show=True
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Roads & Transportation",
        overlay=True,
        control=True,
        show=False
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Place Names & Boundaries",
        overlay=True,
        control=True,
        show=True
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Roads & Transportation",
        overlay=True,
        control=True,
        show=False
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places_Alternate/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Detailed Local Place Names",
        overlay=True,
        control=True,
        show=False
    ).add_to(m)

    folium.TileLayer(
        tiles="https://tiles.arcgis.com/tiles/P3ePLMYs2RVChkJx/arcgis/rest/services/Esri_Hydro_Reference_Overlay/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Hydro Reference",
        name="Waterways & Geographic Features",
        overlay=True,
        control=True,
        show=False
    ).add_to(m)

    if boundary_file.exists():
        folium.GeoJson(
            str(boundary_file),
            name="Upper Beas Basin Boundary",
            style_function=lambda feature: {
                "color": "#22d3ee",
                "weight": 3,
                "fillOpacity": 0.04
            },
            tooltip="Provisional Upper Beas Basin Boundary"
        ).add_to(m)

    value_columns = {
        "Rainfall": ("rainfall_mm", "mm"),
        "Surface Soil Moisture": ("sm_surface", "m³/m³"),
        "Root-zone Soil Moisture": ("sm_rootzone", "m³/m³")
    }

    cluster_data = None

    if selected_layer == "DBSCAN Clusters":
        if selected_date == pd.Timestamp("2015-09-22").date() and dbscan_file.exists():
            cluster_data = pd.read_csv(dbscan_file)
            day = day.merge(
                cluster_data[["grid_id", "cluster"]],
                on="grid_id",
                how="left"
            )

    if selected_layer in value_columns:
        column, unit = value_columns[selected_layer]
        values = pd.to_numeric(day[column], errors="coerce")
        valid = values.dropna()

        if len(valid):
            low = float(valid.min())
            high = float(valid.max())

            if low == high:
                high = low + 1e-9

            scale = LinearColormap(
                ["#2563eb", "#06b6d4", "#a3e635", "#facc15", "#ef4444"],
                vmin=low,
                vmax=high
            )
            scale.caption = f"{selected_layer} ({unit})"
            scale.add_to(m)
        else:
            scale = None
    else:
        scale = None

    grid_layer = folium.FeatureGroup(
        name=f"{selected_layer} — {selected_date}",
        show=True
    )

    cluster_colors = [
        "#06b6d4", "#a3e635", "#facc15", "#a78bfa",
        "#fb923c", "#34d399", "#f472b6", "#60a5fa",
        "#c084fc", "#2dd4bf", "#f87171"
    ]

    for _, row in day.iterrows():
        lat = row.get("latitude")
        lon = row.get("longitude")

        if pd.isna(lat) or pd.isna(lon):
            continue

        cluster_value = row.get("cluster", None)

        if selected_layer == "DBSCAN Clusters":
            if cluster_data is None:
                color = "#94a3b8"
                layer_value = "Not verified for this date"
            else:
                if pd.isna(cluster_value):
                    color = "#94a3b8"
                    layer_value = "Cluster label unavailable"
                else:
                    cluster_value = int(cluster_value)
                    color = (
                        "#ef4444" if cluster_value == -1
                        else cluster_colors[cluster_value % len(cluster_colors)]
                    )
                    layer_value = (
                        "Noise (-1)" if cluster_value == -1
                        else f"Cluster {cluster_value}"
                    )
        else:
            value = pd.to_numeric(
                pd.Series([row.get(column)]),
                errors="coerce"
            ).iloc[0]

            if pd.isna(value):
                continue

            color = scale(value)
            layer_value = f"{value:.4f} {unit}"

        popup_text = (
            f"<b>Grid ID:</b> {int(row['grid_id'])}<br>"
            f"<b>Date:</b> {selected_date}<br>"
            f"<b>Layer:</b> {escape(str(selected_layer))}<br>"
            f"<b>Value:</b> {escape(str(layer_value))}<br>"
            f"<b>Rainfall:</b> {row['rainfall_mm']:.3f} mm<br>"
            f"<b>Surface moisture:</b> {row['sm_surface']:.4f}"
            f"<br><b>Root-zone moisture:</b> {row['sm_rootzone']:.4f}"
            f"<br><b>Elevation:</b> {row['elevation_mean_m']:.1f} m"
            f"<br><b>Slope:</b> {row['slope_mean_deg']:.2f}°"
        )

        folium.CircleMarker(
            location=[float(lat), float(lon)],
            radius=6,
            color="#ffffff",
            weight=1,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            tooltip=f"Grid {int(row['grid_id'])} | {layer_value}",
            popup=folium.Popup(popup_text, max_width=320)
        ).add_to(grid_layer)

    grid_layer.add_to(m)

    if events_file.exists():
        events = pd.read_csv(events_file)
        events["latitude"] = pd.to_numeric(events["latitude"], errors="coerce")
        events["longitude"] = pd.to_numeric(events["longitude"], errors="coerce")
        events = events.dropna(subset=["latitude", "longitude"])

        event_layer = MarkerCluster(name="Historical Flood Records")

        for _, event in events.iterrows():
            settlement = escape(str(event.get("settlement", "Unknown")))
            river = escape(str(event.get("river", "Unknown")))
            event_type = escape(str(event.get("event_type_group", "Unknown")))
            event_date = escape(str(event.get("event_date", "Date unavailable")))

            popup = (
                f"<b>Historical Flood Record</b><br>"
                f"<b>Settlement:</b> {settlement}<br>"
                f"<b>River:</b> {river}<br>"
                f"<b>Event type:</b> {event_type}<br>"
                f"<b>Date:</b> {event_date}"
            )

            folium.CircleMarker(
                location=[event["latitude"], event["longitude"]],
                radius=7,
                color="#ffffff",
                weight=2,
                fill=True,
                fill_color="#ef4444",
                fill_opacity=1,
                tooltip=f"Historical flood: {settlement}",
                popup=folium.Popup(popup, max_width=300)
            ).add_to(event_layer)

        event_layer.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    components.html(
        m.get_root().render(),
        height=760,
        scrolling=False
    )


st.sidebar.markdown("""
<div style="padding:18px 8px 24px 8px">
    <div style="font-size:12px;letter-spacing:2px;color:#22d3ee;font-weight:800">
        RESEARCH INTELLIGENCE
    </div>
    <div style="font-size:23px;font-weight:800;margin-top:8px">
        🌊 UPPER BEAS
    </div>
    <div style="font-size:11px;color:#91a9c2;margin-top:5px">
        FLOOD RESEARCH PLATFORM
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("NAVIGATION")

pages = [
    "Command Center",
    "Interactive Earth",
    "Environmental Intelligence",
    "DBSCAN Explorer",
    "Historical Validation",
    "Research & Methodology"
]

page = st.sidebar.radio(
    "Select module",
    pages,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding:10px;color:#91a9c2;font-size:11px;line-height:1.8">
    <span style="color:#22d3ee;font-weight:700">STUDY REGION</span><br>
    Upper Beas Basin<br>
    Kullu, Himachal Pradesh<br>
    India<br><br>
    <span style="color:#22d3ee;font-weight:700">STUDY PERIOD</span><br>
    2015 — 2025<br><br>
    <span style="color:#22d3ee;font-weight:700">MODEL</span><br>
    Density-Based Spatial Clustering
</div>
""", unsafe_allow_html=True)

if page == "Command Center":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">GEOSPATIAL RESEARCH PLATFORM / 01</div>
        <h1>Flood Intelligence Command Center</h1>
        <p>Multi-source environmental analysis and DBSCAN-based
        clustering of potential flash-flood precursor patterns.</p>
        <span class="tag">UPPER BEAS BASIN</span>
        <span class="tag">2015–2025</span>
        <span class="tag">RESEARCH PROTOTYPE</span>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    metrics = [
        ("ENVIRONMENTAL RECORDS", "1.30M", "Integrated observations"),
        ("GRID LOCATIONS", "325", "Spatial research cells"),
        ("STUDY DURATION", "11 YEARS", "2015 to 2025"),
        ("HISTORICAL RECORDS", "128", "Coordinate-bearing records")
    ]

    for col, metric in zip(cols, metrics):
        with col:
            metric_card(*metric)

    st.write("")
    left, right = st.columns([1.65, 1])

    with left:
        section_header("Study Area Overview", "Spatial extent of the Upper Beas research basin")
        show_image("01_upper_beas_study_area_map.png")

    with right:
        section_header("Research Objectives", "Main analytical goals")
        objectives = [
            "Integrate rainfall, terrain and soil moisture.",
            "Engineer antecedent environmental features.",
            "Identify density-based environmental clusters.",
            "Compare patterns with historical flood records.",
            "Evaluate parameter sensitivity and stability."
        ]
        for item in objectives:
            st.markdown(f"🔹 {item}")

    st.markdown("""
    <div class="panel">
        <span class="tag">IMPORTANT RESEARCH LIMITATION</span>
        <p style="color:#c4d5e6;margin-top:12px">
        This application explores environmental density patterns.
        It is a research prototype, not an operational flood-warning
        or validated flood-prediction system.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "Interactive Earth":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">GEOSPATIAL MODULE / 02</div>
        <h1>Interactive Earth Explorer</h1>
        <p>Explore satellite imagery and daily environmental conditions
        across the Upper Beas Basin.</p>
    </div>
    """, unsafe_allow_html=True)

    @st.cache_data
    def load_environmental_data():
        df = pd.read_csv(
            DATA / "integrated_environmental_dataset_2015_2025.csv"
        )
        df["date"] = pd.to_datetime(df["date"])
        return df

    env = load_environmental_data()

    section_header(
        "Environmental Analysis Controls",
        "Choose a date and environmental variable to inspect."
    )

    col1, col2 = st.columns([1, 1.5])

    with col1:
        selected_date = st.date_input(
            "Select analysis date",
            value=pd.Timestamp("2015-09-22").date(),
            min_value=pd.Timestamp("2015-01-01").date(),
            max_value=pd.Timestamp("2025-12-31").date()
        )

    with col2:
        selected_layer = st.selectbox(
            "Select environmental layer",
            [
                "Rainfall",
                "Surface Soil Moisture",
                "Root-zone Soil Moisture",
                "DBSCAN Clusters"
            ]
        )


    day = env[env["date"] == pd.Timestamp(selected_date)].copy()

    if day.empty:
        st.error("No environmental records are available for this date.")
    else:
        section_header(
            f"{selected_layer} — {selected_date.strftime('%d %B %Y')}",
            f"{len(day)} grid-cell records"
        )

        if selected_layer == "Rainfall":
            values = day["rainfall_mm"].dropna()
            unit = "mm"
            label = "Daily rainfall"

        elif selected_layer == "Surface Soil Moisture":
            values = day["sm_surface"].dropna()
            unit = "m³/m³"
            label = "Surface soil moisture"

        elif selected_layer == "Root-zone Soil Moisture":
            values = day["sm_rootzone"].dropna()
            unit = "m³/m³"
            label = "Root-zone soil moisture"

        else:
            values = pd.Series(dtype=float)
            unit = ""
            label = "DBSCAN clusters"

        if selected_layer != "DBSCAN Clusters":
            if len(values) > 0:
                a, b, c = st.columns(3)

                with a:
                    metric_card("BASIN MEAN", f"{values.mean():.3f}", unit)

                with b:
                    metric_card("MINIMUM", f"{values.min():.3f}", unit)

                with c:
                    metric_card("MAXIMUM", f"{values.max():.3f}", unit)

                st.caption(
                    f"{label}: {len(values)} valid grid cells out of {len(day)}."
                )
            else:
                st.warning("This variable is unavailable for the selected date.")

            if selected_layer in [
                "Surface Soil Moisture",
                "Root-zone Soil Moisture"
            ]:
                available = bool(day["smap_available"].all())

                if not available:
                    st.warning(
                        "SMAP soil-moisture observations are not available "
                        "for all grid cells on this date. Missing values "
                        "are not treated as zero."
                    )

        else:
            if selected_date == pd.Timestamp("2015-09-22").date():
                st.success(
                    "Verified point-level DBSCAN labels are available "
                    "for this date. See the coloured grid markers on the map."
                )
                st.caption(
                    "DBSCAN labels use the saved selective configuration: "
                    "environment weight 0.3, eps 1.5, min_samples 6."
                )
            else:
                st.warning(
                    "Individual grid-cell DBSCAN labels have not yet been "
                    "verified for this date. The map's coloured DBSCAN "
                    "markers currently represent 22 September 2015 only."
                )


    a, b, c = st.columns(3)

    with a:
        metric_card("GRID LOCATIONS", "325", "Research grid centroids")

    with b:
        metric_card("HISTORICAL RECORDS", "128", "Coordinate-bearing records")

    with c:
        metric_card("BASIN AREA", "5,657 km²", "Provisional boundary")

    section_header(
        "Upper Beas Satellite Map",
        "Explore satellite imagery, place names, research locations "
        "and historical flood records."
    )

    show_dynamic_map(day, selected_layer, selected_date)

    st.caption(
        "The environmental map updates with the selected date and layer. "
        "Verified DBSCAN grid labels are currently available only for "
        "22 September 2015."
    )

    st.caption(
        "Map layers require an internet connection. "
        "The study-area boundary is provisional."
    )

elif page == "Environmental Intelligence":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">ENVIRONMENTAL MODULE / 03</div>
        <h1>Environmental Intelligence</h1>
        <p>Explore rainfall, elevation and slope characteristics
        across the Upper Beas Basin.</p>
    </div>
    """, unsafe_allow_html=True)

    maps = {
        "Elevation": ("02_upper_beas_elevation_map.png", "Terrain elevation"),
        "Slope": ("03_upper_beas_slope_map.png", "Terrain slope"),
        "Rainfall — 22 September 2015": ("04_upper_beas_rainfall_2015_09_22.png", "CHIRPS rainfall")
    }

    selected = st.selectbox("Select environmental layer", list(maps.keys()))
    filename, description = maps[selected]

    section_header(selected, description)
    show_image(filename)

    st.info("The displayed maps are saved research visualizations. Interactive date-based environmental layers will be connected in a later upgrade.")

elif page == "DBSCAN Explorer":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">MACHINE LEARNING MODULE / 04</div>
        <h1>DBSCAN Cluster Explorer</h1>
        <p>Investigate spatial-environmental density patterns
        identified by DBSCAN.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("EPSILON", "1.5", "Selective configuration")
    with c2:
        metric_card("MIN SAMPLES", "6", "Minimum neighborhood samples")
    with c3:
        metric_card("ENVIRONMENT WEIGHT", "0.3", "Experimental configuration")

    section_header("Environmental Cluster Map", "22 September 2015 | Selective DBSCAN configuration")
    show_image("05_upper_beas_dbscan_clusters_2015_09_22.png")

    st.warning("This map represents combined spatial-environmental density groups, not flood-risk zones or confirmed flood events.")

elif page == "Historical Validation":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">VALIDATION MODULE / 05</div>
        <h1>Historical Validation & Model Stability</h1>
        <p>Compare DBSCAN configurations and examine
        correspondence with historical event locations.</p>
    </div>
    """, unsafe_allow_html=True)

    section_header("Yearly Configuration Comparison", "Baseline versus selective DBSCAN")
    show_image("06_dbscan_yearly_configuration_comparison.png")

    section_header("Historical Event-Control Comparison", "Comparison of event and control cell detection")
    show_image("07_dbscan_event_control_comparison.png")

    result_file = DATA / "dbscan_candidate_event_summary.csv"

    if result_file.exists():
        section_header("Candidate Configuration Results", "Saved historical validation results")
        results = pd.read_csv(result_file)
        st.dataframe(results, use_container_width=True, hide_index=True)

    st.info("The available historical validation sample is limited. The current analysis does not establish statistically significant flood discrimination.")

elif page == "Research & Methodology":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">RESEARCH MODULE / 06</div>
        <h1>Research & Methodology</h1>
        <p>Data sources, processing workflow and scientific scope.</p>
    </div>
    """, unsafe_allow_html=True)

    section_header("Research Workflow")
    steps = [
        ("01", "Data collection", "Rainfall, terrain, soil moisture, basin and historical event records."),
        ("02", "Spatial integration", "Common 325-cell grid across the provisional study area."),
        ("03", "Feature engineering", "Antecedent rainfall and previous-day soil-moisture features."),
        ("04", "DBSCAN clustering", "Density-based analysis of combined spatial and environmental features."),
        ("05", "Historical comparison", "Compare detected clusters with historical event locations."),
        ("06", "Sensitivity analysis", "Evaluate parameter configurations and temporal stability.")
    ]

    for number, title, description in steps:
        st.markdown(f"""
        <div style="display:flex;gap:15px;margin:17px 0">
            <div style="background:#0e7490;color:white;padding:9px 12px;
            border-radius:10px;height:38px;font-weight:800">{number}</div>
            <div>
                <b style="color:#e0f2fe">{title}</b>
                <div style="font-size:12px;color:#91a9c2">{description}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


    section_header("Research Data Sources")
    sources = [
        ("CHIRPS", "Daily precipitation"),
        ("SRTM", "Elevation and terrain slope"),
        ("NASA SMAP", "Surface and root-zone soil moisture"),
        ("HydroSHEDS", "Hydrological basin information"),
        ("HiFlo-DAT", "Historical flood-event records")
    ]
    for name, desc in sources:
        st.markdown(f"**{name}** — {desc}")

    st.markdown("""
    <div class="panel">
        <span class="tag">SCIENTIFIC SCOPE</span>
        <p style="color:#c4d5e6;margin-top:12px">
        The study investigates environmental density patterns that may
        be associated with flash-flood precursor conditions. The
        provisional basin boundary, limited dated event sample and
        unsupervised methodology must be considered when interpreting
        the results.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:25px 0 10px 0;
color:#607b96;font-size:11px">
UPPER BEAS FLOOD RESEARCH PLATFORM · RESEARCH PROTOTYPE · 2015–2025
</div>
""", unsafe_allow_html=True)
