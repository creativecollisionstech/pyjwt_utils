
JSON Web Tokens Utilities in Python
===================================

This project contains utility files for implementing JSON Web Tokens (JWT) sessions in Python.  I also include documentation below for how JSON Web Tokens are used.

The start of this project was based off of a blog post on medium.com by Mike Waites
[Python REST API Authentication with JSON Web Tokens by Mike Waites](https://medium.com/python-rest-api-toolkit/python-rest-api-authentication-with-json-web-tokens-1e06e449f33)

Much of the original documentation on JSON Web tokens was pull from information by Apcelent.
[Original Source](http://blog.apcelent.com/json-web-token-tutorial-with-example-in-python.html)

When building websites, we need a way of authenticating with the web server and securing our communication.

The tradional mode of authentication for websites has been to use cookie based authentication. In a typical REST architecture the server does not keep any client state. The stateless approach of REST makes session cookies inappropriate from the security standpoint. Session hijacking and cross-site request forgery are common security issues while using cookies to secure your REST Service. Hence their arises a need to authenticate and secure a stateless REST service.

We can secure REST API with JSON Web Tokens. JSON Web Tokens are an open, industry standard RFC 7519 method for representing claims securely between two parties.

Installing pyjwt
----------------

The code in this project depends on the pyjwt project.
[pyjwt on GitHub](https://github.com/jpadilla/pyjwt)

To install with pip:

	$ pip install PyJWT


Understanding JSON Web Tokens
-----------------------------

### Structure of a JWT

There are 3 parts to a JWT separated by a ".", each section is created differently. We have the 3 parts which are:

* *header*
* *payload*
* *signature*

	"<base64-encoded header>.<base64-encoded payload>.<base64-encoded signature>"

#### Header

The JWT Header declares that the encoded object is a JSON Web Token (JWT) and the JWT is a JWS that is MACed using the HMAC SHA-256 algorithm. For example:

{
    “alg”: “HS256”,
    “typ”: “JWT”
}

* *"alg"* is a string and specifies the algorithm used to sign the token.

* *"typ"* is a string for the token, defaulted to "JWT". Specifies that this is a JWT token.

#### Payload (Claims)

A claim or a payload can be defined as a statement about an entity that contians security information as well as additional meta data about the token itself.

Following are the claim attributes :

* *iss*: The issuer of the token

* *sub*: The subject of the token

* *aud*: The audience of the token

* *qsh*: query string hash

* *exp*: Token expiration time defined in Unix time

* *nbf*: “Not before” time that identifies the time before which the JWT must not be accepted for processing

* *iat*: “Issued at” time, in Unix time, at which the token was issued

* *jti*: JWT ID claim provides a unique identifier for the JWT

#### Signature

JSON Web Signatre specification are followed to generate the final signed token. JWT Header, the encoded claim are combined, and an encryption algorithm, such as HMAC SHA-256 is applied. The signatures's secret key is held by the server so it will be able to verify existing tokens.


Creating a JWT in Python
------------------------

Encoding a payload

	$ import jwt
	$ encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
    $ encoded
    $ 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'

If you run the above encode function, you will notice that it always returns the same token.  This seems odd right? Shouldn't our tokens be unique?  The problem is we have only given it static data at this point where 'secret' is the key.  Since the payload and the key are always the same, the generated JWT is also always the same.  But this just an example, not how we would actually implement using JSON web tokens in practice.

For us to use the JWT in practice, we need to fill out the information in the payload and encode it with a random key.  This project has created a wrapper function around the jwt.encode function in the example above.

### Using JWTUtils to create a JWT

The purpose of this wrapper class is to make it easier and understand what is necessary to create a JWT.  When we create our JWT, we are going to need to create a Client object, currently defined in jwt_utils.py.  

Once we have the client object, we can created our JWT using the JWTUtils.encodeClientToken function.  You must pass in the client object to this encode function that contains a client "id" and a "secret_key".  The secret key inside of the client object is what replaces the second argument in the jwt.encode function above.

	$ client = Client()
	$ token = JWTUtils.encodeClientToken( client )

Decoding a payload

	$ jwt.decode(encoded, 'secret', algorithms=['HS256'])



