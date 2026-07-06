import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import re
import requests
from io import BytesIO
import plotly.express as px

st.set_page_config(page_title="CA Inter Paper Analyzer", layout="wide")

st.title("CA Inter Past Papers Analyzer & Predictor")

st.sidebar.header("Settings")

# List of subjects with recent paper URLs (update as needed)
subjects = {
    "Paper 1: Advanced Accounting": "https://resource.cdn.icai.org/92099bos-aps4903-int-may2026-p1.pdf",
    "Paper 2: Corporate and Other Laws": "https://resource.cdn.icai.org/92143bos-aps4903-int-may2026-p2.pdf",
    "Paper 3: Taxation": "https://resource.cdn.icai.org/92144bos-aps4903-int-may2026-p3.pdf",
    # Add more from ICAI site
}

# Hardcoded sample weightage from analysis (in real app, parse PDFs)
sample_weightage = {
    "Paper 1: Advanced Accounting": {
        "Accounting Standards": 25-35,
        "Company Accounts & Reconstruction": 20-25,
        "Consolidated Financial Statements": 10-20,
        "Partnership Accounts": 10-15,
    },
    # Add for other papers based on official or parsed data
}

def extract_text_from_pdf(url):
    try:
        response = requests.get(url)
        pdf_file = BytesIO(response.content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except:
        return "Error downloading or reading PDF"

def analyze_paper(text, paper_name):
    # Simple keyword based analysis (improve with NLP)
    chapters = ["Accounting Standards", "Amalgamation", "Consolidation", "Taxation", "Audit", "FM"]
    weights = {ch: text.lower().count(ch.lower()) for ch in chapters}
    total = sum(weights.values()) or 1
    normalized = {k: round((v/total)*100, 2) for k,v in weights.items()}
    return normalized

st.sidebar.selectbox("Select Paper", list(subjects.keys()))

selected_paper = st.selectbox("Choose Paper to Analyze", list(subjects.keys()))

if st.button("Download and Analyze Latest Paper"):
    url = subjects.get(selected_paper)
    if url:
        text = extract_text_from_pdf(url)
        st.text_area("Extracted Text Sample", text[:1000], height=200)
        analysis = analyze_paper(text, selected_paper)
        df = pd.DataFrame(list(analysis.items()), columns=['Chapter/Topic', 'Estimated Weightage %'])
        st.dataframe(df)
        fig = px.pie(df, names='Chapter/Topic', values='Estimated Weightage %', title=f"Predicted Weightage for {selected_paper}")
        st.plotly_chart(fig)
        
        st.subheader("Important Chapters")
        important = sorted(analysis.items(), key=lambda x: x[1], reverse=True)[:3]
        for ch, wt in important:
            st.write(f"**{ch}** - {wt}% (High priority)")
        
        st.subheader("Predicted Questions for Next Year")
        st.write("- Application of key Accounting Standards")
        st.write("- Case studies on reconstruction/amalgamation")
        st.write("- Practical problems on high weightage topics")
        st.write("Focus on trends from last 5-10 attempts.")

st.info("This is a starter app. Enhance with more papers, better NLP (spaCy), database of past analyses.")