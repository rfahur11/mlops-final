# Deploy ke Render.com - Panduan Lengkap

## 📋 Persyaratan
- [ ] GitHub account (push code ke repo)
- [ ] Render.com account (free tier bisa dipakai)
- [ ] Model SavedModel sudah di-generate dan di-push ke GitHub

---

## 🚀 STEP 1: Siapkan Repository GitHub

### 1.1 Pastikan model sudah di-commit
```bash
# Pastikan model terbaru sudah di-serving_model/
ls -la serving_model/rfahrur6045-pipeline/

# Commit semua file penting
git add .
git commit -m "Deploy: SavedModel dengan serving_json signature fix"
git push origin main
```

### 1.2 File yang perlu ada di GitHub:
```
rfahrur6045-pipeline/
├── serve/
│   └── Dockerfile (TF-Serving image)
├── serving_model/
│   └── rfahrur6045-pipeline/
│       └── 1779211431/  (model version dengan 18 features)
│           ├── saved_model.pb
│           ├── variables/
│           └── assets/
├── render.yaml (baru - sudah dibuat)
└── requirements.txt
```

---

## 🎯 STEP 2: Setup Render.com

### 2.1 Login ke Render.com
1. Buka https://dashboard.render.com/
2. Sign up atau login dengan GitHub

### 2.2 Connect GitHub Repository
1. Click **"New +"** → **"Web Service"**
2. Select **"Public Git repository"**
3. Paste repository URL: `https://github.com/YOUR_GITHUB_USERNAME/rfahrur6045-pipeline`
4. Click **"Connect"**

### 2.3 Configure Deployment
| Setting | Value |
|---------|-------|
| **Name** | `ecommerce-churn-serving` |
| **Environment** | `Docker` |
| **Region** | `Singapore` (atau pilih terdekat) |
| **Branch** | `main` |
| **Dockerfile Path** | `./serving/Dockerfile` |
| **Docker Context** | `.` |

### 2.4 Environment Variables (opsional)
Jika ada Kaggle API key atau credentials:
```
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_key
```

---

## 📦 STEP 3: Custom Dockerfile untuk Render (Jika perlu)

Jika Dockerfile di `serving/` perlu adjustment:

```dockerfile
FROM tensorflow/serving:2.12.0

# Salin model (pastikan path relatif ke root repo)
COPY ./serving_model/rfahrur6045-pipeline /models/ecommerce_churn

# Environment
ENV MODEL_NAME=ecommerce_churn
ENV PORT=8501

# Expose
EXPOSE 8500
EXPOSE 8501

# Run TF Serving
ENTRYPOINT ["tensorflow_model_server", \
  "--rest_api_port=8501", \
  "--model_name=ecommerce_churn", \
  "--model_base_path=/models/ecommerce_churn"]
```

---

## ✅ STEP 4: Deploy

### 4.1 Via Render Dashboard
1. Setelah konfigurasi, click **"Create Web Service"**
2. Render akan:
   - Build Docker image
   - Push ke registry
   - Deploy container
   - Assign public URL (cth: `https://ecommerce-churn-serving.onrender.com`)

### 4.2 Monitor Deployment
```
Dashboard → Logs
```
Tunggu sampai status **"Live"** dan tidak ada error.

---

## 🧪 STEP 5: Test Endpoint di Production

Setelah deploy live, test API:

```bash
curl --location 'https://ecommerce-churn-serving.onrender.com/v1/models/ecommerce_churn:predict' \
--header 'Content-Type: application/json' \
--data '{
  "signature_name": "serving_json",
  "inputs": {
    "Tenure": [3],
    "CityTier": [1],
    "WarehouseToHome": [10],
    "HourSpendOnApp": [1],
    "NumberOfDeviceRegistered": [2],
    "SatisfactionScore": [3],
    "NumberOfAddress": [1],
    "Complain": [0],
    "OrderAmountHikeFromlastYear": [11.0],
    "CouponUsed": [0],
    "OrderCount": [3],
    "DaySinceLastOrder": [5],
    "CashbackAmount": [0],
    "PreferredLoginDevice": ["Mobile Phone"],
    "PreferredPaymentMode": ["Debit Card"],
    "Gender": ["Female"],
    "PreferedOrderCat": ["Grocery"],
    "MaritalStatus": ["Single"]
  }
}'
```

**Expected Response:**
```json
{
  "predictions": [[0.35]]  // Churn probability
}
```

---

## ⚙️ STEP 6: Advanced Configuration

### 6.1 Auto-Deploy on Push
Render.com otomatis deploy ulang saat ada `git push`:
```bash
# Setiap push akan trigger deploy baru
git add .
git commit -m "Update model"
git push origin main
```

### 6.2 Disable Auto-Deploy (jika perlu)
1. Dashboard → Settings
2. Toggle **"Auto-Deploy"** → OFF
3. Deploy manual via **"Manual Deploy"** button

### 6.3 Monitor & Logging
```
Dashboard → Logs
```
- Realtime logs TF-Serving
- Error tracking
- Performance metrics

---

## 💾 STEP 7: Model Updates

Untuk update model di production:

```bash
# 1. Regenerate model di local
# (Jalankan TFX pipeline notebook cell 34)

# 2. Copy ke serving_model/
cp -r pipelines/rfahrur6045-pipeline/Trainer/model/58/Format-Serving \
  serving_model/rfahrur6045-pipeline/1779211431/

# 3. Commit & push
git add serving_model/
git commit -m "Update model version 1779211431"
git push origin main

# 4. Render otomatis build & deploy ulang
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Build gagal** | Check logs di Render Dashboard → Logs |
| **Model tidak load** | Pastikan path model relatif benar di Dockerfile |
| **Timeout 60 detik** | TF-Serving butuh waktu load, cek health check endpoint |
| **Memory insufficient** | Upgrade ke plan berbayar atau optimize model |

---

## 📊 Pricing (Render.com)
- **Starter**: $7/month (640 MB RAM) - untuk testing
- **Standard**: $12/month (1 GB RAM) - recommended untuk production
- **Premium**: $29/month (2 GB RAM+) - untuk high traffic

---

## ✨ Bonus: Custom Domain

1. Beli domain di Namecheap, GoDaddy, dll
2. Di Render Dashboard → Settings → Custom Domain
3. Add DNS records (Render akan guide)
4. Akses via `https://yourmodel.com/v1/models/ecommerce_churn:predict`

---

## 📝 Summary

| Aspek | Status |
|-------|--------|
| **Code Ready** | ✅ Di GitHub |
| **Model Ready** | ✅ SavedModel dengan dual signatures |
| **Docker Ready** | ✅ Dockerfile di serving/ |
| **Config Ready** | ✅ render.yaml sudah dibuat |
| **Ready Deploy** | ✅ Tinggal connect GitHub ke Render |

**Next Step:** Push ke GitHub dan connect ke Render.com! 🚀
