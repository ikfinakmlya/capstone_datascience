import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "ObesityDataSet.csv"
df = pd.read_csv(file_path)

# 1. Tampilkan beberapa baris pertama dan informasi umum dataset
print("Beberapa baris pertama:")
print(df.head(5))

print("\nInformasi Umum Dataset:")
print(df.info())

print("\nStatistik Deskriptif:")
print(df.describe(include='all'))  # Tambahkan include='all' untuk menampilkan statistik kategorikal

print("\nJumlah baris dan kolom:", df.shape)

# Cek missing values
print("\nMissing Values per Kolom:")
print(df.isnull().sum())

# Cek nilai unik tiap kolom
print("\nJumlah Nilai Unik per Kolom:")
print(df.nunique())

# Cek data duplikat
print("\nJumlah Data Duplikat:")
print(df.duplicated().sum())

# Cek keseimbangan data pada kolom target
print("\nDistribusi Kelas pada Target (NObeyesdad):")
print(df['NObeyesdad'].value_counts())

# Visualisasi distribusi target
plt.figure(figsize=(10, 5))
sns.countplot(x='NObeyesdad', data=df, order=df['NObeyesdad'].value_counts().index, color='orange')
plt.title('Distribusi Kelas Obesitas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Deteksi outlier dengan boxplot untuk fitur numerik
numerik_cols = df.select_dtypes(include=['float64', 'int64']).columns
plt.figure(figsize=(15, 10))
for i, col in enumerate(numerik_cols, 1):
    plt.subplot(3, 3, i)
    sns.boxplot(x=df[col])
    plt.title(f'Boxplot: {col}')
plt.tight_layout()
plt.show()
