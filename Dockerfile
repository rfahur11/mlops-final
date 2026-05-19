# 1. Gunakan image dasar TFX dari Google
FROM tensorflow/tfx:1.14.0

# 2. Tetapkan direktori kerja
WORKDIR /workspace

# 3. Salin file requirements.txt ke dalam container
COPY requirements.txt /workspace/

# 4. Instal library tambahan menggunakan pip bawaan sistem
RUN pip install --no-cache-dir -r requirements.txt

# 5. Ekspos port Jupyter
EXPOSE 8888

# 6. RESET entrypoint bawaan Apache Beam
ENTRYPOINT []

# 7. Jalankan Jupyter menggunakan modul python utama tanpa token
CMD ["python", "-m", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token=''"]