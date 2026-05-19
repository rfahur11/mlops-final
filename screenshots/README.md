# Screenshots

Folder ini berisi bukti screenshot submission.

| Nama File | Keterangan |
|---|---|
| `rfahrur6045-deployment.png` | Screenshot bukti model berjalan di Railway (cloud) |
| `rfahrur6045-monitoring.png` | Screenshot dashboard Prometheus |
| `rfahrur6045-pylint.png` | Screenshot hasil pylint pada folder modules |
| `rfahrur6045-grafana-dashboard.png` | Screenshot dashboard Grafana (bonus) |

## Cara Mengambil Screenshot

### 1. rfahrur6045-deployment.png
Setelah deploy ke Railway, buka URL Railway dan jalankan:
```bash
curl https://<railway-url>/v1/models/ecommerce_churn
```
Screenshot hasilnya (harus menunjukkan `"state": "AVAILABLE"`).

### 2. rfahrur6045-monitoring.png
Buka http://localhost:9090, jalankan query:
```
up{job="tensorflow-serving"}
```
Screenshot halaman Prometheus dengan hasil query.

### 3. rfahrur6045-pylint.png
Jalankan di terminal:
```bash
pylint modules/ecommerce_transform.py modules/ecommerce_trainer.py
```
Screenshot outputnya.

### 4. rfahrur6045-grafana-dashboard.png
Buka http://localhost:3000, buat dashboard, screenshot hasilnya.
