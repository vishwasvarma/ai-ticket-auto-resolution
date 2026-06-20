from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Ticket
from backend.schemas import TicketCreateSchema
from model.ai_engine import solve_ticket
import random
import string
from backend.dependencies import get_current_user

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
def create_ticket(
    data: TicketCreateSchema,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:

        ticket_number = generate_ticket_number()

        ai_result = solve_ticket(data.description)

        print("AI RESULT:", ai_result)

        category = "Unknown"
        response = "No response"
        confidence = 0

        if isinstance(ai_result, dict):

            # Error case
            if "error" in ai_result:

                response = ai_result["error"]

            # Manual review case
            elif "response" in ai_result:

                category = ai_result.get("category", "Unknown")

                response = ai_result.get(
                    "response",
                    "Manual review required"
                )

                confidence = ai_result.get(
                    "confidence",
                    0
                )

            # Normal AI case
            elif "user_view" in ai_result:

                category = ai_result["user_view"].get(
                    "category",
                    "Unknown"
                )

                response = ai_result["user_view"].get(
                    "response",
                    "No response generated"
                )

                confidence = ai_result["internal"].get(
                    "confidence",
                    0
                )

        status = decide_status(float(confidence))

        new_ticket = Ticket(
            ticket_number=ticket_number,
            title=data.title,
            description=data.description,
            category=category,
            response=response,
            status=status,
            user_id=current_user.id
        )

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        return {

            "ticket_number": ticket_number,

            "title": data.title,

            "category": category,

            "response": response,

            "status": status

        }

    except Exception as e:

        return {

            "error": str(e)

        }

@router.get("")
def get_tickets(
    status: str = Query(None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "ADMIN":
        return {"error": "Access denied. Admins only."}

    query = db.query(Ticket)

    if status:
        query = query.filter(Ticket.status == status)

    tickets = query.all()

    return [
        {
            "ticket_number": t.ticket_number,
            "title": t.title,
            "category": t.category,
            "status": t.status
        }
        for t in tickets
    ]



@router.get("/my")
def get_my_tickets(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tickets = db.query(Ticket).filter(Ticket.user_id == current_user.id).all()

    return [
        {
            "ticket_number": t.ticket_number,
            "title": t.title,
            "category": t.category,
            "status": t.status
        }
        for t in tickets
    ]


@router.get("/{ticket_number}")
def get_ticket(
    ticket_number: str,
    db: Session = Depends(get_db)
):
    t = db.query(Ticket).filter(Ticket.ticket_number == ticket_number).first()

    if not t:
        return {"error": "Ticket not found"}

    return {
        "ticket_number": t.ticket_number,
        "title": t.title,
        "description": t.description,
        "category": t.category,
        "response": t.response,
        "status": t.status
    }


@router.patch("/{ticket_number}")
def update_ticket(
    ticket_number: str,
    response: str,
    status: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "ADMIN":
        return {"error": "Access denied. Admins only."}

    ticket = db.query(Ticket).filter(Ticket.ticket_number == ticket_number).first()

    if not ticket:
        return {"error": "Ticket not found"}

    ticket.response = response
    ticket.status = status

    db.commit()
    db.refresh(ticket)

    return {"message": "Ticket updated successfully"}