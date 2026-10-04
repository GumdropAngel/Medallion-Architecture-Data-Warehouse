import sqlite3
import pandas as pd

#koneksi ke database gold_layer
conn = sqlite3.connect('gold_layer.db')
cursor = conn.cursor()

print("Membangun ulang Data Mart (View) dengan Super Join...")

#menghapus view lama
cursor.execute("DROP VIEW IF EXISTS dm_sales_analysis;")

#membuat View baru dengan Casting tipe data yang lebih ketat
query_create_view = """
CREATE VIEW dm_sales_analysis AS
SELECT 
    SUBSTR(CAST(f.order_date AS TEXT), 1, 4) AS sales_year,
    COALESCE(dp.category, dp.product_line, 'Other') AS category,
    COALESCE(dp.subcategory, dp.product_name, 'Other') AS subcategory,
    COALESCE(dc.country, 'Unknown Country') AS country,
    COUNT(f.order_number) AS total_transactions,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_revenue
FROM fact_sales f
LEFT JOIN dim_product dp 
    ON TRIM(UPPER(CAST(f.product_key AS TEXT))) = TRIM(UPPER(CAST(dp.product_key AS TEXT)))
LEFT JOIN dim_customer dc 
    ON CAST(f.customer_id AS REAL) = CAST(dc.customer_id AS REAL)
GROUP BY 
    sales_year,
    category,
    subcategory,
    country;
"""

#eksekusi pembuatan View
cursor.execute(query_create_view)
conn.commit()

print("View 'dm_sales_analysis' berhasil diperbarui!\n")

#validasi Data
df_datamart = pd.read_sql("SELECT * FROM dm_sales_analysis LIMIT 5;", conn)
print("Menampilkan 5 baris pertama dari Data Mart:")
print(df_datamart.to_string(index=False))

conn.close()