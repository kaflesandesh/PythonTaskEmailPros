import pandas
import matplotlib.pyplot as plt
from typing import Dict
import constants
import log_parse
import file_management


def finish_time(data: Dict[str, pandas.DataFrame]) -> pandas.DataFrame:
    exercise_start = data["exercise"]["exercise_start"].iloc[0]
    milestone_data = data["milestone"]
    finishes = milestone_data[(milestone_data["name"] == "exercise_finished")]
    finishes = finishes[["timestamp_reached", "team_id"]]
    finishes["duration"] = pandas.to_timedelta(
        finishes["timestamp_reached"] - pandas.Timestamp(exercise_start)
    )
    return finishes


def plot_milestones(finishes: pandas.DataFrame) -> None:
    overall_avg_time = finishes["duration"].mean()
    plt.figure(figsize=(10, 6))

    plt.bar(
        finishes["team_id"],
        finishes["duration"].dt.total_seconds() / 60,
        color="skyblue",
        label="Team Average",
    )
    plt.errorbar(
        finishes["team_id"],
        finishes["duration"].dt.total_seconds() / 60,
        yerr=finishes["duration"].dt.total_seconds() / 60,
        fmt="none",
        ecolor="black",
        capsize=5,
        capthick=2,
        label="Standard Deviation",
    )
    plt.axhline(
        y=overall_avg_time.total_seconds() / 60,
        color="orange",
        linestyle="--",
        label="Overall Average",
    )

    plt.xlabel("Team ID")
    plt.ylabel("Average Time (minutes)")
    plt.title("Average Time taken by Teams to Finish Exercises")
    plt.xticks(finishes["team_id"])
    plt.legend()
    plt.tight_layout()
    plt.savefig("finish_time_plot.png")
    file_management.save_plot("finish_time_plot.png")


def main(teams: int, plot: bool, csv: bool) -> pandas.DataFrame:
    milestone_data = log_parse.get_merged_logs(teams, constants.MILESTONE_LOGS)
    exercise_data = log_parse.get_logs(0, "exercise.jsonl", False)
    data = finish_time({"milestone": milestone_data, "exercise": exercise_data})
    if plot and not data.empty:
        data = data.dropna()
        if not data.empty:
            plot_milestones(data)
    if csv and not data.empty:
        data.to_csv("exercise_finish_time.csv")
        file_management.save_csv("exercise_finish_time.csv")
    return data


if __name__ == "__main__":
    main(5, True, True)
