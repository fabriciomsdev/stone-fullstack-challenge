cd backend/rest-api/ \
&& echo "RUNNING UNIT TESTS ..." \
&& echo "1 - Installing Virtual Env For tests ... " \
&& python3 -m venv test-venv \
&& echo "2 - Reading Virtual Env ... " \
&& source test-venv/bin/activate \
&& echo "3 - Installing dependencies ... " \
&& pip install -r requirements/requirements.txt \
&& pip install -r requirements/requirements-dev.txt \
&& echo "4 - Finally ... " \
&& echo " TESTING ... " \
&& python -m unittest discover .