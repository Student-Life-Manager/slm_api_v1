### How to use `access_token` and `refresh_token`

- send access token for authenticated routes as `Bearer {access_token}`
- if a route returns with `401 Unauthorized` exception, you can either make user log in to the app again or use `refresh_token` to generate new tokens for a user.
- send both `access_token` and `refresh_token` to `/auth_user/me/auth` and it will return new tokens. Access token is valid for 24 hours and refresh token is valid for 5 days.
