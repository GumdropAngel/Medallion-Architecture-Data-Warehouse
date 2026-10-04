import pandas as pd
from sqlalchemy import create_engine

#koneksi
engine_silver = create_engine('sqlite:///silver_layer.db')
engine_gold = create_engine('sqlite:///gold_layer.db')

print("Membangun Star Schema untuk Gold Layer...")

#membaca data dari Silver
slv_sales = pd.read_sql("SELECT * FROM slv_sales", engine_silver)
slv_cust_info = pd.read_sql("SELECT * FROM slv_cust_info", engine_silver)
slv_cust_az = pd.read_sql("SELECT * FROM slv_cust_az12", engine_silver)
slv_loc = pd.read_sql("SELECT * FROM slv_loc_a101", engine_silver)
slv_prd = pd.read_sql("SELECT * FROM slv_prd_info", engine_silver)
slv_cat = pd.read_sql("SELECT * FROM slv_px_cat", engine_silver)

#1. membuat dimensi customer
#join CRM cust info dengan ERP AZ12 dan ERP LOC berdasarkan ID yang sudah dicleaning
dim_customer = pd.merge(slv_cust_info, slv_cust_az, left_on='cst_key', right_on='CID_CLEAN', how='left')
dim_customer = pd.merge(dim_customer, slv_loc, left_on='cst_key', right_on='CID_CLEAN', how='left')
#merapikan kolom
dim_customer = dim_customer[['cst_id', 'cst_key', 'cst_firstname', 'cst_lastname', 'cst_marital_status', 'GEN', 'BDATE', 'CNTRY']]
dim_customer.columns = ['customer_id', 'customer_key', 'first_name', 'last_name', 'marital_status', 'gender', 'birth_date', 'country']

#2. membuat dimensi product
#join CRM product dengan ERP category
dim_product = pd.merge(slv_prd, slv_cat, left_on='CAT_JOIN_KEY', right_on='ID', how='left')
#merapikan kolom
dim_product = dim_product[['prd_id', 'prd_key', 'prd_nm', 'CAT', 'SUBCAT', 'MAINTENANCE', 'prd_cost', 'prd_line']]
dim_product.columns = ['product_id', 'product_key', 'product_name', 'category', 'subcategory', 'maintenance', 'product_cost', 'product_line']

#3. membuat tabel fakta sales
fact_sales = slv_sales.copy()
fact_sales.columns = ['order_number', 'product_key', 'customer_id', 'order_date', 'ship_date', 'due_date', 'sales_amount', 'quantity', 'price']

#menyimpan ke Gold layer
dim_customer.to_sql('dim_customer', engine_gold, if_exists='replace', index=False)
dim_product.to_sql('dim_product', engine_gold, if_exists='replace', index=False)
fact_sales.to_sql('fact_sales', engine_gold, if_exists='replace', index=False)

print("Gold Layer (Star Schema) Selesai Dibangun!")