from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse

from app.constants import EMAIL_LABELS_LIST

import smtplib
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static/dist"), name="static")
app.mount("/assets", StaticFiles(directory="app/static/dist/assets"), name="assets")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("app/static/dist/index.html")
    
@app.get("/labels")        
async def get_labels():
    labels_list = list(EMAIL_LABELS_LIST.keys())
    return labels_list

@app.post("/submit/")
async def submit(
    email: str = Form(...),
    auth_code: str = Form(...),
    songname: str = Form(...),
    artists: str = Form(...),
    message: str = Form(...),
    selected_emails: str = Form(...),
):
    error_messages = []

    if not selected_emails:
        error_messages.append("No E-Mail selected!")
    if not songname:
        error_messages.append("No Song Name entered!")
    if not artists:
        error_messages.append("No Artist(s) entered!")
    if not message.strip():
        error_messages.append("No Message entered!")
    if not email:
        error_messages.append("No E-Mail address entered!")
    if not email.endswith("@gmail.com"):
        error_messages.append("Use a Gmail address (@gmail.com)!")

    if error_messages:
        return JSONResponse(content={"success": False, "errors": error_messages}, status_code=400)

    try:
        selected_emails_list = json.loads(selected_emails)
        logger.info("Selected emails successfully parsed.")
    except json.JSONDecodeError as e:
        logger.error("Failed to decode selected_emails JSON: %s", str(e))
        return JSONResponse(content={"success": False, "errors": ["Invalid format for selected emails."]}, status_code=400)

    labels_emails = [EMAIL_LABELS_LIST[label] for label in selected_emails_list if label in EMAIL_LABELS_LIST]

    if not labels_emails:
        logger.warning("No valid labels found in selected emails.")
        return JSONResponse(content={"success": False, "errors": ["No valid labels selected!"]}, status_code=400)

    logger.info("Preparing to send emails to: %s", labels_emails)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, auth_code)

        text = f"Subject: Demo Submission: {songname} - {artists}\n\n{message.strip()}"
        for mail in labels_emails:
            server.sendmail(email, mail, text)

        server.quit() 
        logger.info("Emails sent successfully.")
        return JSONResponse(content={"success": True, "message": "Email(s) sent!"})

    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP Authentication failed for email: %s", email)
        return JSONResponse(content={"success": False, "errors": ["Authentication failed. Check your email and password."]}, status_code=401)
    except smtplib.SMTPException as smtp_error:
        logger.error("SMTP error occurred: %s", str(smtp_error))
        return JSONResponse(content={"success": False, "errors": ["An error occurred while sending the email."]}, status_code=500)
    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))
        return JSONResponse(content={"success": False, "errors": ["An error occurred while processing your request. Please try again later."]}, status_code=500)
