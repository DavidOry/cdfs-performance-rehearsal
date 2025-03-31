import pandas as pd
from fpdf import FPDF
import os
from tabulate import tabulate
from datetime import time
import markdown
import pypandoc

# Read in input.xlsx
classes_data = pd.read_excel("input.xlsx", sheet_name="classes")
rehearsals_data = pd.read_excel("input.xlsx", sheet_name="rehearsals")

# Read in class-rosters.xlsx
class_rosters = pd.read_excel("class-rosters.xlsx")

# Create a folder to store the student schedules
if not os.path.exists("student-schedules"):
    os.makedirs("student-schedules")

# Loop through each unique student in the class-rosters file
for student in class_rosters["student"].unique():

    # Filter the class-rosters data to get the classes for this student
    student_classes = class_rosters[class_rosters["student"] == student][
        "class_name"
    ].tolist()

    # Filter the classes_data to get the classes for this student
    student_classes_data = classes_data[
        classes_data["class_name"].isin(student_classes)
    ]

    # student_classes_data = classes_data[
    #     classes_data["class_name"].apply(lambda x: any(sc in x for sc in student_classes))
    # ]

    # Filter the rehearsals_data to get the rehearsals for this student
    student_rehearsals_data = rehearsals_data[
        rehearsals_data["class_name"].isin(student_classes)
    ]

    # Add the URL to the name field in the rehearsals data
    student_rehearsals_data["name"] = student_rehearsals_data.apply(
        lambda row: f"[{row['name']}]({row['url']})" if row["url"] else row["name"],
        axis=1,
    )

    student_classes_data = student_classes_data.rename(
        columns={
            "class_name": "Class",
            "teacher": "Teacher",
            "assistant": "Assistant",
            "day_of_week": "Day",
            "time_of_day": "Time",
        }
    )

    student_classes_data.loc[:, "Time"] = student_classes_data["Time"].apply(
        lambda x: x.strftime("%I:%M %p") if pd.notnull(x) else ""
    )

    student_classes_data["Teacher"] = student_classes_data["Teacher"].fillna("")
    student_classes_data["Assistant"] = student_classes_data["Assistant"].fillna("")
    student_classes_data["Day"] = student_classes_data["Day"].fillna("")

    # Rehearsal data
    student_rehearsals_data.loc[:, "Date"] = student_rehearsals_data["date"].apply(
        lambda x: x.strftime("%B %d, %Y")
    )
    student_rehearsals_data.loc[:, "Start Time"] = student_rehearsals_data[
        "start_time"
    ].apply(lambda x: x.strftime("%I:%M %p"))
    student_rehearsals_data.loc[:, "End Time"] = student_rehearsals_data[
        "end_time"
    ].apply(lambda x: x.strftime("%I:%M %p"))
    student_rehearsals_data.loc[:, "Arrival Time"] = student_rehearsals_data[
        "arrival_time"
    ].apply(lambda x: x.strftime("%I:%M %p") if isinstance(x, time) else "")
    student_rehearsals_data = student_rehearsals_data[
        [
            "name",
            "Date",
            "class_name",
            "dance_name",
            "location",
            "Start Time",
            "End Time",
            "Arrival Time",
        ]
    ]
    student_rehearsals_data = student_rehearsals_data.rename(
        columns={
            "name": "Rehearsal",
            "location": "Location",
            "class_name": "Class",
            "dance_name": "Dance Name",
        }
    )

    student_rehearsals_data["Dance Name"] = student_rehearsals_data["Dance Name"].fillna("")

    with open(os.path.join("student-schedules", f"{student}.md"), "w") as f:
        f.write(f"# {student}\n\n")

        # Write a section heading for the classes
        f.write("## Classes\n\n")

        # Create a table from the tabulate library
        classes_table = tabulate(
            student_classes_data, headers="keys", tablefmt="markdown", showindex=False
        )

        # Write the classes table to the Markdown file
        f.write(classes_table)

        f.write("\n\n")

        # Write a section heading for the rehearsals
        f.write("## Rehearsals\n\n")

        student_rehearsals_data.sort_values(by=["Date", "Start Time"], inplace=True)

        # Create a table from the tabulate library
        rehearsals_table = tabulate(
            student_rehearsals_data,
            headers="keys",
            tablefmt="markdown",
            showindex=False,
            colalign=("left", "left", "left", "left", "left", "right", "right", "right"),
        )

        # Write the rehearsals table to the Markdown file
        f.write(rehearsals_table)
