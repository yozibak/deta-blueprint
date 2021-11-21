
This is minimum blueprint for `fastapi`, deploying on Deta.
Initial schema is written for simple mini blog API

# Set up

detail: https://docs.deta.sh/docs/micros/getting_started

After starting your project, run below:

```
deta new --project <project-id>
```

then edit `deta_setup.py`,

```
deta = Deta('DETA-PROJECT-ID')
db = deta.Base("base-name")
```

And all set. Write your own API.

CRUD on `main.py` and Pydantic schema on `schemas.py`.

Once done, run `deta deploy`.
