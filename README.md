
# 🏛️ PropVision AI — House Price Intelligence Platform


## 🚀 Live Demo  
👉 https://propvision-ai-house-price.streamlit.app/


PropVision AI is a professional, end-to-end machine learning platform for real estate price intelligence. It leverages advanced ML models, a custom demand engine, and market analytics to deliver accurate, explainable, and actionable property valuations. The application features a modern Streamlit UI, interactive visualizations, and robust investment insights.

---

## 🎯 Problem Statement

Real estate valuation is often subjective and varies significantly based on location, demand, and market conditions.  
This project aims to provide a **data-driven, consistent, and explainable pricing system** to support better property investment decisions.

---


## ✨ Key Features

| Feature                | Description |
|------------------------|-------------|
| 🤖 ML-Based Valuation  | XGBoost regression model with robust feature engineering and log-transformed target |
| 🔥 Demand Engine       | Real-time demand scoring based on zone, location quality, and area size |
| 📈 Price Projection    | 10-year, inflation-adjusted price forecasting by zone |
| 🏘️ Zone Comparison     | Side-by-side Rural / Suburban / Urban / Luxury market analysis |
| 🔬 Explainability      | Feature importance breakdown and AI-driven property insights |
| 💎 Premium UI/UX       | Modern Streamlit interface with custom CSS, interactive charts, and responsive design |
| 🛡️ Robustness          | Defensive coding for missing data, unseen zones, and edge cases |
| 📊 Live Market Snapshot| Always-on dashboard with demand, inflation, and growth metrics |

---


## 🧠 Model & Pipeline Details

- **Algorithm:** XGBoost Regressor (with log-transformed target)
- **Evaluation Metric:** R² Score (test split)
- **Feature Engineering:**
  - Area (normalized)
  - Bedrooms
  - Bathrooms
  - Location Rating
  - Property Age
  - Garage Spaces
  - Swimming Pool
  - Zone (encoded)
  - Bed/Bath Ratio
  - Luxury Score
- **Robustness:**
  - Handles missing model.pkl (auto-trains if missing)
  - Safe encoding for unseen zones
  - Defensive against division-by-zero and missing values

---


## 📊 Dataset

- **Type:** Synthetic, structured property dataset (for demonstration)
- **Purpose:** Simulates real-world real estate patterns with engineered features and controlled noise
- **Note:** This project demonstrates ML pipeline design and system architecture, not production-grade price prediction.

---


## 🧠 Demand Engine & Pricing Logic

```
Demand Score = 0.55 × Zone Base + 0.30 × Location Quality + 0.15 × Area Size

Zone Demand Bases:
  Luxury   → 88%    (Inflation: 8.5%/yr)
  Urban    → 75%    (Inflation: 7.2%/yr)
  Suburban → 58%    (Inflation: 5.5%/yr)
  Rural    → 35%    (Inflation: 3.2%/yr)

Demand Multiplier = 1.0 + Demand Score × Market Sensitivity × 0.35
Final Price = AI Base Price × Demand Multiplier
```

**Additional Logic:**
- Market Sensitivity slider allows users to adjust how strongly demand affects price (0.5× to 1.5×)
- All currency values are dynamically formatted (INR/₹ or USD/$)
- Defensive handling for missing or outdated model files

---


## ⚙️ Local Setup & Usage

1. **Clone the repository**
  ```bash
  git clone https://github.com/SaranSusruth/propvision-ai-house-price.git
  cd propvision-ai-house-price
  ```
2. **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```
3. **Train the model** (generates model.pkl)
  ```bash
  python train_model.py
  ```
4. **Run the Streamlit app**
  ```bash
  python -m streamlit run app.py
  ```

Open your browser at: **http://localhost:8501**

---


## 📁 Project Structure

```
propvision-ai/
├── app.py           # Streamlit UI, inference, and analytics
├── train_model.py   # Model training pipeline
├── dataset.csv      # Synthetic dataset
├── model.pkl        # Trained model (auto-generated)
├── requirements.txt # Python dependencies
├── assets/          # Images, screenshots, and static assets
└── README.md        # Documentation
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
- Custom demand-based pricing system with market sensitivity controls
- Interactive, real-time data visualization (Plotly)
- Live market snapshot and zone comparison analytics
- Defensive, production-style code with robust error handling
- Clean, modern UI/UX with premium branding

---


## 🚀 Future Roadmap

- Integration with real-world datasets
- API backend (FastAPI) for scalable deployment
- User authentication and saved reports
- Advanced feature engineering and model tuning
- Automated CI/CD for model retraining and deployment

---


## 👤 Author

**Saran Susruth Manthri Pragada**


---

## 📝 Version & License

- **Current Version:** v4.0-propvision
- **License:** MIT

---

## 💻 Git Commands for Update

To add and commit the updated README file to your GitHub repository, use the following commands:

```bash
git add README.md
git commit -m "docs: Update README to reflect latest app.py logic, UI, and features. Professional alignment with optimized code."
git push
```
