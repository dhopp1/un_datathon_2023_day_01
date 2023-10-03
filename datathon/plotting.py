import matplotlib.pyplot as plt

def line_plot(series1, series2, ax1_color = "blue", ax2_color = "red"):   
    """
    plot two lines side by side
    parameters:
        :series1: Tuple(list, list), a tuple containing the x and y values of the first line
        :series2: Tuple(list, list), a tuple containing the x and y values of the second line
        :ax1_color: str, what color to use for the first axis
        :ax2_color: str, what color to use for the second axis
    """    
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("")
    ax1.set_ylabel("Number of ships at Russian ports", color = ax1_color)
    ax1.plot(series1[0], series1[1])
    ax1.tick_params(axis = "y", labelcolor = ax1_color)
    
    ax2 = ax1.twinx()
    
    ax2.set_ylabel("Russian exports, USD", color = ax2_color)
    ax2.plot(series2[0], series2[1], color = ax2_color)
    ax2.tick_params(axis = "y", labelcolor = ax2_color)
    
    return fig
