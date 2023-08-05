import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

def time_slice(df, time_period):
    """For a `time_period`, creates a dataframe with a row for each country and a column for each AQUASTAT variable.

    Args:
        df: :obj:`pandas.DataFrame` with the columns, `country`, `variable`, `value`, and `time period`
        time_period: time period for filtering the data set and pivoting

    Returns:
        df (:obj:`pandas.DataFrame`): Pivoted dataframe

    """
    if not isinstance(df, pd.DataFrame):
        logger.error("argument `df` is not a Panda's DataFrame object")
        raise TypeError("Provided argument `df` is not a Panda's DataFrame object")

    # Only take data for time period of interest
    df = df[df.time_period == time_period]
    logger.debug("Took data for time period of interest")

    # Pivot table
    df = df.pivot(index='country', columns='variable', values='value')
    logger.debug('Made pivot table')

    df.columns.name = time_period
    logger.debug('Set column name as time period')

    return df


def country_slice(df, country):
    """For a `country`, creates a dataframe with a row for each `variable` and a column for each `time_period`."""
    if not isinstance(df, pd.DataFrame):
        logger.error("argument `df` is not a Panda's DataFrame object")
        raise TypeError("Provided argument `df` is not a Panda's DataFrame object")

    # Only take data for country of interest
    df = df[df.country == country]
    logger.debug('Took data for country of interest')

    # Pivot table
    df = df.pivot(index='variable', columns='time_period', values='value')
    logger.debug('Made pivot table')

    df.index.name = country
    logger.debug('Set column name as country')

    return df


def variable_slice(df, variable):
    """For a `variable`, creates a dataframe with a row for each `country` and a column for each `time_period`."""
    if not isinstance(df, pd.DataFrame):
        logger.error("argument `df` is not a Panda's DataFrame object")
        raise TypeError("Provided argument `df` is not a Panda's DataFrame object")

    df = df[df.variable == variable]
    logger.debug('Took data for variable of interest')

    df = df.pivot(index='country', columns='time_period', values='value')
    logger.debug('Made pivot table')

    return df


def time_series(df, country, variable):
    """For a `country`, creates a time series of a certain `variable`.

    Args:
        df: :obj:`pandas.DataFrame` with the columns, `country`, `variable`, `value`, and `time period`
        country: country for filtering the data set
        variable: variable that time series describes

    Returns:
        df (:obj:`pandas.DataFrame`): Time series of a country's certain variable

    """
    if not isinstance(df, pd.DataFrame):
        logger.error("argument `df` is not a Panda's DataFrame object")
        raise TypeError("Provided argument `df` is not a Panda's DataFrame object")

    # Only take data for country/variable combo
    series = df[(df.country == country) & (df.variable == variable)]
    logger.debug('Took data for country/variable combo')

    # Drop years with no data
    series = series.dropna()[['year_measured', 'value']]
    logger.debug('Dropped years with no data')

    # Change years to int and set as index
    series.year_measured = series.year_measured.astype(int)
    series.set_index('year_measured', inplace=True)
    series.columns = [variable]
    logger.debug('Changed years to int and set as index')

    return series


def plot_heatmap(df,
                 title='',
                 xlabel=None,
                 ylabel=None,
                 label_size=20,
                 tick_label_size=16,
                 cmap=None,
                 xticklabels=None,
                 yticklabels=None,
                 figsize=None,
                 xrotation=90,
                 yrotation=0,
                 **kwargs):
    """Creates a heatmap plot for the dataset.

    Args:
        df: :obj:`pandas.DataFrame` with the columns, `country`, `variable`, `value`, and `time period`
        title: plot title
        xlabel: label of the x axis
        ylabel: label of the y axis
        label_size: fontsize of labels
        tick_label_size: fontsize of tick labels
        cmap: matplotlib colormap name or object, or list of colors
        xticklabels: tick labels of x axis
        yticklabels: tick labels of y axis
        figsize: size of figure
        xrotation: rotation of x axis labels
        yrotation: rotation of y axix labels
        **kwargs: keyword arguments

    Returns:
        fig (:obj:`matplotlib.Figure`):
        ax (:obj:`matplotlib.AxesSubplot`)
    """
    if figsize is None:
        logger.info("You can set figure size if you want")
        figsize = (16, 8)
    fig, ax = plt.subplots(figsize=figsize)

    if xlabel is None:
        logger.info("You can set label of x axis if you want")
        xlabel = ' '.join(df.columns.name.split('_')).capitalize()
    if ylabel is None:
        logger.info("You can set label of y axis if you want")
        ylabel = ' '.join(df.index.name.split('_')).capitalize()

    yticklabels = df.index.tolist() if yticklabels is None else yticklabels
    xticklabels = df.columns.tolist() if xticklabels is None else xticklabels

    if cmap is None:
        logger.info("You can set color map if you want")
        cmap = sns.cubehelix_palette(8, start=.5, rot=-.75)

    ax = sns.heatmap(df, cmap=cmap, **kwargs)
    ax.set_xticklabels(xticklabels, rotation=xrotation, size=tick_label_size)
    ax.set_yticklabels(yticklabels, rotation=yrotation, size=tick_label_size)

    ax.set_title(title, size=label_size)
    ax.set_xlabel(xlabel, size=label_size)
    ax.set_ylabel(ylabel, size=label_size)

    ax.set_ylim([0, len(df)])

    return fig, ax


def plot_histogram(df,
                   column,
                   title='',
                   xlabel=None,
                   ylabel=None,
                   label_size=20,
                   tick_label_size=16,
                   color='#0085ca',
                   alpha=0.8,
                   figsize=None,
                   **kwargs):
    """Creates a heatmap plot for the dataset.
    Args:
        df: :obj:`pandas.DataFrame` with the columns, `country`, `variable`, `value`, and `time period`
        column:
        title: plot title
        xlabel: label of the x axis
        ylabel: label of the y axis
        label_size: fontsize of labels
        tick_label_size: fontsize of tick labels
        color: color of the histogram
        alpha: float (0.0 transparent through 1.0 opaque)
        figsize: size of figure
        **kwargs: keyword arguments

    Returns:
        fig (:obj:`matplotlib.Figure`):
        ax (:obj:`matplotlib.AxesSubplot`)
    """
    if figsize is None:
        logger.info("You can set figure size if you want")
        figsize = (12, 8)
    fig, ax = plt.subplots(figsize=figsize)

    if xlabel is None:
        logger.info("You can set label of x axis if you want")
        xlabel = ' '.join(column.split('_')).capitalize()
    if ylabel is None:
        logger.info("You can set label of y axis if you want")
        ylabel = 'Count'

    ax.hist(df[column], color=color, alpha=alpha, **kwargs)

    ax.set_title(title, size=label_size)
    ax.set_xlabel(xlabel, size=label_size)
    ax.set_ylabel(ylabel, size=label_size)

    return fig, ax
