import mariadb
from flask import Flask, request, Response
import dbcreds
import json
import sys

app = Flask(__name__)

@app.route('/')
def handler():
    return "Hello World"

@app.route('/fruits', methods=['GET', 'POST', 'PATCH'])
def fruits_handler():
    fruit_name = "Banana"

    try: 
        conn = mariadb.connect(
                        user=dbcreds.user,
                        password=dbcreds.password,
                        host=dbcreds.host,
                        port=dbcreds.port,
                        database=dbcreds.database
                        )
        cursor = conn.cursor()

        if request.method == 'GET':
            resp = {
                "fruitName" : fruit_name
            }
            return Response(json.dumps(resp), mimetype='application/json', status=200)
        
        elif request.method == 'POST':
            data = request.get_json()
            
            if data.get("fruitName") == fruit_name:
                return Response("Yes it matches", mimetype='text/html', status=200)
            else:
                return Response("No it doesnt match", mimetype="text/html", status=400)
        
        elif request.method == 'PATCH':
            return Response("This endpoint is under maintenance", mimetype='text/html', status=503)

        else:
            print("Bad request")

    except:
        print("Something went wrong")
        return Response("Something went wrong", status=500)
    finally:
        if (cursor != None):
            cursor.close()
        if (conn != None):
            conn.rollback()
            conn.close()

#Below is setting up script to run in testing or production mode. when running script must provide argument (ex: python app.py testing)
#this code below always at the end of the script after the decorations/functions
#ensure debug=true and CORS only ever available in testing mode
#bjoern only available on linux, cannot run on windows. Will have to properly set up on the VM SSH
#debug=True allows server to restart every time you save, so you dont need to stop and start the server every time you want to see changes

if len(sys.argv) > 1 and len(sys.argv) < 3:
    mode = sys.argv[1]
    if mode == "production":
        import bjoern
        host = "0.0.0.0"
        port = 5000
        print("Running in production mode")
        bjoern.run(app, host, port)
    elif mode == "testing":
        from flask_cors import CORS
        CORS(app)
        print("Running in testing mode")
        #debug=True ONLY EVER used behind testing mode. Do not allow debug=True on production server.
        app.run(debug=True)
    else:
        print("Invalid mode argument. Please choose testing or production")  

else:
    print("No argument provided or too many arguments")
    exit()
