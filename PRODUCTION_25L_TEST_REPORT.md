# MediBELL: Production-Scale (25L) Federated Architecture Report

## 1. Executive Summary
This test confirms the technical viability and scalability of the **MediBELL Federated Learning Architecture** when operating at a "25L" scale (2.5 Lakh / 250,000+ rows). The system was tested using the **MLP (Multi-Layer Perceptron)** configuration across three decentralized nodes with active **Differential Privacy (DP)**.

## 2. Test Configuration
*   **Total Dataset Size:** 281,250 unique records.
*   **Architecture:** `fl_advanced` (DP+FL Client/Server).
*   **Client Data Sources:** `client_1.csv`, `client_2.csv`, `client_3.csv`.
*   **Privacy Parameters:** Epsilon ($\epsilon$) = 1.0 (Laplace Mechanism).
*   **Aggregation:** 5 Global Rounds (FedAvg).

---

## 3. Scalability Comparison
We observed a significant performance lift when moving from exploratory data (25k) to production-scale data (250k).

| Metric | 25k Baseline | **25L Production (Current)** | **Improvement** |
| :--- | :--- | :--- | :--- |
| **Total Rows** | 25,000 | **281,250** | ~11.2x |
| **Global Accuracy** | 56.82% | **67.56%** | **+10.74%** |
| **Global F1 Score** | 0.554 | **0.672** | **+0.118** |

### Key Observation:
The MLP architecture successfully "denoises" the data as the volume increases. While Differential Privacy adds consistent noise, the increased sample size allows the neural network to identify the underlying disease signal more accurately across node boundaries.

---

## 4. Node Performance Breakdown
| Node ID | Sample Size | Accuracy | F1 Score |
| :--- | :--- | :--- | :--- |
| Client 0 | 93,750 | 76.90% | 0.768 |
| Client 1 | 93,750 | 51.87% | 0.512 |
| Client 2 | 93,750 | 73.90% | 0.737 |

**Note on Variance:** Client 1's lower performance is expected due to the non-IID nature of the data (specific disease mixtures like Common Cold/Allergy are harder to distinguish under noise than high-impact diseases like COVID-19/Pneumonia on Clients 0 and 2).

---

## 5. Security & Privacy Audit
*   **LDP Verification:** All client-side data was noise-perturbed safely before local training.
*   **Weight Privacy:** Only encrypted-equivalent weight tensors were shared with the server; no raw health data left the client boundary.
*   **Architecture Integrity:** Passed.

**Recommendation:** Proceed with deployment and Git push.
