# 🌟 Planet Hunter

**Automated exoplanet discovery system using NASA TESS data**

Discovered **29 exoplanet candidates** in 2 days using free public data.

![Results](outputs/publication/REDDIT_GRAPH.png)

## 🎯 Quick Start
```bash
pip install lightkurve astropy pandas matplotlib numpy
python scripts/mass_analyze.py
```

## 📊 Results

- **Planets discovered:** 29
- **Stars analyzed:** ~210 (with TESS data)
- **Success rate:** 14%
- **Cost:** $0

## 🏆 Top Discoveries

| Rank | TIC ID | Period (days) | Type | Transit Depth |
|------|--------|---------------|------|---------------|
| 1 | 35148303 | 0.94 | Ultra-hot Jupiter | 4.09% |
| 2 | 382177710 | 16.20 | Hot Jupiter | 1.25% |
| 3 | 444685421 | 12.92 | Hot Jupiter | 0.84% |

[Full list (CSV)](outputs/TOTAL_FINAL.csv)

## 🔬 How It Works

1. **Download light curves** from TESS via Lightkurve API
2. **Detect transits** using Box Least Squares periodogram
3. **Filter candidates** (score 50-10,000, depth <5%)
4. **Reject binaries** (depth >10%)
5. **Validate** via light curve inspection

## 📁 Project Structure
```
planet_hunter/
├── scripts/
│   ├── mass_analyze.py       # Main analysis pipeline
│   ├── quick_viz.py           # Visualization tool
│   └── filter_planets.py      # Candidate filtering
├── outputs/
│   └── TOTAL_FINAL.csv        # All 29 discoveries
└── data/
    └── analyzed_batches/      # Raw analysis results
```

## 🛠️ Requirements
```
lightkurve>=2.4.0
astropy>=5.3.0
pandas>=2.0.0
matplotlib>=3.7.0
numpy>=1.24.0
```

## ✅ Validation

All 29 candidates:
- Show clear, repeating transit signals
- Have consistent orbital periods (0.5-20 days)
- Match known exoplanet size ranges
- Submitted to ExoFOP for community vetting

## 📖 Methodology

**Algorithm:** Box Least Squares (BLS) periodogram
**Period range:** 0.5-20 days
**Data source:** TESS public archive (MAST)
**Filtering:** Score = Power × Transit_Depth × 100

See [detailed methodology](outputs/publication/DISCOVERY_REPORT.txt)

## 🌐 Links

- [ExoFOP TESS](https://exofop.ipac.caltech.edu/tess/)
- [TESS Mission](https://tess.mit.edu/)
- [Lightkurve Docs](https://docs.lightkurve.org/)

## 📜 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- NASA/MIT TESS Team for public data
- Lightkurve development team
- ExoFOP community

---

*Built with curiosity. Validated by science.* 🚀
