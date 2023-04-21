import unittest
from app import create_app
from database.models import Invitation, RSVP, setup_db, db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        """Setup method for each test case"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('TEST_DATABASE_URL')
        setup_db(self.app, self.database_path)

        self.guest_auth = {'Authorization': f"Bearer {os.environ.get('GUEST_JWT')}"}
        self.admin_auth = {'Authorization': f"Bearer {os.environ.get('ADMIN_JWT')}"}
        self.guest_jwt_sub = os.environ.get('GUEST_JWT_SUB')
        self.invitation = Invitation(name='John Doe', email='johndoe@example.com', description='Please come to my birthday party!')
        self.rsvp = RSVP(invitation_id=1, response='Attending', guest_name='Jane Doe', guest_email='janedoe@example.com', plus_one=True, jwt_sub=self.guest_jwt_sub)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Teardown method for each test case"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        pass

    def test_create_invitation(self):
        """Test creating a new invitation"""

        response = self.client().post('/invitations', json={
            'name': self.invitation.name,
            'email': self.invitation.email,
            'description': self.invitation.description
        }, headers=self.admin_auth)
        self.assertEqual(response.status_code, 200)
        invitation = Invitation.query.filter_by(email=self.invitation.email).first()
        self.assertIsNotNone(invitation)
        self.assertEqual(invitation.name, self.invitation.name)
        self.assertEqual(invitation.email, self.invitation.email)
        self.assertEqual(invitation.description, self.invitation.description)

    def test_get_invitation_not_found(self):
        response = self.client().get('/invitations/999')
        self.assertEqual(response.status_code, 404)

    def test_post_invitation_missing_data(self):
        data = {}
        response = self.client().post('/invitations', json=data, headers=self.admin_auth)
        self.assertEqual(response.status_code, 400)

    def test_unauthorized_access(self):
        response = self.client().post('/invitations', headers=self.guest_auth)
        self.assertEqual(response.status_code, 403)

    def test_get_invitation_rsvps_missing_auth(self):
        response = self.client().get('/invitations/1/rsvps')
        self.assertEqual(response.status_code, 401)

    def test_delete_invitation_missing_auth(self):
        response = self.client().delete('/invitations/1')
        self.assertEqual(response.status_code, 401)

    def test_create_invitation_missing_auth(self):
        invitation = {'name': 'John Doe', 'email': 'john.doe@example.com', 'description': 'Please join us for our wedding!'}
        response = self.client().post('/invitations', json=invitation)
        self.assertEqual(response.status_code, 401)

    def test_retrieve_all_invitations(self):
        """Test retrieving all invitations"""
        response = self.client().get('/invitations')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json.get('success'), True)

    def test_retrieve_invitation_by_id(self):
        """Test retrieving a single invitation by ID"""
        self.invitation.insert()
        
        response = self.client().get(f'/invitations/{self.invitation.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json.get('success'), True)
        self.assertEqual(response.json['invitations']['name'], self.invitation.name)

    def test_update_invitation(self):
        """Test updating an existing invitation by ID"""
        self.invitation.insert()
        
        updated_name = 'Jane Doe'
        response = self.client().patch(f'/invitations/{self.invitation.id}', json={
            'name': updated_name
        }, headers=self.admin_auth)
        self.assertEqual(response.status_code, 200)
        invitation = Invitation.query.filter_by(email=self.invitation.email).first()
        self.assertEqual(invitation.name, updated_name)

    def test_delete_invitation(self):
        """Test deleting an existing invitation by ID"""
        self.invitation.insert()
        
        response = self.client().delete(f'/invitations/{self.invitation.id}', headers=self.admin_auth)
        self.assertEqual(response.status_code, 200)
        invitation = Invitation.query.filter_by(email=self.invitation.email).first()
        self.assertIsNone(invitation)



    def test_create_rsvp(self):
        """Test creating a new RSVP"""
        self.invitation.insert()
        
        response = self.client().post(f'/invitations/{self.invitation.id}/rsvps', json={
            'response': self.rsvp.response,
            'guest_name': self.rsvp.guest_name,
            'guest_email': self.rsvp.guest_email,
            'plus_one': self.rsvp.plus_one
        }, headers=self.guest_auth)
        self.assertEqual(response.status_code, 200)
        rsvp = RSVP.query.filter_by(guest_email=self.rsvp.guest_email).first()
        self.assertIsNotNone(rsvp)
        self.assertEqual(rsvp.response, self.rsvp.response)

    def test_retrieve_rsvp_by_id(self):
        """Test retrieving a single RSVP by ID"""
        self.invitation.insert()
        self.rsvp.insert()
        
        response = self.client().get(f'/invitations/{self.invitation.id}/rsvps/{self.rsvp.id}', headers=self.guest_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['rsvps']['response'], self.rsvp.response)
    
    def test_get_rsvp_not_found(self):
        self.invitation.insert()
        
        response = self.client().get('/invitations/1/rsvps/999', headers=self.guest_auth)
        self.assertEqual(response.status_code, 404)

    def test_update_rsvp(self):
        """Test updating an existing RSVP by ID"""
        self.invitation.insert()
        self.rsvp.insert()
        
        updated_response = 'Not Attending'
        response = self.client().patch(f'/invitations/{self.invitation.id}/rsvps/{self.rsvp.id}', json={
            'response': updated_response
        }, headers=self.guest_auth)
        self.assertEqual(response.status_code, 200)
        rsvp = RSVP.query.filter_by(guest_email=self.rsvp.guest_email).first()
        self.assertEqual(rsvp.response, updated_response)

    def test_delete_rsvp(self):
        """Test deleting an existing RSVP by ID"""
        self.invitation.insert()
        self.rsvp.insert()

        response = self.client().delete(f'/invitations/{self.invitation.id}/rsvps/{self.rsvp.id}', headers=self.guest_auth)
        self.assertEqual(response.status_code, 200)
        rsvp = RSVP.query.filter_by(guest_email=self.rsvp.guest_email).first()
        self.assertIsNone(rsvp)

if __name__ == '__main__':
    unittest.main()