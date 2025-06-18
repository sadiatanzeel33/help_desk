import sqlite3
from datetime import datetime
import json
import requests

# Microsoft Teams Webhook URL
TEAMS_WEBHOOK_URL = "https://outlook.office.com/webhook/..."  # ← Replace with your actual webhook URL

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            issue TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Insert a new ticket into the database
def insert_ticket(name, email, department, issue):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (name, email, department, issue, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, department, issue, created_at))
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Send auto-responder notification
    send_teams_notification(name, email, department, issue, ticket_id)

    return ticket_id

# Fetch all tickets from the database
def get_all_tickets():
    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Send auto response to Microsoft Teams
def send_teams_notification(name, email, department, issue, ticket_id):
    message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "New Help Desk Ticket",
        "themeColor": "0076D7",
        "title": f"🎫 New Ticket #{ticket_id}",
        "sections": [{
            "facts": [
                {"name": "Name:", "value": name},
                {"name": "Email:", "value": email},
                {"name": "Department:", "value": department},
                {"name": "Issue:", "value": issue},
                {"name": "Ticket ID:", "value": str(ticket_id)},
                {"name": "Time:", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            ]
        }]
    }

    headers = {'Content-Type': 'application/json'}
    try:
        requests.post(TEAMS_WEBHOOK_URL, headers=headers, data=json.dumps(message))
    except Exception as e:
        print("Failed to send Teams notification:", e)


