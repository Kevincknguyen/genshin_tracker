from flask import Flask

#from file import Class_name... OR import file_name and include file name inline with classnames can run Class_name.function
    # OR
#from foldername.file_name import filesnames

DB="genshin_schema"

app= Flask(__name__)
app.secret_key="sneakystabby"
