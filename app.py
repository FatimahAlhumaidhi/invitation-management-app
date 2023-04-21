from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from database.models import setup_db, RSVP, Invitation
from auth.auth import AuthError, requires_auth

import os
import logging

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = os.environ.get('LOG_FILE', 'app.log')

def _logger():
    '''
    Setup logger format, level, and handler.

    RETURNS: log object
    '''
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log

LOG = _logger()
LOG.debug("Starting with log level: %s" % LOG_LEVEL)


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def get_index():
        return jsonify(success=True, Hello='World')

    @app.route('/invitations', methods=['GET'])
    def get_invitations():
        '''
        GET list of all invitations
        '''
        invitations = Invitation.query.all()
        return jsonify(success=True, invitations=[i.format() for i in invitations])

    @app.route('/invitations/<int:id>', methods=['GET'])
    def get_invitation(id):
        '''
        GET an invitation by ID
        '''
        invitation = Invitation.query.filter(Invitation.id == id).one_or_none()
        if invitation:
            return jsonify(success=True, invitations=invitation.format())
        else:
            abort(404)
        
    @app.route('/invitations', methods=['POST'])
    @requires_auth('post:invitation')
    def create_invitation(payload):
        '''
        POST an invitation
        requires post:invitation auth
        '''
        data = request.get_json()
        try:
            name = data['name']
            email = data['email']
            description = data['description']
            invitation = Invitation(name=name, email=email, description=description)
            invitation.insert()
            return jsonify(success=True, invitations=invitation.format())
        except:
            abort(400)

    @app.route('/invitations/<int:id>', methods=['PATCH'])
    @requires_auth('patch:invitation')
    def update_invitation(payload, id):
        '''
        PATCH an invitation
        requires patch:invitation auth
        '''
        invitation = Invitation.query.filter(Invitation.id == id).one_or_none()
        try:
            if invitation is None:
                abort(404)
            data = request.get_json()
            if 'name' in data:
                invitation.name = data['name']
            if 'email' in data:
                invitation.email = data['email']
            if 'description' in data:
                invitation.text = data['description']
            invitation.update()
            return jsonify(success=True, invitations=invitation.format())
        except:
            abort(400)

    @app.route('/invitations/<int:id>', methods=['DELETE'])
    @requires_auth('delete:invitation')
    def delete_invitation(payload, id):
        '''
        DELETE an invitation
        requires delete:invitation auth
        '''
        invitation = Invitation.query.get(id)

        if invitation is None:
            abort(404)
        try:
            invitation.delete()
            return jsonify(success=True, invitation_id=id)
        except:
            abort(500)

    
    @app.route('/invitations/<int:invitation_id>/rsvps', methods=['GET'])
    @requires_auth('get:invitation-rsvps')
    def get_rsvps(payload, invitation_id):
        '''
        GET a list of RSVPs to a single invitation
        requires get:invitation-rsvps auth
        '''
        rsvps = RSVP.query.filter_by(invitation_id=invitation_id).all()
        return jsonify(success=True, rsvps=[r.format() for r in rsvps])

    @app.route('/invitations/<int:invitation_id>/rsvps/<int:rsvp_id>', methods=['GET'])
    @requires_auth('get:invitation-rsvp-details')
    def get_rsvp(payload, invitation_id, rsvp_id):
        '''
        GET an RSVP to a single invitation
        requires get:rsvp auth
        '''
        rsvp = RSVP.query.filter(RSVP.invitation_id==invitation_id, RSVP.id==rsvp_id).one_or_none()
        if rsvp:
            if rsvp.jwt_sub != payload['sub']:
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'permissions are not included in the payload'
                    }, 401
                )
            return jsonify(success=True, rsvps=rsvp.format())
        else:
            abort(404)
    
    @app.route('/invitations/<int:invitation_id>/rsvps', methods=['POST'])
    @requires_auth('post:invitation-rsvp')
    def create_rsvp(payload, invitation_id):
        '''
        POST an RSVP
        requires post:rsvp auth
        '''
        invitation = Invitation.query.get(invitation_id)
        if invitation is None:
            abort(404)

        try:
            data = request.get_json()
            guest_name = data.get('guest_name')
            guest_email = data.get('guest_email')
            response = data.get('response')
            plus_one = data.get('plus_one')

            if None in (guest_name, guest_email, response, plus_one):
                abort(404)

            rsvp = RSVP(guest_name=guest_name,
                        jwt_sub=payload['sub'], 
                        guest_email=guest_email, 
                        response=response, 
                        invitation_id=invitation_id,
                        plus_one=plus_one)
            rsvp.insert()

            return jsonify(success=True, rsvps=rsvp.format())
        except:
            abort(400)

    @app.route('/invitations/<int:invitation_id>/rsvps/<int:rsvp_id>', methods=['PATCH'])
    @requires_auth('patch:invitation-rsvp')
    def update_rsvp(payload, invitation_id, rsvp_id):
        '''
        PATCH an RSVP
        requires patch:rsvp auth
        '''
        invitation = Invitation.query.get(invitation_id)
        if invitation is None:
            abort(404)

        try:
            rsvp = RSVP.query.filter_by(invitation=invitation, id=rsvp_id).one_or_none()
            if rsvp is None:
                abort(404)

            if rsvp.jwt_sub != payload['sub']:
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'permissions are not included in the payload'
                    }, 401
                )

            data = request.get_json()

            if 'guest_name' in data:
                rsvp.guest_name = data.get('guest_name')

            if 'guest_email' in data:
                rsvp.guest_email = data.get('guest_email')

            if 'response' in data:
                rsvp.response = data.get('response')

            if 'plus_one' in data:
                rsvp.plus_one = data.get('plus_one')

            rsvp.update()

            return jsonify(success=True, rsvps=rsvp.format())
        except:
            abort(500)

    @app.route('/invitations/<int:invitation_id>/rsvps/<int:rsvp_id>', methods=['DELETE'])
    @requires_auth('delete:invitation-rsvp')
    def delete_rsvp(payload, invitation_id, rsvp_id):
        '''
        DELETE an RSVP
        requires delete:rsvp auth
        '''
        invitation = Invitation.query.get(invitation_id)
        if invitation is None:
            abort(404)

        try:
            rsvp = RSVP.query.filter_by(invitation=invitation, id=rsvp_id).one_or_none()
            if rsvp is None:
                abort(404)

            if rsvp.jwt_sub != payload['sub']:
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'permissions are not included in the payload'
                    }, 401
                )

            rsvp.delete()

            return jsonify(success=True, rsvp_id=rsvp_id)
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
    app.run(host='127.0.0.1')
