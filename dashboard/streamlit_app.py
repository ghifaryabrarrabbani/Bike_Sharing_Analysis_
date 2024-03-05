import streamlit as st
import numpy as pd
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from streamlit_option_menu import option_menu
import os
from PIL import Image

st.set_page_config(
    page_title="Bike Rental Analysis",
    page_icon="🚵", 
)

st.title('🚵 Bike Rental Analysis')
dataday = pd.read_csv('https://raw.githubusercontent.com/ghifaryabrarrabbani/dataset/main/day.csv')
datahour = pd.read_csv('https://raw.githubusercontent.com/ghifaryabrarrabbani/dataset/main/hour.csv')
with st.sidebar:
    selected = option_menu(
        menu_title="Dashboard",
        options=["Dataset","Analysis"],
    )

if selected == "Dataset":
    path = os.path.dirname(__file__)
    my_file = path+'/images/img1.jpg'
    image = Image.open(my_file)
    resized_image = image.resize((650, 350))
    st.image(resized_image, caption='Bike Rental Analysis')

    tab1,tab2,tab3=st.tabs(['Penjelasan Dataset', 'Data per hari', 'Data per jam'])
    with tab1:
        st.write("""

        Dataset Bike-sharing-dataset merupakan kumpulan data yang mencatat perhitungan per jam dan per hari dari penyewaan sepeda selama tahun 2011 dan 2012 di Capital yang bersumber dari situs website Kaggle https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset. Data ini juga mencakup informasi tambahan tentang kondisi cuaca dan musiman pada saat penyewaan. Dataset ini  berisi beberapa variabel yang menjelaskan aspek-aspek berikut:

        - **instant:** Variabel ini merupakan nilai autoincrement yang diberikan untuk setiap entri data dalam dataset.
        - **dteday:** Variabel ini mencatat tanggal saat penyewaan sepeda dilakukan.
        - **season:** Merupakan kategori musim cuaca di Capital, di mana angka 1 hingga 4 mewakili musim-musim tertentu (spring, summer, fall, winter).
        - **yr:** Variabel ini menunjukkan tahun penyewaan sepeda, dengan nilai 0 untuk tahun 2011 dan 1 untuk tahun 2012.
        - **mnth:** Menyatakan bulan saat penyewaan sepeda dilakukan, dengan nilai 1 hingga 12 mewakili bulan-bulan dalam setahun.
        - **hr:** Variabel ini mencatat jam saat penyewaan sepeda terjadi, dengan nilai dari 0 hingga 23 untuk merepresentasikan setiap jam dalam sehari.
        - **holiday:** Mengindikasikan apakah hari tersebut merupakan hari libur atau tidak, dengan nilai 0 untuk tidak dan 1 untuk ya.
        - **weekday:** Mencatat hari saat penyewaan sepeda dilakukan, di mana nilai dari 1 hingga 7 mewakili hari-hari dalam seminggu.
        - **workingday:** Variabel ini menunjukkan apakah hari tersebut merupakan hari kerja atau bukan, dengan nilai 1 untuk hari kerja dan 0 untuk weekend atau hari libur.
        - **weathersit:** Merupakan kategori kondisi cuaca saat penyewaan sepeda dilakukan, di mana nilai 1 hingga 4 menggambarkan kondisi cuaca yang berbeda.
        - **temp:** Variabel ini menyatakan suhu saat penyewaan sepeda dilakukan, dalam satuan derajat Celsius.
        - **atemp:** Menyatakan suhu yang dirasakan saat penyewaan sepeda dilakukan, dalam satuan derajat Celsius.
        - **hum:** Merupakan nilai kelembapan saat penyewaan sepeda dilakukan, dengan nilai yang dibagi 100.
        - **windspeed:** Variabel ini mencatat kecepatan angin saat penyewaan sepeda dilakukan, dengan nilai yang dibagi 67.
        - **casual:** Merepresentasikan jumlah pelanggan biasa yang melakukan penyewaan sepeda.
        - **registered:** Mencatat jumlah pelanggan yang sudah terdaftar (member) yang melakukan penyewaan.
        - **cnt:** Merupakan total dari jumlah pelanggan biasa dan terdaftar yang melakukan penyewaan.

        Dataset ini memberikan informasi yang sangat berguna dalam memahami pola penyewaan sepeda berdasarkan berbagai faktor seperti cuaca, musim, hari dalam seminggu, dan jam dalam sehari.
        """)
    with tab2:
        st.table(dataday.head())

    with tab3:
        st.table(datahour.head())
if selected == "Analysis":
    selected = st.radio('Berikut beberapa analisis yang berhasil dilakukan:'
                        , ['Pengaruh season terhadap penyewaan sepeda',
                            'Perkembangan penyewaan sepeda dari tahun 2011 hingga 2012',
                            'Korelasi terkait waktu terhadap penyewaan sepeda',
                            'Penyewaan sepeda berdasarkan holiday dan per harinya'])
    if selected == 'Pengaruh season terhadap penyewaan sepeda':
        def bike_per_season():
            bike_per_Season = dataday.groupby(['season']).agg({ 'registered': ['sum'],
                             'casual': ['sum'], 'cnt': ['sum'] },).reset_index()
            bike_per_Season = bike_per_Season.rename(columns={'cnt': 'Total'})
            bike_per_Season['season'] = bike_per_Season['season'].replace({1:'Springer', 2:'Summer',3:'Fall', 4:'Winter'})
            bike_per_Season.columns = bike_per_Season.columns.droplevel(1)
            return bike_per_Season
        bike_per_season_df = bike_per_season()
        tab1, tab2, tab3 = st.tabs(['Korelasi', 'Bar Chart', 'Kesimpulan'])
        with tab1:
            correlation_per_season = dataday[['season', 'cnt']].corr()
            st.table(correlation_per_season)
            st.write('Berdasarkan hasil korelasi variabel season terhadap jumlah penyewaan sepeda, terlihat bahwa nilai yang didapatkan adalah sebesar 0.40 terhadap variabel penyewaan, sehingga dapat dikatakan bahwa variabel season memiliki korelasi yang cukup berpengatuh terhadap jumlah penyewaan sepeda.')
       
        with tab2:
            st.table(bike_per_season_df)
            st.bar_chart(data=bike_per_season_df,x='season',y='Total')
            st.write('Kemudian, terlihat bahwa sepeda paling sering disewa pada musim gugur (fall) pada rentang 2011-2012. Musim gugur (fall) menjadi yang diminati bisa menjadi beberapa hal, seperti cuaca yang nyaman karena lebuh sejuk dan nyaman. Kemudian, pada musim gugur daun-daun berjatuhan sehingga menciptakan pemandangan alam yang indah dan umumnya memang setiap musim gugur merupakan momen yang pas untuk melakukan aktivitas seperti bersepeda. Selain itu, ketika musim gugur, juga musim yang sering dijadikan liburan sekolah dan liburan kerja, sehingga penyewaan sepeda pun juga bisa lebih meningkat.')
    
        with tab3:
            st.write('Variabel **season** memiliki pengaruh posiitif terhadap penyewaan sepeda yang kemudian penyewaan sepeda paling sering pada musim gugur dengan berbagai alasan yang dapat mendukung hal tersebut, seperti musim gugur merupakan momen yang pas untuk melakukan aktivitas bersepeda akrena lebih sejuk dan nyaman dengan daun yang berjatuhan. Selain itu, musim gugur juga biasanya menjadi waktu liburan sekolah dan kerja, sehingga penyewaan sepeda pun juga bisa meningkat.')

    elif selected == 'Perkembangan penyewaan sepeda dari tahun 2011 hingga 2012':
        def bike_permonth():
            bike_per_month = dataday.groupby(['yr', 'mnth']).agg({ 'registered': ['sum'],
                             'casual': ['sum'], 'cnt': ['sum'] },).reset_index()

            bike_per_month = bike_per_month.rename(columns={'yr': 'Year', 'mnth': 'Month'})

            bike_per_month['Year'] = bike_per_month['Year'].replace({0:2011, 1:2012})
            bike_per_month['Month'] = bike_per_month['Month'].replace({ 1: 'January', 2: 'February', 3: 'March', 4: 'April',
                5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'
            })
            return bike_per_month
        bike_per_month_df = bike_permonth()
        tab1,tab2=st.tabs(['Line Chart', 'Kesimpulan'])
        with tab1:
            bike_per_month_df.columns = bike_per_month_df.columns.droplevel(1)
            st.table(bike_per_month_df)
            st.write('Jika dilihat berdasarkan per bulan dan per tahun, terlihat terdapat perbedaan uang cukup jauh antara penyewa sepeda yang sudah menjadi member dan belum, terlihat bahwa puncaknya adalah ketika September 2022 dengan jumlah member sebanyak 174795 telah menywa sepeda dan non member telah menyewa sepeda sebanyak 43778 orang.')
            st.write('Kemudian, untuk melihat lebih lanjut, akan dibentuk perkembangannya menggunakan line chart.')

            months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            bike_per_month_df['Month'] = pd.Categorical(bike_per_month_df['Month'], categories=months_order, ordered=True)

            bike_per_month_df = bike_per_month_df.sort_values(by=['Year', 'Month'])

            plt.figure(figsize=(12, 6))
            x_values = range(len(bike_per_month_df))
            plt.plot(x_values, bike_per_month_df['registered'], label='Registered', marker='o', color='blue')
            plt.plot(x_values, bike_per_month_df['casual'], label='Casual', marker='o', color='orange')
            plt.plot(x_values, bike_per_month_df['cnt'], label='Total', marker='o', color='red')

            tick_labels = [month + ' ' + str(year) for month, year in zip(bike_per_month_df['Month'], bike_per_month_df['Year'])]
            plt.xticks(x_values, tick_labels, rotation=90)

            plt.xlabel('Date')
            plt.ylabel('Total')
            plt.title('Total Registered and Casual Users per Month (January 2011 - December 2012)')

            plt.legend()

            plt.tight_layout()

            # Menampilkan plot menggunakan st.pyplot()
            st.pyplot()

            st.write('Terlihat bahwa terjadi kenaikan dan penurunan pada setiap penyewaan sepeda, baik itu untuk member ataupun tidak. Tetapi, terlihat bahwa semakin lama, penyewaan sepeda semakin meningkat dari bulan ke bulan, sehingga dapat dikatakan bahwa ada faktor lain yang mempengaruhi peningkatan penyewaan sepeda, seperti advertisement penyewaan sepeda itu dan lainnya.')

        with tab2:
            st.write('Pada tahun 2011-2012, penyewaan sepeda mengalami kenaikan dan penurunan yang fluktuatif. Akan tetapi, terlihat bahwa terdapat perbedaan yang signifikan antara penyewaan sepeda pada tahun 2011 dan 2012. Terdapat kenaikan yang cukup drastis pada penyewaan sepeda dari Februari-Maret 2022 dan mencapai puncaknya pada September 2022. Hal ini dapat terjadi dengan harus dilakukan penelitian lebih lanjut terkait faktor X pada rentang tersebut, seperti musim, suhu, cuaca, holiday, dan sebagainya.')
    elif selected == 'Korelasi terkait waktu terhadap penyewaan sepeda':
        def konversi_jam(hr):
            if hr >= 0 and hr <= 11:
                return 0
            elif hr >= 12 and hr <= 14:
                return 1
            elif hr >= 15 and hr <= 17:
                return 2
            elif hr >= 18 and hr <= 23:
                return 3
            else:
                return None  # Mengembalikan None jika nilai jam tidak valid

        datahour['konversijam'] = datahour['hr'].apply(konversi_jam)
        def bike_per_konversi():
            bike_per_konversijam = datahour.groupby(['konversijam']).agg({ 'registered': ['sum'],
                             'casual': ['sum'], 'cnt': ['sum'] },).reset_index()

            bike_per_konversijam = bike_per_konversijam.rename(columns={'cnt': 'Total'})

            bike_per_konversijam['konversijam'] = bike_per_konversijam['konversijam'].replace({0:'Morning', 1:'Afternoon',2:'Evening', 3:'Night'})

            bike_per_konversijam = bike_per_konversijam.sort_values(by=('Total', 'sum'), ascending=False)

            return bike_per_konversijam

        tab1,tab2,tab3 = st.tabs(['Korelasi', 'Bar Chart', 'Kesimpulan'])
        with tab1:
            correlation_per_hour = datahour[['hr', 'cnt']].corr()
            st.table(correlation_per_hour)
            st.write('Terlihat bahwa terdapat korelasi positif antara jam dengan jumlah penyewaan sepeda sebesar 0.39. Sehingga, dapat dikatakan bahwa variabel jam memiliki korelasi yang cukup berpengaruh terhadap penyewaan sepeda.')

        with tab2:
            bike_per_konversi_jam_df = bike_per_konversi()
            bike_per_konversi_jam_df.columns = bike_per_konversi_jam_df.columns.droplevel(1)
            st.table(bike_per_konversi_jam_df)
            st.bar_chart(data=bike_per_konversi_jam_df,x='konversijam',y='Total')
            st.write('Terlihat bahwa penyewaan sepeda paling sering dilakukan pada pagi hari atau malam hari. Hal ini dapat diasumsikan terjadi karena pagi dan malam memiliki kondisi suhu yang tidak terlalu panas sehingga orang lebih nyaman bersepda pada saat tersebut.')

        with tab3:
            st.write('Terdapat korelasi positif dari variabel waktu terhadap penyewaan sepeda. Pada waktu, dibagi menjadi 4 kelompok yaitu (0-11) merupakan Morning atau pagi hari, (12-14) merupakan Afternoon atau siang hari, (15-17) merupakan Evening atau sore hari, dan (18-23) merupakan Night atau malam hari. Berdasarkan hasil, penyewa sepeda lebih suka menyewa sepeda pada pagi ataupun malam hari. Hal ini dapat didukung dengan beberapa alasan bahwa pada pagi dan malam hari memiliki kondisi suhu yang tidak terlalu panas dibandingkan siang dan sore hari, sehingga penyewa sepeda lebih nyaman bersepeda pada saat itu.')
    else:
        def bike_per_holiday():
            bike_per_holiday = dataday.groupby('holiday').agg({'cnt': ['sum']}).reset_index()
            bike_per_holiday = bike_per_holiday.rename(columns={'cnt': 'Total'})
            bike_per_holiday['holiday'] = bike_per_holiday['holiday'].replace({0:'Holiday', 1:'Not Holiday'})
            return bike_per_holiday
        tab1,tab2,tab3 = st.tabs(['Holiday', 'Weekday', 'Kesimpulan'])
        with tab1:
            bike_per_holiday_df = bike_per_holiday()
            bike_per_holiday_df.columns = bike_per_holiday_df.columns.droplevel(1)
            st.table(bike_per_holiday_df)
            st.write('Terlihat bahwa jumlah penyewaan sepeda pada rentang 2011-2012 memiliki perbedaan yang sangat jauh dengan musim liburan tidak, sehingga masyarakat lebih suka menyewa sepeda saat liburan.')

            st.bar_chart(data=bike_per_holiday_df, x='holiday', y='Total')
            st.write('Kemudian, jika dilihat berdasarkan nilai korelasi, didapatkan hasil sebagai berikut.')
            correlation_per_holiday = dataday[['holiday', 'cnt']].corr()
            st.table(correlation_per_holiday)
            st.write('Dengan nilai korelasi yang dimiliki cukup kecil (mendekati 0), maka dapat dikatakan holiday tidak memiliki pengaruh besar terhadap penyewaan sepeda.')
        def bike_per_weekday():
            bike_per_weekday = dataday.groupby('weekday').agg({'cnt': ['sum']}).reset_index()

            bike_per_weekday = bike_per_weekday.rename(columns={'cnt': 'Total'})

            return bike_per_weekday
        with tab2:
            bike_per_weekday_df = bike_per_weekday()

            bike_per_weekday_df['weekday'] = bike_per_weekday_df['weekday'].replace({0:'Monday', 1:'Tuesday', 2:'Wednesday',
                                                                                    3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'})
            bike_per_weekday_df.columns = bike_per_weekday_df.columns.droplevel(1)
            st.table(bike_per_weekday_df)    
            st.write('Terlihat bahwa jumlah penyewaan sepeda dari setiap harinya tidak memiliki perbedaan yang signifikan, sehingga penyewaan sepeda tidak terlalu bergantung pada hari.')                                                       
            st.bar_chart(data=bike_per_weekday_df, x='weekday', y='Total')
            st.write('Kemudian, jika dilihat berdasarkan nilai korelasi, didapatkan hasil sebagai berikut.')
            correlation_per_weekday = dataday[['weekday', 'cnt']].corr()
            st.table(correlation_per_weekday)
            st.write('Dengan nilai korelasi yang dimiliki cukup kecil (mendekati 0), maka dapat dikatakan weekday tidak memiliki pengaruh besar terhadap penyewaan sepeda.')
        
