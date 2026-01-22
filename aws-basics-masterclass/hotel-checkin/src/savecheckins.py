import json
import os
import psycopg


def lambda_handler(event, context):
    body = json.loads(event["body"])

    conn = psycopg.connect(
        host=os.environ["DB_HOST"],
        dbname="hotel",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        port=5432,
    )

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO checkins
        (guest_name, email, booking_id, room_type, checkin_date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            body["name"],
            body["email"],
            body["bookingId"],
            body["roomType"],
            body["checkinDate"],
        ),
    )

    conn.commit()
    cur.close()
    conn.close()

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"message": "Check-in saved"})
    }