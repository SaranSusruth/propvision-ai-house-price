# 🏛️ PropVision AI — House Price Intelligence Platform

## 🚀 Live Demo  
👉 https://propvision-ai-house-price.streamlit.app/

PropVision AI is an end-to-end machine learning application that predicts real estate prices using structured property data, enhanced with a custom demand engine, market insights, and long-term investment projections.

---

## 🎯 Problem Statement

Real estate valuation is often subjective and varies significantly based on location, demand, and market conditions.  
This project aims to provide a **data-driven, consistent, and explainable pricing system** to support better property investment decisions.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 ML-Based Valuation | XGBoost regression model trained on structured property data |
| 🔥 Demand Engine | Computes real-time demand score based on zone, location quality, and area |
| 📈 Price Projection | 10-year inflation-based future price estimation |
| 🏘️ Zone Comparison | Compare Rural / Suburban / Urban / Luxury markets |
| 🔬 Explainability | Feature importance visualization |
| 💎 Professional UI | Streamlit app with interactive charts and modern design |

---

## 🧠 Model Details

- **Algorithm:** XGBoost Regressor  
- **Target Variable:** Log-transformed house price  
- **Evaluation Metric:** R² Score (on test split)  
- **Features Used:**
  - Area
  - Bedrooms
  - Bathrooms
  - Location Rating
  - Property Age
  - Garage
  - Pool
  - Zone (encoded)

---

## 📊 Dataset

- The dataset used in this project is **synthetically generated for demonstration purposes**.
- It contains structured property features designed to simulate real-world real estate patterns.
- Small random noise is added during training to improve realism.

⚠️ Note: This project focuses on **ML pipeline design and system architecture**, not production-grade price prediction.

---

## 🧠 Demand Engine Logic

```
Demand Score = 0.55 × Zone Base + 0.30 × Location Quality + 0.15 × Area Size

Zone Demand Bases:
  Luxury   → 88%    Inflation: 8.5%/yr
  Urban    → 75%    Inflation: 7.2%/yr
  Suburban → 58%    Inflation: 5.5%/yr
  Rural    → 35%    Inflation: 3.2%/yr

Demand Multiplier = 1.0 + Demand Score × 0.35
Final Price = AI Base Price × Demand Multiplier
```

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/SaranSusruth/propvision-ai-house-price.git
cd propvision-ai-house-price
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the model
```bash
python train_model.py
```

### 4. Run the application
```bash
python -m streamlit run app.py
```

Open in browser: **http://localhost:8501**

---

## 📁 Project Structure

```
propvision-ai/
├── app.py              # Streamlit UI + inference logic
├── train_model.py      # Model training pipeline
├── dataset.csv         # Synthetic dataset
├── model.pkl           # Saved trained model
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

---

## 📸 Demo

![App Screenshot](assets/demo.png)

---

## 🛠️ Tech Stack

- Python
- Streamlit
- XGBoost
- Scikit-learn
- Pandas
- NumPy
- Plotly

---

## 🏆 Highlights

- End-to-end ML pipeline (training → serialization → inference)
- Custom demand-based pricing system
- Interactive data visualization
- Clean UI/UX with real-time insights

---

## 🚀 Future Improvements

- Integration with real-world datasets
- Deployment with API backend (FastAPI)
- User authentication & saved reports
- Advanced feature engineering

---

## 📌 Author

**Saran Susruth Manthri Pragada**

---
