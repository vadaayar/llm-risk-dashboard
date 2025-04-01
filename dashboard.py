import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime
from PyPDF2 import PdfReader
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Supplier Risk Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.image("images/logo.png", width=180)
st.sidebar.markdown("## 📊 Supplier Risk Navigation")
section = st.sidebar.radio("Go to", ["Dashboard Overview", "LLM Risk Analysis", "Document Risk Analyzer"])

# Header
st.markdown("<h1 style='text-align:center;'>📈 Supplier Risk & Delay Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Empowering companies to proactively monitor supplier delays, assess risks, and act on data-driven insights.</p>", unsafe_allow_html=True)
st.markdown("---")

# Dashboard Overview Section
if section == "Dashboard Overview":
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📉 Supplier Delays Overview")
        delay_data = pd.DataFrame({
            'Company': ['GE', 'Siemens', 'Bosch', 'Lockheed', 'Rolls Royce'],
            'Delay': [4.5, 4.4, 4.3, 4.2, 4.1]
        })
        fig, ax = plt.subplots()
        ax.bar(delay_data['Company'], delay_data['Delay'], color='dodgerblue')
        ax.set_xlabel("Company")
        ax.set_ylabel("Delay")
        st.pyplot(fig)

    with col2:
        st.subheader("📂 Survey-Based Industry Insights")
        try:
            survey_df = pd.read_csv("survey_real.csv")
            fig2, ax2 = plt.subplots()
            ax2.bar(survey_df["Challenges"], survey_df["Responses"], color='orange')
            ax2.set_title("Top Supply Chain Challenges")
            ax2.set_ylabel("Responses")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig2)
        except:
            st.warning("Survey data not found.")

    # Global Supplier Locations
    st.subheader("🌍 Global Supplier Locations")
    try:
        import pydeck as pdk
        locations_df = pd.DataFrame({
            'lat': [40.7128, 48.8566, 35.6895],
            'lon': [-74.0060, 2.3522, 139.6917],
            'label': ['USA', 'France', 'Japan']
        })
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=20, longitude=0, zoom=1),
            layers=[pdk.Layer(
                'ScatterplotLayer',
                data=locations_df,
                get_position='[lon, lat]',
                get_radius=1000000,
                get_color=[255, 0, 0],
                pickable=True
            )]
        ))
    except:
        st.warning("Map could not be loaded.")

    # Insolvency Signals
    st.subheader("⚠️ Signals of Insolvency")
    signals = [
        "Delayed shipments over consecutive quarters",
        "Drop in order volume or cancellations",
        "Negative news sentiment about the supplier",
        "Employee layoffs or factory shutdowns",
        "Payment delays to raw material vendors",
        "Public credit rating downgrade"
    ]
    for s in signals:
        st.markdown(f"- {s}")

# LLM Risk Analysis
elif section == "LLM Risk Analysis":
    st.subheader("🤖 LLM-Based Risk Classification")
    user_input = st.text_area("Paste a Supplier Report or News Article:")

    if st.button("Classify Risk"):
        if user_input.strip():
            from transformers import pipeline
            classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
            prediction = classifier(user_input)[0]
            st.success(f"Predicted Risk Level: **{prediction['label']}** (Confidence: {prediction['score']:.2f})")
        else:
            st.warning("Please enter text to classify.")

    st.subheader("📧 Email Alert Simulation")
    email_input = st.text_input("Send alert to:")
    if st.button("Send Alert"):
        if email_input:
            st.success(f"Simulated alert sent to: **{email_input}**")
        else:
            st.warning("Please enter a valid email.")

# Document Risk Analyzer
elif section == "Document Risk Analyzer":
    st.subheader("📁 Analyze Supplier Documents (PDF)")
    uploaded_file = st.file_uploader("Upload PDF Report", type="pdf")

    if uploaded_file:
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            st.success("Text extracted successfully!")

            st.subheader("☁️ Extracted Word Cloud")
            wordcloud = WordCloud(width=800, height=300, background_color='white').generate(text)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

            st.subheader("🚨 Immediate Measures to Take")
            actions = [
                "Initiate supplier audit for financial health.",
                "Secure alternative vendors for critical components.",
                "Increase safety stock for vulnerable items.",
                "Monitor market signals for further news.",
                "Alert internal procurement teams immediately."
            ]
            for a in actions:
                st.markdown(f"- {a}")

            st.markdown("📥 **Export Risk Report Summary**")
            st.download_button("Download Summary", data=text, file_name="risk_summary.txt")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")

    # 🔍 Extended Survey Insights
    st.markdown("---")
    st.subheader("📘 Extended Survey Insights (Manual Data Summary)")

    # Respondent Demographics
    st.markdown("### 👥 Respondent Demographics")
    demographics_df = pd.DataFrame({
        "Name": ["Risk Management Specialist", "Shweta", "Rajaram Jayakumar", "Hemanth Kummara", "Prasanna Kummara"],
        "Organization": ["-", "BMW", "BorgWarner", "Körber", "GTS"],
        "Role": ["Risk Mgmt Specialist", "Other", "Business Process Lead", "Data Scientist", "Other"],
        "Size": ["Large", "Large", "Large", "Large", "Small"],
        "Industry": ["E-commerce", "Automotive", "Automotive", "Supply Chain", "Other"]
    })
    st.dataframe(demographics_df)

    # Criticality Ratings (Bar Chart)
    st.markdown("### 📊 Importance of Early-Warning System")
    criticality_df = pd.DataFrame({
        "Rating": ["3", "4", "5"],
        "Responses": [1, 2, 2]
    })
    fig3, ax3 = plt.subplots()
    ax3.bar(criticality_df["Rating"], criticality_df["Responses"], color="green")
    ax3.set_title("Criticality of Early-Warning Systems")
    ax3.set_ylabel("No. of Responses")
    st.pyplot(fig3)

    # Feature Suggestions WordCloud
    st.markdown("### 💬 Feature Suggestions from Experts")
    suggestions_text = "advanced integration tools time resolve need domain data expertise real"
    suggestion_wc = WordCloud(width=800, height=300, background_color='white').generate(suggestions_text)
    fig4, ax4 = plt.subplots()
    ax4.imshow(suggestion_wc, interpolation='bilinear')
    ax4.axis("off")
    st.pyplot(fig4)

    # PDF Download Option
    st.markdown("### 📄 Full Survey PDF (Manual Insights)")
    with open("survey.pdf", "rb") as pdf_file:

        PDF_BYTES = pdf_file.read()
    st.download_button("📥 Download Full Survey PDF", data=PDF_BYTES, file_name="Full_Survey.pdf")
    
    
# Footer with timestamp
st.markdown("---")
st.markdown(
    f"<center>💡 <i>This dashboard empowers companies to proactively identify supplier delays and mitigate insolvency risks through data-driven insights, real survey feedback, and intelligent LLM-powered monitoring.</i><br><br>"
    f"🕒 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>"
    f"Made with ❤️ by <b>Harish Kumar Kummara</b> • Powered by <i>AI Supply Chain Intelligence</i> • © 2025</center>",
    unsafe_allow_html=True
)

# Optional Enhancements Section (Message Block)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 16px; padding-top: 10px;'>
        🚀 <b>Want more?</b><br>
        This dashboard can be extended with:
        <ul style='text-align: left; display: inline-block;'>
            <li>🎞️ Beautiful page transitions & animations</li>
            <li>🌙 Dark Mode toggle for accessibility</li>
            <li>📬 Automated Email Alerts with SMTP</li>
            <li>🌐 Embedded version for company intranets or public websites</li>
        </ul>
        🔧 Let me know if you’d like these features added!
    </div>
    """,
    unsafe_allow_html=True
)