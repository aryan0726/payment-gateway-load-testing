from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from datetime import datetime
import random

from app.database import SessionLocal, engine, Base
from app.models import Payment, TransactionLog

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# request model
class PaymentRequest(BaseModel):
    amount: float
    userId: int


# database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create payment
@app.post("/createPayment")
def create_payment(payment: PaymentRequest, db: Session = Depends(get_db)):

    if payment.amount <= 0:
        return {"error": "Invalid amount"}

    payment_id = str(uuid.uuid4())

    # retry mechanism
    success = False
    attempts = 0

    while attempts < 3:
        attempts += 1

        # simulate gateway failure
        if random.random() < 0.2:
            log = TransactionLog(
                payment_id=payment_id,
                action=f"PAYMENT_FAILED_ATTEMPT_{attempts}"
            )
            db.add(log)
            db.commit()
        else:
            success = True
            break

    if not success:
        return {"error": "Payment failed after retries"}

    new_payment = Payment(
        payment_id=payment_id,
        amount=payment.amount,
        user_id=payment.userId,
        status="SUCCESS",
        created_at=datetime.utcnow()
    )

    db.add(new_payment)
    db.commit()

    log = TransactionLog(
        payment_id=payment_id,
        action="PAYMENT_CREATED"
    )

    db.add(log)
    db.commit()

    return {
        "paymentId": payment_id,
        "status": "SUCCESS",
        "attempts": attempts
    }

# payment status
@app.get("/paymentStatus/{payment_id}")
def get_status(payment_id: str, db: Session = Depends(get_db)):

    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()

    if not payment:
        return {"error": "Payment not found"}

    return {
        "paymentId": payment.payment_id,
        "amount": payment.amount,
        "userId": payment.user_id,
        "status": payment.status,
        "createdAt": payment.created_at
    }


# refund payment
@app.post("/refund/{payment_id}")
def refund(payment_id: str, db: Session = Depends(get_db)):

    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()

    if not payment:
        return {"error": "Payment not found"}

    if payment.status != "SUCCESS":
        return {"error": "Refund not allowed"}

    payment.status = "REFUNDED"
    db.commit()

    log = TransactionLog(
        payment_id=payment_id,
        action="REFUND_INITIATED"
    )

    db.add(log)
    db.commit()

    return {"status": "REFUNDED"}