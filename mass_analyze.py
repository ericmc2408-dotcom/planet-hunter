from lightkurve import search_lightcurve
import pandas as pd
import numpy as np
import json
from datetime import datetime
import os

def mass_analyze(max_stars=50, skip=0):
    """
    Analyze stars in batches
    """
    print(f"Starting mass analysis...")
    
    # Check which list to use
    if os.path.exists('data/promising_stars/tic_list.txt'):
        list_file = 'data/promising_stars/tic_list.txt'
        print("Using promising stars list")
    elif os.path.exists('data/nasa_rejected/tic_list.txt'):
        list_file = 'data/nasa_rejected/tic_list.txt'
        print("Using NASA rejected list")
    else:
        print("No star list found! Run smart_selector.py first")
        return
    
    with open(list_file, 'r') as f:
        tic_list = [line.strip() for line in f.readlines()]
    
    print(f"Total stars in list: {len(tic_list)}")
    print(f"Analyzing {max_stars} stars (starting from #{skip})")
    
    results = []
    os.makedirs('data/analyzed_batches', exist_ok=True)
    
    for i, tic_id in enumerate(tic_list[skip:skip+max_stars]):
        print(f"[{i+1}/{max_stars}] {tic_id}...", end=' ')
        
        try:
            search_result = search_lightcurve(tic_id, mission='TESS')
            
            if len(search_result) == 0:
                print("No data")
                continue
            
            lc = search_result[0].download()
            lc = lc.remove_outliers().flatten()
            
            pg = lc.to_periodogram(method='bls', period=np.arange(0.5, 20, 0.02))
            
            best_period = float(pg.period_at_max_power.value)
            max_power = float(pg.max_power.value)
            
            lc_folded = lc.fold(period=best_period)
            transit_depth = max(0, 1 - float(lc_folded.flux.min().value))
            
            score = max_power * (transit_depth * 100)
            
            result = {
                'star_id': tic_id,
                'period_days': best_period,
                'power': max_power,
                'transit_depth_percent': transit_depth * 100,
                'score': score,
                'interesting': score > 50
            }
            
            results.append(result)
            
            status = "INTERESTING!" if score > 50 else "ok"
            print(f"P={best_period:.2f}d, Score={score:.1f} [{status}]")
            
            if (i+1) % 10 == 0:
                df = pd.DataFrame(results)
                df.to_csv(f'data/analyzed_batches/batch_{skip}_{i+1}.csv', index=False)
                print(f"Saved batch {i+1}")
            
        except Exception as e:
            print(f"Error: {str(e)[:50]}")
            continue
    
    if results:
        df = pd.DataFrame(results)
        df.to_csv(f'data/analyzed_batches/batch_{skip}_{max_stars}_final.csv', index=False)
        
        interesting = df[df['interesting'] == True]
        
        print(f"\n{'='*60}")
        print(f"BATCH COMPLETE!")
        print(f"{'='*60}")
        print(f"Analyzed: {len(df)}")
        print(f"Interesting: {len(interesting)}")
        if len(interesting) > 0:
            print(f"\nTop candidates:")
            print(interesting.nlargest(5, 'score')[['star_id', 'period_days', 'score']].to_string(index=False))
        print(f"{'='*60}\n")

if __name__ == '__main__':
    mass_analyze(max_stars=50, skip=0)
