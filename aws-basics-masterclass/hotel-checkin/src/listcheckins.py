import json
import psycopg
import os

def lambda_handler(event, context):
    conn = psycopg.connect(
        host=os.environ['DB_HOST'],
        dbname='hotel',
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        port=5432
    )

    cur = conn.cursor()
    cur.execute("""
        SELECT guest_name, email, booking_id, room_type, checkin_date
        FROM checkins
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "name": r[0],
            "email": r[1],
            "bookingId": r[2],
            "room": r[3],
            "date": str(r[4])
        })

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(result)
    }