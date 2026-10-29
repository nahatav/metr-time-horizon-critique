# METR Time Horizon Critique — 2-Minute Presentation Script

**Presentation Time:** ~2:00 (approx. 290 words at 140 WPM)  
**Deliverable:** 1-page PDF Poster ([METR_time_horizon_critique.pdf](file:///c:/Users/Valmi/Documents/antigravity/fervent-bose/METR_time_horizon_critique.pdf))  
**Speakers:** Valmik Nahata, Varun Sinha, Rishab Kolan, Rishil Chintalapati  

---

### [0:00 – 0:20] Introduction
*(Point to the main METR chart on the top left)*

"This is our design critique of METR’s Time Horizon chart, one of the most widely cited graphs in AI right now. Across the horizontal axis is release date, and up the vertical axis is the task duration an AI model can solve fifty percent of the time, measured in human expert work."

---

### [0:20 – 0:40] Marks and Channels
*(Point to the Marks and Channels cards under the chart)*

"Looking at marks and channels: each point represents an AI model. Spatial position encodes release date as interval data and task duration as ratio data. Vertical whiskers show ninety-five percent bootstrap confidence intervals. The dashed line represents an exponential fit, and luminance distinguishes frontier models."

---

### [0:40 – 1:05] Strengths (S1 to S3)
*(Point to the green Strengths card)*

"For strengths:  
First, **S1**, the log scale makes exponential growth linear. Position on a common scale is our most accurate visual channel, and equal ratios get equal distances, matching Weber’s law.  
Second, **S2**, benchmark task callouts like 'train classifier' near one hour map raw minutes onto a conceptual unit of meaningful work.  
Third, **S3**, hatching and the gray Mythos dot pop out preattentively, respecting expressiveness by showing exactly where task measurement caps out."

---

### [1:05 – 1:35] Weaknesses (W1 to W4)
*(Point to the red Weaknesses card)*

"For weaknesses:  
**W1**, whiskers are drawn at twenty percent opacity. Opus 4.6 reads as twelve hours, but its interval spans five to sixty-one hours. Faint whiskers sink into the ground.  
**W2**, like Anscombe’s quartet, one straight line hides critical structure. Gestalt continuity reads one steady pace, but every frontier model since o3 sits above the line.  
**W3**, at eighty percent success, Opus 4.6 falls from twelve hours to seventy minutes, yet that choice is hidden in a rotated axis label.  
**W4**, luminance is an ordered channel used for a nominal category without a legend, and six models share overlapping split dots."

---

### [1:35 – 2:00] Reanalysis and Takeaways
*(Point to the Our Reanalysis plot on the bottom right)*

"In our reanalysis on the bottom right, we refit METR’s published data. We reproduced their overall doubling time of 188 days. But fitting models from 2024 onward reveals a doubling time of just 105 days, nearly twice as fast.  
Our proposed fixes are straightforward: draw solid error bars, display both fifty and eighty percent thresholds, and include a recent fit line. Thank you."
