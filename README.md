# First WebApp Demo

- This showcases skills in python based web application.
- This first project demonstrates manually driving db migration.
- It also demonstrates populating a vectordb and using that for search.
- Although these datasets are minimal, a commercial product can be derived by scaling up the data-points and query complexity.

# packages, dependencies, tools.

- ubuntu-linux (x86_64)
- python-3.x.y
- pip
- venv
- NO alembic,NO flyway,NO liquibase (to prove bill can do manually). Alembic on second iteration,app
- mariadb
- HTML
- CSS
- Javascript
- jQuery
- Twitter bootstrap
- FastAPI
- mysql-connector-python
- chromadb (vector db)

- NOTE: the bootstrap page (menus) is not connected: we are focussing on the server-side functionality

- NOTE: FastAPI serves both backend and frontend app (via static content)

# To run the web-app

- in the project root directory where installed

- $ fastapi dev ./mainapp.py

## To view app in the web browser home-page

- web-address http://localhost:8000/first-webapp-demo/FirstPythonDemoApp/FirstPythonDemoApp.html

- 0th-step] to manually action everything. (try 'drop db tables' button if unsure)
- 1st-step] press 'create db tables' - check 'Heading12 for return status is True'
- 2nd-step] press 'insert into db' - check 'Heading12 for return status is True'
- 3rd-step] press 'add constraint to db' - check 'Heading12 for return status is True'
- 4th-step] press 'select from db tables' - check 'Heading12 for json data of db (proves data exists in correct db structure)
- 5th-step] press 'ingest from query tables and ingest into chroma db' - check 'Heading12' for return status is successfully ingested
- 6th-step] enter a search term, press 'Query chroma db and retrieve' - check 'Heading12' for returned json. check html/css below list or retrieved items (graphically listed in bootstrap panels)

- NOTE: we only ingested 80 items. suggested search terms: Deluxe, Luxury Hotel, Spa, air shoe, foam shoe,  etc
