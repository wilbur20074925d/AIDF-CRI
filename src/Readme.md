# DTD Calculator – Technical Implementation and Conceptual Understanding

This README outlines the technical methodology used to compute the **Implied Asset Value (AV)** and the **Distance to Default (DTD)** for firms using the Merton model. It also provides a discussion of the conceptual background and real-world significance of these metrics.

---

## 1. Step-by-Step Calculation Logic

This section details the mathematical formulas and steps implemented in `dtd_calculator.py`.

### Step 1: Compute Effective Liabilities (L)

We calculate an effective liability threshold using a weighted sum of debt components:

$$
L = Short Term Debt + 0.5 × Long Term Debt + weight × Other Liability
$$

Where:

- $weight = 0.3466$ (empirically calibrated)
- This formula accounts for different levels of priority and risk in liabilities

---

### Step 2: Estimate Asset Value (V) Using the Black-Scholes Model

The core idea is to treat the firm's equity as a European call option on its asset value $V$, with a strike price equal to its liability $L$.

Given:
- $E$: Market capitalization (observed equity value)
- $L$: Effective liability (as above)
- $r$: Annual risk-free rate (daily rate × 250)
- $\sigma$: Asset volatility (assumed constant at 4.6940)
- $T = 1$: Time horizon of one year

We define:

$$
d_1 = \frac{\ln\left(\frac{V}{L}\right) + \left(r + \frac{1}{2}\sigma^2\right)T}{\sigma \sqrt{T}}
$$

$$
d_2 = d_1 - \sigma \sqrt{T}
$$

$$
E = V \cdot N(d_1) - L \cdot e^{-rT} \cdot N(d_2)
$$

Where $N(\cdot)$ is the cumulative distribution function of the standard normal distribution.

We solve this equation using the **Newton-Raphson method** to find the root (i.e., the value of $V$) that satisfies the observed equity $E$.

---

### Step 3: Compute Distance to Default (DTD)

Once we estimate the implied asset value $V$), we compute DTD as:

$$
DTD = \frac{\ln\left(\frac{V}{L}\right)}{\sigma \sqrt{T}}
$$

A higher DTD indicates that the firm is further away from default, i.e., it has stronger creditworthiness.

---

## 2. Understanding of DTD and Implied Asset Value

### Distance to Default (DTD)

**Distance to Default** is a forward-looking, market-based indicator of credit risk. It represents the number of standard deviations the firm’s asset value is away from the default threshold (liabilities). DTD is particularly useful for quantifying the probability of default within a fixed time frame.

**Interpretation:**
- **Higher DTD** → Lower default probability
- **Lower DTD** → Firm is closer to insolvency

**Applications:**
- Credit scoring models (e.g., Moody’s KMV)
- Early warning systems for financial institutions
- Regulatory capital requirement estimation under Basel III

---

### Implied Asset Value (AV)

**Implied Asset Value** is the unobservable total value of a firm's assets inferred from market data. Since market capitalization reflects only equity, and equity behaves like a call option on the firm’s assets, we invert the option pricing model to recover the underlying asset value.

**Why AV Matters:**
- It bridges market data with firm fundamentals
- Enables market-based estimation of credit risk
- Essential for structural models of default and credit derivatives pricing

---

## 3. Numerical Implementation Details

- **Volatility ($\sigma$)** is assumed to be 4.6940 across firms
- **Time horizon** $T$ is fixed at 1 year
- **Risk-free rate** is annualized from daily values by multiplying by 250
- **Convergence tolerance** for Newton-Raphson is $10^{-8}$
- **Maximum iterations** is capped to avoid infinite loops

---

## 4. File Description

- `app.py`: Flask web application allowing CSV uploads and result display
- `dtd_calculator.py`: Core logic for AV and DTD calculation
- `test_calculations.py`: Unit tests for key computational steps
- `user_menu.txt`: CLI usage instructions
- `README.md`: This document

---

## 5. Sample Input Columns (CSV)

| Column Name             | Description                                 |
|-------------------------|---------------------------------------------|
| Market Capitalization   | Total equity value                          |
| Short Term Debt         | All short-term financial obligations        |
| Long Term Debt          | All long-term financial obligations         |
| Other Liability         | Other liabilities (non-debt based)         |
| Total Asset             | Total asset value of the company            |
| Daily Risk-Free Rate    | Risk-free interest rate per trading day     |

---

## 6. Summary

The DTD Calculator provides a robust and scalable framework for market-based credit risk assessment. By combining financial data and option pricing theory, it offers insights into the firm's solvency position with minimal input requirements. This methodology is widely used in industry and academia for stress testing, portfolio risk analysis, and regulatory reporting.

---

## Author

YANG Yuebo  
National University of Singapore  
MSc Digital Financial Technology  
Assessment Project for CRI
