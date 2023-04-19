# Invitation Management App Project
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project


#### Auth0 Setup

Environment variables:

```bash
export AUTH0_DOMAIN="{your_domain_name}.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="{your_api_audience}"
```

#### Database Setup
With Postgres running, restore a database using the `database.psql` file provided. In terminal run:

```bash
createdb invitdb
psql invitdb < database.psql
```

### Permissions

The following permissions are created under API settings.

* `post:invitation`
* `patch:invitation`
* `delete:invitation`
* `get:invitation-rsvps`
* `get:rsvp-details`
* `post:invitation-rsvp`
* `patch:invitation-rsvp`
* `delete:invitation-rsvp`

### Roles

Two roles are created for users under `Users & Roles` section in Auth0

* Admin:
    * Admin can manage invitations and have the following permissions:
        * `post:invitation`
        * `patch:invitation`
        * `delete:invitation`
        * `get:invitation-rsvps`
        * `get:invitation-rsvp-details`
* Guest:
    * Can perform GET operation on invitations, and CRUD operations on RSVP.
        * `get:invitation-rsvp-details`
        * `post:invitation-rsvp`
        * `patch:invitation-rsvp`
        * `delete:invitation-rsvp`


### Set JWT Tokens 

Use the following link to create users and sign them in. This way, you can generate 

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

#### Launching The App

1. Initialize and activate a virtualenv:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Configure database path to connect local postgres database in `models.py`

    ```python
    database_path = "postgres://{}@{}/{}".format('postgres:postgres', 'localhost:5432', 'invitdb')
    ```

4.  To run the server locally, execute:

    ```bash
    export FLASK_APP=flaskr
    export FLASK_DEBUG=True
    export FLASK_ENVIRONMENT=debug
    flask run --reload
    ```

## API Documentation

### Models
There are two database models:

    Invitation: Represents an Event invitation. 
        model attributes:
        id (primary key): Unique identifier for the invitation.
        name: Name of the invited guest.
        email: Email address of the invited guest.
        description: has the invitation text

    RSVP: Represents an RSVP response to an invitation. 
        model attributes:
        id (primary key): Unique identifier for the RSVP.
        invitation_id: Foreign key referencing the Invitation model.
        response: String representing the guest's response to the invitation (e.g. "Attending", "Not Attending", "Undecided").
        guest_name: Name of the guest who is responding to the invitation.
        guest_email: Email address of the guest who is responding to the invitation.
        plus_one: Boolean indicating whether the guest is bringing a plus one.

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 500: Internal Server Error

### Endpoints

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
