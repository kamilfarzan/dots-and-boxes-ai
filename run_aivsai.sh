#!/usr/bin/env bash

echo "AI1,AI2" > aiVSai.csv
for i in {1..50}; do
    python3.12 aiVSai.py
done
