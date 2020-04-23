#!/bin/bash
python -m cProfile -o output.txt main.py
python -m read.py
