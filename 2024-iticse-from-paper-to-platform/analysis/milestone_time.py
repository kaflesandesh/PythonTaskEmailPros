import pandas
import matplotlib.pyplot as plt
from typing import Dict
import log_parse
import constants
import file_management


def calculate_times(data: Dict[str, pandas.DataFrame]) -> pandas.DataFrame:
    exercise_start = data["exercise"]["exercise_start"].iloc[0]
    milestone_data = data["milestone"]
    data = milestone_data[(milestone_data["name"] != "exercise_finished")]
    data = data[["timestamp_reached", "team_id", "name"]]
    data["duration"] = pandas.to_timedelta(
        data["timestamp_reached"] - pandas.Timestamp(exercise_start)
    )
    data["duration_seconds"] = data["duration"].dt.total_seconds()
    return data


def calculate_averages(time_data: pandas.DataFrame) -> pandas.DataFrame:
    data = (
        time_data.groupby("name")["duration_seconds"].agg(["mean", "std"]).reset_index()
    )
    data.columns = ["name", "avg_minutes", "sd_minutes"]
    data["avg_minutes"] = data["avg_minutes"] / 60
    data["sd_minutes"] = data["sd_minutes"] / 60
    return data


def plot_teams(time_data: pandas.DataFrame, team_data: pandas.Series) -> None:
    team_id = team_data["team_id"]
    time_data = time_data[time_data["team_id"] == team_id]
    time_data = time_data.dropna(subset="duration")
    time_data["duration_minutes"] = time_data["duration_seconds"] / 60
    plt.figure(figsize=(10, 6))

    plt.bar(
        time_data["name"],
        time_data["duration_minutes"],
        color="skyblue",
        label="Time to reach milestone",
    )

    plt.xlabel("Milestones")
    plt.ylabel("Time to reach (minutes)")
    plt.xticks(time_data["name"], rotation=45, ha="right")
    plt.title(f"Time to reach milestones by Team {team_id}")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(f"team-{team_id}_milestones_plot.png")
    file_management.save_plot(f"team-{team_id}_milestones_plot.png")


def plot_milestones(time_data: pandas.DataFrame) -> None:
    plt.figure(figsize=(10, 6))

    plt.bar(
        time_data["name"],
        time_data["avg_minutes"],
        yerr=time_data["sd_minutes"],
        capsize=5,
    )

    plt.xlabel("Milestones")
    plt.ylabel("Average time to reach (minutes)")
    plt.title("Average time to reach milestones")
    plt.grid(axis="y")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(f"time_milestones_plot.png")
    file_management.save_plot(f"time_milestones_plot.png")


def main(teams: int, plot: bool, csv: bool) -> pandas.DataFrame:
    milestone_data = log_parse.get_merged_logs(teams, constants.MILESTONE_LOGS)
    exercise_data = log_parse.get_logs(0, "exercise.jsonl", False)
    teams_data = log_parse.get_logs(0, "teams.jsonl", False)
    time_data = calculate_times(
        {"milestone": milestone_data, "exercise": exercise_data}
    )
    averages_data = calculate_averages(time_data)
    if plot:
        if not time_data.empty:
            for i in range(teams):
                plot_teams(time_data, teams_data.iloc[i])
        if not averages_data.empty:
            plot_milestones(averages_data)
    if csv:
        time_data.to_csv("milestone_reach_time.csv")
        file_management.save_csv("milestone_reach_time.csv")
        averages_data.to_csv("milestone_mean_time.csv")
        file_management.save_csv("milestone_mean_time.csv")
    return time_data


if __name__ == "__main__":
    main(5, True, True)
