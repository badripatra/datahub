# ===Test data utility supporting Automation Services for Data==
__author__ = "Badri Patra"
__copyright__ = "Copyright 2017, Netapp"
__credits__ = ["Badri Patra", "Raghavender Nagarajan"]
__version__ = "1.0.0"
__email__ = "bpatra@netapp.com"
__status__ = "Testing"
# ===Test data utility supporting Automation Services for Data==

import os
import sys
import socket
import json

from flask import Flask,request
from flask_restx import Api, Resource, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Blueprint
from werkzeug.utils import *
import nfs_verifications

flask_app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')


app = Api(app=flask_app,
          version="1.0",
          title="Data Hub Verification APIs",
          description="APIs giving access to Load Test input data, Load Test Results, Scenario Mapping",
          doc='/docs')

app.init_app(blueprint)

verifiation_ns = app.namespace('verifiation', description='Load Test Results')
app.add_namespace(verifiation_ns)

flask_app.register_blueprint(blueprint)

port = int("8083")

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# --------------Add lib directory in Syspath. So that can import libs under that
scriptdir = os.path.dirname(os.path.abspath(__file__))  # Get directory location for script
sys.path.append(os.path.abspath(scriptdir + '/lib'))  # Append custom_module location to Sys Path
os.chdir(scriptdir)  # Switch to Script Directory. Setting for the cron to run

# Route to get test data based on test data type you have mentioned
post_parser = reqparse.RequestParser()
post_parser.add_argument('job_name',  type=list, help='testjob1', location='json', required=True )
post_parser.add_argument('asup_id',  type=list, help='20201015160818', location='json', required=True )

# Route to get test data based on test data type you have mentioned
@verifiation_ns.route("/check_nfs_presence")

class MainClass(Resource):
    @app.doc(responses={200: 'OK'})
    @app.expect(post_parser)
    def post(self):
        json_data = request.json
        job_name = json_data["job_name"]
        asup_id = json_data["asup_id"]
        presence = nfs_verifications.check_nfs_presence(job_name, asup_id)
        return presence


# Run the Flask and make the app available for use
if __name__ == '__main__':
    sys.exit(flask_app.run(host='0.0.0.0', port=port, threaded=True))