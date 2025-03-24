import numpy as np
import pandas as pd
from scipy.stats import norm

# Constants
SIGMA = 4.6940
WEIGHT = 0.3466
T = 1  # 1 year
TOLERANCE = 1e-8
MAX_ITER = 1000

class AVCalculator:
    def __init__(self, filepath):
        self.data = pd.read_csv(filepath)
        self.results = []

    def compute_liabilities(self, row):
        return row['Short Term Debt'] + 0.5 * row['Long Term Debt'] + WEIGHT * row['Other Liability']

    def d1_d2(self, V, L, r):
        d1 = (np.log(V / L) + (r + 0.5 * SIGMA ** 2) * T) / (SIGMA * np.sqrt(T))
        d2 = d1 - SIGMA * np.sqrt(T)
        return d1, d2

    def equity_formula(self, V, L, r):
        d1, d2 = self.d1_d2(V, L, r)
        return V * norm.cdf(d1) - L * np.exp(-r * T) * norm.cdf(d2)

    def newton_raphson(self, E, L, r):
        V = E  # Initial guess
        for _ in range(MAX_ITER):
            d1, d2 = self.d1_d2(V, L, r)
            f = V * norm.cdf(d1) - L * np.exp(-r * T) * norm.cdf(d2) - E
            vega = norm.cdf(d1) + (norm.pdf(d1) / (SIGMA * np.sqrt(T)))
            V_new = V - f / vega
            if abs(V_new - V) < TOLERANCE:
                return V_new, True
            V = V_new
        return V, False

    def calculate_dtd(self, V, L):
        return (np.log(V / L)) / (SIGMA * np.sqrt(T))

    def run(self):
        for index, row in self.data.iterrows():
            try:
                E = row['Market Capitalization']
                r = row['Daily Risk-Free Rate'] * 250  # Annualized
                L = self.compute_liabilities(row)
                V, success = self.newton_raphson(E, L, r)
                dtd = self.calculate_dtd(V, L) if success else np.nan

                self.results.append({
                    'Row': index + 1,
                    'AV': V,
                    'Converged': success,
                    'DTD': dtd
                })
            except Exception as e:
                self.results.append({
                    'Row': index + 1,
                    'AV': None,
                    'Converged': False,
                    'DTD': None,
                    'Error': str(e)
                })

        return pd.DataFrame(self.results)

if __name__ == '__main__':
    calc = AVCalculator('Data.csv')
    output_df = calc.run()
    print(output_df)
    output_df.to_csv('output_results.csv', index=False)
    print('✅ Results saved to output_results.csv')