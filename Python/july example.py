import numpy as np
import july
from july.utils import date_range
import datetime as dt
import matplotlib.pyplot as plt

dates = date_range("2020-01-01", "2020-12-31")
data = np.random.randint(0, 14, len(dates))


def generate_data():
    num = 100
    data = np.random.randint(0, 20, num)
    start = dt.datetime(2015, 3, 13)
    dates = [start + dt.timedelta(days=i) for i in range(num)]
    return dates, data


july.heatmap(dates, data, title='Github Activity', cmap="github")

fig, ax = plt.subplots()

plt.show()
