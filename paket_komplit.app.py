import streamlit as st
import pandas as pd
import numpy as np
import sympy as sp

# ==========================================
# 1. KONFIGURASI HALAMAN & JUDUL
# ==========================================
st.set_page_config(page_title="Project UAS Matematika Komputasi", layout="centered")

st.title("🖥️ Project UAS Matematika Komputasi")
st.header("Metode Newton-Raphson & Secant")
st.write("Aplikasi interaktif mencari akar persamaan nonlinear secara dinamis.")
st.markdown("---")

# ==========================================
# 2. INPUT PARAMETER DARI UI WEB
# ==========================================
st.subheader("⚙️ Input Parameter")

# Input fungsi sebagai TEXT/STRING (Dinamis)
fungsi_input = st.text_input(
    "Masukkan fungsi f(x) yang ingin dicari akarnya:", 
    value="x**3 - 4*x - 9"
)
st.caption("Gunakan sintaks Python: `**` untuk pangkat dan `*` untuk perkalian (Contoh: `x**3 - 4*x - 9`) ")

# Pilihan Metode
metode = st.radio("Pilih Metode Numerik:", ("Newton-Raphson", "Secant"))

# Input tebakan awal berdasarkan metode yang dipilih
col1, col2, col3 = st.columns(3)

with col1:
    x0 = st.number_input("Tebakan Awal (x0):", value=2.0, step=0.1)
with col2:
    # Metode Secant butuh 2 tebakan awal (x0 dan x1)
    if metode == "Secant":
        x1 = st.number_input("Tebakan Kedua (x1):", value=3.0, step=0.1)
    else:
        st.text_input("Tebakan Kedua (x1):", value="Tidak Dibutuhkan", disabled=True)
with col3:
    toleransi = st.number_input("Toleransi (Tingkat Ketelitian):", value=0.0001, format="%.4f", step=0.0001)

# ==========================================
# 3. PROSES SIMBOLIK MATEMATIKA (SYMPY)
# ==========================================
x_simbol = sp.symbols('x')

try:
    ekspresi = sp.sympify(fungsi_input)
    turunan_ekspresi = sp.diff(ekspresi, x_simbol)
    
    if metode == "Newton-Raphson":
        st.info(f"📈 **Turunan pertama f'(x) otomatis:** `{turunan_ekspresi}`")
    
    # SOLUSI UTAMA: Mengubah ekspresi menjadi fungsi numerik yang aman dari NameError
    f_numerik = sp.lambdify(x_simbol, ekspresi, "numpy")
    df_numerik = sp.lambdify(x_simbol, turunan_ekspresi, "numpy")

except Exception as e:
    st.error(f"Sintaks fungsi tidak valid! Mohon periksa kembali penulisan rumus Anda. Error: {e}")
    ekspresi = None

# ==========================================
# 4. EKSEKUSI METODE NUMERIK
# ==========================================
if ekspresi is not None:
    if st.button("Hitung Akar Sekarang"):
        konten_tabel = []
        iterasi = 0
        max_iterasi = 100
        konvergen = False
        
        # ------------------------------------------
        # A. LOGIKA METODE NEWTON-RAPHSON
        # ------------------------------------------
        if metode == "Newton-Raphson":
            x_sekarang = x0
            
            while iterasi < max_iterasi:
                iterasi += 1
                try:
                    # Menggunakan fungsi lambdify yang aman
                    fx = float(f_numerik(x_sekarang))
                    dfx = float(df_numerik(x_sekarang))
                except Exception as eval_err:
                    st.error(f"Gagal mengevaluasi nilai pada x = {x_sekarang}: {eval_err}")
                    break
                
                if dfx == 0:
                    st.error("❌ Error: Turunan f'(x) bernilai 0! Metode Newton-Raphson gagal menemukan akar.")
                    break
                
                x_baru = x_sekarang - (fx / dfx)
                galat = abs(x_baru - x_sekarang)
                
                konten_tabel.append({
                    "Iterasi": iterasi,
                    "x_n": round(x_sekarang, 6),
                    "f(x_n)": round(fx, 6),
                    "f'(x_n)": round(dfx, 6),
                    "x_(n+1)": round(x_baru, 6),
                    "Galat (Error)": round(galat, 6)
                })
                
                if galat < toleransi:
                    konvergen = True
                    akar_ditemukan = x_baru
                    break
                    
                x_sekarang = x_baru

        # ------------------------------------------
        # B. LOGIKA METODE SECANT
        # ------------------------------------------
        elif metode == "Secant":
            x_min1 = x0  
            x_sekarang = x1  
            
            while iterasi < max_iterasi:
                iterasi += 1
                try:
                    # Menggunakan fungsi lambdify yang aman
                    fx_min1 = float(f_numerik(x_min1))
                    fx_sekarang = float(f_numerik(x_sekarang))
                except Exception as eval_err:
                    st.error(f"Gagal mengevaluasi nilai fungsi: {eval_err}")
                    break
                
                if (fx_sekarang - fx_min1) == 0:
                    st.error("❌ Error: Pembagi bernilai 0! Metode Secant gagal.")
                    break
                
                x_baru = x_sekarang - (fx_sekarang * (x_sekarang - x_min1)) / (fx_sekarang - fx_min1)
                galat = abs(x_baru - x_sekarang)
                
                konten_tabel.append({
                    "Iterasi": iterasi,
                    "x_(n-1)": round(x_min1, 6),
                    "x_n": round(x_sekarang, 6),
                    "f(x_(n-1))": round(fx_min1, 6),
                    "f(x_n)": round(fx_sekarang, 6),
                    "x_(n+1)": round(x_baru, 6),
                    "Galat (Error)": round(galat, 6)
                })
                
                if galat < toleransi:
                    konvergen = True
                    akar_ditemukan = x_baru
                    break
                
                x_min1 = x_sekarang
                x_sekarang = x_baru

        # --- MENAMPILKAN HASIL AKHIR ---
        if len(konten_tabel) > 0:
            st.markdown("---")
            st.subheader("📊 Hasil Perhitungan")
            
            if konvergen:
                st.success(f"✅ Konvergen! Perhitungan selesai pada iterasi ke-**{iterasi}**.")
                st.info(f"Akar persamaan yang ditemukan adalah x = **{akar_ditemukan:.6f}** dengan nilai f(x) = **{float(f_numerik(akar_ditemukan)):.6f}**")
            else:
                st.warning("⚠️ Perhitungan mencapai batas maksimum iterasi tanpa mencapai toleransi yang diinginkan.")
            
            df_hasil = pd.DataFrame(konten_tabel)
            st.subheader("📋 Tabel Iterasi Perhitungan")
            st.dataframe(df_hasil, use_container_width=True)
