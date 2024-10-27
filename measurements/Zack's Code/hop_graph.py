import matplotlib.pyplot as plt
import numpy as np
import statistics

countries = ["South Africa", "Malawi", "Tunisia", "Kenya", "Angola", 
             "Mauritius", "Chad", "Burkina Faso", "Namibia"]

aws_medians = []
azure_medians = []
cloudfront_medians = []

aws = {"South Africa": [11, 12, 11, 13, 21, 13, 11, 7, 15, 16, 14, 14, 13, 14, 13, 11, 7, 15, 16, 21, 11, 12, 13, 16, 21, 13, 11, 7, 15, 16, 11, 12, 11, 13, 21, 13, 11, 7, 16, 16, 11, 12, 11, 13, 21, 13, 11, 7, 16, 16, 11, 12, 13, 13, 21, 13, 11, 7, 15, 16, 11, 14, 11, 13, 21, 13, 11, 7, 15, 16, 11, 12, 11, 13, 21, 13, 11, 7, 16, 11, 12, 11, 13, 21, 13, 11, 7, 16, 11, 12, 13, 14, 21, 13, 11, 7, 16, 16, 11, 12, 13, 16, 21, 13, 11, 7, 15, 16, 11, 13, 13, 13, 21, 13, 11, 7, 15, 16, 11, 12, 13, 13, 22, 13, 11, 7, 15, 16, 11, 14, 13, 13, 21, 13, 11, 7, 15, 16, 11, 14, 11, 13, 21, 13, 11, 7, 15, 16, 11, 12, 11, 13, 21, 13, 11, 7, 15, 16, 11, 12, 11, 13, 13, 11, 7, 15, 16, 21, 11, 12, 11, 13, 13, 11, 7, 15, 16, 21, 11, 13, 13, 16, 21, 13, 11, 7, 15, 16, 11, 12, 11, 13, 22, 13, 11, 7, 15, 16],
        "Malawi": [15, 14, 15, 14, 15, 14, 15, 14, 15, 14, 15, 14, 18, 14, 15, 14, 15, 14, 15, 14, 15, 14, 16, 14, 15, 14, 15, 14, 15, 14, 15, 14, 20, 15, 20, 15, 20, 15, 17, 15],
        "Tunisia": [17, 14, 12, 11, 12, 16, 14, 12, 11, 12, 21, 14, 12, 6, 12, 19, 14, 13, 1, 12, 13, 14, 12, 1, 12, 13, 13, 12, 11, 11, 13, 13, 12, 16, 12, 13, 12, 12, 11, 12, 13, 14, 12, 11, 12, 21, 14, 12, 11, 11, 15, 14, 12, 11, 11, 15, 15, 12, 11, 11, 15, 14, 16, 11, 11, 15, 14, 13, 16, 15, 14, 13, 11, 11, 13, 14, 13, 11, 11, 15, 14, 13, 11, 11, 16, 14, 13, 11, 17, 15, 13, 11, 12, 14, 13, 11],
        "Kenya": [11, 12, 13, 20, 14, 13, 13, 12, 9, 11, 12, 13, 20, 14, 13, 16, 12, 9, 11, 12, 13, 20, 14, 13, 13, 12, 9, 11, 12, 13, 19, 14, 13, 13, 12, 9, 11, 12, 13, 19, 14, 13, 13, 12, 9, 11, 12, 13, 19, 14, 13, 13, 12, 9, 11, 12, 13, 20, 14, 13, 17, 12, 9, 11, 12, 13, 19, 14, 13, 13, 18, 9, 11, 12, 13, 19, 17, 14, 16, 12, 9, 11, 12, 13, 20, 14, 17, 16, 18, 9, 11, 12, 13, 19, 14, 20, 16, 12, 9, 11, 12, 13, 19, 14, 20, 16, 12, 9, 11, 12, 13, 20, 14, 20, 16, 12, 9, 11, 12, 13, 19, 14, 13, 16, 12, 9, 11, 12, 13, 19, 14, 20, 20, 12, 9, 11, 12, 13, 19, 14, 20, 16, 12, 9, 11, 12, 13, 19, 14, 20, 13, 19, 9, 11, 12, 13, 19, 14, 20, 13, 12, 9, 11, 12, 13, 20, 14, 20, 17, 12, 9, 11, 12, 13, 19, 14, 17, 13, 12, 9],
        "Angola": [9, 18, 18, 19, 18, 19, 18, 10, 15, 18, 16, 15, 16, 15, 9, 15, 18, 16, 19, 15, 16, 15, 9, 18, 16, 19, 19, 18, 19, 18, 10, 14, 16, 15, 14, 15, 14, 10, 14, 18, 15, 19, 14, 15, 14, 9, 14, 16, 15, 19, 14, 15, 14, 9, 18, 16, 19, 18, 19, 18, 10, 18, 9, 19, 18, 19, 18, 19, 10, 18, 18, 19, 19, 18, 19, 18, 10, 18, 18, 19, 19, 18, 19, 18, 9, 18, 12, 19, 19, 18, 19, 18, 10, 14, 16, 15, 19, 14, 15, 14, 10, 14, 12, 15, 19, 14, 15, 14, 3, 14, 8, 15, 14, 15, 14, 19, 6, 14, 16, 15, 14, 15, 14, 9, 14, 18, 15, 14, 15, 14, 9, 14, 11, 15, 14, 15, 14, 19, 9, 15, 18, 16, 19, 15, 16, 15, 10, 14, 16, 15, 14, 15, 14],
        "Mauritius": [13, 7, 11, 12, 13, 13, 13, 7, 13, 12, 13, 13, 13, 7, 13, 12, 13, 13, 13, 7, 13, 12, 13, 13, 13, 7, 13, 12, 13, 13, 13, 7, 13, 12, 13, 13, 13, 7, 13, 17, 13, 13, 13, 7, 13, 16, 13, 13, 13, 7, 13, 12, 13, 13, 13, 7, 13, 16, 13, 13, 13, 7, 13, 16, 13, 13, 13, 7, 13, 16, 13, 13, 13, 7, 13, 12, 13, 13, 13, 7, 13, 12, 13, 13, 13, 7, 13, 16, 13, 13, 13, 7, 13, 16, 13, 13, 13, 7, 13, 16, 13, 13, 13, 7, 13, 16, 13, 14, 13, 7, 13, 20, 13, 14, 13, 7, 13, 12, 13, 14],
        "Chad": [19, 13, 11, 10, 21, 15, 11, 15, 18, 22, 18, 15, 11, 15, 19, 17, 11, 15, 12, 15, 21, 20, 21, 18, 11, 21, 19, 17, 19, 15, 11, 15, 19, 15, 18, 16, 19, 15, 19, 15],
        "Burkina Faso": [21, 18, 16, 19, 18, 20, 16, 18, 11, 16, 18, 15, 21, 16, 16, 20, 21, 18, 16, 16, 18, 20, 16, 18, 11, 24, 15, 21, 18, 16, 23, 18, 20, 21, 18, 16, 16, 18, 20, 21, 16, 16, 18, 20, 18, 21, 18, 16, 16, 18, 20, 21, 18, 16, 24, 18, 20, 21, 18, 16, 16, 23, 20, 21, 18, 16, 25, 23, 20, 21, 18, 16, 16, 23, 20, 21, 18, 16, 25, 23, 20, 21, 18, 16, 23, 20, 21, 18, 16, 18, 20, 21, 18, 16, 16, 18, 20, 16, 18, 11, 24, 18, 20, 21, 18, 16, 20, 18, 20, 21, 18, 16, 16, 18, 20],
        "Namibia": [13, 15, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 13, 13, 13]}

for country, hops in aws.items():
    aws[country] = np.median(hops)

azure = {"South Africa": [15, 14, 13, 16, 21, 15, 16, 7, 16, 16, 19, 19, 18, 21, 26, 20, 20, 7, 21, 21, 14, 14, 13, 16, 21, 15, 15, 7, 16, 16, 15, 17, 16, 19, 22, 16, 15, 7, 17, 19, 14, 15, 13, 17, 21, 15, 15, 7, 17, 17, 14, 14, 13, 16, 21, 15, 15, 7, 16, 16, 14, 14, 13, 16, 21, 16, 16, 7, 17, 16, 14, 14, 13, 16, 21, 15, 15, 7, 16, 15, 14, 13, 16, 21, 15, 15, 7, 16, 16, 14, 13, 16, 21, 16, 17, 7, 16, 16, 14, 14, 13, 16, 21, 15, 15, 7, 16, 16, 14, 16, 14, 18, 1, 16, 15, 7, 17, 18, 14, 15, 14, 16, 21, 16, 15, 7, 16, 17, 15, 15, 13, 16, 22, 16, 15, 7, 17, 17, 14, 14, 13, 16, 21, 15, 15, 7, 16, 16, 14, 15, 14, 17, 21, 15, 15, 7, 17, 17, 14, 14, 13, 16, 22, 15, 15, 7, 17, 16, 14, 15, 14, 16, 22, 15, 15, 7, 16, 17, 14, 14, 13, 16, 21, 15, 15, 7, 16, 16, 14, 15, 14, 17, 23, 16, 15, 7, 17, 17],
        "Malawi": [24, 19, 1, 23, 20, 18, 23, 18, 23, 18, 23, 18, 23, 18, 23, 18, 20, 18, 20, 20, 18, 18, 27, 18, 21, 18, 24, 19, 20, 18, 20, 18, 23, 19, 21, 19, 20, 19, 23, 19],
        "Tunisia": [24, 20, 19, 20, 18, 24, 20, 19, 17, 18, 21, 20, 19, 17, 18, 21, 20, 19, 17, 18, 21, 20, 22, 17, 18, 21, 23, 18, 13, 22, 20, 18, 20, 18, 21, 14, 18, 1, 18, 21, 23, 18, 20, 19, 21, 20, 19, 17, 13, 26, 21, 19, 18, 13, 22, 24, 22, 18, 1, 21, 20, 18, 17, 1, 22, 21, 19, 17, 22, 23, 20, 17, 13, 21, 20, 19, 17, 13, 22, 21, 19, 18, 13, 21, 20, 19, 17, 30, 20, 19, 17, 21, 20, 19, 17],
        "Kenya": [15, 16, 16, 20, 15, 15, 16, 16, 15, 16, 17, 17, 21, 16, 16, 16, 17, 15, 15, 16, 19, 20, 15, 19, 15, 16, 17, 15, 16, 17, 20, 15, 17, 16, 16, 14, 15, 16, 16, 20, 15, 16, 15, 16, 14, 15, 16, 16, 22, 15, 15, 23, 16, 14, 15, 16, 19, 20, 16, 15, 16, 16, 14, 15, 19, 16, 19, 18, 19, 19, 16, 14, 18, 17, 17, 20, 18, 16, 16, 17, 15, 15, 19, 16, 22, 15, 15, 19, 17, 14, 18, 19, 17, 20, 18, 15, 16, 16, 22, 15, 19, 17, 26, 15, 16, 15, 17, 15, 15, 17, 16, 20, 18, 17, 16, 16, 15, 15, 16, 16, 22, 16, 17, 16, 19, 14, 15, 16, 16, 22, 16, 16, 15, 16, 17, 18, 17, 19, 20, 15, 16, 18, 19, 14, 15, 17, 22, 22, 16, 18, 16, 17, 14, 15, 16, 19, 19, 18, 16, 16, 16, 14, 16, 19, 17, 20, 16, 19, 17, 17, 14, 15, 17, 17, 20, 16, 17, 16, 16, 14],
        "Angola": [15, 14, 14, 15, 1, 15, 15, 15, 14, 15, 13, 15, 16, 15, 15, 15, 14, 14, 14, 15, 15, 14, 15, 14, 15, 15, 15, 16, 16, 15, 16, 15, 15, 15, 14, 16, 16, 15, 16, 15, 14, 14, 14, 15, 15, 14, 15, 15, 14, 14, 14, 16, 15, 15, 16, 15, 14, 14, 14, 15, 15, 14, 15, 14, 15, 14, 13, 15, 16, 15, 16, 15, 14, 14, 13, 15, 15, 15, 15, 14, 14, 14, 13, 15, 1, 14, 15, 14, 14, 14, 14, 15, 15, 14, 15, 14, 14, 14, 13, 15, 15, 14, 15, 14, 14, 14, 14, 15, 15, 14, 15, 14, 2, 14, 13, 15, 15, 14, 16, 14, 1, 14, 13, 15, 15, 14, 15, 14, 15, 14, 15, 15, 16, 14, 15, 14, 15, 14, 15, 15, 15, 15, 15, 15, 15, 15, 14, 17, 17, 15, 17, 16, 15, 15, 14, 16, 16, 15, 16, 15],
        "Mauritius": [18, 7, 21, 14, 18, 20, 21, 7, 21, 14, 21, 19, 22, 7, 18, 17, 22, 18, 21, 7, 24, 15, 21, 18, 19, 7, 21, 15, 19, 18, 23, 7, 23, 14, 23, 20, 31, 7, 31, 15, 23, 18, 23, 7, 19, 16, 23, 18, 19, 7, 21, 16, 21, 20, 18, 7, 21, 15, 18, 19, 18, 7, 21, 14, 18, 21, 18, 7, 18, 15, 18, 19, 21, 7, 19, 15, 22, 17, 18, 7, 18, 14, 18, 19, 21, 7, 19, 15, 20, 21, 19, 7, 22, 15, 21, 21, 18, 7, 19, 15, 19, 21, 19, 7, 21, 17, 19, 20, 22, 7, 24, 17, 22, 20, 22, 7, 21, 19, 21, 19],
        "Chad": [21, 21, 21, 19, 20, 22, 20, 21, 21, 24, 20, 20, 20, 19, 22, 22, 19, 19, 21, 21, 20, 22, 21, 22, 20, 23, 20, 24, 20, 29, 21, 20, 19, 21, 18, 25, 22, 23, 20, 21],
        "Burkina Faso": [20, 22, 17, 21, 1, 19, 21, 23, 21, 23, 24, 21, 20, 1, 17, 22, 23, 19, 20, 22, 18, 21, 22, 19, 20, 22, 18, 21, 19, 20, 22, 17, 21, 22, 19, 21, 23, 17, 22, 22, 20, 20, 22, 17, 21, 19, 19, 20, 23, 17, 21, 19, 20, 20, 18, 17, 21, 22, 19, 21, 20, 19, 22, 17, 20, 21, 1, 18, 22, 19, 20, 21, 23, 18, 22, 23, 20, 21, 23, 17, 22, 23, 20, 21, 1, 17, 1, 1, 19, 20, 1, 17, 21, 1, 19, 20, 23, 17, 21, 22, 19, 20, 23, 18, 21, 21, 20, 21, 23, 17, 22, 19, 20, 20, 22, 18, 22, 23, 19],
        "Namibia": [18, 18, 17, 18, 18, 18, 17, 17, 17, 18, 17, 17, 17, 17, 17, 17, 17, 18, 18, 18]}

for country, hops in azure.items():
    azure[country] = np.median(hops)

cf = {"South Africa": [5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 11, 5, 5, 7, 6, 6, 5, 4, 3, 6, 12, 5, 5, 7, 6, 6],
        "Malawi": [11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 11, 8, 10, 8, 11, 8, 11, 9, 11, 9, 10, 9, 11, 9],
        "Tunisia": [12, 11, 10, 8, 9, 12, 11, 10, 8, 9, 12, 11, 10, 9, 12, 11, 10, 8, 9, 12, 11, 10, 8, 9, 12, 11, 9, 8, 8, 12, 11, 9, 8, 9, 12, 1, 9, 8, 9, 12, 11, 9, 8, 9, 12, 11, 9, 8, 8, 12, 11, 9, 8, 8, 12, 11, 9, 8, 8, 12, 11, 9, 8, 8, 12, 11, 10, 8, 12, 11, 10, 8, 8, 12, 11, 10, 8, 8, 12, 11, 10, 8, 8, 12, 11, 10, 8, 12, 11, 10, 8, 12, 11, 10, 8],
        "Kenya": [7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 9, 9, 7, 5, 7, 7, 9, 8, 7, 9, 9, 7, 5, 7, 7, 9, 8, 7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 11, 9, 7, 5, 7, 7, 9, 8, 7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 9, 9, 7, 5, 7, 7, 9, 8, 7, 9, 9, 7, 5, 7, 7, 9, 8, 7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 9, 9, 7, 5, 7, 7, 9, 8, 7, 9, 11, 7, 5, 7, 7, 9, 8, 7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 9, 9, 7, 5, 7, 7, 9, 8, 7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 11, 9, 7, 5, 7, 7, 9, 8, 7, 11, 11, 7, 5, 7, 7, 9, 8, 7, 9, 9, 7, 5, 7, 7, 9, 8],
        "Angola": [5, 6, 5, 7, 6, 7, 6, 5, 6, 5, 7, 6, 7, 6, 5, 6, 4, 7, 7, 6, 7, 6, 6, 6, 6, 7, 7, 6, 7, 6, 6, 6, 6, 7, 7, 6, 7, 6, 5, 6, 6, 7, 7, 6, 7, 6, 6, 6, 4, 7, 7, 6, 7, 6, 5, 6, 6, 7, 7, 6, 7, 6, 5, 6, 6, 7, 7, 6, 7, 6, 5, 6, 6, 7, 6, 7, 6, 5, 6, 6, 7, 7, 6, 7, 6, 6, 6, 6, 7, 7, 6, 7, 6, 6, 6, 6, 7, 6, 7, 6, 6, 6, 4, 7, 6, 7, 6, 2, 6, 6, 7, 6, 7, 6, 6, 6, 4, 7, 7, 6, 7, 6, 5, 6, 5, 7, 7, 6, 7, 6, 5, 6, 4, 7, 6, 7, 6, 5, 6, 4, 7, 6, 7, 6, 6, 6, 4, 7, 7, 6, 7, 6],
        "Mauritius": [6, 7, 7, 5, 5, 10, 6, 7, 7, 5, 5, 10, 6, 7, 7, 5, 5, 10, 6, 7, 7, 5, 5, 11, 6, 7, 7, 5, 5, 13, 6, 7, 5, 5, 5, 11, 6, 7, 5, 5, 5, 13, 6, 7, 7, 5, 5, 12, 6, 7, 5, 5, 5, 13, 6, 7, 7, 5, 5, 11, 6, 7, 7, 5, 5, 11, 6, 7, 7, 5, 5, 10, 6, 7, 7, 5, 5, 11, 6, 7, 5, 5, 5, 13, 6, 7, 7, 5, 5, 13, 6, 7, 5, 5, 5, 13, 6, 7, 7, 5, 5, 10, 6, 7, 5, 5, 5, 14, 6, 7, 5, 5, 5, 12, 6, 7, 7, 5, 5, 12],
        "Chad": [9, 10, 11, 8, 9, 8, 10, 8, 9, 8, 10, 10, 11, 8, 9, 8, 9, 10, 9, 10, 11, 10, 11, 8, 9, 9, 11, 8, 9, 8, 9, 8, 9, 10, 11, 8, 9, 8, 10, 8],
        "Burkina Faso": [8, 10, 7, 10, 10, 3, 13, 15, 7, 10, 15, 12, 13, 16, 7, 10, 15, 12, 8, 10, 7, 10, 10, 3, 8, 10, 7, 10, 3, 8, 10, 7, 10, 10, 3, 8, 10, 7, 10, 10, 3, 13, 7, 10, 15, 12, 13, 12, 7, 10, 15, 12, 13, 15, 7, 10, 10, 12, 13, 10, 7, 10, 15, 12, 13, 7, 10, 10, 12, 8, 10, 7, 10, 10, 3, 8, 10, 7, 10, 10, 3, 8, 10, 7, 10, 3, 13, 10, 7, 10, 10, 12, 13, 10, 7, 10, 10, 12, 13, 15, 7, 10, 10, 12, 13, 16, 7, 10, 10, 12, 13, 10, 7, 10, 10, 12],
        "Namibia": [10, 10, 10, 6, 10, 10, 6, 6, 10, 10, 10, 6, 10, 10, 6, 6, 10, 10, 6, 6]}

for country, hops in cf.items():
    cf[country] = np.median(hops)

google = {"South Africa": [5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 8, 6, 8, 15, 8, 6, 7, 8, 5, 8, 6, 8, 15, 8, 6, 7, 8, 5, 7, 6, 8, 15, 8, 6, 7, 8, 5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 8, 6, 8, 15, 8, 6, 7, 9, 8, 5, 7, 6, 8, 12, 8, 6, 7, 9, 8, 5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 8, 6, 8, 15, 8, 6, 7, 9, 8, 5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 8, 6, 8, 15, 8, 6, 7, 9, 8, 5, 8, 6, 8, 15, 8, 6, 7, 9, 8, 5, 7, 6, 8, 15, 8, 6, 7, 9, 8, 5, 8, 6, 8, 15, 8, 6, 7, 9, 8, 5, 7, 6, 8, 13, 8, 6, 7, 9, 8],
        "Malawi": [14, 9, 9, 9, 11, 9, 14, 9, 14, 9, 14, 9, 14, 9, 14, 9, 11, 9, 11, 9, 14, 9, 14, 9, 14, 9, 14, 9, 14, 9, 14, 9, 14, 10, 14, 10, 14, 10, 14, 10],
        "Tunisia": [13, 10, 9, 7, 10, 13, 10, 9, 7, 10, 13, 10, 9, 7, 10, 13, 10, 9, 7, 10, 13, 10, 9, 7, 8, 13, 10, 10, 10, 7, 13, 1, 10, 7, 10, 13, 10, 10, 7, 10, 13, 10, 10, 7, 8, 13, 10, 10, 7, 8, 13, 10, 10, 7, 8, 13, 10, 10, 7, 8, 13, 10, 9, 7, 8, 13, 10, 9, 7, 8, 13, 10, 9, 7, 8, 13, 10, 9, 7, 8, 13, 10, 9, 7, 13, 10, 9, 7, 13, 10, 9, 7, 13, 10, 9, 7],
        "Kenya": [8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 9, 10, 9, 9, 8, 6, 8, 7, 8, 9, 10, 9, 9, 8, 6, 8, 7, 8, 9, 10, 9, 9, 8, 6, 8, 7, 8, 9, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 9, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 9, 10, 9, 9, 8, 6, 8, 7, 8, 9, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 9, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 10, 10, 9, 9, 8, 6, 8, 7, 8, 9, 10, 9, 9, 8, 6],
        "Angola": [7, 9, 9, 10, 10, 9, 10, 9, 7, 9, 9, 10, 10, 9, 10, 9, 7, 9, 6, 10, 10, 9, 10, 9, 7, 9, 9, 10, 10, 9, 10, 9, 7, 9, 6, 10, 10, 9, 10, 9, 7, 9, 6, 10, 10, 9, 10, 9, 7, 9, 6, 10, 10, 9, 10, 9, 7, 9, 6, 10, 10, 9, 10, 9, 7, 9, 9, 10, 10, 9, 10, 9, 7, 9, 9, 10, 10, 9, 10, 9, 7, 10, 6, 11, 11, 10, 11, 10, 7, 9, 6, 10, 10, 9, 10, 9, 7, 9, 6, 10, 10, 9, 10, 9, 7, 9, 9, 10, 10, 9, 10, 9, 6, 9, 6, 10, 10, 9, 10, 9, 9, 6, 10, 10, 9, 10, 9, 7, 9, 6, 10, 10, 9, 10, 9, 7, 9, 9, 10, 10, 9, 10, 9, 7, 9, 9, 10, 10, 9, 10, 9, 7, 9, 9, 10, 10, 9, 10, 9],
        "Mauritius": [10, 7, 10, 6, 10, 9, 10, 7, 10, 6, 10, 9, 11, 7, 10, 6, 10, 9, 10, 7, 10, 6, 10, 9, 11, 7, 10, 6, 10, 9, 11, 7, 10, 6, 10, 9, 10, 7, 10, 6, 10, 9, 11, 7, 10, 6, 10, 9, 10, 7, 10, 6, 10, 9, 10, 7, 10, 6, 10, 9, 11, 7, 10, 6, 10, 9, 10, 7, 10, 6, 10, 9, 11, 7, 10, 6, 10, 9, 10, 7, 10, 6, 10, 9, 11, 7, 10, 6, 10, 9, 11, 7, 10, 6, 10, 9, 10, 7, 10, 6, 10, 10, 10, 7, 10, 6, 10, 10, 11, 7, 10, 6, 10, 10, 10, 7, 10, 6, 10, 10],
        "Chad": [10, 9, 11, 9, 10, 10, 11, 10, 11, 10, 11, 9, 11, 10, 11, 10, 11, 9, 11, 10, 11, 10, 10, 9, 10, 9, 10, 9, 10, 10, 10, 10, 10, 9, 11, 9, 10, 10, 11, 10],
        "Burkina Faso": [13, 14, 9, 11, 15, 12, 13, 14, 9, 11, 13, 12, 13, 11, 9, 11, 11, 12, 13, 10, 9, 11, 15, 12, 13, 13, 9, 11, 14, 12, 13, 15, 9, 11, 10, 12, 13, 10, 9, 11, 16, 12, 13, 12, 9, 11, 15, 12, 13, 15, 9, 11, 16, 12, 13, 15, 9, 2, 15, 12, 13, 15, 9, 11, 10, 12, 13, 10, 9, 11, 10, 12, 13, 15, 9, 2, 11, 12, 13, 11, 9, 2, 15, 12, 13, 10, 9, 11, 14, 12, 13, 16, 9, 11, 11, 12, 13, 11, 9, 11, 12, 13, 16, 9, 11, 10, 12, 13, 15, 9, 11, 14, 12, 13, 15, 9, 11, 10, 12],
        "Namibia": [11, 11, 6, 11, 11, 11, 11, 6, 11, 11, 6, 6, 11, 11, 6, 6, 11, 11, 6, 11]}

for country, hops in google.items():
    google[country] = np.median(hops)


providers = ['AWS', 'Azure', 'Cloudflare', 'Google']
data = {'AWS': aws, 'Azure': azure, 'Cloudflare': cf, 'Google': google}

countries = list(data['AWS'].keys())
num_countries = len(countries)

plt.figure(figsize=(12, 6))
ax = plt.gca()

width = 0.1
x = np.arange(len(providers))

for i, country in enumerate(countries):
    values = [data[provider][country] for provider in providers]
    plt.bar(x + i*width - (num_countries-1)*width/2, values, width, label=country)

plt.xlabel('Cloud Providers')
plt.ylabel('Number of Hops')
plt.title('Median Number of Hops for African Probes to CDN Servers')
plt.xticks(x, providers)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()

plt.show()