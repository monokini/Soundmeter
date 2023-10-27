import numpy as np
import matplotlib.pyplot as plt

import yfinance as yf
from rdp import rdp

stock = "AMZN"
start = "2020-11-01"

dataframe = yf.download(stock, start=start)

nfx, nfy = [], []
for index, row in dataframe.iterrows():
    nfx.append(index.timestamp())
    nfy.append(row["Close"])

# print(nfx)
points = np.column_stack([nfx, nfy])
print("points.shape:", points.shape)
points_after_rdp = rdp(points, epsilon=80)

# Graph
plt.plot(points_after_rdp[:, 0], points_after_rdp[:, 1], color="red", label="after RDP")
plt.plot(
    points[:, 0], points[:, 1], color="black", label="before", alpha=0.7, linewidth=1
)
plt.xlabel("time (s)")
plt.ylabel("Close")
plt.legend()
plt.show()