import streamlit as st
import zipfile
import pandas as pd
from gemma_client import analyze_image_safe
from exif_utils import get_gps_or_mock

st.set_page_config(
    page_title="Rapid Response Drone Mapper",
    page_icon="🚁",
    layout="wide"
)

def analyze_image_cached(filename: str, image_bytes: bytes) -> dict:
    return analyze_image_safe(image_bytes)

st.sidebar.title("🚁 Rapid Response Drone Mapper")
st.sidebar.write("### Gemma 4 Powered")
st.sidebar.write("Upload a ZIP of drone images for disaster analysis.")

st.sidebar.markdown("### ✅ Supported Formats")
st.sidebar.write("JPG")
st.sidebar.write("JPEG")
st.sidebar.write("PNG")

st.title("🚁 Rapid Response Drone Mapper")

st.write(
    "Upload a ZIP file containing drone images. "
    "Gemma will analyze each image and estimate disaster severity."
)

uploaded_zip = st.file_uploader(
    "📂 Upload ZIP File",
    type=["zip"]
)

images = []
if uploaded_zip:
    st.success("✅ ZIP uploaded successfully!")
    try:
        zip_ref = zipfile.ZipFile(uploaded_zip)
    except zipfile.BadZipFile:
        st.error("The uploaded file is not a valid ZIP archive.")
        zip_ref = None

    if zip_ref:
        for file in zip_ref.namelist():
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                with zip_ref.open(file) as f:
                    images.append((file, f.read()))
        zip_ref.close()
    
    st.write(f"### {len(images)} Images Found")

analyze = st.button("🚀 Analyze Images")

if analyze and images:
    with st.spinner("Analyzing images with Gemma..."):
        results = []
        for name, data in images:
            lat, lon = get_gps_or_mock(data)
            ai_result = analyze_image_cached(name, data)
            results.append({
                "filename": name,
                "lat": lat,
                "lon": lon,
                "severity_score": ai_result["severity_score"],
                "hazard_summary": ai_result["hazard_summary"],
                "error": ai_result.get("error", "")
            })
        
        df = pd.DataFrame(results)

        st.divider()
        st.header("📊 Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        high_count = len(df[df["severity_score"] >= 7])
        med_count = len(df[(df["severity_score"] >= 4) & (df["severity_score"] < 7)])
        low_count = len(df[(df["severity_score"] > 0) & (df["severity_score"] < 4)])
        
        with col1:
            st.metric("Images", str(len(images)))
        with col2:
            st.metric("High Severity", str(high_count))
        with col3:
            st.metric("Medium", str(med_count))
        with col4:
            st.metric("Low", str(low_count))

        st.divider()
        st.header("🗺 Disaster Map")
        st.map(df[["lat", "lon"]])

        st.divider()
        st.header("📋 Results")
        result_columns = ["filename", "severity_score", "hazard_summary"]
        if df["error"].astype(bool).any():
            result_columns.append("error")
            st.warning(
                "Some images could not be analyzed. Expand the error column below "
                "to see the exact API or image validation message."
            )
        st.dataframe(df[result_columns], width="stretch")

        st.divider()
        st.header("🖼 Image Preview")
        
        preview_cols = st.columns(3)
        for idx, (name, data) in enumerate(images):
            with preview_cols[idx % 3]:
                st.image(data, caption=name, width="stretch")
elif analyze:
    st.warning("Please upload a ZIP file first.")
