You need the following settings in a `.env` file:

```
DEBUG=True  # Defaults to False
DJANGO_SETTINGS_MODULE=core.settings
SECRET_KEY=<YOUR_SECRET_KEY>
DATABASE_URL=<YOUR_DATABASE_URL>
```

`DATABASE_URL` follows the 12-factor [dj-database-url] schema.

[dj-database-url]: https://github.com/kennethreitz/dj-database-url#url-schema

Run the app with `Procfile`.

To be continued...
