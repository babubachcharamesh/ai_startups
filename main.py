import streamlit as st
import pandas as pd
import random
import re
import json
import os
import plotly.express as px
import textwrap


# ──────────────────────────────────────────────────────────────
# Page configuration & Neon cosmic theme
st.set_page_config(page_title="AI Startups Universe • 2026", layout="wide", page_icon="🌌")

def apply_custom_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap');
        
        * { font-family: 'Outfit', sans-serif; }
        
        .stApp {
            background: radial-gradient(circle at top right, #1a0033, #0b001f, #000d1a);
            color: #ececff;
        }
        
        h1, h2, h3 { 
            color: #00ffff !important; 
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
            font-weight: 700;
        }

        /* Glassmorphism Cards */
        .card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 24px;
            border: 1px solid rgba(0, 255, 255, 0.15);
            padding: 28px;
            margin: 16px 0;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .card:hover {
            transform: translateY(-8px) scale(1.02);
            border-color: rgba(0, 255, 255, 0.6);
            box-shadow: 0 20px 50px rgba(0, 255, 255, 0.25);
            background: rgba(255, 255, 255, 0.06);
        }

        .startup-name {
            font-size: 32px;
            font-weight: 700;
            color: #00ffff;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }

        .meta { font-size: 14px; margin: 6px 0; opacity: 0.9; }
        .founded  { color: #ff00ff; font-weight: 600; }
        .location { color: #8e94f2; }
        .funding  { color: #00ffcc; font-weight: 600; }
        .valuation { color: #ffbb33; font-weight: 700; }
        .sector   { 
            display: inline-block;
            background: rgba(0, 255, 255, 0.1);
            padding: 4px 12px;
            border-radius: 100px;
            color: #00ffff;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 12px;
        }

        .progress-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 100px;
            height: 10px;
            margin: 20px 0 8px 0;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 100px;
            background: linear-gradient(90deg, #00ffff, #ff00ff);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        }

        /* Sidebar Glass */
        section[data-testid="stSidebar"] {
            background-color: rgba(10, 10, 30, 0.8) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Expander Reset */
        .stExpander {
            border: none !important;
            background: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Data Helpers with Caching

@st.cache_data
def load_and_process_data():
    json_path = os.path.join("data", "startups.json")
    if not os.path.exists(json_path):
        return pd.DataFrame()
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    rows = []
    for category, startups in data.items():
        for s in startups:
            s_copy = s.copy()
            s_copy['Category'] = category
            s_copy['Funding_B'] = parse_money(s_copy.get('Money', ''))
            s_copy['Valuation_B'] = get_valuation(s_copy.get('Money', ''))
            rows.append(s_copy)
    
    return pd.DataFrame(rows)

def parse_money(text):
    if not text or 'N/A' in str(text).upper(): return 0.0
    try:
        m = re.search(r'\$(\d+(?:\.\d+)?)\s*([BMK])?', str(text), re.I)
        if not m: return 0.0
        v = float(m.group(1))
        u = (m.group(2) or 'B').upper()
        return v if u == 'B' else v/1000 if u == 'M' else v/1000000 if u == 'K' else v
    except:
        return 0.0

def get_valuation(text):
    m = re.search(r'(?:valuation|val)\s*[:=]\s*\$?(\d+(?:\.\d+)?)\s*([BMK])?', str(text), re.I)
    if m:
        v = float(m.group(1))
        u = (m.group(2) or 'B').upper()
        return v if u == 'B' else v/1000 if u == 'M' else v
    return parse_money(text) * 5  # rough fallback

# ──────────────────────────────────────────────────────────────
# Main Application

def main():
    apply_custom_styles()
    
    df = load_and_process_data()
    if df.empty:
        st.error("Data source not found. Please ensure 'data/startups.json' exists.")
        return

    st.title("🌌 AI Startups Universe • 2026")
    st.markdown("### Interactive Cosmic Intelligence Map & Market Outlook")

    # Filters
    with st.sidebar:
        st.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=80)
        st.header("✨ Exploration Deck")
        
        categories = sorted(df['Category'].unique())
        selected_cats = st.multiselect("Sectors", options=categories, default=categories)
        
        min_year = int(df['Year'].min())
        max_year = int(df['Year'].max())
        year_range = st.slider("Founding Window", min_year, max_year, (min_year, max_year))
        
        search = st.text_input("🔍 Search Neural Network", "", placeholder="Name, tech or location...")

    # Filtered logic
    filtered = df[
        (df['Category'].isin(selected_cats)) &
        (df['Year'].between(*year_range))
    ]
    
    if search:
        search_query = search.lower()
        filtered = filtered[
            filtered['Name'].str.lower().str.contains(search_query) |
            filtered['Desc'].str.lower().str.contains(search_query) |
            filtered['Loc'].str.lower().str.contains(search_query)
        ]

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Startups Tracked", len(filtered))
    with m2:
        total_funding = filtered['Funding_B'].sum()
        st.metric("Total Funding", f"${total_funding:.1f}B")
    with m3:
        avg_val = filtered['Valuation_B'].mean()
        st.metric("Avg. Valuation", f"${avg_val:.2f}B")

    # Charts
    st.write("---")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("🏆 Valuation Leaderboard")
        val_df = filtered[filtered['Valuation_B'] > 0].sort_values('Valuation_B', ascending=False).head(15)
        if not val_df.empty:
            fig = px.bar(
                val_df, x="Name", y="Valuation_B", color="Valuation_B",
                color_continuous_scale="Viridis",
                template="plotly_dark"
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title=None,
                yaxis_title="Valuation ($B)",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("📊 Sector Mix")
        sector_counts = filtered['Category'].value_counts().reset_index()
        fig_pie = px.pie(sector_counts, values='count', names='Category', hole=0.5, template="plotly_dark")
        fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    # Grid Display
    st.subheader(f"✨ Identified Entities: {len(filtered)}")
    
    if filtered.empty:
        st.warning("No cosmic anomalies detected with current filters.")
    else:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(filtered.iterrows()):
            with cols[idx % 3]:
                fund_b = row['Funding_B']
                val_b = row['Valuation_B']
                pct = min(100, (fund_b / max(1, val_b)) * 100) if val_b > 0 else 0
                
                # Clean and split money string to avoid encoding breaks
                money_raw = row.get('Money', 'N/A').replace('•', '|')
                funding_short = money_raw.split('|')[0].strip()
                
                # Use a more robust HTML assembly with dedent and strip
                # IMPORTANT: No blank lines between HTML tags to prevent Markdown code block triggers
                card_html = textwrap.dedent(f"""
                    <div class="card">
                        <div class="startup-name">{row['Name']}</div>
                        <div class="meta location">📍 {row['Loc']}</div>
                        <div class="meta description"><i>{row['Desc']}</i></div>
                        <div class="meta funding">💰 Funding: {funding_short}</div>
                        <div class="meta valuation">🏆 Est. Val: ${val_b:.1f}B</div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {pct}%;"></div>
                        </div>
                        <div style="font-size:11px; color:#00ffff; text-align:right; opacity:0.7; margin-bottom: 15px;">
                            Capitalization Ratio: {pct:.1f}%
                        </div>
                        <div class="sector">#{row['Category']}</div>
                        <div class="meta founded" style="margin-top:10px; opacity:0.6;">Est. {row['Year']}</div>
                    </div>
                """).strip()
                st.markdown(card_html, unsafe_allow_html=True)

    if random.random() > 0.9:
        st.balloons()

if __name__ == "__main__":
    main()
