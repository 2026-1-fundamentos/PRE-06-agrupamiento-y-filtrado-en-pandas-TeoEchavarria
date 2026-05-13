"""Homework solution: grouping and filtering with pandas."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "files" / "input"
OUTPUT_DIR = BASE_DIR / "files" / "output"
PLOTS_DIR = BASE_DIR / "files" / "plots"


def generate_outputs() -> None:
	"""Generate the summary CSV and the top-10 drivers plot."""

	drivers = pd.read_csv(INPUT_DIR / "drivers.csv")
	timesheet = pd.read_csv(INPUT_DIR / "timesheet.csv")

	summary = (
		timesheet.groupby("driverId", as_index=False)
		.agg({"hours-logged": "sum", "miles-logged": "sum"})
		.merge(drivers[["driverId", "name"]], on="driverId", how="left")
		.loc[:, ["driverId", "name", "hours-logged", "miles-logged"]]
		.sort_values("miles-logged", ascending=False)
	)

	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	summary.to_csv(OUTPUT_DIR / "summary.csv", index=False)

	top10 = summary.head(10)

	PLOTS_DIR.mkdir(parents=True, exist_ok=True)
	fig, ax = plt.subplots(figsize=(10, 6))
	ax.bar(top10["name"], top10["miles-logged"], color="#2f6f8f")
	ax.set_title("Top 10 Drivers by Miles Logged")
	ax.set_xlabel("Driver")
	ax.set_ylabel("Miles Logged")
	ax.tick_params(axis="x", labelrotation=45)
	fig.tight_layout()
	fig.savefig(PLOTS_DIR / "top10_drivers.png", dpi=150)
	plt.close(fig)


if __name__ == "__main__":
	generate_outputs()