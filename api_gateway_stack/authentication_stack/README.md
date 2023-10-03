## Stack for generation of authentication lambdas

Current lambdas:

Initiate Auth: sets a nonce in cookie, set a "next" parameter in cookie if present (for redirection after authentication), and redirects the user to AWS cognito for authentication

Postlogin: After user has been redirected back from cognito, initiates code-exchange (See OAUTH PKCE flow), checks if tokens are valid, sets a 'access_token_cookie', a 'csrf' value in cookie (for javascript use to prevent CSRF attacks), a 'logged_in' cookie (for javascript to access to know if user is logged in or not). Then, gets the 'next' parameter from cookie and redirects the user to main page, a "access_token_expires" cookie to indicate the time the access token expires

Logout: Unsets all access token cookies and directs user to cognito logout page, which directs back to main page
