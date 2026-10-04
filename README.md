#  Medallion Architecture Data Warehouse

This repository implements a **Medallion Architecture** (Bronze, Silver, Gold, and Data Mart) to build a modern Data Warehouse from scratch. This project demonstrates how to integrate data from disparate sources (ERP and CRM systems), cleanse it, model it into a *Star Schema*, and present it through visualizations that are useful for business decision-making. The entire pipeline is designed to be orchestrated using **Apache Airflow**.

##  Background

The *Medallion Architecture* approach (often associated with the Lakehouse architecture) logically organizes data in a lakehouse into multiple layers, with the goal of incrementally and progressively improving the structure and quality of data as it flows through each layer:
1. **Bronze**: *Raw Data*
2. **Silver**: *Cleansed & Conformed Data*
3. **Gold**: *Curated Business-level Data* (*Star Schema*)

In this repository, we simulate this advanced enterprise architecture using lightweight tools (Python + SQLite) so that it can be easily run locally (PC/Laptop) without the need to set up heavy cloud environments or clusters, while still retaining the fundamental enterprise concepts.

---

##  Data Sources

The data is sourced from two different but complementary systems (located in the `data source/` folder):

*   **ERP System (`source_erp`)**
    *   `CUST_AZ12.csv`: Customer data from the ERP.
    *   `LOC_A101.csv`: Customer location/country data.
    *   `PX_CAT_G1V2.csv`: Product category data.
*   **CRM System (`source_crm`)**
    *   `cust_info.csv`: Personal customer information.
    *   `prd_info.csv`: Product specifications and names.
    *   `sales_details.csv`: Transaction/sales details.

---

##  Architecture Layers (The Pipeline)

### 1. 🥉 Bronze Layer (`1_bronze.py`)
This layer is responsible for ingesting raw data from CSV files without changing its content or meaning.
- Reads all source files using **Pandas**.
- Loads the data directly into an SQLite database (`bronze_layer.db`).
- Purpose: To maintain the history and lineage of raw data in case traceback or reprocessing is needed.

### 2. 🥈 Silver Layer (`2_silver.py`)
A transition layer where data cleansing and format standardization are performed.
- **Customer ID Standardization**: Removes the text "NAS" from the ERP CustomerID, and removes dashes (`-`) from the LocationID.
- **Key Generation**: Manipulates CRM product codes to generate a *Join Key* so they can later be joined with categories from the ERP system.
- Loads this cleansed data into a new database (`silver_layer.db`).

### 3. 🥇 Gold Layer (`3_gold.py`)
The presentation layer where *Business Logic* is applied. Data from the Silver Layer is joined and reshaped into a dimensional model (**Star Schema**).
- **Customer Dimension (`dim_customer`)**: A super-join between CRM customer info, ERP AZ12, and ERP LOC.
- **Product Dimension (`dim_product`)**: Joins product specification tables from the CRM with category tables from the ERP.
- **Fact Table (`fact_sales`)**: Extracts transaction details and standardizes column names.
- This data is loaded into `gold_layer.db` and is highly optimized for high-performance querying.

### 4.  Data Mart (`4_datamart.py`)
This layer is aimed at specific business units by providing a *Wide Table* (a table where all dimensions are joined together, ready to be processed directly by analysts or BI tools).
- Creates the `dm_sales_analysis` *View* inside `gold_layer.db`.
- Performs aggregations (SUM/COUNT) on sales revenue and quantity, grouped by year, country, and product category.

### 5.  Visualization & Reporting (`5_visualisasi.py`)
This final script acts as a simple *Business Intelligence* (BI) tool:
- Fetches the *View* from the Data Mart.
- Uses `matplotlib` and `seaborn` to render charts:
  - **Total Revenue per Product Category** (Bar Chart).
  - **Top 5 Countries by Revenue** (Bar Chart).
- Saves the resulting charts as PNG images (`grafik_kategori.png` & `grafik_negara.png`).

---

##  Orchestration with Apache Airflow

The entire process above is tied together into an automated pipeline using **Apache Airflow**. 
The DAG file `dag_medallion.py` defines a *Directed Acyclic Graph* that ensures a sequential execution order:
`task_bronze >> task_silver >> task_gold >> task_datamart`

This simulates a production environment where data engineers schedule the extraction and transformation of data every night (e.g., via a `@daily` batch).

---

##  How to Run

### Prerequisites:
Ensure you have the following Python libraries installed:
```bash
pip install pandas sqlalchemy matplotlib seaborn
```

### Option 1: Manual Execution (Standalone)
Run the python scripts sequentially in your terminal:
```bash
python 1_bronze.py
python 2_silver.py
python 3_gold.py
python 4_datamart.py
python 5_visualisasi.py
```

### Option 2: Using Airflow
1. Place `dag_medallion.py` into your Airflow `dags/` folder (e.g., `/opt/airflow/dags/`).
2. Ensure that scripts `1_bronze.py` through `4_datamart.py` are located in a path accessible by the DAG, and adjust the *paths* inside the DAG if necessary.
3. Start the Airflow webserver and scheduler, unpause the `medallion_architecture_etl` DAG, and observe the process!
