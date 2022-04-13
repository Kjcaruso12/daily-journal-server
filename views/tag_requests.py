import sqlite3
import json
from models import Tag

def get_all_tags():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            t.id,
            t.subject
        FROM Tags t
        """)

        # Initialize an empty list to hold all location representations
        tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Location class above.
            entry = Tag(row['id'], row['subject'])

            tags.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(tags)