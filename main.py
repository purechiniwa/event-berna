import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re

# MySQL connection
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

    submitted = st.form_submit_button("✅ Submit Event")

    if submitted:
        datetime_start_obj = datetime.combine(date_start, time_start)
        datetime_end_obj = datetime.combine(date_end, time_end)

        if datetime_end_obj < datetime_start_obj:
            st.error("❌ End date and time cannot be before start date and time.")
        else:
            datetime_start = datetime_start_obj.strftime("%Y-%m-%d %H:%M:%S")
            datetime_end = datetime_end_obj.strftime("%Y-%m-%d %H:%M:%S")

            # === Generate custom event_id ===
            # Take first letters of each word (lowercase)
            initials = ''.join([word[0] for word in description.split() if word.isalpha()]).lower()
            initials = re.sub(r'[^a-z]', '', initials)

            # Extract parts for formatting
            start_day = date_start.strftime("%d")
            start_month = date_start.strftime("%m")
            end_day = date_end.strftime("%d")
            year = date_end.strftime("%Y")

            # Build ID: ekm-11/11-09-2025
            event_id = f"{initials}-{start_day}/{start_month}-{end_day}-{year}"

            try:
                conn = create_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO event (event_id, description, date_start, date_end)
                    VALUES (%s, %s, %s, %s)
                """, (event_id, description, datetime_start, datetime_end))
                conn.commit()

                cursor.close()
                conn.close()

                st.success(f"✅ Event '{description}' berhasil dimasukkan! Event ID: {event_id}")

            except Error as e:
                st.error(f"❌ Insert error: {e}")
