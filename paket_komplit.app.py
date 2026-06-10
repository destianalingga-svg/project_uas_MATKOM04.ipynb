import streamlit as st
import pandas as pd
import numpy as np
import sympy as sp

# ==========================================
# 1. KONFIGURASI HALAMAN & JUDUL MASTER
# ==========================================
st.set_page_config(page_title="Project UAS Matematika Komputasi", layout="centered")

st.title("🖥️ Project UAS Matematika Komputasi")
st.write("**Nama Kelompok:** Nadin Nur Indah, Destiana Lingga Sari, Rezza Ramadani")
st.markdown("---")

# ==========================================
# 2. NAVIGASI MENU DI SIDEBAR (SEBELAH KIRI)
# ==========================================
st.sidebar.title("🧭 Navigasi Metode")
menu = st.sidebar.selectbox(
    "Pilih Metode Numerik:",
    ("Bisection (Bagi Dua)", "Newton-Raphson", "Secant (Tali Busur)")
)

# Definisi simbol matematika universal
x_simbol = sp.symbols('x')

# ==========================================
# 3. LOGIKA UNTUK MASING-MASING METODE
# ==========================================

# ------------------------------------------
# A. METODE BISECTION
# ------------------------------------------
if menu == "Bisection (Bagi Dua)":
    st.header("🧮 Metode Bisection (Bagi Dua)")
    
    fungsi_input = st.text_input("Masukkan fungsi f(x):", value="x**3 - 4*x - 9", key="bis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.number_input("Batas Bawah (a):", value=2.0)
    with col2:
        b = st.number_input("Batas Atas (b):", value=3.0)
    with col3:
        toleransi = st.number_input("Toleransi:", value=0.0001, format="%.4f")

    try:
        ekspresi = sp.sympify(fungsi_input)
        f_bis = sp.lambdify(x_simbol, ekspresi, "numpy")
    except Exception as e:
        st.error(f"Sintaks fungsi tidak valid: {e}")
        ekspresi = None

    if ekspresi is not None and st.button("Hitung Bisection"):
        try:
            if f_bis(a) * f_bis(b) >= 0:
                st.error("❌ Nilai f(a) dan f(b) harus berlawanan tanda! Interval tidak mengurung akar.")
            else:
                konten_tabel = []
                iterasi = 0
                c = (a + b) / 2
                
                while abs(b - a) >= toleransi and iterasi < 100:
                    iterasi += 1
                    c = (a + b) / 2
                    fc = f_bis(c)
                    
                    konten_tabel.append({
                        "Iterasi": iterasi,
                        "Batas Bawah (a)": round(a, 6),
                        "Batas Atas (b)": round(b, 6),
                        "Titik Tengah (c)": round(c, 6),
                        "f(c)": round(fc, 6),
                        "Lebar Interval": round(abs(b - a), 6)
                    })
                    
                    if f_bis(a) * fc < 0:
                        b = c
                    else:
                        a = c
                
                st.success(f"✅ Konvergen! Akar ditemukan pada x = **{c:.6f}**")
                st.dataframe(pd.DataFrame(konten_tabel), use_container_width=True)
        except Exception as e:
            st.error(f"Terjadi kesalahan perhitungan: {e}")

# ------------------------------------------
# B. METODE NEWTON-RAPHSON
# ------------------------------------------
elif menu == "Newton-Raphson":
    st.header("📈 Metode Newton-Raphson")
    
    fungsi_input = st.text_input("Masukkan fungsi f(x):", value="x**3 - 4*x - 9", key="nr")
    
    col1, col2 = st.columns(2)
    with col1:
        x0 = st.number_input("Tebakan Awal (x0):", value=2.0)
    with col2:
        toleransi = st.number_input("Toleransi:", value=0.0001, format="%.4f")

    try:
        ekspresi = sp.sympify(fungsi_input)
        turunan_ekspresi = sp.diff(ekspresi, x_simbol)
        st.info(f"🔍 **Turunan f'(x) Otomatis:** `{turunan_ekspresi}`")
        
        # Mengubah ekspresi matematika menjadi fungsi Python yang siap dieksekusi
        f_nr = sp.lambdify(x_simbol, ekspresi, "numpy")
        df_nr = sp.lambdify(x_simbol, turunan_ekspresi, "numpy")
    except Exception as e:
        st.error(f"Sintaks fungsi salah: {e}")
        ekspresi = None

    if ekspresi is not None and st.button("Hitung Newton-Raphson"):
        konten_tabel = []
        x_sekarang = x0
        iterasi = 0
        konvergen = False
        
        while iterasi < 100:
            iterasi += 1
            fx = f_nr(x_sekarang)
            dfx = df_nr(x_sekarang)
            
            if dfx == 0:
                st.error("❌ Turunan bernilai 0! Metode gagal.")
                break
                
            x_baru = x_sekarang - (fx / dfx)
            galat = abs(x_baru - x_sekarang)
            
            konten_tabel.append({
                "Iterasi": iterasi,
                "x_n": round(float(x_sekarang), 6),
                "f(x_n)": round(float(fx), 6),
                "f'(x_n)": round(float(dfx), 6),
                "x_(n+1)": round(float(x_baru), 6),
                "Galat": round(float(galat), 6)
            })
            
            if galat < toleransi:
                konvergen = True
                st.success(f"✅ Konvergen! Akar ditemukan pada x = **{x_baru:.6f}**")
                break
            x_sekarang = x_baru
            
        st.dataframe(pd.DataFrame(konten_tabel), use_container_width=True)

# ------------------------------------------
# C. METODE SECANT
# ------------------------------------------
elif menu == "Secant (Tali Busur)":
    st.header("📐 Metode Secant")
    
    fungsi_input = st.text_input("Masukkan fungsi f(x):", value="x**3 - 4*x - 9", key="sec")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        x0 = st.number_input("Tebakan Awal 1 (x0):", value=2.0)
    with col2:
        x1 = st.number_input("Tebakan Awal 2 (x1):", value=3.0)
    with col3:
        toleransi = st.number_input("Toleransi:", value=0.0001, format="%.4f")

    try:
        ekspresi = sp.sympify(fungsi_input)
        f_sec = sp.lambdify(x_simbol, ekspresi, "numpy")
    except Exception as e:
        st.error(f"Sintaks fungsi salah: {e}")
        ekspresi = None

    if ekspresi is not None and st.button("Hitung Secant"):
        konten_tabel = []
        x_min1 = x0
        x_sekarang = x1
        iterasi = 0
        
        while iterasi < 100:
            iterasi += 1
            fx_min1 = f_sec(x_min1)
            fx_sekarang = f_sec(x_sekarang)
            
            if (fx_sekarang - fx_min1) == 0:
                st.error("❌ Pembagi bernilai 0! Metode gagal.")
                break
                
            x_baru = x_sekarang - (fx_sekarang * (x_sekarang - x_min1)) / (fx_sekarang - fx_min1)
            galat = abs(x_baru - x_sekarang)
            
            konten_tabel.append({
                "Iterasi": iterasi,
                "x_(n-1)": round(float(x_min1), 6),
                "x_n": round(float(x_sekarang), 6),
                "x_(n+1)": round(float(x_baru), 6),
                "Galat": round(float(galat), 6)
            })
            
            if galat < toleransi:
                st.success(f"✅ Konvergen! Akar ditemukan pada x = **{x_baru:.6f}**")
                break
                
            x_min1 = x_sekarang
            x_sekarang = x_baru
            
        st.dataframe(pd.DataFrame(konten_tabel), use_container_width=True)
