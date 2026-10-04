import pandas as pd
from sqlalchemy import create_engine

#koneksi ke Bronze dan Silver
engine_bronze = create_engine('sqlite:///bronze_layer.db')
engine_silver = create_engine('sqlite:///silver_layer.db')

print("Mulai Cleansing ke Silver Layer...")

#1. cleansing customer ERP AZ12
df_cust_az = pd.read_sql("SELECT * FROM erp_cust_az12", engine_bronze)
df_cust_az['CID_CLEAN'] = df_cust_az['CID'].str.replace('NAS', '')

#2. cleansing location ERP
df_loc = pd.read_sql("SELECT * FROM erp_loc_a101", engine_bronze)
df_loc['CID_CLEAN'] = df_loc['CID'].str.replace('-', '') 

#3. cleansing CRM product (membuat join key)
df_prd = pd.read_sql("SELECT * FROM crm_prd_info", engine_bronze)
#mengekstrak 2 blok pertama, ubah - jadi _ (contoh: CO-RF -> CO_RF)
df_prd['CAT_JOIN_KEY'] = df_prd['prd_key'].apply(lambda x: "_".join(str(x).split('-')[:2]))

#data yang lain cukup di-copy (misal sales dan kategori) karena formatnya sudah cukup baik
df_sales = pd.read_sql("SELECT * FROM crm_sales", engine_bronze)
df_cust_info = pd.read_sql("SELECT * FROM crm_cust_info", engine_bronze)
df_px_cat = pd.read_sql("SELECT * FROM erp_px_cat", engine_bronze)

#load ke Silver
df_cust_az.to_sql('slv_cust_az12', engine_silver, if_exists='replace', index=False)
df_loc.to_sql('slv_loc_a101', engine_silver, if_exists='replace', index=False)
df_prd.to_sql('slv_prd_info', engine_silver, if_exists='replace', index=False)
df_sales.to_sql('slv_sales', engine_silver, if_exists='replace', index=False)
df_cust_info.to_sql('slv_cust_info', engine_silver, if_exists='replace', index=False)
df_px_cat.to_sql('slv_px_cat', engine_silver, if_exists='replace', index=False)

print("Silver Layer Selesai!")