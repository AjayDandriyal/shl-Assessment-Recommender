# 🧠 Assessment Recommender System

An intelligent recommender system that suggests the most relevant assessments to hiring managers based on the roles they are hiring for.

- ![Screenshot 2025-04-07 004724](https://github.com/user-attachments/assets/2dcfb931-7e2f-4348-a1a0-8e8d50b9bb0c)
  
---


## 🔍 Project Overview


This project aims to streamline the hiring process by recommending contextually appropriate assessments from SHL using machine learning and automation. It includes:

- 🔄 **Automated Web Scraping**: Extracts up-to-date assessment data directly from SHL website using Selenium.
- 📊 **TF-IDF-Based Recommendation Engine**: Uses Natural Language Processing (NLP) techniques to retrieve the top 10 related assessments, followed by LLM-based re-ranking to recommend assessments tailored to job role descriptions.
- 🚀 **FastAPI Backend**: Powers scalable and fast REST APIs for retrieving recommendations.
- 💡 **Streamlit Frontend**: Provides an intuitive and interactive UI for hiring managers to explore the suggested assessments.
  
- ![Screenshot 2025-04-07 004850](https://github.com/user-attachments/assets/30afc354-1569-4d73-9493-795e3f71746a)


---


## 📁 Folder Structure


```
shl-assessment-recommender/
├── app.py # Streamlit frontend application
├── api.py # FastAPI backend server
├── recommend.py # TF-IDF based recommendation logic
├── scrape_shl.py # Web scraper for SHL assessments
│
├── data/
│ └── shl_assessments.csv # Cleaned and structured SHL data
│
├── requirements.txt # Python package dependencies
└── README.md # Project documentation
```
---


## 🚀 Getting Started

### 1. 🔧 Setup Environment

Activate your environment:

```bash
shl/scripts/activate

```
or

Install the required dependencies directly:
```bash
pip install -r requirements.txt
```
### 1. 🔧 Run the Application

To launch the Streamlit frontend (automatically connects to the backend):
```bash
streamlit run app.py
```


## 📌 Technologies Used

- FastAPI – High-performance web framework for building APIs
- Streamlit – Rapid UI development for ML apps
- scikit-learn – Machine Learning and TF-IDF vectorization
- pandas – Data processing and manipulation
- Selenium – Web scraping SHL assessment data
- Gemini (LLM) – Re-ranking retrieved assessments to align with job role descriptions

## Contact

For questions or contributions, feel free to reach out or open an issue.

Email : dandriyalajay4@gmail.com
