import pandas as pd
import matplotlib.pyplot as plt
import os

def barPlot(dictdata, name, title, xlabel, ylabel, index=999):
    os.makedirs("./images/balaImages", exist_ok=True)
    if index == 999:
        plotdata = pd.DataFrame.from_dict(dictdata)
    else:
        plotdata = pd.DataFrame.from_dict([dictdata])

    ax = plotdata.plot(kind="bar", figsize=(15, 8))
    ax.tick_params(axis='x', labelrotation=0)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    for p in ax.patches:
        ax.annotate(
            str(p.get_height()), xy=(p.get_x() + 0.02, p.get_height() + 0.5), fontsize=10, rotation=90
        )

    plt.savefig(f'./images/balaImages/{name}.png', bbox_inches='tight')
    plt.close()
