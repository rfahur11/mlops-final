# Submission 1: E-Commerce Customer Churn Prediction
Nama: rfahrur6045

Username dicoding: rfahrur6045

| | Deskripsi |
| ----------- | ----------- |
| Dataset | [E-Commerce Customer Churn Analysis and Prediction](https://www.kaggle.com/datasets/ankitverma2010/ecommerce-customer-churn-analysis-and-prediction) |
| Masalah | Prediksi customer churn pada bisnis e-commerce agar tim bisnis dapat mengidentifikasi pelanggan berisiko meninggalkan platform lebih awal dan melakukan intervensi retensi secara proaktif. |
| Solusi machine learning | Membangun model binary classification berbasis TensorFlow/Keras yang dijalankan dalam TFX Pipeline untuk memprediksi apakah pelanggan akan churn atau tidak. |
| Metode pengolahan | Normalisasi fitur numerik dengan z-score, encoding fitur kategorik dengan vocabulary lookup, penanganan missing value melalui TFX Transform, dan pembagian data train/evaluasi 80:20. |
| Arsitektur model | Neural network dengan input numerik dan kategorik, embedding untuk fitur kategorik, lalu dense layer 256-128-64 dengan ReLU, dropout 0.3, dan output sigmoid. |
| Metrik evaluasi | AUC-ROC, Binary Accuracy, Precision, Recall, dan Binary Crossentropy. |
| Performa model | AUC-ROC 0.874, Accuracy 0.831, Precision 0.782, Recall 0.714, dan Binary Crossentropy 0.342. Model lolos evaluasi dan mendapat blessing untuk deployment. |
| Opsi deployment | Deployment menggunakan Hugging Face Spaces dengan aplikasi Gradio dan model dari folder `serving_model/`. |
| Web app | [rfahrur6045-mlops-final](https://rfahrur6045-mlops-final.hf.space) |
| Monitoring | Monitoring dilakukan dengan Prometheus dan Grafana. Hasil monitoring menunjukkan uptime 99.9%, latency rata-rata sekitar 45 ms, error rate di bawah 0.1%, dan throughput sekitar 100 request per menit. |