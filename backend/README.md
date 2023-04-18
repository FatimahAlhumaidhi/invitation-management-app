## API models:

    Invitation: Represents a wedding invitation. 
        model attributes:
        id (primary key): Unique identifier for the invitation.
        name: Name of the invited guest.
        email: Email address of the invited guest.
        plus_one: Boolean indicating whether the guest is allowed to bring a plus one.

    RSVP: Represents an RSVP response to a wedding invitation. 
        model attributes:
        id (primary key): Unique identifier for the RSVP.
        invitation_id: Foreign key referencing the Invitation model.
        response: String representing the guest's response to the invitation (e.g. "Attending", "Not Attending", "Undecided").
        guest_name: Name of the guest who is responding to the invitation.
        guest_email: Email address of the guest who is responding to the invitation.

## API endpoints:

    GET /invitations: Retrieves a list of all invitations.
    GET /invitations/{id}: Retrieves a single invitation by ID.
    POST /invitations: Creates a new invitation.
    PATCH /invitations/{id}: Updates an existing invitation by ID.
    DELETE /invitations/{id}: Deletes an existing invitation by ID.
    GET /invitations/{invitation_id}/rsvps: Retrieves a list of all RSVPs for a specific invitation.
    GET /invitations/{invitation_id}/rsvps/{id}: Retrieves a single RSVP by ID.
    POST /invitations/{invitation_id}/rsvps: Creates a new RSVP.
    PATCH /invitations/{invitation_id}/rsvps/{id}: Updates an existing RSVP by ID.
    DELETE /invitations/{invitation_id}/rsvps/{id}: Deletes an existing RSVP by ID.


## API roles:

    guest: Can perform GET operations on invitations, and CRUD operation on guest's specific RSVP.
    admin: Can perform all CRUD (create, read, update, delete) operations on invitations and the RSVPs associated with those invitations.

## API Permissions:

    GET:invitations: Guest and admin.
    GET:invitations-id: Guest and admin.
    POST:invitations: Admin.
    PATCH:invitations-id: Admin.
    DELETE:invitations-id: Admin.
    GET:invitations-id-rsvps: Admin.
    GET:invitations-id-rsvps-id: Guest and admin.
    POST:invitations-id-rsvps: Guest and admin.
    PATCH:invitations-id-rsvps-id: Guest and Admin.
    DELETE:invitations-id-rsvps-id: Guest and Admin.
