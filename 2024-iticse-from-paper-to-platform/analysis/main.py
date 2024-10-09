import correct_tool_usage
import exercise_completion
import milestone_time
import milestones_count
import tool_usage
import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("teams", metavar="N", type=int, help="number of teams")
    parser.add_argument(
        "-p", "--plot", help="exports plots of analytics", action="store_true"
    )
    parser.add_argument(
        "-c", "--csv", help="export csv files from data", action="store_true"
    )
    parser.add_argument(
        "--correct", help="only correct tool analytics", action="store_true"
    )
    parser.add_argument(
        "--completed", help="only exercise completed analytics", action="store_true"
    )
    parser.add_argument(
        "--time", help="only milestone reach time analytics", action="store_true"
    )
    parser.add_argument(
        "--count", help="only milestone count analytics", action="store_true"
    )
    parser.add_argument(
        "--usage", help="only tool usage analytics", action="store_true"
    )
    parser.add_argument(
        "-a", "--all", help="will do all analytics", action="store_true"
    )
    args = parser.parse_args()

    if args.all:
        args.correct = True
        args.completed = True
        args.time = True
        args.count = True
        args.usage = True

    if args.plot and not os.path.isdir(os.path.join("..", "plots")):
        os.makedirs(os.path.join("..", "plots"))
    if args.csv and not os.path.isdir(os.path.join("..", "data")):
        os.makedirs(os.path.join("..", "data"))
    if args.correct:
        correct_tool_usage.main(args.teams, args.plot, args.csv)
    if args.completed:
        exercise_completion.main(args.teams, args.plot, args.csv)
    if args.time:
        milestone_time.main(args.teams, args.plot, args.csv)
    if args.count:
        milestones_count.main(args.teams, args.plot, args.csv)
    if args.usage:
        tool_usage.main(args.teams, args.plot, args.csv)


if __name__ == "__main__":
    main()
