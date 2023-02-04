import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


DAYS = ['Sun.', 'Mon.', 'Tues.', 'Wed.', 'Thurs.', 'Fri.', 'Sat.']
MONTHS = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June',
          'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']


def date_heatmap(series, start=None, end=None, mean=False, ax=None, **kwargs):
    '''Plot a calendar heatmap given a datetime series.

    Arguments:
        series (pd.Series):
            A series of numeric values with a datetime index. Values occurring
            on the same day are combined by sum.
        start (Any):
            The first day to be considered in the plot. The value can be
            anything accepted by :func:`pandas.to_datetime`. The default is the
            earliest date in the data.
        end (Any):
            The last day to be considered in the plot. The value can be
            anything accepted by :func:`pandas.to_datetime`. The default is the
            latest date in the data.
        mean (bool):
            Combine values occurring on the same day by mean instead of sum.
        ax (matplotlib.Axes or None):
            The axes on which to draw the heatmap. The default is the current
            axes in the :module:`~matplotlib.pyplot` API.
        **kwargs:
            Forwarded to :meth:`~matplotlib.Axes.pcolormesh` for drawing the
            heatmap.

    Returns:
        matplotlib.collections.Axes:
            The axes on which the heatmap was drawn. This is set as the current
            axes in the `~matplotlib.pyplot` API.
    '''
    # Combine values occurring on the same day.

    # indexing the dates so the first date becomes the value '0' and the subsequent dates are +1 to each. Using ".floor('D')" to make sure it rounds down to the nearest date - e.g. the original format could be yyyy-mm-dd-hh-mm-ss <-- it accounts for the different formats.
    dates = series.index.floor('D')
    # grouping by the dates to make sure theres only one value per date
    group = series.groupby(dates)
    # If the argument passed to the function is "mean" then average the groupby by day, otherwise sum it up per day
    series = group.mean() if mean else group.sum()

    # Parse start/end, defaulting to the min/max of the index.
    # start is a function argument, in the 'start or series.index.min()' statement, python will first try to find start and check if it is None (or False), if it is, it will then do the 'series.index.min()' part. If 'start' is populated, then it will use 'start' as the value. The 'or' acts as a way of setting a default value in this case.
    # Would a better way be putting 'series.index.min()' as the argument default in the def() statement?
    start = pd.to_datetime(start or series.index.min())
    end = pd.to_datetime(end or series.index.max())

    # We use [start, end) as a half-open interval below.
    # Adding one day to the 'end' date as the code later does not actually include the end but uses it as a stopping point. [] <-- means included, () <-- means excluded.
    end += np.timedelta64(1, 'D')

    # Get the previous/following Sunday to start/end.
    # Pandas and numpy day-of-week conventions are Monday=0 and Sunday=6.
    # This function treats sunday as the first day of the week. DatetimeObject.dayofweek will bring back a number 0-6 to specify what day of week it is. Monday = 0, so this person uses the modulo formula to find the starting sunday, even if it is not in range within the numerical data.
    # Pretty sure you can delete the '% 7' as it does not change the answer.
    start_sun = start - np.timedelta64((start.dayofweek + 1), 'D')

    end_sun = end + np.timedelta64(7 - end.dayofweek - 1, 'D')

    # Create the heatmap and track ticks.
    # Integer division so there's no decimals when creating the plot.
    num_weeks = (end_sun - start_sun).days // 7
    # np.zeros creates an array of size x, y and fills it all with 0s.
    heatmap = np.zeros((7, num_weeks))

    ticks = {}  # week number -> month name
    # Loop through this code for the number of weeks calculated in num_weeks.
    for week in range(num_weeks):
        # using range 7 (0-6) as we know that 0-6 is the weekday index in datetimeObject.dayofweek.
        for day in range(7):
            # Setting the date in each loop by adding a week to it each time.
            date = start_sun + np.timedelta64(7 * week + day, 'D')
            # date.day brings back the day number of the month. E.g. 14th Dec would bring back 14.
            # If the day of the month is the 1st, add the week number to the dictionary as the key, and set the value to the previous month. We set the value to the previous month because e.g. if we start the loop in janurary, the first month it gets to is Feb, so we want to label the looped through Jan as Jan.
            # date.month brings back the month number.
            if date.day == 1:
                ticks[week] = MONTHS[date.month - 1]
            # if the dayofyear (1st Jan = 1), change the value of the week to "week number + year"
            if date.dayofyear == 1:
                ticks[week] += f'\n{date.year}'
            # if the date is more than the start date and less than the end date, then in the heatmap array that currently contains zeros, add the value from the dataset to populate the heatmap with series.get(date_to_get, )
            if start <= date < end:
                heatmap[day, week] = series.get(date, 0)

    # Get the coordinates, offset by 0.5 to align the ticks.
    y = np.arange(8) - 0.5
    x = np.arange(num_weeks + 1) - 0.5

    # Plot the heatmap. Prefer pcolormesh over imshow so that the figure can be
    # vectorized when saved to a compatible format. We must invert the axis for
    # pcolormesh, but not for imshow, so that it reads top-bottom, left-right.
    ax = ax or plt.gca()
    mesh = ax.pcolormesh(x, y, heatmap, **kwargs)
    ax.invert_yaxis()

    # Set the ticks.
    ax.set_xticks(list(ticks.keys()))
    ax.set_xticklabels(list(ticks.values()))
    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(DAYS)

    # Set the current image and axes in the pyplot API.
    plt.sca(ax)
    plt.sci(mesh)

    return ax


def date_heatmap_demo():
    '''An example for `date_heatmap`.

    Most of the sizes here are chosen arbitrarily to look nice with 1yr of
    data. You may need to fiddle with the numbers to look right on other data.
    '''
    # Get some data, a series of values with datetime index.
    data = np.random.randint(5, size=365)
    data = pd.Series(data)
    data.index = pd.date_range(start='2017-01-01', end='2017-12-31', freq='1D')

    # Create the figure. For the aspect ratio, one year is 7 days by 53 weeks.
    # We widen it further to account for the tick labels and color bar.
    figsize = plt.figaspect(7 / 56)
    fig = plt.figure(figsize=figsize)

    # Plot the heatmap with a color bar.
    ax = date_heatmap(data, edgecolor='black')
    plt.colorbar(ticks=range(5), pad=0.02)

    # Use a discrete color map with 5 colors (the data ranges from 0 to 4).
    # Extending the color limits by 0.5 aligns the ticks in the color bar.
    cmap = mpl.cm.get_cmap('Blues', 5)
    plt.set_cmap(cmap)
    plt.clim(-0.5, 4.5)

    # Force the cells to be square. If this is set, the size of the color bar
    # may look weird compared to the size of the heatmap. That can be corrected
    # by the aspect ratio of the figure or scale of the color bar.
    ax.set_aspect('equal')

    # Save to a file. For embedding in a LaTeX doc, consider the PDF backend.
    # http://sbillaudelle.de/2015/02/23/seamlessly-embedding-matplotlib-output-into-latex.html
    fig.savefig('heatmap.pdf', bbox_inches='tight')

    # The firgure must be explicitly closed if it was not shown.
    plt.close(fig)


date_heatmap_demo()
