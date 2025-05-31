import streamlit as st
import pandas as pd
import joblib

# Load model dan preprocessor
model = joblib.load('model/xgboost_model.pkl')  
preprocessor = joblib.load('model/preprocessor.pkl')

# Konfigurasi halaman
st.set_page_config(page_title="Attrition Prediction", page_icon="🧠", layout="centered")

st.title("🧠 Prediksi Karyawan Keluar")
st.markdown("Masukkan informasi karyawan di bawah ini untuk memprediksi kemungkinan mereka akan keluar dari perusahaan.")

# Opsi inputan kategorikal
valid_options = {
    'BusinessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
    'Department': ['Sales', 'Research & Development', 'Human Resources'],
    'EducationField': ['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources', 'Other'],
    'Gender': ['Male', 'Female'],
    'JobRole': ['Sales Executive', 'Research Scientist', 'Laboratory Technician', 'Manufacturing Director',
                'Healthcare Representative', 'Manager', 'Sales Representative', 'Research Director', 'Human Resources'],
    'MaritalStatus': ['Single', 'Married', 'Divorced'],
    'OverTime': ['Yes', 'No'],
}

satisfaction_range = [1, 2, 3, 4]

# Formulir Input
with st.form("attrition_form"):
    user_input = {}

    user_input['Age'] = st.number_input('Usia', min_value=18, max_value=65, value=30, format="%d", 
                                        help="Usia karyawan dalam tahun. Rentang usia yang diterima adalah antara 18 hingga 65 tahun."
                                        )
    user_input['BusinessTravel'] = st.selectbox('Frekuensi Perjalanan Bisnis', options=valid_options['BusinessTravel'], 
                                                help="Frekuensi perjalanan bisnis karyawan. Tiga pilihan yang tersedia: 1) Non-Travel (tidak pernah bepergian untuk pekerjaan), 2) Travel_Rarely (jarang bepergian), 3) Travel_Frequently (sering bepergian)."
                                                )
    user_input['Department'] = st.selectbox('Departemen', options=valid_options['Department'], 
                                            help="Departemen tempat karyawan bekerja. Ada tiga pilihan: 1) Sales, 2) Research & Development, 3) Human Resources."
                                            )
    user_input['DistanceFromHome'] = st.number_input('Jarak ke Kantor (km)', min_value=1, max_value=100, value=10, format="%d", 
                                                     help="Jarak dari rumah ke kantor dalam km."
                                                     )
    user_input['Education'] = st.slider('Tingkat Pendidikan (1-4)', min_value=1, max_value=4, value=3, 
                                        help="Pilih tingkat pendidikan karyawan: 1 (Tidak lulus sekolah menengah), 2 (Lulus sekolah menengah), 3 (Sarjana), 4 (Pascasarjana)."
                                        )
    user_input['EducationField'] = st.selectbox('Bidang Pendidikan', options=valid_options['EducationField'], 
                                                help="Bidang pendidikan terakhir karyawan. Pilih bidang yang relevan dengan latar belakang pendidikan karyawan."
                                                )
    user_input['EnvironmentSatisfaction'] = st.selectbox('Kepuasan Lingkungan Kerja (1-4)', options=satisfaction_range, 
                                                         help="Skor kepuasan karyawan terhadap lingkungan kerjanya, dengan rentang 1 hingga 4. 1 berarti tidak puas, dan 4 berarti sangat puas."
                                                         )
    user_input['Gender'] = st.selectbox('Jenis Kelamin', options=valid_options['Gender'], 
                                        help="Jenis kelamin karyawan."
                                        )
    user_input['JobRole'] = st.selectbox('Jabatan', options=valid_options['JobRole'], 
                                         help="Jabatan atau posisi pekerjaan karyawan. Pilih salah satu dari daftar jabatan yang tersedia."
                                         )
    user_input['JobSatisfaction'] = st.selectbox('Kepuasan Pekerjaan (1-4)', options=satisfaction_range, 
                                                 help="Skor kepuasan pekerjaan karyawan, dengan rentang 1 hingga 4. 1 berarti tidak puas, sementara 4 berarti sangat puas."
                                                 )
    user_input['MaritalStatus'] = st.selectbox('Status Pernikahan', options=valid_options['MaritalStatus'], 
                                               help="Status pernikahan karyawan, pilih antara Single, Married, atau Divorced."
                                               )
    user_input['MonthlyIncome'] = st.number_input('Gaji Bulanan', min_value=1000, step=100, 
                                                  help="Gaji bruto karyawan per bulan dalam USD."
                                                  )
    user_input['WorkLifeBalance'] = st.slider('Keseimbangan Kehidupan Kerja (1-4)', min_value=1, max_value=4, value=3, 
                                              help="Skor keseimbangan kehidupan kerja karyawan, dengan rentang 1 hingga 4. 1 berarti tidak puas, sementara 4 berarti sangat puas."
                                              )
    user_input['DailyRate'] = st.number_input('Tarif Harian', min_value=100, max_value=10000, value=500, 
                                              help="Tarif harian karyawan."
                                              )
    user_input['PerformanceRating'] = st.slider('Penilaian Kinerja (1-4)', min_value=1, max_value=4, value=3, 
                                                help="Penilaian kinerja karyawan."
                                                )
    user_input['PercentSalaryHike'] = st.slider('Kenaikan Gaji (%)', min_value=0, max_value=50, value=10, 
                                                help="Persentase kenaikan gaji tahunan."
                                                )
    user_input['RelationshipSatisfaction'] = st.slider('Kepuasan Hubungan Kerja (1-4)', min_value=1, max_value=4, value=3, 
                                                       help="Skor kepuasan hubungan kerja."
                                                       )
    user_input['YearsWithCurrManager'] = st.number_input('Tahun dengan Manajer Saat Ini', min_value=0, max_value=30, value=5, 
                                                         help="Jumlah tahun bekerja dengan manajer saat ini."
                                                         )
    user_input['YearsAtCompany'] = st.number_input('Tahun di Perusahaan', min_value=0, max_value=30, value=5, 
                                                   help="Jumlah tahun bekerja di perusahaan."
                                                   )
    user_input['HourlyRate'] = st.number_input('Tarif Per Jam', min_value=10, max_value=100, value=25, 
                                               help="Tarif per jam karyawan."
                                               )
    user_input['YearsInCurrentRole'] = st.number_input('Tahun dalam Posisi Saat Ini', min_value=0, max_value=30, value=3, 
                                                       help="Jumlah tahun dalam posisi saat ini."
                                                       )
    user_input['MonthlyRate'] = st.number_input('Tarif Bulanan', min_value=1000, max_value=100000, value=5000, 
                                                help="Tarif bulanan karyawan."
                                                )
    user_input['YearsSinceLastPromotion'] = st.number_input('Tahun Sejak Promosi Terakhir', min_value=0, max_value=30, value=2, 
                                                            help="Jumlah tahun sejak promosi terakhir."
                                                            )
    user_input['JobInvolvement'] = st.slider('Keterlibatan Pekerjaan (1-4)', min_value=1, max_value=4, value=3, 
                                             help="Tingkat keterlibatan karyawan dalam pekerjaannya (skor 1-4)"
                                             )
    user_input['TrainingTimesLastYear'] = st.number_input('Jumlah Pelatihan Tahun Lalu', min_value=0, max_value=10, value=1, 
                                                          help="Jumlah pelatihan yang diikuti tahun lalu."
                                                          )
    user_input['StockOptionLevel'] = st.slider('Tingkat Opsi Saham', min_value=0, max_value=3, value=1, 
                                               help="Level opsi saham yang diberikan (0 = tidak ada, 1 = rendah, 2 = sedang, 3 = tinggi)"
                                               )
    user_input['NumCompaniesWorked'] = st.number_input('Jumlah Perusahaan yang Pernah Dikerjakan', min_value=0, max_value=20, value=3, 
                                                       help="Jumlah perusahaan yang pernah menjadi tempat kerja karyawan."
                                                       )
    user_input['OverTime'] = st.selectbox('Lembur', options=valid_options['OverTime'], 
                                          help="Apakah karyawan bekerja lembur? (Yes/No)"
                                          )
    user_input['JobLevel'] = st.slider('Tingkat Pekerjaan', min_value=1, max_value=5, value=3, 
                                       help="Tingkat posisi pekerjaan karyawan dalam organisasi."
                                       )
    user_input['TotalWorkingYears'] = st.number_input('Total Tahun Bekerja', min_value=0, max_value=50, value=10, 
                                                      help="Total jumlah tahun bekerja secara keseluruhan."
                                                      )

    submitted = st.form_submit_button("🔍 Prediksi")

# Prediksi
if submitted:
    try:
        df_input = pd.DataFrame([user_input])
        df_transformed = preprocessor.transform(df_input)
        prediction = model.predict(df_transformed)

        st.subheader("📊 Hasil Prediksi:")
        if prediction[0] == 1:
            st.error("🔴 Karyawan kemungkinan **AKAN KELUAR** dari perusahaan.")
        else:
            st.success("🟢 Karyawan kemungkinan **AKAN BERTAHAN** di perusahaan.")

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses input: {e}")

# Footer
st.caption("Copyright © 2025 – Dibuat oleh Fitria")
