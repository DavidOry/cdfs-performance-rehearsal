import streamlit as st
import pandas as pd
from datetime import datetime, time

st.set_page_config(
    page_title="Rehearsal Helper", page_icon="https://www.cdandfs.com/favicon.ico"
)

# Read data from XLSX file
classes_data = pd.read_excel("input.xlsx", sheet_name="classes")
rehearsals_data = pd.read_excel("input.xlsx", sheet_name="rehearsals")

# Main app
st.title("CDF&S May Performance Rehearsal Helper")

# Get user input for class name
class_name_list = classes_data['class_name'].apply(lambda x: x.split(' -- ')[0] if ' -- ' in x else x).unique()
class_name = st.selectbox("Enter class name", [""] + class_name_list.tolist())

# Filter data based on user input
if class_name:
    classes_match = classes_data[
        classes_data["class_name"].str.contains(class_name, case=False)
    ]
    rehearsals_match = rehearsals_data[
        rehearsals_data["class_name"].str.contains(class_name, case=False)
    ]

    # Display classes data
    if not classes_match.empty:
        st.write("Class Information:")
        st.dataframe(
            classes_match.rename(
                columns={
                    "class_name": "Class Name",
                    "teacher": "Teacher",
                    "assistant": "Assistant",
                    "day_of_week": "Class Day of Week",
                    "time_of_day": "Class Time",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    # Display rehearsals data with download buttons
    if not rehearsals_match.empty:
        st.write("Rehearsals:")
        rehearsals_table = rehearsals_match.copy()
        rehearsals_table["Date"] = rehearsals_table["date"].apply(
            lambda x: x.strftime("%B %d, %Y")
        )
        rehearsals_table["Start Time"] = rehearsals_table["start_time"].apply(
            lambda x: x.strftime("%I:%M %p")
        )
        rehearsals_table["End Time"] = rehearsals_table["end_time"].apply(
            lambda x: x.strftime("%I:%M %p")
        )
        rehearsals_table["Arrival Time"] = rehearsals_table["arrival_time"].apply(
            lambda x: x.strftime("%I:%M %p") if isinstance(x, time) else ""
        )
        rehearsals_table["name"] = rehearsals_table.apply(
            lambda row: f"[{row['name']}]({row['url']})" if row["url"] else row["name"],
            axis=1,
        )
        rehearsals_table = rehearsals_table[
            [
                "name",
                "Date",
                "class_name",
                "location",
                "Start Time",
                "End Time",
                "Arrival Time",
                "information",
            ]
        ]
        rehearsals_table = rehearsals_table.rename(
            columns={
                "name": "Rehearsal",
                "location": "Location",
                "class_name": "Class",
                "information": "Information",
            }
        )
        rehearsals_table["Information"] = rehearsals_table["Information"].fillna("")
        st.markdown(rehearsals_table.to_markdown(index=False))
