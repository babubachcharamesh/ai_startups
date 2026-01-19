# 🌌 AI Startups Universe • 2026

An advanced, interactive Streamlit-based intelligence map and market outlook for the AI startup ecosystem. This application provides a futuristic, "Neon Cosmic" visualization of the most influential entities in the foundation model and frontier AI space.

![App Preview](https://img.icons8.com/nolan/128/artificial-intelligence.png)

## ✨ Features

- **Cosmic Intelligence Map**: A high-speed, glassmorphism-inspired UI for exploring the AI landscape.
- **Interactive Metrics**: Real-time tracking of total funding, average valuations, and entity counts.
- **Valuation Leaderboard**: Sleek Plotly visualizations showing the economic giants of the AI world.
- **Micro-Filtering**: Filter by sector (Foundation Models, Computer Vision, Robotics, etc.), founding year, or neural search (text search).
- **Capitalization Ratios**: Visual progress bars within each startup card showing the ratio of funding to estimated valuation.
- **Responsive Grid**: Dynamic 3-column layout that adapts to your exploration needs.

## 🚀 Technology Stack

- **Core**: Python 3.12
- **Framework**: [Streamlit](https://streamlit.io/)
- **Data Handling**: Pandas & JSON
- **Visualizations**: Plotly (Dark Template)
- **Styling**: Vanilla CSS with Glassmorphism & Neon HSL palettes.
- **Environment Management**: [uv](https://github.com/astral-sh/uv)

## 🛠️ Local Setup

To run this project locally, ensure you have Python 3.12 and [uv](https://github.com/astral-sh/uv) installed.

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd AI_startups
   ```

2. **Sync dependencies**:
   ```bash
   uv sync
   ```

3. **Run the application**:
   ```bash
   uv run streamlit run main.py
   ```

## ☁️ Deployment

This application is configured for seamless deployment on **Streamlit Cloud** (`streamlit.app`).

- **Python Version**: 3.12+
- **Requirements**: Provided in `requirements.txt` (generated via `uv export`).
- **Data Source**: Uses `data/startups.json` for persistence and caching.

## 🎨 Design Philosophy: "Neon Cosmic"

The application utilizes a custom-built design system defined in `main.py`:
- **Glassmorphism**: Transparent, blurred background elements for a premium feel.
- **Vibrant Gradients**: HSL-tailored colors (#00ffff to #ff00ff) for progress and highlights.
- **Micro-Animations**: Smooth hover transitions and scaling effects on data cards.
- **High-Contrast Typography**: Using the 'Outfit' font for maximum readability in dark mode.

---
*Created with ❤️ for the AI Community in 2026.*
