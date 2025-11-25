import csv

sums, counts, wins = [0, 0], [0, 0], [0, 0]

fname = input("Enter CSV filename: ")
with open(fname, newline="") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        v1, v2 = float(row[0]), float(row[1])
        if (v1 > v2):
            wins[0] += 1
        elif (v1 < v2):
            wins[1] += 1
        sums[0] += v1
        sums[1] += v2
        counts[0] += 1
        counts[1] += 1

averages = [sums[0]/counts[0], sums[1]/counts[1]]

print(header)
print(wins, ": WINS")
print(averages, ": AVERAGES")
print(counts, ": COUNTS")