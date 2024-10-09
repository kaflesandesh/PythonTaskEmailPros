import pandas
import log_parse
import constants
import matplotlib.pyplot as plt
import file_management
from typing import List


def tools_count(data: pandas.DataFrame) -> pandas.DataFrame:
    data = data[data["action_type"] == "COMMAND"]
    return data[["team_id", "name"]]


def plotter(
    data: pandas.DataFrame,
    avg_usage: float,
    teams: int,
    tool: str,
    team_list: List[int],
) -> None:
    plt.figure(figsize=(10, 6))

    bars = plt.bar(data["team_id"], data["usage_count"], color="skyblue", label="Usage Count")

    for bar, value in zip(bars, data["usage_count"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value}",
            ha='center',
            va='bottom'
        )

    plt.axhline(y=avg_usage, color="orange", linestyle="--", label="Average Usage")

    plt.xlabel("Team ID")
    plt.ylabel("Number of Times Used")
    plt.xticks(team_list)
    if teams:
        plt.title(f"Usage of '{tool}' by Teams")
    else:
        plt.title(f"Usage of tools by Teams")
    plt.legend()
    plt.grid(axis="y")
    if int(max(data["usage_count"])) > 20:
        plt.yticks(range(0, int(max(data["usage_count"])) + 1, 5))
    else:
        plt.yticks(range(1, int(max(data["usage_count"])) + 1))


    plt.tight_layout()
    plt.savefig(f"{tool}_usage_plot.png")
    file_management.save_plot(f"{tool}_usage_plot.png")


def plot_tools(data: pandas.DataFrame, tool: str, teams_list: List[int]) -> None:
    data = (
        data[data["name"] == tool]
        .groupby("team_id")
        .size()
        .reset_index(name="usage_count")
    )
    if data.empty:
        return None

    avg_usage = data["usage_count"].mean()

    plotter(data, avg_usage, True, tool, teams_list)


def plot_all(data: pandas.DataFrame, teams_list: List[int]) -> None:
    data = data.groupby("team_id").size().reset_index(name="usage_count")
    if data.empty:
        return None
    avg_usage = data["usage_count"].mean()
    plotter(data, avg_usage, False, "tools", teams_list)


def main(teams: int, plot: bool, csv: bool) -> pandas.DataFrame:
    team_tool_data = tools_count(log_parse.get_merged_logs(teams, constants.TOOLS_LOG))
    teams_list = list(
        range(team_tool_data["team_id"].min(), team_tool_data["team_id"].max() + 1)
    )
    exercise_tools = log_parse.get_logs(0, "exercise_tools.jsonl", False)
    exercise_tools = exercise_tools[["name"]]
    if plot:
        if not team_tool_data.empty:
            for tool in exercise_tools["name"]:
                plot_tools(team_tool_data, tool, teams_list)
            plot_all(team_tool_data, teams_list)
    if csv:
        data = team_tool_data.groupby("name").size().reset_index(name="count")
        data.to_csv("team_tool_usage.csv")
        file_management.save_csv("team_tool_usage.csv")
    return team_tool_data


if __name__ == "__main__":
    main(12, True, True)
