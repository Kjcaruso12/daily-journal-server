import sqlite3
import json
from models import JournalEntry, Mood, Tag, EntryTag, entry_tag

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId,
            m.label
        FROM JournalEntries e
        JOIN Moods m
            ON m.id = e.moodId
        """)

        # Initialize an empty list to hold all location representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            rowId = row['id']

            db_cursor.execute("""
            SELECT
                t.id,
                t.subject
            FROM EntryTags et
            JOIN Tags t
                ON t.id = et.tag_id
            JOIN Journalentries e
                ON e.id = ?
            WHERE et.entry_id = e.id
            GROUP BY t.id
            """, ( rowId, ))

            data = db_cursor.fetchall()

            tags = []

            for current_tag in data:

                tag = Tag(current_tag['id'], current_tag['subject'])

                tags.append(tag.__dict__)

            entry = JournalEntry(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])

            mood = Mood(row['moodId'], row['label'])

            entry.mood = mood.__dict__

            entry.tags = tags

            entries.append(entry.__dict__)


    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId,
            m.label
        FROM JournalEntries e
        JOIN Moods m
            ON m.id = e.moodId
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Iterate list of data returned from database

        db_cursor.execute("""
        SELECT
            t.id,
            t.subject
        FROM EntryTags et
        JOIN Tags t
            ON t.id = et.tag_id
        JOIN Journalentries e
            ON e.id = ?
        WHERE et.entry_id = e.id
        GROUP BY t.id
        """, ( id, ))

        data2 = db_cursor.fetchall()

        tags = []

        for current_tag in data2:

            tag = Tag(current_tag['id'], current_tag['subject'])

            tags.append(tag.__dict__)

        # Create a location instance from the current row
        entry = JournalEntry(data['id'], data['concept'], data['entry'], data['date'], data['moodId'])

        mood = Mood(data['moodId'], data['label'])

        entry.mood = mood.__dict__

        entry.tags = tags

    return json.dumps(entry.__dict__)


def get_entries_by_query(text):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId
        FROM JournalEntries e
        WHERE e.entry LIKE ?
        """, ( '%' + text +  '%', ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = JournalEntry(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])

            entries.append(entry.__dict__)

    return json.dumps(entries)


def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO JournalEntries
            ( concept, entry, date, moodId )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['moodId'] ))

        id = db_cursor.lastrowid

        new_entry['id'] = id

        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO EntryTags
                ( entry_Id, tag_id )
            VALUES
                ( ?, ? );
            """, (id, tag))


    return json.dumps(new_entry)


def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM JournalEntries
        WHERE id = ?
        """, (id, ))

def update_entry(id, new_entry):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE JournalEntry
            SET
                concept = ?,
                entry = ?,
                date = ?,
                moodId = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['date'], new_entry['moodId']
              , id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True