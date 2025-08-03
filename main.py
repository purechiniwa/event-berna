import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# MySQL connection function (reuse yours or import if modularized)
def create_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        ssl_verify_cert=False,
        ssl_disabled=False
    )

st.set_page_config(page_title="Event Entry", layout="centered")
st.title("📅 Event Input Form")

with st.form("event_form"):
    description = st.text_input("Event Description")
    date_start = st.date_input("Start Date")
    time_start = st.time_input("Start Time")
    date_end = st.date_input("End Date")
    time_end = st.time_input("End Time")

    submitted = st.form_submit_button("Submit Event")

    if submitted:
        # Combine date and time into datetime objects
        datetime_start_obj = datetime.combine(date_start, time_start)
        datetime_end_obj = datetime.combine(date_end, time_end)

        # Validate: End datetime must not be before start datetime
        if datetime_end_obj < datetime_start_obj:
            st.error("❌ End date and time cannot be before start date and time.")
        else:
            datetime_start = datetime_start_obj.strftime("%Y-%m-%d %H:%M:%S")
            datetime_end = datetime_end_obj.strftime("%Y-%m-%d %H:%M:%S")

            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO event (description, date_start, date_end)
                    VALUES (%s, %s, %s)
                """, (description, datetime_start, datetime_end))
                conn.commit()

                event_id = cursor.lastrowid  # get the inserted event_id

                cursor.close()
                conn.close()

                st.success(f"✅ Event '{description}' berhasil dimasukkan! dengan Event ID: {event_id}")
            except Error as e:
                st.error(f"❌ Insert error: {e}")
