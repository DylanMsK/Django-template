CREATE USER your_username WITH ENCRYPTED PASSWORD 'your_password';

CREATE DATABASE your_database_name
  WITH 
  OWNER = your_username
  ENCODING = 'UTF8'
  LC_COLLATE = 'ko_KR.UTF-8'
  LC_CTYPE = 'ko_KR.UTF-8';