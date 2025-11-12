#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

def generate(rows:int=10000, seed:int=42):
    np.random.seed(seed)
    dates = pd.date_range(start="2023-01-01", end="2024-12-31")
    n_dates = len(dates)
    channels = ["Facebook","Google","Email","Affiliate","TV","Organic","LinkedIn","Instagram"]
    regions = ["North","South","East","West"]
    devices = ["Desktop","Mobile","Tablet"]
    campaign_types = ["Awareness","Consideration","Conversion"]
    rows_list = []
    for i in range(rows):
        date = dates[np.random.randint(0, n_dates)]
        channel = np.random.choice(channels, p=[0.25,0.25,0.15,0.05,0.05,0.15,0.05,0.05])
        campaign_id = f"camp_{np.random.randint(1,31):03d}"
        region = np.random.choice(regions)
        device = np.random.choice(devices, p=[0.5,0.45,0.05])
        ctype = np.random.choice(campaign_types, p=[0.3,0.4,0.3])
        base_spend_channel = {"Facebook":800,"Google":1200,"Email":150,"Affiliate":300,"TV":2000,"Organic":50,"LinkedIn":400,"Instagram":600}[channel]
        type_multiplier = {"Awareness":0.8,"Consideration":1.0,"Conversion":1.2}[ctype]
        month = date.month
        season = 1.2 if month in [11,12] else (0.9 if month in [6,7] else 1.0)
        spend = max(5, np.random.normal(loc=base_spend_channel*type_multiplier*season, scale=base_spend_channel*0.4))
        impressions = max(10, int(spend * np.random.uniform(20,80)))
        ctr = np.clip(np.random.normal(0.03 if channel in ["Facebook","Google","Instagram"] else 0.01, 0.01), 0.001, 0.2)
        clicks = int(impressions * ctr)
        conv_rate = np.clip(np.random.normal(0.02 if ctype=="Conversion" else 0.005, 0.01), 0.0001, 0.5)
        conversions = int(clicks * conv_rate)
        rev_per_conv = {"Facebook":60,"Google":80,"Email":40,"Affiliate":50,"TV":150,"Organic":30,"LinkedIn":120,"Instagram":55}[channel]
        revenue = conversions * rev_per_conv * np.random.uniform(0.6,1.5)
        if np.random.rand() < 0.005:
            spend *= np.random.uniform(3,8)
            revenue *= np.random.uniform(0.2,4.0)
        cust_acquisition_cost = spend / max(1, conversions)
        rows_list.append({
            "date": date.strftime("%Y-%m-%d"),
            "channel": channel,
            "campaign_id": campaign_id,
            "spend": round(spend,2),
            "impressions": int(impressions),
            "clicks": int(clicks),
            "conversions": int(conversions),
            "revenue": round(float(revenue),2),
            "cust_acquisition_cost": round(float(cust_acquisition_cost),2) if conversions>0 else None,
            "region": region,
            "device": device,
            "campaign_type": ctype
        })
    df = pd.DataFrame(rows_list)
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--out", type=str, default="data/raw/marketing_campaign.csv")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    df = generate(rows=args.rows, seed=args.seed)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")

if __name__ == "__main__":
    main()
