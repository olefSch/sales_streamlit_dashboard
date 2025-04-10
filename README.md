# 🏢 IT Architecture for Data-Driven Decision-Making 📊

This repository contains the documentation and design of an IT architecture for a data-driven company. The goal is to develop a scalable, secure, and efficient architecture that supports data-driven decision-making. The project combines modern data architecture concepts, such as Data Mesh and Medallion Architecture, with interactive visualization tools like Streamlit to provide actionable insights for management.

## 📝 Project Description

### 1. Context and Development 🛠️

This project was developed during a **2.5-day hackathon** as part of the **DS Data Management Fundamentals** course at the **Duale Hochschule Baden-Württemberg (DHBW)**. The course is taught by _Prof. Dr. Giacomo Welsch_. The project was created by _Philipp Meyer & Ole Schildt_.

The hackathon focused on designing a conceptual IT architecture for a data-driven company while implementing an interactive data visualization dashboard. The work was divided into two main tasks:

1. **Designing a scalable IT architecture** for data integration, storage, processing, quality assurance, governance, analytics, and compliance.
2. **Developing an interactive Streamlit dashboard** using a publicly available Kaggle dataset to deliver actionable insights for sales management. 💼📈

---

### 2. Requirements and Goals 🎯

#### **Task 1: IT Architecture Design**

The architecture is designed to meet the following requirements:

- **📥 Data Sources and Integration:** Incorporate at least four systems (e.g., ERP, CRM, webshop, Google Analytics) and define five detailed integration scenarios.
- **💾 Data Processing and Storage:** Implement a Data Lakehouse (Delta Lake) with Medallion Architecture and ETL/ELT workflows.
- **✅ Data Quality and Governance:** Define mechanisms to ensure data quality, security, and compliance, including data contracts and governance principles.
- **📊 Data Analysis and Visualization:** Leverage tools like Streamlit and Google Looker to create dashboards and analyses.
- **🔒 Compliance and Security:** Ensure adherence to data protection and security regulations.

#### **Task 2: Streamlit Dashboard**

The second part of the project focuses on building an **interactive Streamlit dashboard** based on a publicly available sales dataset from Kaggle ([Sales Datasets](https://www.kaggle.com/datasets/?search=sales)). The dashboard aims to:

- 🧹 Load and clean the dataset by removing incomplete or erroneous data.
- 📈 Provide **interactive visualizations** (e.g., time series, geographical maps, KPIs) to allow users to filter and analyze data.
- 🖥️ Deliver a **user-friendly and intuitive interface** to support sales management decision-making.

## 📂 Repository Structure

This repository is organized into two main sections corresponding to the two tasks outlined:

1. **Task 1: IT Architecture Design**
   Content related to the IT architecture design is located within the `e-commerce_architecture` directory. This section focuses on the conceptual design of a scalable IT architecture for data-driven decision-making.

2. **Task 2: Streamlit Dashboard**
   The remainder of the repository contains the implementation of the interactive Streamlit dashboard, which provides actionable sales insights based on the Kaggle dataset.

```tree
.
├── README.md
├── config.yaml
├── e-commerce_architecture
│   ├── Architecture_Report.pdf
│   ├── base_architecture.excalidraw.svg
│   ├── example_process.excalidraw.svg
│   └── latex_source
│       ├── content.tex
│       ├── main.tex
│       ├── references.bib
│       └── titlepage.tex
├── main.py
├── pyproject.toml
├── ruff.toml
├── src
│   ├── Home.py
│   ├── __pycache__
│   │   ├── coming.cpython-313.pyc
│   │   ├── config.cpython-313.pyc
│   │   └── loader.cpython-313.pyc
│   ├── config.py
│   ├── loader.py
│   ├── pages
│   │   ├── 1.py
│   │   ├── 2.py
│   │   ├── 3.py
│   │   └── 4.py
│   └── utils
│       ├── __pycache__
│       │   └── utils.cpython-313.pyc
│       └── utils.py
└── uv.lock
```

## ⚙️ Prerequisites

### For executiuon

To run this project, ensure the following prerequisites are met:

1. **Python Installation**
   Make sure Python is installed on your system (preferably **Python 3.10** or later). You can download it from [python.org](https://www.python.org).

2. **Install `uv`**
   The `uv` package is used to manage and run the project efficiently. Install it using a package manager (e.g., Homebrew for macOS/Linux):

   ```bash
   brew install uv
   ```

   Alternatively, install it via `pip`:

   ```bash
   pip install uv
   ```

   **Why use `uv`?**

   - **Simplified Workflow:** `uv` streamlines project management by automating tasks such as dependency installation and virtual environment setup.
   - **Efficient Development:** It provides commands to run the project quickly, helping developers focus on building and testing.
   - **Environment Management:** Ensures consistency across different development environments.

After installing `uv`, the required dependencies for the project will be handled automatically when you run the commands provided in the installation section.

### For development

1. **Install Ruff**:

   - Formatting with Rust speed ;)

   ```bash
   brew/pip install ruff
   ```

2. Helpful settings and extensions for VS Code are in the `.vscode` directory. They automatically apply as workspace settings over the user settings.

## Environment Variables

To access datasets from Kaggle, you need to set up the Kaggle API. Follow these steps:

### Download Your Kaggle API Key

1. Log in to your Kaggle account.
2. Go to your Kaggle account settings.
3. Scroll down to the **API** section and click **Create New API Token**. This will download a `kaggle.json` file.
4. Place the `kaggle.json` File in the `.kaggle` Directory

#### **Why use the `Kaggle API`?**

- **Automated Dataset Downloads**: Easily download datasets directly into your project using simple commands.
- **Seamless Integration**: Integrate Kaggle datasets into workflows without manually downloading files from the website.
- **Access to Competitions and Datasets**: Quickly fetch competition data or explore open datasets for analysis.

## 🚀 Installation and Execution

To run the project, simply execute the following command:

```bash
  uv run main.py
```

This command will automatically handle dependency installation, environment setup, and execution.
