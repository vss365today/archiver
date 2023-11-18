# #vss365 today Archiver
> Generate a static, flat file version of #vss365 today

Note that this does _not_ fully download and archive the website. It is custom-built with a specific
use case for a one-time event. You won't be able to generate a full site archive using this tool.

## Requirements

- Python 3.11+
- Poetry 1.6.1+

### Required Secrets
- API_DOMAIN
- APP_DOMAIN
- DIST_PATH
- STATIC_FILES_URL
- SYS_VARS_PATH (in env)


## Usage
- `poetry install`
- `poetry shell`
- `python ./archiver.py`

## License
[MIT](LICENSE)
