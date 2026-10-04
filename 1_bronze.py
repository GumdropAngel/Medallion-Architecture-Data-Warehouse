import pandas as pd
from sqlalchemy import create_engine
import os

#membuat koneksi database Bronze
engine_bronze = create_engine('sqlite:///bronze_layer.db')

#mapping file dengan nama folder yang benar ke nama tabel bronze
files_to_load = {
    'data source/source_erp/CUST_AZ12.csv': 'erp_cust_az12',
    'data source/source_erp/LOC_A101.csv': 'erp_loc_a101',
    'data source/source_erp/PX_CAT_G1V2.csv': 'erp_px_cat',
    'data source/source_crm/sales_details.csv': 'crm_sales',
    'data source/source_crm/cust_info.csv': 'crm_cust_info',
    'data source/source_crm/prd_info.csv': 'crm_prd_info'
}

print("Membangun Bronze Layer...")
for file_path, table_name in files_to_load.items():
    try:
        #mengecek apakah file benar-benar ada sebelum dibaca
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.to_sql(table_name, engine_bronze, if_exists='replace', index=False)
            print(f"Berhasil meload {file_path} ke tabel {table_name}")
        else:
            print(f"ERROR: File '{file_path}' tidak ditemukan! Pastikan nama foldernya sama persis.")
    except Exception as e:
        print(f"Terjadi error pada {file_path}: {e}")

print("Bronze Layer Selesai!")