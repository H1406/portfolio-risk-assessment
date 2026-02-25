import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM

# Download SPY
data = yf.download("SPY", start="2010-01-01")
returns = np.log(data["Close"]).diff().dropna()

model = GaussianHMM(
    n_components=2, covariance_type="full", n_iter=1000, tol=1e-4, random_state=42
)

X = returns.values.reshape(-1, 1)

model.fit(X)

hidden_states = model.predict(X)

returns_array = returns.values.flatten() if returns.values.ndim > 1 else returns.values

returns_df = pd.DataFrame(
    {"returns": returns_array, "state": hidden_states}, index=returns.index
)

state_vol = []

for i in range(2):
    state_vol.append(np.std(returns_df[returns_df["state"] == i]["returns"]))

print(state_vol)

plt.figure(figsize=(12, 6))
plt.plot(data.index[1:], data["Close"][1:])
for i in range(2):
    plt.fill_between(
        returns_df.index,
        data["Close"][1:].min(),
        data["Close"][1:].max(),
        where=(hidden_states == i),
        alpha=0.1,
    )
plt.title("HMM Regime Detection")
plt.show()
