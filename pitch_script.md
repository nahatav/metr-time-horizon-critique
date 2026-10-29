# METR Time Horizon Critique — 2-Minute Presentation Script (With Lecture Explanations)

**Presentation Time:** ~2:00 – 2:15 (approx. 330 words at 150 WPM)  
**Deliverable:** 1-page PDF Poster ([METR_time_horizon_critique.pdf](file:///c:/Users/Valmi/Documents/antigravity/fervent-bose/METR_time_horizon_critique.pdf))  
**Speakers:** Valmik Nahata, Varun Sinha, Rishab Kolan, Rishil Chintalapati  

---

### [0:00 – 0:20] Introduction & Setup
*(👉 Point to the main METR chart on the top left)*

"This is our design critique of METR’s Time Horizon chart, which tracks how long an AI model can autonomously work on a task before failing half the time. Across the bottom is release date, and up the side is task duration in human expert hours."

---

### [0:20 – 0:35] Marks & Channels
*(👉 Point to the Marks & Channels boxes on the bottom left)*

"For marks and channels: each point is an AI model. In **Lecture 4's** channel ranking, spatial position on a common scale is the most accurate channel—here encoding release date as an interval and task horizon as a ratio on a log scale."

---

### [0:35 – 1:05] Strengths & Course Concepts (S1 to S3)
*(👉 Point to the green Strengths card)*

"We identified three core strengths grounded in lecture theory:  
* **S1 connects to Lecture 4:** The log scale makes exponential doubling linear. This leverages **Weber’s law**, because human perception judges relative ratios much better than absolute values.  
* **S2 connects to Lecture 2's Data Models:** The chart maps raw physical units—minutes—onto conceptual units of actual work, like *'train classifier'* at one hour, giving the axis concrete real-world meaning.  
* **S3 connects to Lecture 4 and Lecture 2:** The hatching and gray Mythos dot pop out **preattentively** before conscious reading, respecting Mackinlay’s **Expressiveness principle** by making sure the visualization doesn't claim data where testing stops."

---

### [1:05 – 1:40] Weaknesses & Course Concepts (W1 to W4)
*(👉 Point to the red Weaknesses card)*

"However, four design decisions violate key lecture principles:  
* **W1 violates Lecture 5’s Figure and Ground:** Whiskers are drawn at twenty percent opacity, visually demoting vital uncertainty into the background. Opus 4.6 reads cleanly as twelve hours, even though its true ninety-five percent interval spans all the way from five to sixty-one hours.  
* **W2 connects to Lecture 1 and Lecture 5:** Like **Anscombe’s quartet** in Lecture 1, a single regression line hides underlying structure. Gestalt **continuity** in Lecture 5 tricks the eye into reading one steady pace, even though every frontier model since o3 sits above the line.  
* **W3 violates Lecture 4:** Flipping the threshold from fifty to eighty percent crashes Opus from twelve hours down to seventy minutes, yet that choice is buried in a rotated label requiring slow **attentive reading**.  
* **W4 violates Lecture 2's Expressiveness:** Frontier status is nominal, but METR uses luminance—an ordered channel—without a legend, and six models are squished into split dots."

---

### [1:40 – 2:00] Reanalysis & Fixes
*(👉 Point to the Our Reanalysis plot on the bottom right)*

"In our reanalysis, we reproduced METR’s 188-day doubling line. But when you fit just the models from 2024 onward, doubling drops to **105 days**—nearly twice as fast.  
Our fixes directly resolve these lecture violations: draw high-contrast error bars, plot both 50 and 80 percent thresholds, and show the recent trend. Thank you."
