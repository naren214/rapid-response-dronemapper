# 🚁 Rapid Response Drone Mapper

A Streamlit hackathon prototype that uses Google Gemma 4 to summarize visible hazards in drone imagery and organize the results for review. Severity scores are AI estimates that require human review.

---

## Problem Statement

During disasters such as floods, earthquakes, cyclones, and landslides, emergency teams receive hundreds of drone images. Manually reviewing every image is slow and delays critical rescue operations.

Rapid Response Drone Mapper automates this process by analyzing aerial images using AI, estimating disaster severity, and visualizing affected locations on an interactive map.

---

## Features

- 📂 Upload a ZIP containing drone images
- 🤖 AI-powered image analysis using Gemma 4
- 📊 Severity estimate (1–10) for each successful analysis
- 📝 Automatic hazard summary generation
- 🗺 Interactive map showing images with usable EXIF GPS metadata
- 📈 Dashboard with disaster statistics
- 🖼 Image preview gallery
- ⚠ Graceful handling of invalid or failed image analyses

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | Web Application |
| Google Gemma 4 | Vision & Disaster Analysis |
| Pandas | Data Processing |
| Pillow | Image Validation |
| piexif | GPS Metadata Extraction |

---

## Project Structure

```
.
├── app.py               # Streamlit application
├── gemma_client.py      # Gemma API integration
├── exif_utils.py        # GPS metadata extraction
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How It Works

1. Upload a ZIP containing drone images.
2. Images are extracted automatically.
3. GPS coordinates are read from EXIF metadata.
4. Gemma analyzes each image and predicts:
   - Disaster severity score
   - Hazard summary
5. Results are displayed in:
   - Interactive map
   - Dashboard
   - Results table
   - Image gallery

---

## Installation

Clone the repository:

```bash
git clone https://github.com/naren214/rapid-response-dronemapper.git
cd rapid-response-dronemapper
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Set your API key:

```bash
export GEMINI_API_KEY=YOUR_API_KEY
```

or create:

```
.streamlit/secrets.toml
```

```toml
GEMINI_API_KEY="YOUR_API_KEY"
```

---

## Run the Project

```bash
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. Images without usable GPS metadata still appear in the results and gallery when the image can be decoded.

---

## Sample Workflow

```
Upload ZIP
      │
      ▼
Extract Images
      │
      ▼
Read GPS Metadata
      │
      ▼
Gemma Vision Analysis
      │
      ▼
Severity Score + Hazard Summary
      │
      ▼
Map + Dashboard + Results
```

---

## Future Enhancements

- Live drone video analysis
- Heatmap visualization
- Multi-disaster detection
- Rescue priority recommendations
- Damage segmentation
- Historical disaster comparison
- PDF report generation
- Real-time satellite imagery support

---

## Team

**Team Name:** *Hackers*

**Hackathon:** *GDG VIT Chennai - Build with Gemma*

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- Google Gemma 4
- Streamlit
- Open-source Python community
- Hackathon organizers
