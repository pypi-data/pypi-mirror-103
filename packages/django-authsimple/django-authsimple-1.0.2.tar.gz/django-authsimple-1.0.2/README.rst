===========
 simpleauth
===========

simpleauth is a Django app to implement simple authentication 
in django project.

Quick start
-----------

1. Add "authentication" to your INSTALLED_APPS setting like this

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'authentication',
    ]

2. Include the authentication URLconf in your project urls.py like this

.. code-block:: python

    path('auth/', include('authentication.urls')),

3. Create a "simpleAuth.py" file at project level(where manage.py is located)

.. code-block:: python

    DOMAIN = "http://127.0.0.1:8000"          # for default djangoserver (use your domain name)
    SENDER_EMAIL_ID = "YOUR_MAIL_ID"
    SENDER_PASSWORD = 'YOUR MAIL_ID PASSWORD'
    SERVER_NAME = 'smtp.gmail.com'            # for gmail (use your mail servername)
    # NOTE : TURN ON LESS SECURE APP OPTION IN UR GOOGLE ACCOUNT

4. Run ``python manage.py migrate`` to create the authentication models.

5. Start the development server and visit http://127.0.0.1:8000/auth/register to register user.

6. visit http://127.0.0.1:8000/auth/login to login.
    
7. visit http://127.0.0.1:8000/auth/logout to logout.
   
8. visit http://127.0.0.1:8000/auth/forgot_password to forgot_password.
