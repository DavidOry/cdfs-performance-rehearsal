import streamlit as st
import pandas as pd
from datetime import datetime, time

# Read data from XLSX file
classes_data = pd.read_excel('input.xlsx', sheet_name='classes')
rehearsals_data = pd.read_excel('input.xlsx', sheet_name='rehearsals')

# Create a function to create a calendar invite file
def create_calendar_invite(event_data):
    cal = icalendar.Calendar()
    event = icalendar.Event()
    event.add('summary', event_data['name'])
    event.add('description', event_data['information'])
    start_time = datetime.combine(event_data['date'], event_data['start_time'])
    end_time = datetime.combine(event_data['date'], event_data['end_time'])
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    cal.add_component(event)
    return cal.to_ical()

# Main app
st.title("CDF&S May Performance Rehearsal Helper")

# Get user input for class name
class_name = st.text_input("Enter class name")

# Filter data based on user input
if class_name:
    classes_match = classes_data[classes_data['class_name'].str.contains(class_name, case=False)]
    rehearsals_match = rehearsals_data[rehearsals_data['class_name'].str.contains(class_name, case=False)]

    # Display classes data
    if not classes_match.empty:
        st.write("Class Information:")
        st.dataframe(classes_match.rename(columns={
            'class_name': 'Class Name', 
            'teacher': 'Teacher', 
            'assistant': 'Assistant', 
            'day_of_week': 'Class Day of Week', 
            'time_of_day': 'Class Time'
        }), use_container_width=True, hide_index=True)

    # Display rehearsals data with download buttons
    if not rehearsals_match.empty:
        st.write("Rehearsals:")
        rehearsals_table = rehearsals_match.copy()
        rehearsals_table['Date'] = rehearsals_table['date'].apply(lambda x: x.strftime('%B %d, %Y'))
        rehearsals_table['Start Time'] = rehearsals_table['start_time'].apply(lambda x: x.strftime('%I:%M %p'))
        rehearsals_table['End Time'] = rehearsals_table['end_time'].apply(lambda x: x.strftime('%I:%M %p'))
        rehearsals_table['Arrival Time'] = rehearsals_table['arrival_time'].apply(lambda x: x.strftime('%I:%M %p') if isinstance(x, time) else '')
        rehearsals_table = rehearsals_table[['name', 'Date', 'Start Time', 'End Time', 'Arrival Time', 'information']]
        rehearsals_table = rehearsals_table.rename(columns={'name': 'Rehearsal', 'information': 'Information'})
        st.dataframe(rehearsals_table, use_container_width=True, hide_index=True)
