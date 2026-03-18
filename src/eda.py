import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np

plt.style.use("seaborn-v0_8")

# timed plots

# plots two time series side by side
def plot_double(dataFrame, col1, col2, title1, title2, ylabel1, ylabel2, x_column="Év", start_zero=False):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # left plot
    ax1.plot(dataFrame[x_column], dataFrame[col1], marker="o")
    ax1.set(title=title1, xlabel=x_column, ylabel=ylabel1)
    ax1.grid(True, alpha=0.3)

    # right plot
    ax2.plot(dataFrame[x_column], dataFrame[col2], marker="o")
    ax2.set(title=title2, xlabel=x_column, ylabel=ylabel2)
    ax2.grid(True, alpha=0.3)

    # to see absolute drops vs relative changes
    if start_zero:
        ax1.set_ylim(bottom=0)
        ax2.set_ylim(bottom=0)

    plt.tight_layout()
    plt.show()

def plot_indexed_series(dataFrame, columns, title, x_column="Év",):

    plt.figure(figsize=(12,5))

    for col in columns:
        # normalize to 100 based on the first row to compare growth rates
        # even if the raw scales are totally different
        indexed = dataFrame[col] / dataFrame[col].iloc[0] * 100
        plt.plot(dataFrame[x_column], indexed, label=col)

    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel("Index (első év = 100)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.show()

# --------------------
# correlation analysis

def plot_scatter(dataFrame, x, y, title, xlabel, ylabel):

    plt.figure(figsize=(6,5))

    plt.scatter(dataFrame[x], dataFrame[y])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.grid(True, alpha=0.3)
    plt.show()

# default and detrended correlation matrices placed next to each other
def plot_dual_correlation_matrix(dataFrame, columns, titles):

    # simple correlation matrix
    corr_raw = dataFrame[columns].corr()
    # for detrended correlation matrix, calculate YoY percent change to remove time trend
    # drop the first row because it has no comparable previous year
    corr_detrended = dataFrame[columns].pct_change().dropna().corr()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # create masks for the upper triangle to improve clarity
    mask_raw = np.triu(np.ones_like(corr_raw, dtype=bool))
    mask_det = np.triu(np.ones_like(corr_detrended, dtype=bool))

    # plot 1: raw
    sns.heatmap(corr_raw, mask=mask_raw, annot=True, cmap="coolwarm", center=0,
                fmt=".2f", linewidths=0.5, square=True, ax=ax1, cbar=False)
    ax1.set_title(titles[0])
    
    # plot 2: detrended
    sns.heatmap(corr_detrended, mask=mask_det, annot=True, cmap="coolwarm", center=0,
                fmt=".2f", linewidths=0.5, square=True, ax=ax2, cbar=False)

    for ax in [ax1, ax2]:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    plt.tight_layout()
    plt.show()

# two linear regression model fits placed next to each other
def plot_comparative_scatters(dataFrame, x_variables, y_variables, titles):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    axes = [ax1, ax2]

    for i in range(2):
        sns.regplot(
            data=dataFrame, 
            x=x_variables[i], 
            y=y_variables[i], 
            ax=axes[i],
            scatter_kws={'alpha':0.6},
            line_kws={'color':'red'}
        )
        axes[i].set_title(titles[i])
        axes[i].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# timed plot that will be able to show the zero tolerance and the covid breakpoints pointed out in our analysis
def plot_time_series(dataFrame, column, title, ylabel, breakpoints=None, x_column="Év"):

    plt.figure(figsize=(12,5))

    plt.plot(dataFrame[x_column], dataFrame[column], marker="o")
    plt.xticks(dataFrame[x_column], rotation=45)

    # add break lines
    if breakpoints:
        y_max = plt.ylim()[1]
        for year, label in breakpoints:
            plt.axvline(x=year, linestyle="--", alpha=0.7)
            plt.text(year, y_max * 0.95, label, rotation=90, va="top", ha="right", fontsize=10)

    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()