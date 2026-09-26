# Basic manual test checklist:
#
# 1. Register a new user.
# 2. Log in with the correct password.
# 3. Try an incorrect password.
# 4. Try six failed logins and confirm temporary blocking.
# 5. Log out and verify the session is removed.
# 6. Log in as admin and open /admin.
#
# For automated tests, use pytest and Flask's test client.
