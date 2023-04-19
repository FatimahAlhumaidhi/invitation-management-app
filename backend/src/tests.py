import unittest
from .app import app, db
from .database.models import Invitation, RSVP

class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        """Setup method for each test case"""
        self.client = app.test_client()
        self.invitation = Invitation(name='John Doe', email='johndoe@example.com', description='Please come to my birthday party!')
        self.rsvp = RSVP(response='Attending', guest_name='Jane Doe', guest_email='janedoe@example.com', plus_one=True)
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Teardown method for each test case"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_invitation(self):
        """Test creating a new invitation"""
        response = self.client.post('/invitations', json={
            'name': self.invitation.name,
            'email': self.invitation.email,
            'description': self.invitation.description
        })
        self.assertEqual(response.status_code, 201)
        invitation = Invitation.query.filter_by(email=self.invitation.email).first()
        self.assertIsNotNone(invitation)
        self.assertEqual(invitation.name, self.invitation.name)
        self.assertEqual(invitation.email, self.invitation.email)
        self.assertEqual(invitation.description, self.invitation.description)

    def test_get_invitation_not_found(self):
        response = self.app.get('/invitations/999')
        self.assertEqual(response.status_code, 404)

    def test_get_rsvp_not_found(self):
        response = self.app.get('/invitations/1/rsvps/999')
        self.assertEqual(response.status_code, 404)

    def test_post_invitation_missing_data(self):
        data = {}
        response = self.app.post('/invitations', json=data, headers={'Authorization': 'Bearer {JWT_Token}'})
        self.assertEqual(response.status_code, 400)

    def test_unauthorized_access(self):
        response = self.app.post('/invitations', headers={})
        self.assertEqual(response.status_code, 401)

    def test_get_invitation_rsvps_401(self):
        response = self.app.get('/invitations/1/rsvps')
        self.assertEqual(response.status_code, 401)

    def test_delete_invitation_401(self):
        response = self.app.delete('/invitations/1')
        self.assertEqual(response.status_code, 401)

    def test_create_invitation_401(self):
        invitation = {'name': 'John Doe', 'email': 'john.doe@example.com', 'description': 'Please join us for our wedding!'}
        response = self.app.post('/invitations', json=invitation)
        self.assertEqual(response.status_code, 401)

    def test_retrieve_all_invitations(self):
        """Test retrieving all invitations"""
        response = self.client.get('/invitations')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_retrieve_invitation_by_id(self):
        """Test retrieving a single invitation by ID"""
        with app.app_context():
            db.session.add(self.invitation)
            db.session.commit()
        response = self.client.get(f'/invitations/{self.invitation.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], self.invitation.name)

    def test_update_invitation(self):
        """Test updating an existing invitation by ID"""
        with app.app_context():
            db.session.add(self.invitation)
            db.session.commit()
        updated_name = 'Jane Doe'
        response = self.client.patch(f'/invitations/{self.invitation.id}', json={
            'name': updated_name
        })
        self.assertEqual(response.status_code, 200)
        invitation = Invitation.query.filter_by(email=self.invitation.email).first()
        self.assertEqual(invitation.name, updated_name)

    def test_delete_invitation(self):
        """Test deleting an existing invitation by ID"""
        with app.app_context():
            db.session.add(self.invitation)
            db.session.commit()
        response = self.client.delete(f'/invitations/{self.invitation.id}')
        self.assertEqual(response.status_code, 204)
        invitation = Invitation.query.filter_by(email=self.invitation.email).first()
        self.assertIsNone(invitation)

    def test_create_rsvp(self):
        """Test creating a new RSVP"""
        with app.app_context():
            db.session.add(self.invitation)
            db.session.commit()
        response = self.client.post(f'/invitations/{self.invitation.id}/rsvps', json={
            'response': self.rsvp.response,
            'guest_name': self.rsvp.guest_name,
            'guest_email': self.rsvp.guest_email,
            'plus_one': self.rsvp.plus_one
        })
        self.assertEqual(response.status_code, 201)
        rsvp = RSVP.query.filter_by(guest_email=self.rsvp.guest_email).first()
        self.assertIsNotNone(rsvp)
        self.assertEqual(rsvp.response, self.rsvp.response)

    def test_retrieve_all_rsvps_for_invitation(self):
        """Test retrieving all RSVPs for a specific invitation"""
        with app.app_context():
            db.session.add(self.invitation)
            db.session.add(self.rsvp)
            db.session.commit()
        response = self.client.get(f'/invitations/{self.invitation.id}/rsvps')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_retrieve_rsvp_by_id(self):
        """Test retrieving a single RSVP by ID"""
        with app.app_context():
            db.session.add(self.invitation)
            db.session.add(self.rsvp)
            db.session.commit()
        response = self.client.get(f'/invitations/{self.invitation.id}/rsvps/{self.rsvp.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], self.rsvp.response)

    def test_update_rsvp(self):
        """Test updating an existing RSVP by ID"""
        with app.app_context():
            db.session.add(self.invitation)
            db.session.add(self.rsvp)
            db.session.commit()
        updated_response = 'Not Attending'
        response = self.client.patch(f'/invitations/{self.invitation.id}/rsvps/{self.rsvp.id}', json={
            'response': updated_response
        })
        self.assertEqual(response.status_code, 200)
        rsvp = RSVP.query.filter_by(guest_email=self.rsvp.guest_email).first()
        self.assertEqual(rsvp.response, updated_response)

    def test_delete_rsvp(self):
        """Test deleting an existing RSVP by ID"""
        with app.app_context():
            db.session.add(self.invitation)
            db.session.add(self.rsvp)
            db.session.commit()
        response = self.client.delete(f'/invitations/{self.invitation.id}/rsvps/{self.rsvp.id}')
        self.assertEqual(response.status_code, 204)
        rsvp = RSVP.query.filter_by(guest_email=self.rsvp.guest_email).first()
        self.assertIsNone(rsvp)

if __name__ == 'main':
    unittest.main()