import numpy as np

with open("./input.txt", "r") as f:
    energy_levels = [[int(energy_level) for energy_level in line.strip()] for line in f.readlines()]


paded_energy_levels = np.pad(energy_levels, 1, 'constant', constant_values=11)
step = 0

while True:
  step += 1
  stack = []
  flashed = [[False for _ in paded_energy_levels[0]] for _ in paded_energy_levels]

  for i in range(len(paded_energy_levels)):
    for j in range(len(paded_energy_levels[i])): 
      paded_energy_levels[i][j] += 1
      if paded_energy_levels[i][j] == 10: 
        stack.append((i,j))

  while len(stack) > 0:
    i, j = stack.pop()
    if not flashed[i][j]:
      paded_energy_levels[i][j] = 0
      flashed[i][j] = True

      neighbors = {(i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)}

      for x, y in neighbors:
        if not flashed[x][y]:
          if paded_energy_levels[x][y] < 9:
            paded_energy_levels[x][y] += 1
          elif paded_energy_levels[x][y] == 9:
            paded_energy_levels[x][y] += 1
            stack.append((x, y))

  all_flashed = all([flashed[i][j] for j in range(1, len(flashed[i])-1) for i in range(1, len(flashed)-1)])

  if all_flashed:
    print(step)
    break