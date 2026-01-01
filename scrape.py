"""
Scraper Google Play Store (Dicoding - Proyek Analisis Sentimen)

Output: dataset_playstore.csv
Kolom: text, rating, label, at, reviewId, appId

Label dibuat dari rating:
  1-2 -> negatif
  3   -> netral
  4-5 -> positif

Cara pakai (contoh):
  pip install -r requirements.txt
  python scrape.py --app_id com.whatsapp --target 12000 --lang id --country id

Catatan:
- Jalankan secara wajar (tidak agresif).
- Pastikan dataset hasil scraping >= 3000 sampel (untuk nilai maksimal, targetkan >= 10000).
"""

import argparse
import pandas as pd
from tqdm import tqdm
from google_play_scraper import Sort, reviews

def rating_to_label(score: int) -> str:
    if score <= 2:
        return "negatif"
    if score == 3:
        return "netral"
    return "positif"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app_id", default="com.whatsapp")
    ap.add_argument("--lang", default="id")
    ap.add_argument("--country", default="id")
    ap.add_argument("--target", type=int, default=12000)
    ap.add_argument("--batch", type=int, default=200)
    ap.add_argument("--out", default="dataset_playstore.csv")
    args = ap.parse_args()

    all_rows = []
    token = None

    pbar = tqdm(total=args.target, desc=f"Scraping {args.app_id}")
    while len(all_rows) < args.target:
        result, token = reviews(
            args.app_id,
            lang=args.lang,
            country=args.country,
            sort=Sort.NEWEST,
            count=min(args.batch, args.target - len(all_rows)),
            continuation_token=token,
        )

        if not result:
            break

        for r in result:
            text = (r.get("content") or "").strip()
            score = int(r.get("score") or 0)
            if not text:
                continue
            all_rows.append({
                "text": text,
                "rating": score,
                "label": rating_to_label(score),
                "at": str(r.get("at")),
                "reviewId": r.get("reviewId"),
                "appId": args.app_id,
            })

        pbar.update(min(args.batch, args.target - pbar.n))
        if token is None:
            break

    pbar.close()

    df = pd.DataFrame(all_rows).drop_duplicates(subset=["reviewId"]).reset_index(drop=True)
    df = df[df["label"].isin(["negatif", "netral", "positif"])]
    df.to_csv(args.out, index=False, encoding="utf-8")

    print("Saved:", args.out, "rows:", len(df))
    print(df["label"].value_counts())

    if len(df) < 3000:
        print("WARNING: data < 3000. Ganti app_id / ulangi scraping.")

if __name__ == "__main__":
    main()
