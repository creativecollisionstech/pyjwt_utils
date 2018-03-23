"""
Python JSON Web Token Utils

Written by: J. Patrick Farrell
Copyright 2018 Creative Collisions Technology, LLC

This project is based on a post by Mike Waites on medium.com
https://medium.com/python-rest-api-toolkit/python-rest-api-authentication-with-json-web-tokens-1e06e449f33

You can find his GitHub account at:
https://github.com/mikeywaites

This project uses the pyjwt framework to create create and decode get_token_from_request.  Check the README.md
file for information.
"""

from datetime import datetime, timedelta
import jwt


class Client():

	def __init__(self):

		self.name = ""
		self.id = 1
		self.secret_key = 'secret' # TODO: Generate random key for client


class JWTUtils():

	@staticmethod
	def decodeClientToken(client, token):
		"""
		Decode and validate a client JWT.
		"""

		verify_claims = ['sig', 'aud', 'exp', 'nbf', 'iat']
		required_claims = ['exp', 'iat', 'nbf', 'aud']

		options = {
			'verify_' + claim: True
			for claim in verify_claims
		}

		options.update({
			'require_' + claim: True
			for claim in required_claims
		})

		try:
			return jwt.decode(
				token,
				str(client.secret_key),
				options=options,
				algorithms=['HS256'],
				audience=str(client.id),
				leeway=0
			)
		except jwt.InvalidTokenError:
			return False

	@staticmethod
	def encodeClientToken(client, user_id=None):
		"""
		Create a new JWT for the specified client.
		JWT's require the following claims be present.
		exp - token expiry date (Time token expires)
		iat - token issued timestamp (Time token created)
		nbf - timestamp indicating when the token can start being used (usually now)
		sub - the `subject` of this token (an optional user_id)
		aud - the audience this token is valid for, our api client (typically the browser client).

		Note: The calling function must keep track of this client object because we will need it to decode the JWT.
		"""
		iat = datetime.utcnow()
		exp = iat + timedelta(days=30)
		nbf = iat

		payload = {
			'exp': exp,
			'iat': iat,
			'nbf': nbf,
			'aud': str(client.id)
		}

		if user_id:
			payload['sub'] = user_id

		return jwt.encode(
			payload,
			str(client.secret_key),
			algorithm='HS256',
			headers=None
		).decode('utf-8')

	@staticmethod
	def getTokenFromHeaders(headers):
		"""
		Parse Authorization header in the form of 'Bearer {token}'.
		TODO: Make the errors more explicit rather than just returning False.
		"""

		auth_header_value = headers.get('Authorization', None)

		if not auth_header_value:
			return False

		parts = auth_header_value.split()

		if parts[0].lower() != 'bearer':
			return False
		elif len(parts) == 1:
			return False
		elif len(parts) > 2:
			return False

		return parts[1]


if __name__ == '__main__':

	# Example
	client = Client()
	token = JWTUtils.encodeClientToken( client )
	print "Encoded token is:\n%s\n" % token

	decoded_token = JWTUtils.decodeClientToken( client, token )
	print "Decoded token is:\n%s" % decoded_token


