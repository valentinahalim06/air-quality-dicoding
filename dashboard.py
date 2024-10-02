import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

combined_df = pd.read_csv('combined.csv') 

st.title("Air Quality Analysis Dashboard")

st.subheader("Interaksi untuk Analisis Kualitas Udara")

question1 = st.checkbox("Lihat fluktuasi polutan antara Musim Panas dan Musim Dingin di Wanliu")

if question1:
    wanliu_df = combined_df[combined_df['station'] == 'Wanliu']

    if wanliu_df.empty:
        st.write("Tidak ada data untuk stasiun Wanliu.")
    else:
        summer_df = wanliu_df[wanliu_df['month'].isin([6, 7, 8])]  
        winter_df = wanliu_df[wanliu_df['month'].isin([12, 1, 2])]  

        if summer_df.empty or winter_df.empty:
            st.write("Data untuk musim panas atau musim dingin tidak tersedia.")
        else:
            pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
            summer_avg = summer_df[pollutants].mean()
            winter_avg = winter_df[pollutants].mean()

            fluctuation = pd.DataFrame({
                'Summer': summer_avg,
                'Winter': winter_avg
            })

            fig1, ax1 = plt.subplots(figsize=(10, 6))
            fluctuation[['Summer', 'Winter']].plot(kind='bar', ax=ax1)
            ax1.set_title('Fluktuasi Konsentrasi Polutan Antara Musim Panas dan Musim Dingin (Wanliu)')
            ax1.set_ylabel('Konsentrasi Polutan (µg/m³)')
            ax1.set_xlabel('Polutan')
            st.pyplot(fig1)

            st.write("""
            - Konsentrasi karbon monoksida (CO) pada musim dingin sangat tinggi, mencapai lebih dari 2000 µg/m³, sedangkan pada musim panas konsentrasinya jauh lebih rendah. CO adalah polutan dengan fluktuasi tertinggi antara kedua musim.
            - Polutan lainnya, seperti PM2.5, PM10, SO2, NO2, dan O3, memiliki perbedaan kecil antara musim panas dan musim dingin.
            - Tingginya konsentrasi CO pada musim dingin menunjukkan bahwa pembakaran bahan bakar mungkin menjadi kontributor utama polusi pada musim dingin.
            """)

question2 = st.checkbox("Lihat perbandingan rata-rata konsentrasi PM2.5 di jam sibuk dan non-sibuk")

if question2:
    hourly_avg = combined_df.groupby(['station', 'hour'])['PM2.5'].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='hour', y='PM2.5', hue='station', data=hourly_avg, marker='o', ax=ax2)
    ax2.axvspan(7, 9, color='gray', alpha=0.3, label='Busy Hours')
    ax2.axvspan(12, 14, color='yellow', alpha=0.3, label='Non-Busy Hours')
    ax2.set_title('Rata-rata Konsentrasi PM2.5 di Jam Sibuk dan Non-Sibuk di Ketiga Stasiun')
    ax2.set_ylabel('Konsentrasi PM2.5 (µg/m³)')
    ax2.set_xlabel('Jam')
    ax2.legend(title='Stasiun')
    st.pyplot(fig2)

    st.write("""
    - Rata-rata konsentrasi PM2.5 meningkat signifikan setelah jam sibuk (07:00-09:00) di ketiga stasiun, menunjukkan aktivitas manusia yang berkontribusi terhadap peningkatan polusi.
    - Pada jam non-sibuk (12:00-14:00), konsentrasi PM2.5 cenderung lebih rendah dan stabil.
    - Shunyi cenderung memiliki konsentrasi yang sedikit lebih tinggi dibandingkan Tiantan dan Wanliu, namun secara umum ketiga stasiun memiliki pola yang sama.
    - Konsentrasi PM2.5 tertinggi terlihat pada malam hari, sementara konsentrasi terendah terjadi pada dini hari.
    """)

st.write("Dashboard ini menyajikan analisis kualitas udara berdasarkan data konsentrasi polutan PM2.5 dan CO di beberapa stasiun di Tiongkok. Semua grafik dan insight dihasilkan dari data yang dikumpulkan antara 2013-2017.")
st.markdown('Dashboard by Valentina Halim')