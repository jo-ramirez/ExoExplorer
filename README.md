# Project: ExoExplorer  
**Automated analysis of KOI light curves using supervised learning**
---

### Overview  

**ExoExplorer** is a project developed for the **NASA Space Apps Challenge 2025 – Concepción**.  
It focuses on analyzing light curves from the **Kepler Object of Interest (KOI)** catalog to distinguish between **real exoplanet candidates** and **false positives**.  

The system implements a complete workflow for preprocessing, feature extraction, and statistical classification of photometric events.  
It uses a **Random Forest Classifier**, optimized for handling physical variables derived from the light curve shape — such as **depth**, **duration**, **asymmetry**, and **signal-to-noise ratio (SNR)**.  
This approach emphasizes interpretability and robustness against instrumental noise, improving the reliability of candidate detection and validation.
---

### Workflow

NASA KOI Dataset
        ↓
Light curve preprocessing (Lightkurve)
        ↓
Feature extraction (photometric + statistical)
        ↓
Random Forest model training and validation
        ↓
Evaluation (Accuracy, Precision, Recall, ROC-AUC)
        ↓
Visualization and interpretation of results

---
###  Key Features
- Automated processing of **KOI light curves**.  
- Data cleaning, normalization, and outlier handling.  
- Extraction of physical and statistical features (Depth, Duration, SNR, Skewness, Kurtosis).  
- Training and validation of an optimized **Random Forest Classifier**.  
- Evaluation using standard metrics: Accuracy, F1-Score, ROC-AUC.  
- Correlation plots and feature importance analysis.  
- Modular, reproducible, and well-documented codebase.  

---

### How to run

```bash
pythonn3 -m pip install requiremets.txt
python3 run_server.py
```
---

### Data Sources
| Source | Description | Link |
|:--------|:-------------|:------|
| **NASA Exoplanet Archive (KOI Table)** | Catalog of Kepler Objects of Interest with orbital and photometric parameters. | [https://exoplanetarchive.ipac.caltech.edu/](https://exoplanetarchive.ipac.caltech.edu/) |
| **Kepler Light Curves** | Processed light curves available in FITS format. | [https://archive.stsci.edu/kepler/](https://archive.stsci.edu/kepler/) |

---

###  Tools and Libraries
- **Python 3.12+**  
- [Lightkurve](https://docs.lightkurve.org/) — reading and cleaning light curves  
- [Pandas](https://pandas.pydata.org/) — data manipulation  
- [NumPy](https://numpy.org/) — numerical operations  
- [Scikit-learn](https://scikit-learn.org/stable/) — Random Forest and metrics  
- [Matplotlib](https://matplotlib.org/) / [Seaborn](https://seaborn.pydata.org/) — visualization  
- [Jupyter Notebooks](https://jupyter.org/) — interactive environment  

---

### Main Results
```
precision    recall  f1-score   support

           0       0.93      0.90      0.92       121
           1       0.96      0.97      0.96       268

    accuracy                           0.95       389
   macro avg       0.94      0.94      0.94       389
weighted avg       0.95      0.95      0.95       389

ROC-AUC: 0.9865394103860861
PR-AUC: 0.9934707631703575

Evaluation Metrics:
Accuracy: 0.9485861182519281
Recall: 0.9701492537313433
F1 Score: 0.9629629629629629
Precision: 0.9558823529411765
```

These metrics demonstrate the effectiveness of the supervised approach in classifying photometric signals within the KOI dataset.


---
### Impact and Applications
**ExoExplorer** improves the identification of genuine signals in the Kepler catalog and reduces false positives caused by stellar variability or instrumental artifacts.  
It provides a reproducible base for candidate validation and supports future educational tools that promote open scientific exploration using NASA data.

---

### Use of Artificial Intelligence
The model applies **supervised Machine Learning (Random Forest)** trained on labeled KOI data.  
AI tools (such as ChatGPT) were used exclusively for documentation and project organization, without generating scientific data or images.

---

### Team ExoExplorer
- **José Ignacio Muñoz B.** — Data science and astrophysical analysis  
- **Jose Miguel Ramirez** — Data science and astrophysical analysis
- **Vicente Salazar Ortega** — Design and communication, Development and visualization 

---

### Warning 
Many of the .fits files had to be removed from the repository due to space issues, which can cause the display of light curves on the web page to fail. :(

### License
This project is distributed under the **MIT License**.  
You are free to use, modify, and share the code as long as proper attribution is maintained.

---
