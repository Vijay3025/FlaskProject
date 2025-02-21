from app import create_app
from flask import current_app


app  = create_app()


# with app.app_context():
#     print(list(current_app.url_map.iter_rules()))

app.run(host="0.0.0.0")#,threaded=False)






