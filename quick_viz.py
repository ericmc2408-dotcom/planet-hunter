from lightkurve import search_lightcurve
import matplotlib.pyplot as plt
import numpy as np
import os

def quick_viz(star_id):
    print(f"Analyzing {star_id}...")
    
    # Download
    lc = search_lightcurve(star_id, mission='TESS')[0].download()
    lc_clean = lc.remove_outliers().flatten()
    
    # Periodogram
    pg = lc_clean.to_periodogram(method='bls', period=np.arange(0.5, 20, 0.01))
    best_period = pg.period_at_max_power
    
    # Fold
    lc_folded = lc_clean.fold(period=best_period)
    
    # Plot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Raw
    lc.plot(ax=ax1)
    ax1.set_title(f'{star_id} - Raw Light Curve', fontsize=14, fontweight='bold')
    
    # Clean
    lc_clean.plot(ax=ax2, color='orange')
    ax2.set_title(f'{star_id} - Cleaned', fontsize=14, fontweight='bold')
    
    # Periodogram
    pg.plot(ax=ax3)
    ax3.axvline(best_period.value, color='red', linestyle='--', linewidth=2)
    ax3.set_title(f'Periodogram (P={best_period:.2f}d)', fontsize=14, fontweight='bold')
    
    # Folded
    lc_folded.scatter(ax=ax4)
    ax4.set_title(f'Folded Light Curve', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    # Save
    os.makedirs('outputs/top_candidates', exist_ok=True)
    filename = f'outputs/top_candidates/{star_id.replace(" ", "_")}_full.png'
    plt.savefig(filename, dpi=150)
    print(f"Saved: {filename}")
    
    plt.show()
    
    # Stats
    transit_depth = 1 - float(lc_folded.flux.min().value)
    
    print(f"\n{'='*60}")
    print(f"CANDIDATE ANALYSIS: {star_id}")
    print(f"{'='*60}")
    print(f"Period: {best_period:.4f} days")
    print(f"Transit Depth: {transit_depth*100:.2f}%")
    print(f"Power: {pg.max_power:.2f}")
    print(f"Planet/Star Radius: {np.sqrt(transit_depth):.3f}")
    print(f"\nIf Sun-like star:")
    print(f"  Planet radius: ~{np.sqrt(transit_depth)*109:.1f} Earth radii")
    print(f"  Classification: {'Jupiter-class' if np.sqrt(transit_depth)*109 > 10 else 'Neptune-class'}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    # Analyze TOP 1
    quick_viz('TIC 18413404')
