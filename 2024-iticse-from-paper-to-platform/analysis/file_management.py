import os
import shutil
import constants


def save_plot(name: str) -> None:
    path = os.path.join(constants.PLOTS_FOLDER, name)
    if os.path.isfile(path):
        os.remove(path)
    shutil.move(name, os.path.join(constants.PLOTS_FOLDER))


def save_csv(name: str) -> None:
    path = os.path.join(constants.CSV_FOLDER, name)
    if os.path.isfile(path):
        os.remove(path)
    shutil.move(name, os.path.join(constants.CSV_FOLDER))
