import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Mengambil data dari Data Mart untuk visualisasi...")

#koneksi ke database gold_layer
conn = sqlite3.connect('gold_layer.db')
df = pd.read_sql("SELECT * FROM dm_sales_analysis", conn)
conn.close()

if not df.empty:
    #mengatur tema grafik agar terlihat baik
    sns.set_theme(style="whitegrid")

    #visualisasi 1 : total revenue per kategori produk
    plt.figure(figsize=(10, 6))
    df_cat = df.groupby('category')['total_revenue'].sum().reset_index()
    df_cat = df_cat.sort_values(by='total_revenue', ascending=False)
    
    sns.barplot(data=df_cat, x='category', y='total_revenue', hue='category', palette='viridis', legend=False)
    plt.title('Total Pendapatan (Revenue) per Kategori Produk', fontsize=14, fontweight='bold')
    plt.xlabel('Kategori Produk', fontsize=12)
    plt.ylabel('Total Pendapatan ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('grafik_kategori.png', dpi=300)
    plt.show()

    #visualisasi 2 : top 5 negara dengan pendapatan tertinggi
    plt.figure(figsize=(10, 6))
    df_country = df.groupby('country')['total_revenue'].sum().reset_index()
    df_country = df_country.sort_values(by='total_revenue', ascending=False).head(5)
    
    sns.barplot(data=df_country, x='country', y='total_revenue', hue='country', palette='magma', legend=False)
    plt.title('Top 5 Negara Pelanggan dengan Pendapatan Tertinggi', fontsize=14, fontweight='bold')
    plt.xlabel('Negara', fontsize=12)
    plt.ylabel('Total Pendapatan ($)', fontsize=12)
    plt.tight_layout()
    plt.savefig('grafik_negara.png', dpi=300)
    plt.show()

    print("Visualisasi selesai! File 'grafik_kategori.png' dan 'grafik_negara.png' telah tersimpan.")
else:
    print("Data kosong. Silakan cek kembali isi dari View kamu.")