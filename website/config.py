from dotenv import load_dotenv
load_dotenv()

import os

db_host_local = os.environ.get('DB_HOST_LOCAL')
db_name_local = os.environ.get('DB_NAME_LOCAL')
db_user_local = os.environ.get('DB_USERNAME_LOCAL')
db_password_local = os.environ.get('DB_PASSWORD_LOCAL')

db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')