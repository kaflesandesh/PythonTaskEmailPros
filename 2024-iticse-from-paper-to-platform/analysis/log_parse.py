import os
import pandas
from typing import Dict, List


def read_logs(team_number: int, log_file: str, teams: bool) -> pandas.DataFrame:
    path = os.path.join("..", "logs", log_file)
    if teams:
        path = os.path.join("..", "logs", f"team-{team_number}", log_file)
    with open(path) as logs_file:
        logs = pandas.read_json(logs_file, lines=True)
    if teams:
        logs["team_id"] = team_number
    return logs


def get_logs(number_of_teams: int, log_file: str, teams: bool) -> pandas.DataFrame:
    path = os.path.join("..", "logs")
    team_num = min(
        [
            int(folder.split("-")[1])
            for folder in os.listdir(path)
            if os.path.isdir(os.path.join(path, folder))
        ]
    )
    data = read_logs(team_num, log_file, teams)
    for i in range(1 + team_num, number_of_teams + team_num):
        data = pandas.concat([data, read_logs(i, log_file, teams)])
    return data


def get_merged_logs(
    number_of_teams: int, log_files: Dict[str, List[str]]
) -> pandas.DataFrame:
    team_df = []
    overall_df = []
    for key, files in log_files.items():
        if key == "teams":
            for file in files:
                team_df.append(get_logs(number_of_teams, file, True))
        else:
            for file in files:
                overall_df.append(read_logs(0, file, False))
    team_df = pandas.concat(team_df)
    overall_df = pandas.concat(overall_df)
    return pandas.merge(team_df, overall_df)
