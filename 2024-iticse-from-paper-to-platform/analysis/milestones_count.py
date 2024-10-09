import pandas
import matplotlib.pyplot as plt
import constants
import log_parse
import file_management


def milestone_cleanup(data: pandas.DataFrame) -> (pandas.DataFrame, int):
    number_of_milestones = max(data["milestone_id"])
    data = data[data["reached"]]
    return data[["team_id", "name"]], number_of_milestones


def plotter(
    data: pandas.DataFrame,
    avg: float,
    height_of_bars: int,
    name: str,
    team: bool,
) -> None:
    plt.figure(figsize=(10, 6))
    names = {
        "column": "name",
        "label": "Milestone Count",
        "xlabel": "Milestone",
        "ylabel": "Number of teams that reached Milestone",
    }
    if team:
        names = {
            "column": "team_id",
            "label": "Time Count",
            "xlabel": "Teams",
            "ylabel": "Number of milestones team reached",
        }

    plt.bar(data[names["column"]], data["count"], color="skyblue", label=names["label"])

    plt.axhline(
        y=avg,
        color="orange",
        linestyle="--",
        label=f"Average {names['xlabel']} Reached",
    )

    plt.xlabel(names["xlabel"])
    plt.ylabel(names["ylabel"])
    plt.grid(axis="y")
    if team:
        plt.xticks(data[names["column"]])
        plt.title("Number of milestones reached by team")
    else:
        plt.xticks(data[names["column"]], rotation=90)
        plt.title("Number of teams that reached milestone")
    plt.yticks(range(0, int(max(data["count"]) + 1)))
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{name}_milestone_plot.png")
    file_management.save_plot(f"{name}_milestone_plot.png")


def plot_teams(data: pandas.DataFrame, number_of_milestones: int) -> None:
    data = data.groupby("team_id").size().reset_index(name="count")  
    if data.empty:
        return None
    avg = data["count"].mean()
    plotter(data, avg, number_of_milestones, "team", True)


def plot_milestones(data: pandas.DataFrame, number_of_teams: int, milestones: pandas.DataFrame) -> None:
    milestones = milestones["name"]
    data = data.groupby("name").size().reset_index(name="count")
    merged = pandas.merge(milestones, data, how='left')
    merged.fillna(0, inplace=True)
    merged['count'] = merged['count'].astype(int)
    data = merged.drop_duplicates()

    if data.empty:
        return None
    avg = data["count"].mean()
    plotter(data, avg, number_of_teams, "milestone", False)


def main(teams: int, plot: bool, csv: bool) -> pandas.DataFrame:
    milestone_data, number_of_milestones = milestone_cleanup(
        log_parse.get_merged_logs(teams, constants.MILESTONE_LOGS)
    )
    milestones = log_parse.get_logs(12, "exercise_milestones.jsonl", False)
    if plot:
        if not milestone_data.empty:
            plot_teams(milestone_data, number_of_milestones)
            plot_milestones(milestone_data, teams, milestones)
    if csv:
        data = milestone_data.groupby("name").size().reset_index(name="count")
        milestones = milestones["name"]
        merged = pandas.merge(milestones, data, how='left')
        merged.fillna(0, inplace=True)
        merged['count'] = merged['count'].astype(int)
        data = merged.drop_duplicates()
        data.to_csv("milestones_by_name.csv")
        file_management.save_csv("milestones_by_name.csv")
        data = milestone_data.groupby("team_id").size().reset_index(name="count")
        data.to_csv("milestones_by_team.csv")
        file_management.save_csv("milestones_by_team.csv")
    return milestone_data


if __name__ == "__main__":
    main(12, True, True)