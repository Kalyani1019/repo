# from fastapi import FastAPI, Request, HTTPException
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# import random
# import string

# app = FastAPI()

# # Mount the "templates" directory to serve static files
# app.mount("/static", StaticFiles(directory="templates"), name="static")

# # Dictionary to store short URL mappings
# url_mapping = {}

# class URLRequest(BaseModel):
#     url: str

# def generate_short_code(length=6):
#     """Generate a random short URL code"""
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# @app.get("/", response_class=HTMLResponse)
# async def home():
#     """Serve the HTML page"""
#     try:
#         with open("templates/index.html", "r") as file:
#             html_content = file.read()
#         return HTMLResponse(content=html_content)
#     except FileNotFoundError:
#         return HTMLResponse(content="<h1>index.html not found in templates/</h1>", status_code=404)

# @app.post("/shorten")
# async def shorten_url(request: URLRequest):
#     """Endpoint to shorten a URL"""
#     short_code = generate_short_code()
#     url_mapping[short_code] = request.url
#     return {"shortened_url": f"http://127.0.0.1:8000/{short_code}"}

# @app.get("/{short_code}")
# async def redirect_to_url(short_code: str):
#     """Redirect a short URL to its original URL"""
#     if short_code in url_mapping:
#         return RedirectResponse(url_mapping[short_code])
#     raise HTTPException(status_code=404, detail="Short URL not found")




from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random
import string

app = FastAPI()

# Mount the "templates" directory to serve static files
app.mount("/static", StaticFiles(directory="templates"), name="static")

# Dictionary to store short URL mappings and hit counts
url_mapping = {}
url_hits = {}  # Stores the number of times a short URL is accessed

class URLRequest(BaseModel):
    url: str

def generate_short_code(length=6):
    """Generate a random short URL code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the HTML page"""
    try:
        with open("templates/index.html", "r") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html not found in templates/</h1>", status_code=404)

@app.post("/shorten")
async def shorten_url(request: URLRequest):
    """Endpoint to shorten a URL"""
    short_code = generate_short_code()
    url_mapping[short_code] = request.url
    url_hits[short_code] = 0  # Initialize hit count
    return {"shortened_url": f"http://127.0.0.1:8000/{short_code}"}

@app.get("/{short_code}")
async def redirect_to_url(short_code: str):
    """Redirect a short URL to its original URL and count hits"""
    if short_code in url_mapping:
        url_hits[short_code] += 1  # Increment hit count
        return RedirectResponse(url_mapping[short_code])
    raise HTTPException(status_code=404, detail="Short URL not found")

@app.get("/stats/{short_code}")
async def get_url_stats(short_code: str):
    """Return the number of times the short URL has been accessed"""
    if short_code in url_hits:
        return {"short_code": short_code, "hits": url_hits[short_code]}
    raise HTTPException(status_code=404, detail="Short URL not found")

