import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('BA_Processed_Table.csv')  # Adjust path
    return df

df = load_data()

# Sidebar
st.sidebar.title("Filters")
sentiment_filter = st.sidebar.multiselect("Select Sentiment", options=df['Sentiment'].unique(), default=df['Sentiment'].unique())

# Filter data
filtered_df = df[df['Sentiment'].isin(sentiment_filter)]

# Header
st.title("British Airways Review Dashboard")
st.markdown("Explore customer sentiments and feedback trends.")

# KPIs
st.subheader("Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews", len(filtered_df))
col2.metric("Positive", sum(filtered_df['Sentiment'] == 'Positive'))
col3.metric("Negative", sum(filtered_df['Sentiment'] == 'Negative'))

# Sentiment Distribution
st.subheader("Sentiment Distribution")
sentiment_counts = filtered_df['Sentiment'].value_counts()
st.bar_chart(sentiment_counts)

# Word Cloud
st.subheader("Most Frequent Words")
text = " ".join(review for review in filtered_df['reviews'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
st.image(wordcloud.to_array(), use_column_width=True)

# Top Reviews
st.subheader("Sample Reviews")
for Sentiment in ['Positive', 'Negative','Neutral']:
    st.markdown(f"**Top {Sentiment} Review:**")
    review = filtered_df[filtered_df['Sentiment'] == Sentiment]['reviews'].iloc[0]
    st.info(review)

# Raw Data
st.subheader("Raw Data")
st.dataframe(filtered_df)

# Download
st.download_button("Download Filtered Data", filtered_df.to_csv(index=False), "filtered_reviews.csv")
