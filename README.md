# Identity Reconciliation Backend
Submitted by: Aditya Jaiswal  
Task: Bitespeed Identity Reconciliation Backend Assignment

This is a FastAPI based backend that solves the identity reconciliation problem.  
The objective is to merge multiple records of a user based on email and phone number and return a single primary contact with all related secondary contacts.

## Live API URL  
https://cooperative-warmth-production-d455.up.railway.app/

## Repository  
https://github.com/adityajaiswal25/Identity-Reconciliation

---

## Problem Summary
The system determines if a new incoming request belongs to an existing user or a new one.  
If the email or phone number already exists in the database, the system merges them under one primary user.  
If both are new, a new primary record is created.

The system maintains:
- One primary contact for a user group  
- All other connected contacts as secondary  
- Proper merging when email and phone overlap across different users  

---

## API Endpoint

### POST /identify
Accepts email and phone from the request body.  
Detects if the user already exists and returns merged identity details.

#### Example Request

```
POST /identify
Content-Type: application/json

{
  "email": "test@gmail.com",
  "phone": "99999"
}
```

#### Example Response

```json
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["test@gmail.com"],
    "phoneNumbers": ["99999"],
    "secondaryContactIds": []
  }
}
```

---

## Reconciliation Logic (Simplified Overview)
1. Search for any contact matching the email or phone.
2. If none found, create a new primary contact.
3. If matches found, pick the smallest id as the primary.
4. Convert other conflicting primary contacts to secondary.
5. If new information arrives (new email or phone), create a secondary entry.
6. Output the merged identity:  
   - Primary ID  
   - All emails  
   - All phone numbers  
   - All secondary contact IDs  

---

## Database Schema

### contacts table
| Column | Type | Description |
|--------|------|-------------|
| `id` | Primary Key | Unique identifier for each contact |
| `email` | String | Email address |
| `phone` | String | Phone number |
| `linkedId` | Foreign Key | Reference to contacts.id for linking |
| `linkPrecedence` | Enum | Either 'primary' or 'secondary' |
| `createdAt` | Timestamp | Creation timestamp |
| `updatedAt` | Timestamp | Last update timestamp |
| `deletedAt` | Timestamp | Soft delete timestamp |

---

## How To Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/adityajaiswal25/Identity-Reconciliation.git
   cd Identity-Reconciliation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variable**
   ```bash
   export DATABASE_URL="your_postgres_url"
   ```

4. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Open Swagger Docs**
   Navigate to: http://127.0.0.1:8000/docs

---

## Deployment
The project is deployed on Railway.  
- `DATABASE_URL` is set using Railway PostgreSQL connection string  
- Database table was created manually using Railway SQL editor  

---

## Technology Stack
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Hosting**: Railway
- **API Documentation**: Swagger/OpenAPI

---

## Notes
- The project is built in simple FastAPI  
- Code follows a clean and understandable flow
- Focus is on correctness and clarity rather than complexity
- Fast identity reconciliation with efficient merging logic
