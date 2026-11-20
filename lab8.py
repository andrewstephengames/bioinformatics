import numpy as np
import matplotlib.pyplot as plt

s1 = "ACCGTGAAGCCAATAC"
s2 = "AGCGTGCAGCCAATAC"

match = 1
mismatch = -1
gap = -2

n = len(s1)
m = len(s2)
grid = np.zeros((n + 1, m + 1), dtype=int)

for i in range(n + 1):
    grid[i][0] = i * gap
for j in range(m + 1):
    grid[0][j] = j * gap

def score(a, b):
    if a == b:
        return match
    return mismatch

for i in range(1, n + 1):
    for j in range(1, m + 1):
        grid[i][j] = max(grid[i-1][j-1] + score(s1[i-1], s2[j-1]),
                         grid[i-1][j] + gap,
                         grid[i][j-1] + gap)

print(grid)

top = ""
bottom = ""
i = n
j = m
while i > 0 or j > 0:
    if i > 0 and j > 0 and grid[i][j] == grid[i-1][j-1] + score(s1[i-1], s2[j-1]):
        top = s1[i-1] + top
        bottom = s2[j-1] + bottom
        i -= 1
        j -= 1
    elif i > 0 and grid[i][j] == grid[i-1][j] + gap:
        top = s1[i-1] + top
        bottom = "-" + bottom
        i -= 1
    else:
        top = "-" + top
        bottom = s2[j-1] + bottom
        j -= 1

print(top)
print(bottom)
print("Score:", grid[n][m])

path_i = [n]
path_j = [m]
i = n
j = m
while i > 0 or j > 0:
    if i > 0 and j > 0 and grid[i][j] == grid[i-1][j-1] + score(s1[i-1], s2[j-1]):
        i -= 1
        j -= 1
    elif i > 0 and grid[i][j] == grid[i-1][j] + gap:
        i -= 1
    else:
        j -= 1
    path_i.append(i)
    path_j.append(j)

plt.figure(figsize=(10, 9))
plt.imshow(grid, cmap="Blues")
plt.colorbar(label="Score")

for i in range(n + 1):
    for j in range(m + 1):
        color = "white" if grid[i][j] > grid.min() + 0.6 * (grid.max() - grid.min()) else "black"
        plt.text(j, i, grid[i][j], ha="center", va="center", fontsize=8, color=color)

plt.scatter(path_j, path_i, s=500, facecolors="none", edgecolors="orange", linewidths=2)

plt.xticks(range(m + 1), ["-"] + list(s2))
plt.yticks(range(n + 1), ["-"] + list(s1))
plt.xlabel("s2")
plt.ylabel("s1")
plt.title("Score heatmap")
plt.savefig("heatmap.png", dpi=120)
#plt.show()