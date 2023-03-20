import os
import pandas as pd


def delete_lines(file, lines_to_delete=[]):
    with open(file, "r") as f:
        lines = f.readlines()
    for line in lines_to_delete:
        if line < len(lines):
            lines[line] = ""
    with open(file, "w") as f:
        f.write("".join(lines))


def convert_log_to_csv(file_name):
    file_dir = "./csvs/" + file_name
    os.rename(file_dir + ".log", file_dir + ".csv")
    file_dir = file_dir + ".csv"
    delete_lines(file_dir, [0])
    df = pd.read_csv(file_dir)
    reached_last_line = False
    lines_to_delete = []
    for index, row in df.iterrows():
        if row["product"] == "skip" or reached_last_line:
            lines_to_delete.append(index + 1)
        elif row["0 timestamp"] == "Submission logs:":
            reached_last_line = True
            lines_to_delete.append(index + 1)
    delete_lines(file_dir, lines_to_delete)


if __name__ == "__main__":
    convert_log_to_csv("test1")
