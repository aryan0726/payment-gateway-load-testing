# Payment Gateway Load Testing System

## Overview
This project simulates a payment gateway backend system and performs load testing to evaluate its performance under concurrent requests.

The system provides APIs to create payments, check payment status, and process refunds while maintaining transaction logs and retry mechanisms.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Apache JMeter

## Features

- Payment Creation API
- Payment Status API
- Refund API
- Retry mechanism for failed payment attempts
- Transaction logging
- Load testing using Apache JMeter

## API Endpoints

### Create Payment
POST /createPayment

Example Request

{
"amount": 500,
"userId": 101
}


### Get Payment Status
GET /paymentStatus/{payment_id}

### Refund Payment
POST /refund/{payment_id}

## Project Structure
payment-gateway-load-testing
│
├── app
│ ├── main.py
│ ├── database.py
│ └── models.py
│
├── test-cases
│ └── manual_test_cases.txt
│
├── requirements.txt
└── .gitignore


## Load Testing

Apache JMeter was used to simulate concurrent requests.

Test configuration:

- Threads: 100
- Ramp-up period: 10 seconds
- Loop count: 50
- Total requests: 15,000

Result:

- 0% error rate
- ~700+ requests/sec throughput

## Author

Aryan Raj
