# ⚡️ Wind & Solar Generation Data Pipeline

This project fetches **1 year’s worth of wind and solar generation data** from Elexon's BMRS API, stores it in a **SQLite database**, and provides multiple ways to **visualize** the data and run **unit tests**.

---

## 📌 Features

- Fetches **weekly batches** of data from the Elexon API
- Stores data in a **SQLite** database (`generation_data.db`)
- Visualizes data using:
  - 📊 **Interactive Plotly charts** (one per energy source)
  - 🧊 **Heatmaps** for daily generation (separated by source)
- Includes **unit tests** for data-fetching logic

---

## 🚀 Installation

### 1. Clone the repo (or copy the files)
```bash
git clone <your-repo-url>
cd <project-folder>

## 🧪 API Used

[Elexon BMRS API - Wind and Solar Endpoint](https://bmrs.elexon.co.uk/api-documentation/endpoint/generation/actual/per-type/wind-and-sola)

## 📄 License

This project is submitted for technical review. No license included.
