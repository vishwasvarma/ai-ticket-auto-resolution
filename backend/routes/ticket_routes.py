from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Ticket
from backend.schemas import TicketCreateSchema
from model.ai_engine import solve_ticket
import random
import string

router = APIRouter(prefix="/tickets", tags=["Tickets"])


def generate_ticket_number():
    return "TCK" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def decide_status(confidence):
    if confidence >= 55:
        return "resolved"
    elif confidence >= 40:
        return "open"
    else:
        return "needs_attention"


@router.post("/create")
def create_ticket(data: TicketCreateSchema, db: Session = Depends(get_db)):

    try:
        ticket_number = generate_ticket_number()

        ai_result = solve_ticket(data.description)

        category = "Unknown"
        response = "No response"
        confidence = 0

        if isinstance(ai_result, dict):
            category = ai_result.get("category", "Unknown")
            response = ai_result.get("response", "No response")

            confidence = (
                ai_result.get("Confidence Score")
                or ai_result.get("confidence")
                or 0
            )

        status = decide_status(float(confidence))

        new_ticket = Ticket(
            ticket_number=ticket_number,
            title=data.title,
            description=data.description,
            category=str(category),
            response=str(response),
            status=status
        )

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

        return {
            "ticket_number": ticket_number,
            "category": category,
            "response": response
        }

    except Exception as e:
        return {"error": str(e)}


@router.get("")
def get_tickets(
    status: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Ticket)

    if status:
        query = query.filter(Ticket.status == status)

    return query.all()


@router.get("/{ticket_number}")
def get_ticket(ticket_number: str, db: Session = Depends(get_db)):
    return db.query(Ticket).filter(Ticket.ticket_number == ticket_number).first()


@router.patch("/{ticket_number}")
def update_ticket(ticket_number: str, response: str, status: str, db: Session = Depends(get_db)):

    ticket = db.query(Ticket).filter(Ticket.ticket_number == ticket_number).first()

    if not ticket:
        return {"error": "Ticket not found"}

    ticket.response = response
    ticket.status = status

    db.commit()
    db.refresh(ticket)

    return {"message": "Ticket updated successfully"}