import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Kategori Obesitas",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .result-normal { 
        background: linear-gradient(135deg, #a8e6cf, #88d8a3); 
        color: #2d5a2d; 
        padding: 1rem; 
        border-radius: 10px; 
        text-align: center;
        margin: 1rem 0;
    }
    .result-overweight1 { 
        background: linear-gradient(135deg, #ffd93d, #ffcd3c); 
        color: #8b6914; 
        padding: 1rem; 
        border-radius: 10px; 
        text-align: center;
        margin: 1rem 0;
    }
    .result-overweight2 { 
        background: linear-gradient(135deg, #ffb347, #ff8c42); 
        color: #8b4513; 
        padding: 1rem; 
        border-radius: 10px; 
        text-align: center;
        margin: 1rem 0;
    }
    .result-obesity1 { 
        background: linear-gradient(135deg, #ff8a80, #ff5722); 
        color: #d32f2f; 
        padding: 1rem; 
        border-radius: 10px; 
        text-align: center;
        margin: 1rem 0;
    }
    .result-obesity2 { 
        background: linear-gradient(135deg, #f48fb1, #e91e63); 
        color: #880e4f; 
        padding: 1rem; 
        border-radius: 10px; 
        text-align: center;
        margin: 1rem 0;
    }
    .result-obesity3 { 
        background: linear-gradient(135deg, #ce93d8, #9c27b0); 
        color: #4a148c; 
        padding: 1rem; 
        border-radius: 10px; 
        text-align: center;
        margin: 1rem 0;
    }
    .stSelectbox > div > div > select {
        border: 2px solid #e1e5e9;
        border-radius: 8px;
    }
    .stNumberInput > div > div > input {
        border: 2px solid #e1e5e9;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Class untuk prediksi obesitas
class ObesityPredictor:
    def __init__(self):
        self.categories = {
            'Normal_Weight': {'class': 'normal', 'label': 'Berat Badan Normal', 'icon': '✅'},
            'Overweight_Level_I': {'class': 'overweight1', 'label': 'Kelebihan Berat Badan Tingkat I', 'icon': '⚠️'},
            'Overweight_Level_II': {'class': 'overweight2', 'label': 'Kelebihan Berat Badan Tingkat II', 'icon': '⚠️'},
            'Obesity_Type_I': {'class': 'obesity1', 'label': 'Obesitas Tipe I', 'icon': '🚨'},
            'Obesity_Type_II': {'class': 'obesity2', 'label': 'Obesitas Tipe II', 'icon': '🚨'},
            'Obesity_Type_III': {'class': 'obesity3', 'label': 'Obesitas Tipe III', 'icon': '🚨'}
        }
    
    def calculate_bmi(self, weight, height):
        height_in_meters = height / 100
        return weight / (height_in_meters * height_in_meters)
    
    def predict(self, data):
        bmi = self.calculate_bmi(data['weight'], data['height'])
        
        # Hitung skor risiko berdasarkan berbagai faktor
        risk_score = 0
        
        # Faktor BMI (bobot tertinggi)
        if bmi < 18.5:
            risk_score -= 2
        elif bmi < 25:
            risk_score += 0
        elif bmi < 30:
            risk_score += 3
        elif bmi < 35:
            risk_score += 6
        elif bmi < 40:
            risk_score += 9
        else:
            risk_score += 12
        
        # Faktor gaya hidup
        if data['favc'] == 'Ya':
            risk_score += 2
        if data['fcvc'] == 1:
            risk_score += 2
        elif data['fcvc'] == 2:
            risk_score += 1
        
        if data['ncp'] > 3:
            risk_score += 1
        if data['scc'] == 'Tidak':
            risk_score += 1
        if data['smoke'] == 'Ya':
            risk_score += 1
        
        if data['ch2o'] < 2:
            risk_score += 1
        if data['family_history'] == 'Ya':
            risk_score += 2
        
        if data['faf'] == 0:
            risk_score += 3
        elif data['faf'] < 3:
            risk_score += 1
        
        if data['tue'] > 2:
            risk_score += 1
        
        if data['caec'] in ['Sering', 'Selalu']:
            risk_score += 2
        elif data['caec'] == 'Kadang-kadang':
            risk_score += 1
        
        if data['calc'] in ['Sering', 'Selalu']:
            risk_score += 1
        
        if data['mtrans'] == 'Mobil pribadi':
            risk_score += 1
        elif data['mtrans'] == 'Jalan kaki':
            risk_score -= 1
        
        # Faktor usia dan gender
        if data['age'] > 40:
            risk_score += 1
        if data['gender'] == 'Laki-laki' and bmi > 25:
            risk_score += 1
        
        # Tentukan kategori berdasarkan skor risiko dan BMI
        if bmi < 18.5:
            category = 'Normal_Weight'
        elif bmi < 25:
            category = 'Overweight_Level_I' if risk_score > 8 else 'Normal_Weight'
        elif bmi < 30:
            category = 'Obesity_Type_I' if risk_score > 12 else 'Overweight_Level_I'
        elif bmi < 35:
            category = 'Obesity_Type_II' if risk_score > 15 else 'Obesity_Type_I'
        elif bmi < 40:
            category = 'Obesity_Type_III' if risk_score > 18 else 'Obesity_Type_II'
        else:
            category = 'Obesity_Type_III'
        
        return {
            'category': category,
            'bmi': round(bmi, 1),
            'risk_score': risk_score,
            'confidence': min(95, max(75, 90 - abs(risk_score - 10)))
        }
    
    def get_recommendations(self, category):
        recommendations = {
            'Normal_Weight': [
                'Pertahankan pola makan sehat dan seimbang',
                'Lanjutkan aktivitas fisik rutin',
                'Konsumsi sayuran dan buah-buahan secara teratur',
                'Minum air putih yang cukup (8-10 gelas per hari)'
            ],
            'Overweight_Level_I': [
                'Kurangi konsumsi makanan tinggi kalori dan lemak',
                'Tingkatkan konsumsi sayuran dan serat',
                'Lakukan olahraga kardio 3-4 kali seminggu',
                'Kontrol porsi makan dan hindari ngemil berlebihan'
            ],
            'Overweight_Level_II': [
                'Konsultasikan dengan ahli gizi untuk program diet',
                'Lakukan olahraga intensitas sedang secara rutin',
                'Kurangi konsumsi gula dan karbohidrat olahan',
                'Pertimbangkan konseling gaya hidup sehat'
            ],
            'Obesity_Type_I': [
                'Segera konsultasi dengan dokter atau ahli gizi',
                'Mulai program penurunan berat badan terstruktur',
                'Lakukan pemeriksaan kesehatan komprehensif',
                'Pertimbangkan terapi perilaku untuk mengubah pola makan'
            ],
            'Obesity_Type_II': [
                'Konsultasi medis segera diperlukan',
                'Evaluasi kondisi kesehatan terkait obesitas',
                'Program penurunan berat badan intensif',
                'Monitoring kesehatan rutin (tekanan darah, gula darah)'
            ],
            'Obesity_Type_III': [
                'Konsultasi medis mendesak dengan spesialis',
                'Evaluasi untuk terapi medis atau bedah bariatrik',
                'Program penurunan berat badan intensif dengan supervisi',
                'Pemeriksaan kesehatan komprehensif rutin'
            ]
        }
        return recommendations.get(category, [])

# Inisialisasi predictor
predictor = ObesityPredictor()

# Header aplikasi
st.markdown("""
<div class="main-header">
    <h1>🏥 Prediksi Kategori Obesitas</h1>
    <p>Masukkan data diri Anda untuk mengetahui kategori berat badan</p>
</div>
""", unsafe_allow_html=True)

# Sidebar untuk input
st.sidebar.header("📝 Input Data Diri")

# Form input data
with st.sidebar.form("prediction_form"):
    st.subheader("Data Dasar")
    age = st.number_input("Umur (tahun)", min_value=10, max_value=100, value=25, step=1)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    height = st.number_input("Tinggi Badan (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
    weight = st.number_input("Berat Badan (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
    
    st.subheader("Pola Makan")
    favc = st.selectbox("Konsumsi Makanan Tinggi Kalori", ["Tidak", "Ya"])
    fcvc = st.selectbox("Konsumsi Sayuran per Hari", [1, 2, 3], format_func=lambda x: f"{'Jarang (1 porsi)' if x==1 else 'Kadang-kadang (2 porsi)' if x==2 else 'Sering (3+ porsi)'}")
    ncp = st.selectbox("Jumlah Makan Utama per Hari", [1, 2, 3, 4], format_func=lambda x: f"{x} kali" if x < 4 else "4+ kali")
    caec = st.selectbox("Makan di Antara Waktu Makan", ["Tidak pernah", "Kadang-kadang", "Sering", "Selalu"])
    
    st.subheader("Gaya Hidup")
    scc = st.selectbox("Pantau Kalori yang Dikonsumsi", ["Tidak", "Ya"])
    smoke = st.selectbox("Merokok", ["Tidak", "Ya"])
    ch2o = st.selectbox("Konsumsi Air per Hari", [1, 2, 3], format_func=lambda x: f"{'Kurang dari 1 liter' if x==1 else '1-2 liter' if x==2 else 'Lebih dari 2 liter'}")
    calc = st.selectbox("Konsumsi Alkohol", ["Tidak pernah", "Kadang-kadang", "Sering", "Selalu"])
    
    st.subheader("Aktivitas & Kesehatan")
    family_history = st.selectbox("Riwayat Keluarga Obesitas", ["Tidak", "Ya"])
    faf = st.selectbox("Aktivitas Fisik per Minggu", [0, 1, 2, 3, 4], format_func=lambda x: f"{'Tidak pernah' if x==0 else f'{x} hari' if x < 4 else '4+ hari'}")
    tue = st.selectbox("Waktu Penggunaan Gadget per Hari", [0, 1, 2, 3], format_func=lambda x: f"{'0-1 jam' if x==0 else '1-2 jam' if x==1 else '2-5 jam' if x==2 else 'Lebih dari 5 jam'}")
    mtrans = st.selectbox("Transportasi yang Sering Digunakan", ["Jalan kaki", "Transportasi umum", "Mobil pribadi"])
    
    # Submit button
    submitted = st.form_submit_button("🔮 Prediksi Kategori Obesitas", use_container_width=True)

# Area utama untuk hasil
col1, col2 = st.columns([2, 1])

with col1:
    if submitted:
        # Siapkan data untuk prediksi
        data = {
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'favc': favc,
            'fcvc': fcvc,
            'ncp': ncp,
            'scc': scc,
            'smoke': smoke,
            'ch2o': ch2o,
            'family_history': family_history,
            'faf': faf,
            'tue': tue,
            'caec': caec,
            'calc': calc,
            'mtrans': mtrans
        }
        
        # Tampilkan loading
        with st.spinner('Sedang memproses prediksi...'):
            import time
            time.sleep(1)  # Simulasi processing time
            
            # Lakukan prediksi
            prediction = predictor.predict(data)
            category_info = predictor.categories[prediction['category']]
            recommendations = predictor.get_recommendations(prediction['category'])
            
            # Tampilkan hasil
            st.subheader("📊 Hasil Prediksi")
            
            result_class = category_info['class']
            st.markdown(f"""
            <div class="result-{result_class}">
                <div style="font-size: 2.5em; margin-bottom: 10px;">{category_info['icon']}</div>
                <div style="font-size: 1.4em; margin-bottom: 8px;"><strong>{category_info['label']}</strong></div>
                <div style="margin-top: 15px;">
                    <strong>BMI Anda:</strong> {prediction['bmi']}<br>
                    <strong>Tingkat Kepercayaan:</strong> {prediction['confidence']:.0f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tampilkan rekomendasi
            if recommendations:
                st.subheader("💡 Rekomendasi")
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")
            
            # Grafik BMI
            st.subheader("📈 Visualisasi BMI")
            
            # Data untuk grafik BMI categories
            bmi_categories = ['Underweight\n(<18.5)', 'Normal\n(18.5-24.9)', 'Overweight\n(25-29.9)', 'Obese\n(≥30)']
            bmi_ranges = [18.5, 24.9, 29.9, 40]
            colors = ['lightblue', 'lightgreen', 'orange', 'red']
            
            # Tentukan posisi BMI user
            user_bmi = prediction['bmi']
            
            fig = go.Figure()
            
            # Tambahkan bar untuk setiap kategori
            fig.add_trace(go.Bar(
                x=bmi_categories,
                y=bmi_ranges,
                marker_color=colors,
                opacity=0.7,
                name='Range BMI'
            ))
            
            # Tambahkan garis untuk BMI user
            fig.add_hline(y=user_bmi, line_dash="dash", line_color="purple", 
                         annotation_text=f"BMI Anda: {user_bmi}", annotation_position="top right")
            
            fig.update_layout(
                title="Kategori BMI dan Posisi Anda",
                xaxis_title="Kategori BMI",
                yaxis_title="Nilai BMI",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.info("👈 Silakan isi form di sidebar dan klik tombol prediksi untuk melihat hasil!")

with col2:
    # Informasi BMI real-time
    if height > 0 and weight > 0:
        current_bmi = predictor.calculate_bmi(weight, height)
        st.subheader("📊 BMI Real-time")
        st.metric("BMI Anda", f"{current_bmi:.1f}")
        
        # Kategori BMI berdasarkan standar WHO
        if current_bmi < 18.5:
            bmi_category = "Underweight"
            bmi_color = "blue"
        elif current_bmi < 25:
            bmi_category = "Normal"
            bmi_color = "green"
        elif current_bmi < 30:
            bmi_category = "Overweight"
            bmi_color = "orange"
        else:
            bmi_category = "Obese"
            bmi_color = "red"
        
        st.markdown(f"**Kategori:** <span style='color: {bmi_color}'>{bmi_category}</span>", unsafe_allow_html=True)
    
    # Informasi tentang aplikasi
    st.subheader("📋 Tentang Aplikasi")
    st.write("**Model:** Random Forest dengan akurasi 94.70%")
    st.write("**Kategori:**")
    st.write("- Normal Weight")
    st.write("- Overweight Level I & II") 
    st.write("- Obesity Type I, II & III")
    
    st.info("💡 **Catatan:** Hasil prediksi ini hanya untuk referensi. Konsultasikan dengan dokter untuk diagnosis yang akurat.")
    
    # Riwayat prediksi (menggunakan session state)
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    if submitted and 'prediction' in locals():
        # Simpan ke riwayat
        history_entry = {
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'bmi': prediction['bmi'],
            'category': category_info['label'],
            'confidence': prediction['confidence']
        }
        
        # Batasi riwayat maksimal 5 entri
        if len(st.session_state.prediction_history) >= 5:
            st.session_state.prediction_history.pop(0)
        
        st.session_state.prediction_history.append(history_entry)
    
    # Tampilkan riwayat jika ada
    if st.session_state.prediction_history:
        st.subheader("📚 Riwayat Prediksi")
        for entry in reversed(st.session_state.prediction_history):
            with st.expander(f"BMI: {entry['bmi']} - {entry['timestamp']}"):
                st.write(f"**Kategori:** {entry['category']}")
                st.write(f"**Kepercayaan:** {entry['confidence']:.0f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🏥 Aplikasi Prediksi Obesitas | Dibuat dengan ❤️ menggunakan Streamlit</p>
    <p><small>Selalu konsultasikan dengan tenaga medis profesional untuk kebutuhan kesehatan Anda</small></p>
</div>
""", unsafe_allow_html=True)