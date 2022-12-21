import json
import time
from configparser import ConfigParser
from flask import Flask, request
from api4jenkins import Jenkins
from jira import JIRA



config = ConfigParser()
config.read("paramjenkinsadmin.ini")

app = Flask(__name__)

@app.route('/gitlab',methods=['POST'])
def gitlab_push():
    data = json.loads (request.data)
    print ("GITLAB Project")
    print (f"Project: {data['project']}\n"
          f"Event: {data['object_kind']}\n\n")

    #push
    if data ['object_kind'] == 'push':
        config_data = config ["JENKINS"]
        host_jenkins = config_data ['hostjenkins']
        username_jenkins = config_data ['usernamejenkins']
        password_jenkins = config_data ['passwordjenkins']
        server = Jenkins (host_jenkins, auth = (username_jenkins, password_jenkins))
        job_name = config_data ['job']
        job = server.get_job (job_name) 
        item = job.build ()
        while not item.get_build ():
            time.sleep (1)
        build = item.get_build ()
        while build.building:
            time.sleep (1)
        while build.result is None:
            time.sleep (1)
        print (build.result)
        resultt = build.result

        config_data3 = config ["JIRA"]
        host_jira = config_data3 ['hostjira']
        api_token_jira = config_data3 ['api_token_jira']
        jira = JIRA (host_jira , token_auth = (api_token_jira))

        issueja = config_data3 ['issue_key']
        issue = jira.issue (issueja)
        jira.add_comment (issue, f"Pipeline result: {resultt}.")
    return "OK"





if __name__ == '__main__':
    config_data4 = config ["HOST"]
    host = config_data4 ['host']
    port = config_data4 ['port']
    app.run (host= host, port= port)
