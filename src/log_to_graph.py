import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import yaml
import numpy as np
from numpy import typing as npt


cfg = yaml.full_load(open(os.getcwd() + "/config.yml", 'r'))


def delete_lines(file, lines_to_delete=[]):
    with open(file, "r") as f:
        lines = f.readlines()
    for line in lines_to_delete:
        if line < len(lines):
            lines[line] = ""
    with open(file, "w") as f:
        f.write("".join(lines))


def set_colour(money_arr, colour_arr):
    if money_arr[-1] < money_arr[-2]:
        # red
        colour_arr = np.vstack((colour_arr, [0.75, 0, 0, 1]))
    elif money_arr[-1] > money_arr[-2]:
        # green
        colour_arr = np.vstack((colour_arr, [0, 0.48, 0, 1]))
    else:
        colour_arr = np.vstack((colour_arr, [0, 0, 0, 1]))
    return colour_arr


def add_to_plot(x_axis: npt.NDArray, y_axis: npt.NDArray, colours: npt.NDArray, ax: plt.axis, subplot: int, title: str):
    i = 1
    lines = []
    while i < y_axis.size:
        lines.append([(x_axis[i - 1], y_axis[i - 1]), (x_axis[i], y_axis[i])])
        i = i + 1
    lc = mc.LineCollection(lines, colors=colours)
    ax[subplot].add_collection(lc)
    ax[subplot].autoscale()
    ax[subplot].margins(0.1)
    ax[subplot].axhline(y=0, color='black', linestyle='--')
    ax[subplot].set_title(title)
    ax[subplot].set_xlim(left=0)


def update_vals(money_in_item: npt.NDArray, price_arr: npt.NDArray, item_count: npt.NDArray, price: float, volume: int, buying: bool = True):
    if buying:
        money_in_item = money_in_item - (price * volume)
        item_count = item_count + volume
    else:
        money_in_item = money_in_item + (price * volume)
        item_count = item_count - volume
    price_arr = np.append(price_arr, price)
    return money_in_item, item_count, price_arr


def convert_log_to_csv(file_name):
    # get file location
    file_dir = "./csvs/" + file_name
    # rename .log to .csv
    # os.rename(file_dir + ".log", file_dir + ".csv")
    file_dir = file_dir + ".csv"
    # get rid of header and random line
    # delete_lines(file_dir, [0, 2])
    # read csv as pandas df
    df = pd.read_csv(file_dir)
    money_in_bananas_arr = np.array([0])
    b_colour = np.empty((0, 4), int)
    p_colour = np.empty((0, 4), int)
    bp_colour = np.empty((0, 4), int)
    pp_colour = np.empty((0, 4), int)
    money_in_pearls_arr = np.array([0])
    b_profit = np.array([0])
    p_profit = np.array([0])
    b_prices = np.array
    p_prices = np.array
    b_time = np.array([0])
    p_time = np.array([0])
    money_in_bananas = 0
    money_in_pearls = 0
    bananas_cnt = 0
    pearl_cnt = 0
    for index, row in df.iterrows():
        # bought bananas
        if row["product"] == "BANANAS" and not pd.isnull(row["buy_price"]):
            money_in_bananas, bananas_cnt, b_prices = \
                update_vals(money_in_bananas, b_prices, bananas_cnt, row["buy_price"], row["buy_volume"])
        # sold bananas
        elif row["product"] == "BANANAS":
            money_in_bananas, bananas_cnt, b_prices = \
                update_vals(money_in_bananas, b_prices, bananas_cnt, row["sell_price"], row["sell_volume"], False)
        # bought pearls
        if row["product"] == "PEARLS" and not pd.isnull(row["buy_price"]):
            money_in_pearls, pearl_cnt, p_prices = \
                update_vals(money_in_pearls, p_prices, pearl_cnt, row["buy_price"], row["buy_volume"])
        # sold pearls
        elif row["product"] == "PEARLS":
            money_in_pearls, pearl_cnt, p_prices = \
                update_vals(money_in_pearls, p_prices, pearl_cnt, row["sell_price"], row["sell_volume"], False)
        # other things
        if row["product"] == "PEARLS":
            p_time = np.append(p_time, float(row["0 timestamp"]) / 1000)
            money_in_pearls_arr = np.append(money_in_pearls_arr, money_in_pearls)
            p_colour = set_colour(money_in_pearls_arr, p_colour)
            p_profit = np.append(p_profit, money_in_pearls_arr[-1] + (pearl_cnt * np.average(p_prices[1:])))
            pp_colour = set_colour(p_profit, pp_colour)
        elif row["product"] == "BANANAS":
            b_time = np.append(b_time, float(row["0 timestamp"]) / 1000)
            money_in_bananas_arr = np.append(money_in_bananas_arr, money_in_bananas)
            b_colour = set_colour(money_in_bananas_arr, b_colour)
            b_profit = np.append(b_profit, money_in_bananas_arr[-1] + (bananas_cnt * np.average(b_prices[1:])))
            bp_colour = set_colour(b_profit, bp_colour)

    money_in_bananas = money_in_bananas + (np.average(b_prices[1:]) * bananas_cnt)
    money_in_pearls = money_in_pearls + (np.average(p_prices[1:]) * pearl_cnt)
    fig, axis = plt.subplots(4, 1)
    add_to_plot(b_time, money_in_bananas_arr, b_colour, axis, 0, "Bananas")
    add_to_plot(p_time, money_in_pearls_arr, p_colour, axis, 1, "Pearls")
    add_to_plot(b_time, b_profit, bp_colour, axis, 2, "Banana Profits")
    add_to_plot(p_time, p_profit, pp_colour, axis, 3, "Pearl Profits")
    fig.set_size_inches(20, 18.5)
    file_name = file_name + ".png"
    fig.savefig(os.path.join(cfg["PATHS"]["PLOTS"], file_name), dpi=100)
    print("bananas remaining: " + str(bananas_cnt))
    print("final profit in banans: " + str(money_in_bananas))
    print("pearls remaining: " + str(pearl_cnt))
    print("final profit in pearls: " + str(money_in_pearls))


if __name__ == "__main__":
    convert_log_to_csv("test4")
