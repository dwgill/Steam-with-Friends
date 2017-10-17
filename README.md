# Steam with Friends

## Dev Setup
Make sure you have Python3.5+ installed. This project uses a [Vitual
Environment][venv], so setup a virtual environment first:

    python3 -m venv .venv

[Activate the virtual environment to enter your development Python
environment.][venv activate] On Windows there should be scripts in
`.venv/bin/Scripts` to activate it. On Unix-like systems you should just need
to `source` the activate script:

    source .venv/bin/activate

Once you've activate the virtual environment anything you do with Python will
isolated to this project directory. Now we can install the project requirements
without installing them system-wide:

    pip install -r python_requirements.txt

With the Python packages installed you should be able to run the server directly
on your local machine:

    python app.py

[venv]: https://docs.python.org/3.5/tutorial/venv.html
[venv activate]: https://virtualenv.pypa.io/en/stable/userguide/#activate-script
