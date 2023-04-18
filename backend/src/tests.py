import unittest
import json
from app import app, db
from .database.models import Invitation, RSVP

class WeddingInvitationTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()
        self.app.testing = True
        self.invitation = {"name": "John Doe", "email": "johndoe@gmail.com", "plus_one": True}
        self.rsvp = {"response": "Attending", "guest_name": "Jane Smith", "guest_email": "janesmith@gmail.com"}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_create_invitation(self):
        """Test API can create an invitation (POST request)"""
        res = self.app.post('/invitations', json=self.invitation)
        self.assertEqual(res.status_code, 201)

    def test_get_all_invitations(self):
        """Test API can get a list of all invitations (GET request)"""
        res = self.app.get('/invitations')
        self.assertEqual(res.status_code, 200)

    def test_get_invitation_by_id(self):
        """Test API can get a single invitation by ID (GET request)"""
        invitation = Invitation(name="John Doe", email="johndoe@gmail.com", plus_one=True)
        invitation.insert()
        res = self.app.get(f'/invitations/{invitation.id}')
        self.assertEqual(res.status_code, 200)

    def test_update_invitation(self):
        """Test API can update an existing invitation (PATCH request)"""
        invitation = Invitation(name="John Doe", email="johndoe@gmail.com", plus_one=True)
        invitation.insert()
        res = self.app.patch(f'/invitations/{invitation.id}', json={"plus_one": False})
        self.assertEqual(res.status_code, 200)

    def test_delete_invitation(self):
        """Test API can delete an existing invitation (DELETE request)"""
        invitation = Invitation(name="John Doe", email="johndoe@gmail.com", plus_one=True)
        invitation.insert()
        res = self.app.delete(f'/invitations/{invitation.id}')
        self.assertEqual(res.status_code, 200)

    def test_create_rsvp(self):
        """Test API can create an RSVP (POST request)"""
        invitation = Invitation(name="John Doe", email="johndoe@gmail.com", plus_one=True)
        invitation.insert()
        res = self.app.post(f'/invitations/{invitation.id}/rsvps', json=self.rsvp)
        self.assertEqual(res.status_code, 201)

    def test_get_all_rsvps_for_invitation(self):
        """Test API can get a list of all RSVPs for an invitation (GET request)"""
        invitation = Invitation(name="John Doe", email="johndoe@gmail.com", plus_one=True)
        invitation.insert()
        rsvp = RSVP(response="Attending", guest_name="Jane Smith", guest_email="janesmith@gmail.com")
        rsvp.invitation_id = invitation.id
        rsvp.insert()
        res = self.app.get(f'/invitations/{invitation.id}/rsvps')
        self.assertEqual(res.status_code, 200)

    def test_create_rsvp(self):
        invitation = Invitation(name='John Doe', email='johndoe@example.com', plus_one=True)
        db.session.add(invitation)
        db.session.commit()
        data = {
            'invitation_id': invitation.id,
            'response': 'Attending',
            'guest_name': 'Jane Doe',
            'guest_email': 'janedoe@example.com'
        }
        response = self.client.post(f'/invitations/{invitation.id}/rsvps', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_rsvps_for_invitation(self):
        invitation = Invitation(name='John Doe', email='johndoe@example.com', plus_one=True)
        db.session.add(invitation)
        rsvp1 = RSVP(invitation_id=invitation.id, response='Attending', guest_name='Jane Doe', guest_email='janedoe@example.com')
        rsvp2 = RSVP(invitation_id=invitation.id, response='Not Attending', guest_name='Bob Smith', guest_email='bobsmith@example.com')
        db.session.add_all([rsvp1, rsvp2])
        db.session.commit()
        response = self.client.get(f'/invitations/{invitation.id}/rsvps')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)