from datetime import datetime
import re

from flask import Flask
from flask import request
from flask import jsonify

from auth import requires_auth
from database import get_connection
from config import ALLOWED_STATUS

app = Flask(__name__)

QUERIES = {

    1: """
       SELECT *
       FROM customer
       WHERE customer_id = ?
       """,

    2: """
       SELECT *
       FROM orders
       WHERE order_id = ?
       """,

    3: """
       SELECT *
       FROM products
       WHERE product_code = ?
       """,

    4: """
       SELECT *
       FROM invoices
       WHERE invoice_no = ?
       """,

    5: """
       SELECT *
       FROM shipments
       WHERE shipment_id = ?
       """,

    6: """
       SELECT *
       FROM accounts
       WHERE account_no = ?
       """,

    7: """
       SELECT *
       FROM status_table
       WHERE status = ?
       """
}


def validate_filter(value):

    if value is None:
        raise ValueError("Missing filter")

    if len(value) > 50:
        raise ValueError("Filter too long")

    if not re.match(
        r'^[A-Za-z0-9_-]+$',
        value
    ):
        raise ValueError(
            "Invalid filter value"
        )


def validate_insert(data):

    required = [
        "reference_number",
        "entry_date",
        "marker",
        "status"
    ]

    for field in required:

        if field not in data:
            raise ValueError(
                f"Missing field {field}"
            )

    if len(data["reference_number"]) > 30:
        raise ValueError(
            "reference_number too long"
        )

    if len(data["marker"]) > 20:
        raise ValueError(
            "marker too long"
        )

    if data["status"] not in ALLOWED_STATUS:
        raise ValueError(
            "Invalid status"
        )

    datetime.strptime(
        data["entry_date"],
        "%Y-%m-%d"
    )


@app.route("/health")
def health():

    return jsonify({
        "status": "UP"
    })


@app.route(
    "/query/<int:query_id>",
    methods=["GET"]
)
@requires_auth
def run_query(query_id):

    if query_id not in QUERIES:

        return jsonify({
            "error":
            "Invalid query id"
        }), 404

    try:

        filter_value = request.args.get(
            "filter"
        )

        validate_filter(
            filter_value
        )

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            QUERIES[query_id],
            [filter_value]
        )

        columns = [
            col[0]
            for col in cursor.description
        ]

        rows = cursor.fetchall()

        result = []

        for row in rows:

            result.append(
                dict(
                    zip(columns, row)
                )
            )

        return jsonify(result)

    except Exception as ex:

        return jsonify({
            "error": str(ex)
        }), 400

    finally:

        try:
            conn.close()
        except:
            pass


@app.route(
    "/insert",
    methods=["POST"]
)
@requires_auth
def insert_record():

    try:

        data = request.get_json()

        validate_insert(data)

        sql = """
            INSERT INTO target_table
            (
                reference_number,
                entry_date,
                marker,
                status
            )
            VALUES
            (
                ?, ?, ?, ?
            )
        """

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            sql,
            [
                data["reference_number"],
                data["entry_date"],
                data["marker"],
                data["status"]
            ]
        )

        conn.commit()

        return jsonify({
            "status": "SUCCESS"
        })

    except Exception as ex:

        return jsonify({
            "error": str(ex)
        }), 400

    finally:

        try:
            conn.close()
        except:
            pass


if __name__ == "__main__":

    app.run()
