# Deploy Quick Reference - Render.com

## 🚀 Quick Deploy Steps

### 1️⃣ Push to GitHub
```bash
# Windows PowerShell
.\deploy.ps1

# Linux/Mac
bash deploy.sh
```

### 2️⃣ Connect to Render.com

**URL:** https://dashboard.render.com/

| Field | Value |
|-------|-------|
| Service Name | `ecommerce-churn-serving` |
| Git Repo | Your GitHub repo |
| Branch | `main` |
| Runtime | `Docker` |
| Region | `Singapore` (or closest) |
| Dockerfile Path | `./serving/Dockerfile` |
| Docker Context | `.` |
| Plan | `Starter` ($7/mo) or `Standard` ($12/mo) |

### 3️⃣ Deploy!
Click "Create Web Service" → Wait for build → Get live URL

---

## 🧪 Test After Deployment

Replace `YOUR_RENDER_URL` with actual URL from Render dashboard:

```bash
curl --location 'https://YOUR_RENDER_URL/v1/models/ecommerce_churn:predict' \
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
  "predictions": [[0.35]]
}
```

---

## 📊 Model Endpoints

After deploy, endpoints available:

| Endpoint | Purpose |
|----------|---------|
| `/v1/models/ecommerce_churn/metadata` | Model metadata & signatures |
| `/v1/models/ecommerce_churn:predict` | Prediction (with signature_name & inputs) |
| `http://localhost:8501/` | Health check / root |

---

## 🔄 Update Model

1. Regenerate model locally (run TFX pipeline)
2. Copy to `serving_model/rfahrur6045-pipeline/`
3. Commit & push:
   ```bash
   git add serving_model/
   git commit -m "Update model v$(date +%s)"
   git push origin main
   ```
4. Render auto-deploys 🎉

---

## ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `render.yaml` | Render deployment config |
| `serving/Dockerfile` | Docker image for TF-Serving |
| `deploy.sh` / `deploy.ps1` | Helper scripts |
| `DEPLOY_GUIDE.md` | Detailed guide |

---

## 💡 Tips & Tricks

### Monitor Deployment
```
Render Dashboard → Logs
```
- Real-time deployment logs
- Error tracking
- Container output

### Enable Auto-Deploy
Push to GitHub → Render auto-deploys
(Set in Render settings)

### Custom Domain
1. Buy domain (Namecheap, GoDaddy, etc)
2. Render Dashboard → Settings → Custom Domain
3. Add DNS records (Render guides you)

### Performance Tuning
- `Standard` plan (1 GB RAM) recommended for production
- Enable batching in Dockerfile ✅ (already done)
- Monitor CPU/Memory in Render dashboard

---

## 🆘 Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails | Check logs in Render |
| Model not loading | Verify path in Dockerfile |
| Timeout error | Starter plan might be slow, upgrade to Standard |
| Wrong response | Check signature_name matches model |

---

## 📞 Useful Resources

- **Render Docs:** https://render.com/docs
- **TF-Serving Docs:** https://www.tensorflow.org/tfx/serving/api_rest
- **Docker Docs:** https://docs.docker.com/
