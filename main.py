from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from database import get_connection
from auth import authenticate
from models import InsertRequest

app = FastAPI()

#
# Fixed predefined queries
#

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


def validate_filter(value: str):

    if len(value) > 50:
        raise HTTPException(
            status_code=400,
            detail="Filter too long"
        )

    if not value.replace(
        "_", ""
    ).replace(
        "-", ""
    ).isalnum():

        raise HTTPException(
            status_code=400,
            detail="Invalid filter value"
        )


@app.get("/health")
def health():

    return {
        "status": "UP"
    }


@app.get("/query/{query_id}")
def run_query(
        query_id: int,
        filter_value: str,
        user=Depends(authenticate)
):

    if query_id not in QUERIES:

        raise HTTPException(
            status_code=404,
            detail="Invalid query id"
        )

    validate_filter(filter_value)

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            QUERIES[query_id],
            [filter_value]
        )

        columns = [
            desc[0]
            for desc in cursor.description
        ]

        rows = cursor.fetchall()

        results = [
            dict(zip(columns, row))
            for row in rows
        ]

        return results

    finally:

        conn.close()


@app.post("/insert")
def insert_record(
        request: InsertRequest,
        user=Depends(authenticate)
):

    conn = get_connection()

    try:

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

        cursor = conn.cursor()

        cursor.execute(
            sql,
            [
                request.reference_number,
                str(request.entry_date),
                request.marker,
                request.status
            ]
        )

        conn.commit()

        return {
            "result": "success"
        }

    finally:

        conn.close()

