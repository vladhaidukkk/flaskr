serve:
	@flask --app flaskr run --debug

test:
	@pytest

cov:
	@coverage run -m pytest

cov-rep:
	@coverage report

cov-html:
	@coverage html
