import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_metadata.csv")

df = load_data()

# Layout
st.title("CORD-19 Research Dashboard")
st.markdown("Explore trends in COVID-19 research papers using the CORD-19 dataset.")

# Show sample data
if st.checkbox("Show Sample data"):
    st.write(df.sample(10))

# Toggle: All data vs Yearly
view_mode = st.radio("Choose View Mode:", ["All Data", "By Year"])

if view_mode == "By Year":
    # Sidebar filter only appears if user selects "By Year"
    st.sidebar.header("Filters")
    year_filter = st.sidebar.slider(
        "Select Year",
        int(df["year"].min()),
        int(df["year"].max()),
        int(df["year"].min())
    )
    df_view = df[df["year"] == year_filter]
    st.subheader(f"Publications in {year_filter}")
    st.write(df_view.shape[0])
else:
    df_view = df  # use full dataset
    st.subheader("Showing All Data")

# Visualization 1: Publications over time
st.subheader(" Publications over Time")
year_counts = df["year"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10,4))
year_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of papers")
st.pyplot(fig)

# Visualization 2: Top Journals
st.subheader(" Top Journals")
top_journals = df_view["journal"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8,5))
top_journals.plot(kind="barh", ax=ax)
ax.set_xlabel("Number of papers")
st.pyplot(fig)

# Visualization 3: Word Cloud (Titles)
st.subheader(" Word Cloud of Titles")
titles = " ".join(df_view["title"].dropna().astype(str).tolist())
wc = WordCloud(width=1200, height=600, background_color="white").generate(titles)
fig, ax = plt.subplots(figsize=(12,6))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Visualization 4: Top Sources
if "source_x" in df_view.columns:
    st.subheader(" Top Sources")
    top_sources = df_view["source_x"].fillna("Unknown").value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8,5))
    top_sources.plot(kind="barh", ax=ax)
    ax.set_xlabel("Number of papers")
    st.pyplot(fig)
