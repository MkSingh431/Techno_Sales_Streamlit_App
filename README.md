# Techno Sales — Streamlit App

This repository contains a Streamlit dashboard for Techno Sales analysis.

**Contents**
- **app.py**: Main Streamlit application ([app.py](app.py)).
- **Complete_Techno_Sales_Data.csv**: Dataset used by the app.
- **.streamlit/config.toml**: Streamlit theme/configuration.
- Images: `logo.jpg`, `techno logo.jpg`, supervisor images used by the UI.
- **requirements.txt**: Python dependencies.

**This README** provides step-by-step instructions for running locally and deploying the app (Streamlit Community Cloud, Docker, and Heroku).

**Prerequisites**
- Python 3.9+ installed
- Git (for deployment to Streamlit Cloud)
- (Optional) Docker installed for container deployment

**1) Local setup (recommended)**
- Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- On Command Prompt (Windows):

```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Verify the `.streamlit/config.toml` file exists (theme). If you want custom theme values, edit:

- Ensure images referenced in `app.py` are present in the project root (e.g., `logo.jpg`, `techno logo.jpg`, supervisor images).

- Run the app locally:

```bash
streamlit run app.py
```

Open the printed local URL in your browser (usually http://localhost:8501).


**2) Important files & config**
- app.py — main application. Key behaviors:
  - Reads `Complete_Techno_Sales_Data.csv` from project root.
  - Places background via CSS helpers (`set_background_color` / `set_background_image`).
  - Sidebar filters and search widgets use session state keys: `status_filter`, `supervisor_filter`, `year_filter`, `brand_filter`.
- .streamlit/config.toml — Streamlit theme settings. Keep this file in `.streamlit/`.
- requirements.txt — ensure it contains packages used (pandas, streamlit, matplotlib, seaborn, folium, streamlit-folium, etc.).


**3) Common runtime issues & fixes**
- File-not-found for images or CSV: ensure file names and casing match; Windows paths are case-insensitive but deployment platforms may be case-sensitive.
- Pandas parsing dates: `app.py` coerces dates with `errors='coerce'` and drops NaT rows — check `Order_Date` format in CSV.
- CSS background not applied: check valid CSS color names or hex values; long base64 images may slow initial load.
- ValueError from `st.columns` unpacking: number of variables must match number of columns returned (e.g., `a,b=st.columns(2)`). See `app.py` where columns are defined.


**4) Deploy to Streamlit Community Cloud (recommended for Streamlit apps)**
1. Create a GitHub repository and push this project.
   - Ensure `app.py`, `requirements.txt`, `.streamlit/config.toml`, and any images/data you need are committed.
2. Go to https://streamlit.io/cloud and sign in with GitHub.
3. Click "New app" → select the repo, branch, and the file path `app.py`.
4. Add any secrets (if needed) via "Advanced settings" → "Secrets" (for API keys).
5. Click "Deploy". Streamlit Cloud will install requirements from `requirements.txt` and run `streamlit run app.py`.

Notes:
- Keep dataset size small or use an external data store for large data (Cloud storage / database).
- For private data, set up secrets or load data from an authenticated service rather than pushing CSV to the repo.


**5) Deploy with Docker**
- Create a `Dockerfile` (example):

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

- Build and run:

```bash
docker build -t techno-sales:latest .
docker run -p 8501:8501 techno-sales:latest
```


**6) Deploy to Heroku (alternative)**
Heroku can run Streamlit but requires a custom `Procfile` and small tweaks.

- `Procfile` example:

```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

- Ensure `requirements.txt` is accurate.
- Create Heroku app and push the repo (or connect GitHub):

```bash
heroku create <app-name>
git push heroku main
```

Note: Heroku has limited persistent storage and ephemeral file system — store large datasets externally.


**7) Recommended GitHub branch & secrets**
- Keep `main` or `master` as the production branch.
- Add any credentials to the host provider (Streamlit Cloud/Heroku) via their secrets/ENV settings — do not commit secrets to the repo.


**8) Troubleshooting checklist**
- App fails to start: check `requirements.txt` for missing packages.
- Missing columns errors: verify CSV columns exactly match those used in `app.py` (e.g., `Order_Date`, `Total_Sales`, `Assigned Supervisor`, `Status`, `Brand`, `State_Code`).
- Mapping/warnings: unmapped state codes produce a warning in the UI — update `state_mapping` in `app.py`.
- CSS or images not loading on Deployment: verify images are included in the repo and referenced by correct name.


**9) Quick maintenance notes**
- To change theme colors, edit [.streamlit/config.toml](.streamlit/config.toml).
- To enable debugging logs, run with environment variable `STREAMLIT_DEBUG=1` or add prints in `app.py` (avoid verbose logs in production).


**10) Contact / Next steps**
- If you want, I can:
  - Run the app locally and verify the UI for you.
  - Create a `Dockerfile` and Heroku `Procfile` in the repo.
  - Prepare a minimal GitHub repo layout and push it for Streamlit Cloud deployment.

---
Generated: March 1, 2026
