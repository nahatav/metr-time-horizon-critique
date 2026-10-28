# METR's Time Horizon Chart Is Easy to Read, and Easy to Overread

A one page design critique of METR's chart "Length of software tasks that different LLMs can complete 50% of the time" (Time Horizon 1.1), made for DSC 106 Project 2.5 at UC San Diego.

**Live page:** https://nahatav.github.io/metr-time-horizon-critique/

**PDF:** [METR_time_horizon_critique.pdf](METR_time_horizon_critique.pdf)

## Authors

Valmik Nahata, Varun Sinha, Rishab Kolan, Rishil Chintalapati

## What is in the critique

* The original chart, annotated with three strengths (S1 to S3) and four weaknesses (W1 to W4), each tied to a concept from Lectures 1 to 6.
* A table of the chart's marks and channels with their data types.
* A reanalysis of METR's published estimates. Refitting their data recovers their trend line (doubling every 188 days), but every frontier model from o3 onward sits above it, and a fit to models from 2024 on doubles every 105 days.

## Sources

* Original chart: https://metr.org/time-horizons/
* Data: https://metr.org/assets/benchmark_results_1_1.yaml (copied here as `benchmark_results_1_1.yaml`)
* METR analysis code: https://github.com/METR/eval-analysis-public

## Rebuilding

```
pip install pyyaml numpy playwright
python build.py        # writes index.html
python shot.py --pdf   # renders the PDF (uses Microsoft Edge through Playwright)
```
