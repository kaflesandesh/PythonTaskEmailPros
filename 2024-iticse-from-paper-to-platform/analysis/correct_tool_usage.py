import pandas
import matplotlib.pyplot as plt
import log_parse
import constants
import numpy as np
import file_management


def evaluate_usage(data: pandas.DataFrame) -> pandas.DataFrame:
    data = data[["content", "name", "default_response"]]

    data = data.assign(
        correct=data.apply(
            lambda row: int(row["default_response"] not in row["content"]), axis=1
        )
    )
    data = data.assign(
        incorrect=data.apply(
            lambda row: int(row["default_response"] in row["content"]), axis=1
        )
    )
    data = data[data["name"] != "sharing_system"]
    return data.groupby("name").agg({"correct": "sum", "incorrect": "sum"})


def plotter(data: pandas.DataFrame) -> None:
    plt.figure(figsize=(10, 6))

    bar_width = 0.35
    index = np.arange(len(data.index))

    plt.figure(figsize=(10, 6))

    plt.bar(index, data["correct"], bar_width, label="Correct")
    plt.bar(index + bar_width, data["incorrect"], bar_width, label="Incorrect")

    plt.xlabel("Name")
    plt.ylabel("Count")
    plt.title("Correct vs Incorrect Usage by Tool")
    plt.xticks(index + bar_width / 2, data.index, rotation=45)
    plt.legend()

    plt.grid(axis="both", which="both")

    plt.tight_layout()
    plt.savefig("correct_usage_plot.png")
    file_management.save_plot("correct_usage_plot.png")


def main(teams: int, plot: bool, csv: bool) -> pandas.DataFrame:
    team_tool_data = evaluate_usage(
        log_parse.get_merged_logs(teams, constants.TOOLS_LOG)
    )
    if plot:
        if not team_tool_data.empty:
            plotter(team_tool_data)
    if csv:
        team_tool_data.to_csv("correct_usage.csv")
        file_management.save_csv("correct_usage.csv")
    return team_tool_data


if __name__ == "__main__":
    main(12, True, True)
