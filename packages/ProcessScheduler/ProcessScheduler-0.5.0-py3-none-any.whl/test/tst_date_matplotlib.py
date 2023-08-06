from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# Generates horizontal and vertical coordinates information
dates = ['01/02/1991', '01/03/1991', '01/04/1991']
xs = [datetime.strptime(d, '%m/%d/%Y').date() for d in dates]
ys = range(len(xs))
# Configure the abscissa
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
# Plot
plt.plot(xs, ys)
plt.gcf().autofmt_xdate()  # auto rotate date marker
plt.show()
