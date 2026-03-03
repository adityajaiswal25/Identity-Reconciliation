# Identity Reconciliation Backend
Submitted by: Aditya Jaiswal  
Task: Identity Reconciliation Backend Assignment

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
## Real-time Benefits and Use Cases

### Benefits
- **Unified Customer Profile**: Consolidate fragmented customer data across multiple touchpoints into a single, authoritative record, enabling a 360-degree view of customer interactions and behavior.
- **Enhanced Data Quality**: Eliminate duplicate records and data inconsistencies, improving data integrity and reducing operational costs associated with managing redundant information.
- **Improved Customer Experience**: Enable personalized marketing, customer service, and communications by maintaining accurate customer identities across all channels.
- **Real-time Synchronization**: Instantly identify and merge duplicate contacts as new information arrives, ensuring database consistency without batch processing delays.
- **Scalability**: Handle high-volume identity matching efficiently with minimal latency, supporting businesses of all sizes.

### Use Cases
- **E-commerce Platforms**: Merge customer accounts when users register with different email addresses or phone numbers, preventing duplicate orders and ensuring consistent order history.
- **CRM Systems**: Consolidate customer records from multiple sales channels, ensuring unified communication and preventing duplicate outreach.
- **Financial Institutions**: Identify and merge duplicate customer accounts for KYC (Know Your Customer) compliance and fraud prevention.
- **Marketing Automation**: Maintain accurate contact lists by identifying and merging duplicate leads from various marketing campaigns and sources.
- **Multi-channel Retail**: Synchronize customer identities across online, mobile, and physical store interactions for seamless omnichannel experiences.
- **Healthcare Systems**: Link patient records across multiple healthcare providers using email and phone identifiers for better care coordination.
- **SaaS Platforms**: Prevent duplicate user accounts and ensure data consistency when users have multiple sign-up methods (email, phone, social login).

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
