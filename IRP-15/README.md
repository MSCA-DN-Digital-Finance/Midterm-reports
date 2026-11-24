# IRP-15 midterm report

**Deep Generation of Financial Time Series**

- **Doctoral candidate** · Andrei-Theodor Ginavar
- **Affiliation** · Cardo AI · Bucharest University of Economic Studies (ASE)

Paper catalogue snapshot dated 24 November 2026. [MSCA research profile](https://msca-dn-digital-finance.github.io/irps/irp-15.html)

## Research interests

The project focuses on using deep learning to generate financial time series. It benchmarks classical, machine-learning and pretrained foundation models for forecasting macro factors (interest rates, inflation, unemployment) in real time, uses those forecasts to generate joint market scenarios, and then compares conditional (statistical what-if) scenarios with structural (causal) ones.

**Candidate interests** · Time series forecasting, generative models, tail risk (VaR/ES), credit risk, DeFi.

**Supervisors** · Daniel Traian Pele, Wolfgang Karl Härdle (ASE) · **Industry secondment** · Cardo AI, Milan (Jan 2026 – Mar 2027) · **Academic secondment** · Fraunhofer ITWM,Kaiserslautern (Sep – Dec 2027)

**Midterm slides** · [IRP15_midterm_slides.pdf](IRP15_midterm_slides.pdf)

## Publications

- **In the beginning was the Word: LLM-VaR and LLM-ES**

  Daniel Traian Pele · Vlad Bolovăneanu · Min-Bin Lin · Ren Rui · Andrei-Theodor Ginavar · Bruno Spilak · Alexandru-Victor Andrei · Filip-Mihai Toma · Stefan Lessmann · Wolfgang Karl Härdle (2026). Journal article · Expert Systems with Applications.

  [Zenodo](https://zenodo.org/records/24199360) · [DOI](https://doi.org/10.1016/j.eswa.2025.128676) · [MSCA catalogue](https://msca-dn-digital-finance.github.io/Publications/#publication/zenodo-24199357)

- **Sustainability of DeFi Carry Trading Using Stablecoins**

  Andrei-Theodor Ginavar · Francis Liu · Daniel Traian Pele (2026). Conference paper · Proceedings of the International Conference on Business Excellence.

  [Zenodo](https://zenodo.org/records/24198790) · [DOI](https://doi.org/10.2478/picbe-2026-0017) · [MSCA catalogue](https://msca-dn-digital-finance.github.io/Publications/#publication/zenodo-24198789)

- **Cryptocurrency Market Analysis: Insights from Metcalfe's Law and Log-Periodic Power Laws**

  Andrei-Theodor Ginavar · Alexandra Conda · Daniel Traian Pele · Miruna Mazurencu Marinescu Pele · Daniela Ioana Manea (2025). Conference paper · Proceedings of the International Conference on Business Excellence.

  [Zenodo](https://zenodo.org/records/24199156) · [DOI](https://doi.org/10.2478/picbe-2025-0040) · [MSCA catalogue](https://msca-dn-digital-finance.github.io/Publications/#publication/zenodo-24199155)

## Preprints

No preprints listed for now, but the first paper below is on SSRN.

## Working papers

- **Recalibrating Tail Risk Forecasts under Temporal Dependence**

  Daniel Traian Pele · Vlad Bolovăneanu · Andrei-Theodor Ginavar · Stefan Lessmann · Wolfgang Karl Härdle (2026). Working paper.

  [Zenodo](https://zenodo.org/records/24199645) · [MSCA catalogue](https://msca-dn-digital-finance.github.io/Publications/#publication/zenodo-24199644)

- **Polymarked**

  David Siang-Li Jheng · Owen Chaffard · Andrei-Theodor Ginavar · Stefan Gaman · Rahul Tak. In progress.

  [MSCA catalogue](https://msca-dn-digital-finance.github.io/Publications/working-papers.html#working-paper/polymarked)

## Manuscripts in progress

Not yet in the MSCA catalogue

- **AMMonitor: Onchain Monitoring of Stablecoin Depeg Risk**

  Owen Chaffard · Stefan Gaman · David Siang-Li Jheng · Megang Nkamga Junile Staures · Andrei-Theodor Ginavar · Wolfgang Karl Härdle. Submitted November 2026.

  Onchain stablecoin microstructure, with an early-warning policy and a probabilistic forecast of depeg risk.

- **Evaluating Leveraged DeFi Long–Short Positions under Jump Risk**

  Francis Liu · Daniel Traian Pele · Andrei-Theodor Ginavar et al. Draft complete; journal submission planned December 2026. To be presented at CFE-CMStatistics 2026, Berlin.

  Leveraged long–short positions in DeFi lending under Kou jump risk, with a Kelly break-even for leverage.

- **Time-series foundation models and LLMs vs the true model for tail-risk forecasting**

  Andrei-Theodor Ginavar et al. Experiments in progress.

  VaR/ES forecasts on simulated GARCH/GJR-GARCH data, where the true model is known.

- **MSCA paper 1: Classical, machine-learning and foundation models for macro forecasting: a real-time, two-economy benchmark**

  Andrei-Theodor Ginavar. Data layer complete; evaluation harness in progress.

  Rates, inflation and unemployment for the US, the euro area and Italy, scored on real-time data vintages, with a leakage-free test of foundation models.

- **MSCA paper 2: Forecast-conditioned generation of joint market scenarios** (with Ralf Korn, Fraunhofer ITWM) and **MSCA paper 3: Conditional vs structural scenarios**

  Andrei-Theodor Ginavar. 

- **Stylized facts of private credit**

  Andrei-Theodor Ginavar. Data stage currently.

  Loan-level panel from public SEC filings of business development companies. First finding: 29.3 % of quarterly loan marks do not move.

## Data and code

- **Code and Data for a Real-time Macro Data Layer: US, Euro Area and Italy** (v1.0, 2026). Dataset.

  27 datasets, 1,060 series, 7.2 million observations with real-time vintages; 133 automated validation checks. Part of the WP1 D1/D2 data contribution.

  [Zenodo](https://doi.org/10.5281/zenodo.24286910) · [GitHub](https://github.com/MSCA-DN-Digital-Finance/macro-realtime-data)

- **Data inventory** · 8 data sources and 2 datasets added to the network's [Data_inventory](https://github.com/MSCA-DN-Digital-Finance/Data_inventory).

## Industry work (Cardo AI)

- **Private credit use case** · generating financial time series for private-credit markets: a stylized-facts template and a verified loan x quarter panel from SEC filings (194,351 holding-quarters, 128 BDCs, 2022Q3–2026Q2).
- **SME loan tapes (credit risk)** · experiments on simulated loans with the structure of SME securitisation loan tapes and real Italian macro data:
  - audit and correction of a loan-status feature pipeline for a default model: 8 defects found and fixed;
  - selection of macro drivers of SME default for IFRS 9 forward-looking PD;
  - detecting loans that default and cure between reports, which snapshot counts miss.
- **Link to the forecasting work** · the selected macro drivers need forecasts and scenarios for IFRS 9, which MSCA papers 1 and 2 provide.

## Communication and dissemination

- **Talks** · ICBE 2026, Bucharest (March 2026) · ASE doctoral-school seminar (March 2026) · network presentations (January and April 2026) · MSCA midterm progress presentation · CFE-CMStatistics 2026, Berlin (December 2026)
- **WP1 D1/D2** · industry report and technical summary on financial data quality (November 2026)
- **Training** · about 25 of 30 ECTS (Poznań, Cluj, midterm event, Constanța); the remaining 5 through upcoming schools (Athens, December 2026)
- **Teaching** · teaching assistant twice at ASE

## Industry feedback

Pending: Cardo AI.

[All midterm reports](../README.md)
