# from fastapi import APIRouter, HTTPException
# from database import get_db_connection  # Import your DB connection function
# from models import URLRequest
# from utils import generate_short_url  # Import the missing function
# import psycopg2

# router = APIRouter()

# @router.post("/shorten")
# def shorten_url(request: URLRequest):
#     short_url = request.custom_alias if request.custom_alias else generate_short_url()

#     try:
#         conn = get_db_connection()  # Get a fresh DB connection
#         with conn.cursor() as cursor:  # Ensure a new cursor is created
#             cursor.execute(
#                 "INSERT INTO urls (long_url, short_url) VALUES (%s, %s) RETURNING short_url",
#                 (request.long_url, short_url),
#             )
#             conn.commit()  # Commit transaction
#         return {"short_url": short_url}

#     except psycopg2.Error as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

#     finally:
#         conn.close()  # Ensure the connection is always closed

#------------------------------example---------------------------
from fastapi import APIRouter, HTTPException
from database import get_db_connection  # Ensure this function is correctly implemented
from models import URLRequest
from utils import generate_short_url  # Ensure this function generates a short URL
import psycopg2
import validators  # For URL validation

router = APIRouter()

@router.post("/shorten")
def shorten_url(request: URLRequest):
    # Validate if long_url is a valid URL
    if not validators.url(request.long_url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    short_url = request.custom_alias if request.custom_alias else generate_short_url()

    try:
        conn = get_db_connection()  # Get a fresh DB connection
        with conn.cursor() as cursor:
            # Check if custom alias already exists
            if request.custom_alias:
                cursor.execute("SELECT 1 FROM urls WHERE short_url = %s", (short_url,))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="Custom alias already in use")

            # Insert the new short URL entry
            cursor.execute(
                "INSERT INTO urls (long_url, short_url) VALUES (%s, %s) RETURNING short_url",
                (request.long_url, short_url),
            )
            conn.commit()

        # Return the full shortened URL
        return {"short_url": f"http://127.0.0.1:8080/{short_url}"}

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        conn.close()  # Always close the DB connection

@router.get("/{short_url}")
def redirect_url(short_url: str):
    """Retrieve original long URL from DB using the short URL"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT long_url FROM urls WHERE short_url = %s", (short_url,))
            result = cursor.fetchone()
            if result:
                return {"long_url": result[0]}
            else:
                raise HTTPException(status_code=404, detail="Short URL not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        conn.close()

