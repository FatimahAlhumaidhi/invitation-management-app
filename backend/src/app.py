import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from database.models import db_drop_and_create_all, setup_db, RSVP, Invitation
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    db_drop_and_create_all()

    @app.route('/invitations')
    def get_invitations():
        invitations = Invitation.query.all()
        return jsonify([i.format() for i in invitations])

    @app.route('/invitations/<int:id>')
    def get_invitation(id):
        invitation = Invitation.query.filter(Invitation.id == id).one_or_none()
        if invitation:
            return jsonify(invitation.format())
        else:
            abort(404)

    @app.route('/invitations/<int:invitation_id>/rsvps')
    @requires_auth('get:rsvps')
    def get_rsvps(payload, invitation_id):
        rsvps = RSVP.query.filter_by(invitation_id=invitation_id).all()
        return jsonify(sucess=True, rsvp=[r.format() for r in rsvps])

    @app.route('/invitations/<int:invitation_id>/rsvps/<int:rsvp_id>')
    @requires_auth('get:rsvp')
    def get_rsvp(payload, invitation_id, rsvp_id):
        rsvp = RSVP.query.filter(RSVP.invitation_id==invitation_id, RSVP.id==rsvp_id).one_or_none()
        if rsvp:
            if rsvp.jwt_sub != payload['sub']:
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'permissions are not included in the payload'
                    }, 401
                )
            return jsonify(rsvp.format())
        else:
            abort(404)
        
    @app.route('/invitations', methods=['POST'])
    @requires_auth('post:invitations')
    def create_invitation(payload):
        data = request.get_json()
        try:
            name = data['name']
            email = data['email']
            text = data['text']
            invitation = Invitation(name=name, email=email, text=text)
            invitation.insert()
            return jsonify(invitation.format())
        except:
            abort(400)

    @app.route('/invitations/<int:id>', methods=['PATCH'])
    @requires_auth('patch:invitations')
    def update_invitation(payload, id):
        invitation = Invitation.query.filter(Invitation.id == id).one_or_none()
        try:
            if invitation is None:
                abort(404)
            data = request.get_json()
            if 'name' in data:
                invitation.name = data['name']
            if 'email' in data:
                invitation.email = data['email']
            if 'text' in data:
                invitation.text = data['text']
            invitation.update()
            return jsonify(invitation.format())
        except:
            abort(400)

    @app.route('/invitations/<int:id>', methods=['DELETE'])
    @requires_auth('delete:invitations')
    def delete_invitation(payload, id):
        invitation = Invitation.query.get(id)

        if invitation is None:
            abort(404)
        try:
            invitation.delete()
            return jsonify({'success': True, 'invitation_id':id})
        except:
            abort(500)
    
    @app.route('/invitations/<int:invitation_id>/rsvps', methods=['POST'])
    @requires_auth('post:rsvp')
    def create_rsvp(payload, invitation_id):
        invitation = Invitation.query.get(invitation_id)
        if invitation is None:
            abort(404)

        try:
            data = request.get_json()
            guest_name = data.get('guest_name')
            guest_email = data.get('guest_email')
            response = data.get('response')

            if not guest_name or not guest_email or not response:
                abort(404)

            rsvp = RSVP(guest_name=guest_name,jwt_sub=payload['sub'], guest_email=guest_email, response=response, invitation_id=invitation_id)
            rsvp.insert()

            return jsonify(rsvp.format())
        except:
            abort(400)


    @app.route('/invitations/<int:invitation_id>/rsvps/<int:rsvp_id>', methods=['DELETE'])
    @requires_auth('delete:rsvp')
    def delete_rsvp(payload, invitation_id, rsvp_id):
        invitation = Invitation.query.get(invitation_id)
        if invitation is None:
            abort(404)

        try:
            rsvp = RSVP.query.filter_by(invitation=invitation, id=rsvp_id).first()
            if rsvp is None:
                abort(404)

            if rsvp.jwt_sub != payload['sub']:
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'permissions are not included in the payload'
                    }, 401
                )

            rsvp.delete()

            return jsonify({'success': True, 'rsvp_id':rsvp_id})
        except:
            abort(500)


    @app.route('/invitations/<int:invitation_id>/rsvps/<int:rsvp_id>', methods=['PATCH'])
    @requires_auth('patch:rsvp')
    def update_rsvp(payload, invitation_id, rsvp_id):
        invitation = Invitation.query.get(invitation_id)
        if invitation is None:
            abort(404)

        try:
            rsvp = RSVP.query.filter_by(invitation=invitation, id=rsvp_id).first()
            if rsvp is None:
                abort(404)

            if rsvp.jwt_sub != payload['sub']:
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'permissions are not included in the payload'
                    }, 401
                )

            data = request.get_json()
            guest_name = data.get('guest_name')
            guest_email = data.get('guest_email')
            response = data.get('response')

            if guest_name:
                rsvp.guest_name = guest_name

            if guest_email:
                rsvp.guest_email = guest_email

            if response:
                rsvp.response = response

            rsvp.update()

            return jsonify(rsvp.format())
        except:
            abort(500)

    

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    
    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, 
                    "error": 404, 
                    "message": "resource not found"}),
            404
        )
    
    @app.errorhandler(400)
    def not_found(error):
        return (
            jsonify({"success": False, 
                    "error": 400, 
                    "message": "bad request"}),
            400
        )

    @app.errorhandler(AuthError)
    def not_authorized(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
