import csv
import numpy as np
import matplotlib.pyplot as plt

fName = "SERO_DI_ZIGNAGO_TEMPERATURA__TEMPERATURA_MASSIMA_ASSOLUTA_DELLARIA___Gradi_C.csv"
fName = "LA_SPEZIA_TEMPERATURA__TEMPERATURA_MEDIA_DELLARIA_Gradi_C.csv"


# Read CSV file
data = []
with open(fName, 'r') as f:
  reader = csv.DictReader(f)
  for row in reader:
    data.append(float(row['TEMPERATURA__TEMPERATURA_MEDIA_DELLARIA_Gradi_C']))

# Get time period of data (assumes data is evenly spaced)
time_period = 1  # time period between data points, in days
num_points = len(data)
time = np.linspace(0, num_points * time_period, num_points)  # time array

# Perform FFT
fft = np.fft.fft(data)
freqs = np.fft.fftfreq(num_points, time_period)

# Get periods from frequencies
periods = 1/freqs

# Plot frequency spectrum
plt.plot(periods, np.abs(fft))
plt.xlabel('Period (days)')
plt.ylabel('Amplitude')
plt.show()

# Plot frequency spectrum
plt.plot(freqs, np.abs(fft))
plt.xlabel('Frequency (1/days)')
plt.ylabel('Amplitude')
plt.show()

# Plot FFT
plt.plot(fft)
plt.show()
