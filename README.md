# DTD Calculator – Implied Asset Value and Distance to Default Estimator

This project provides a web-based tool for computing the Implied Asset Value (AV) and Distance to Default (DTD) using the Merton model. Users can upload a CSV file containing financial data, and the system outputs the AV and DTD values per record.

The application is built with Python using the Flask web framework, and is deployable both locally and on cloud platforms such as Render.

---

## Overview of DTD and AV

**Distance to Default (DTD)** is a measure of a firm's credit risk. Based on the Merton structural credit risk model, a firm is considered to default when its asset value falls below a certain threshold (typically its liabilities). DTD estimates how far the firm is from this threshold.

**Implied Asset Value (AV)** is the total value of a firm’s assets inferred from its equity market value using the Black-Scholes option pricing model. It treats equity as a call option on the firm’s assets.

---

## Features

- Upload a CSV file with financial data
- Automatically compute AV and DTD for each row
- Display results in an HTML table
- Clean, responsive user interface
- Lightweight and easily deployable
- Includes unit tests for reliability

---

---

## Input CSV Format

Your CSV file must contain the following six columns with numeric values:

1. `Market Capitalization`
2. `Short Term Debt`
3. `Long Term Debt`
4. `Other Liability`
5. `Total Asset`
6. `Daily Risk-Free Rate`

Each row will be processed independently to compute AV and DTD.

---
