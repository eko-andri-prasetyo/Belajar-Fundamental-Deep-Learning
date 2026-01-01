# Langkah Cepat (Target Bintang 5)

## 1) Scraping (Kriteria 1 + Data >= 10k)
```bash
pip install -r requirements.txt
python scrape.py --app_id com.whatsapp --target 12000 --out dataset_playstore.csv
```
Pastikan file `dataset_playstore.csv` terbentuk dan jumlah baris >= 3000 (disarankan 10000+).

## 2) Training + 3 eksperimen + inference
Buka `sentiment_training.ipynb` di Colab → `Runtime > Run all`.
Pastikan:
- output akurasi tampil
- confusion matrix tampil
- inference tampil (label negatif/netral/positif)

## 3) Untuk “mengunci” >92%
Jalankan bagian **Fine-tune IndoBERT** (opsional) di notebook.

## 4) Submit
Zip 1 folder ini berisi minimal:
- sentiment_training.ipynb (SUDAH ADA OUTPUT)
- scrape.py
- requirements.txt
- dataset_playstore.csv (HASIL SCRAPING)
