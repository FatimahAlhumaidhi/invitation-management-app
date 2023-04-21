# Invitation Management App Project
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project

the app is deployed [here](https://invitation-management-app.herokuapp.com/)

## App setup 

### Environment variables
create a .env file and save the following variables
```bash
AUTH0_DOMAIN={your_domain_name}.auth0.com
API_AUDIENCE={your_api_audience}
DATABASE_URL=postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...] #example: postgresql://postgres@localhost:5432/invitdb
```

### Database Setup
With Postgres running, create a database and optionally populate it with `database.psql` file provided by running:

```bash
createdb dbname
psql dbname < database.psql
```


### Set JWT Tokens 

use auth0 app URI format to get the JWT [example](https://dev-4ljjfs2dj2o7l6el.us.auth0.com/authorize?audience=apiv2&response_type=token&client_id=3Q6Za4vm6fTlqvkqgeDPOAkqmQuxtFC6&redirect_uri=http://localhost:5000)

```bash
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

#### Launching The App

1. Initialize and activate a virtual environment using python virtualenv:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the server locally:

    ```bash
    export FLASK_APP=flaskr
    export FLASK_DEBUG=True
    export FLASK_ENVIRONMENT=debug
    flask run --reload
    ```

## API Documentation

### Models
There are two database models to this app:

* Invitation: Represents an Event invitation. 
    * id (primary key): Unique identifier for the invitation.
    * name: Name of the host.
    * email: Email address of the host.
    * description: has the invitation text.

* RSVP: Represents an RSVP response to an invitation. 
    * id (primary key): Unique identifier for the RSVP.
    * invitation_id: Foreign key referencing the Invitation model.
    * response: String representing the guest's response to the invitation (e.g. "Attending", "Not Attending", "Undecided").
    * guest_name: Name of the guest who is responding to the invitation.
    * guest_email: Email address of the guest who is responding to the invitation.
    * plus_one: Boolean indicating whether the guest is bringing a plus one.


### Permissions

The following permissions are created under API settings.

* `post:invitation`
* `patch:invitation`
* `delete:invitation`
* `get:invitation-rsvps`
* `get:invitation-rsvp-details`
* `post:invitation-rsvp`
* `patch:invitation-rsvp`
* `delete:invitation-rsvp`

### Roles

Two roles are created for users under `Users & Roles` section in Auth0

* Admin:
    * represents a person that manages the invitations in the database
    * Admin have the following permissions:
        * `post:invitation`
        * `patch:invitation`
        * `delete:invitation`
        * `get:invitation-rsvps`
        * `get:invitation-rsvp-details`
* Guest:
    * represents a person that can respond to an invitation
    * Guest have the following permissions:
        * `get:invitation-rsvp-details`
        * `post:invitation-rsvp`
        * `patch:invitation-rsvp`
        * `delete:invitation-rsvp`

## API endpoints:

* `GET /invitations` 
    * Retrieves a list of all invitations.
* `GET /invitations/{id}`
    * Retrieves a single invitation by ID.
* `POST /invitations`
    * Creates a new invitation.
* `PATCH /invitations/{id}`
    * Updates an existing invitation by ID.
* `DELETE /invitations/{id}` 
    * Deletes an existing invitation by ID.
* `GET /invitations/{invitation_id}/rsvps`
    * Retrieves a list of all RSVPs for a specific invitation.
* `GET /invitations/{invitation_id}/rsvps/{id}`
    * Retrieves a single RSVP by ID.
* `POST /invitations/{invitation_id}/rsvps` 
    * Creates a new RSVP.
* `PATCH /invitations/{invitation_id}/rsvps/{id}` 
    * Updates an existing RSVP by ID.
* `DELETE /invitations/{invitation_id}/rsvps/{id}` 
    * Deletes an existing RSVP by ID.

## Endpoint Sample output

### Base URL
`http://localhost:5000`

### Error Handling
The application will return the following error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 422: Not Processable

Errors are returned as JSON objects in the following format:

```json
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```
### Endpoints

`GET /invitations`
- Returns a list of all invitations.
- Sample Request: 
```bash
curl -X GET \
    http://localhost:5000/invitations \
    -H 'Content-Type: application/json' 
```
- Sample response
```json
{
  "success": true,
  "invitations": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "description": "Please join us to celebrate our wedding."
    },
    {
      "id": 2,
      "name": "Jane Doe",
      "email": "jane@example.com",
      "description": "Please join us to celebrate our baby shower."
    }
  ]
}
```

`GET /invitations/int:id`
- Returns an invitation by id.
- Sample Request: 
```bash
curl -X GET \
    http://localhost:5000/invitations/1 \
    -H 'Content-Type: application/json' 
```
- Sample response
```json
{
  "success": true,
  "invitations": {
    "id": 1,
    "name": "John Smith",
    "email": "john@example.com",
    "description": "Please join us to celebrate our wedding."
  }
}
```

`POST /invitations`
- Create a new invitation.
- Sample Request:
```bash
curl -X POST\
    http://localhost:5000/invitations \
    -H 'Authorization: Bearer {$TOKEN}' \
    -H 'Content-Type: application/json' \
    -d '{"name":"John Smith", 
        "email":"john@example.com", 
        "description":"Please join us to celebrate our wedding."}'
```
- Sample response
```json
{
  "success": true,
  "invitations": {
    "id": 3,
    "name": "John Smith",
    "email": "john@example.com",
    "description": "Please join us to celebrate our wedding."
  }
}
```

`PATCH /invitations/int:id`
- Update an invitation by id.
- Sample Request:
```bash
curl -X PATCH \
    http://localhost:5000/invitations/1 \
    -H 'Authorization: Bearer {$TOKEN}' \
    -H 'Content-Type: application/json' \
    -d '{"name":"John Doe"}'
```
- Sample response
```json
{
  "success": true,
  "invitations": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "description": "Please join us to celebrate our wedding."
  }
}
```

`DELETE /invitations/int:id`
- Delete an invitation by id.
- Sample Request:
```bash
curl -X DELETE \
    http://localhost:5000/invitations/1 \
    -H 'Authorization: Bearer {$TOKEN}' \
    -H 'Content-Type: application/json' 
```
- Sample response
```json
{
  "success": true,
  "invitation_id": 1
}
```

`GET /invitations/int:invitation_id/rsvps`
- Get a list of RSVPs for an invitation by id.
- Sample Request:
```bash
curl -X GET \
    http://localhost:5000/invitations/1/rsvps \
    -H "Authorization: Bearer {$TOKEN}" \
    -H 'Content-Type: application/json' 
```
- Sample response
```json
{
  "success": true,
  "rsvps": [
    {
      "id": 1,
      "guest_name": "Mary Smith",
      "guest_email": "mary@example.com",
      "response": "Attending",
      "plus_one": true,
      "invitation_id": 1
    },
    {
      "id": 2,
      "guest_name": "Tom Jones",
      "guest_email": "tom@example.com",
      "response": "Not Attending",
      "plus_one": false,
      "invitation_id": 2
    }
  ]
}
```

`GET /invitations/int:invitation_id/rsvps/int:rsvp_id`
- Returns an rsvp by id.
- Sample Request: 
```bash
curl -X GET \
  http://localhost:5000/invitations/1/rsvps/1 \
  -H 'Authorization: Bearer {$TOKEN}' \
  -H 'Content-Type: application/json' 
```
- Sample Response:
```json
{
    "success": true, 
    "rsvps": {
        "guest_name": "John Doe", 
        "guest_email": "john.doe@gmail.com", 
        "response": "Attending", 
        "plus_one": "True"
    }
}
```

`POST /invitations/int:invitation_id/rsvps`
- Creates a new RSVP for the given invitation ID.
- Sample Request: 
```bash
curl -X POST \
  http://localhost:5000/invitations/1/rsvps \
  -H 'Authorization: Bearer {$TOKEN}' \
  -H 'Content-Type: application/json' \
  -d '{
	"guest_name": "Jane Smith",
	"guest_email": "jane.smith@example.com",
	"response": "Not Attending",
	"plus_one": false
    }'
```
- Sample Response:
```json
{
  "success": true,
  "rsvps": {
    "id": 2,
    "guest_name": "Jane Smith",
    "guest_email": "jane.smith@example.com",
    "response": "Not Attending",
    "plus_one": false,
    "invitation_id": 1
  }
}
```

`PATCH /invitations/int:invitation_id/rsvps/int:rsvp_id`
- Updates an existing RSVP for the given invitation ID and RSVP ID.
- Sample Request:
```bash
curl -X PATCH \
  http://localhost:5000/invitations/1/rsvps/1 \
  -H 'Authorization: Bearer {$TOKEN}' \
  -H 'Content-Type: application/json' \
  -d '{
	"guest_name": "John Smith",
	"guest_email": "john.smith@example.com",
	"response": "Not Attending",
	"plus_one": false
}'
```
- Sample Response:
```json
{
  "success": true,
  "rsvps": {
    "id": 1,
    "guest_name": "John Smith",
    "guest_email": "john.smith@example.com",
    "response": "Not Attending",
    "plus_one": false,
    "invitation_id": 1
  }
}
```

`DELETE /invitations/int:invitation_id/rsvps/int:rsvp_id`
- Deletes an existing RSVP for the given invitation ID and RSVP ID.
- Sample Request:
```bash
curl -X DELETE \
  http://localhost:5000/invitations/1/rsvps/1 \
  -H 'Authorization: Bearer {$TOKEN}' \
  -H 'Content-Type: application/json' 
```
- Sample Response:
```json
{
  "success": true,
  "rsvp_id": 1
}
```