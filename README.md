
This is minimum blueprint for `fastapi`, deploying on Deta.
Initial schema is written for simple mini blog API

# Set up

detail: https://docs.deta.sh/docs/micros/getting_started

After starting your project on Deta console (https://web.deta.sh/home), run below:

```
git clone git@github.com:yozibak/deta-blueprint.git
mv deta-blueprint <your-api-dir-name> # change directory name
deta new --python ./<your-api-dir-name> --project <deta-project-name> 
```

You'll be prompted like so:

```
{
	"name": "your-api-name",
	"id": "your-api-id",
	"project": "project-id",
	"runtime": "python3.9",
	"endpoint": "http endpoint",
	"region": "ap-southeast-1",
	"visor": "enabled",
	"http_auth": "disabled"
}
```

then edit `deta_setup.py`,

```
deta = Deta('deta-project-id')
db = deta.Base("base-name")
```

And all set. Write your own API.

CRUD on `main.py` and Pydantic schema on `schemas.py`.

Once done, run `deta deploy`.
