import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import collections as mc
from matplotlib.pyplot import figure
import yaml
import numpy as np

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
        # colour_arr = np.insert(colour_arr, [[0.48, 1, 0, 1]], axis=0)
        colour_arr = np.vstack((colour_arr, [1, 0, 0, 1]))
    elif money_arr[-1] > money_arr[-2]:
        # colour_arr = np.insert(colour_arr, [[1, 0, 0, 1]], axis=0)
        colour_arr = np.vstack((colour_arr, [0.48, 1, 0, 1]))
    else:
        # colour_arr = np.insert(colour_arr, [[1, 1, 1, 1]], axis=0)
        colour_arr = np.vstack((colour_arr, [1, 1, 1, 1]))
    return colour_arr


def convert_log_to_csv(file_name):
    # get file location
    file_dir = "./csvs/" + file_name
    # rename .log to .csv
    os.rename(file_dir + ".log", file_dir + ".csv")
    file_dir = file_dir + ".csv"
    # get rid of header and random line
    delete_lines(file_dir, [0, 2])
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
            money_in_bananas = money_in_bananas - (row["buy_price"] * row["buy_volume"])
            bananas_cnt = bananas_cnt + row["buy_volume"]
            b_prices = np.append(b_prices, row["buy_price"])
        # sold bananas
        elif row["product"] == "BANANAS":
            money_in_bananas = money_in_bananas + (row["sell_price"] * row["sell_volume"])
            bananas_cnt = bananas_cnt - row["sell_volume"]
            b_prices = np.append(b_prices, row["sell_price"])
        # bought pearls
        if row["product"] == "PEARLS" and not pd.isnull(row["buy_price"]):
            money_in_pearls = money_in_pearls - (row["buy_price"] * row["buy_volume"])
            pearl_cnt = pearl_cnt + row["buy_volume"]
            p_prices = np.append(p_prices, row["buy_price"])
        # sold pearls
        elif row["product"] == "PEARLS":
            money_in_pearls = money_in_pearls + (row["sell_price"] * row["sell_volume"])
            pearl_cnt = pearl_cnt - row["sell_volume"]
            p_prices = np.append(p_prices, row["sell_price"])
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
    i = 1
    lines = []
    while i < money_in_bananas_arr.size:
        lines.append([(b_time[i - 1], money_in_bananas_arr[i - 1]), (b_time[i], money_in_bananas_arr[i])])
        i = i + 1
    lc = mc.LineCollection(lines, colors=b_colour)
    axis[0].add_collection(lc)
    axis[0].autoscale()
    axis[0].margins(0.1)
    axis[0].axhline(y=0, color='black', linestyle='--')
    axis[0].set_title("Bananas")
    i = 1
    p_lines = []
    while i < money_in_pearls_arr.size:
        p_lines.append([(p_time[i - 1], money_in_pearls_arr[i - 1]), (p_time[i], money_in_pearls_arr[i])])
        i = i + 1
    lc1 = mc.LineCollection(p_lines, colors=p_colour)
    axis[1].add_collection(lc1)
    axis[1].autoscale()
    axis[1].margins(0.1)
    axis[1].axhline(y=0, color='black', linestyle='--')
    axis[1].set_title("Pearls")
    i = 1
    lines1 = []
    while i < b_profit.size:
        lines1.append([(b_time[i - 1], b_profit[i - 1]), (b_time[i], b_profit[i])])
        i = i + 1
    lc = mc.LineCollection(lines1, colors=bp_colour)
    axis[2].add_collection(lc)
    axis[2].autoscale()
    axis[2].margins(0.1)
    axis[2].axhline(y=0, color='black', linestyle='--')
    axis[2].set_title("Pearls Profits")
    i = 1
    p_lines1 = []
    while i < p_profit.size:
        p_lines1.append([(p_time[i - 1], p_profit[i - 1]), (p_time[i], p_profit[i])])
        i = i + 1
    lc1 = mc.LineCollection(p_lines1, colors=pp_colour)
    axis[3].add_collection(lc1)
    axis[3].autoscale()
    axis[3].margins(0.1)
    axis[3].axhline(y=0, color='black', linestyle='--')
    axis[3].set_title("Bananas Profits")
    fig.set_size_inches(18.5, 18.5)
    file_name = file_name + ".png"
    fig.savefig(os.path.join(cfg["PATHS"]["PLOTS"], file_name), dpi=100)
    print(money_in_pearls)
    print(money_in_bananas)
    print("bananas: " + str(bananas_cnt))
    print("pearls: " + str(pearl_cnt))


if __name__ == "__main__":
    convert_log_to_csv("test4")
