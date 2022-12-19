from flask import Flask, request, abort
from flask import Flask, request
import json
import gitlab
import jenkins
import requests
from jira import JIRA
from configparser import ConfigParser

config = ConfigParser()
config.read("paramjenkinsadmin.ini")

app = Flask(__name__)

@app.route('/gitlab',methods=['POST'])
def foo():
   data = json.loads(request.data)
   print("GITLAB Project")
   print (f"Project: {data['project']}\n"
          f"Event: {data['object_kind']}\n\n")

    #push->jenkins build job
   if data['object_kind'] == 'push':
      config_data = config["JENKINS"]
      hostJenkins = config_data['hostjenkins']
      usernameJenkins = config_data['usernamejenkins']
      passwordJenkins = config_data['passwordjenkins']
      server = jenkins.Jenkins(hostJenkins, username=usernameJenkins, password=passwordJenkins)
      job = config_data['job']
      server.build_job(job)
      print("\n")

    return "OK"



@app.route('/jenkins', methods=['POST'])
def foo1():
    data = json.loads(request.data)
    print(data['result'])

    #jenkins build-> update issue
    config_data3 = config["JIRA"]
    hostJira = config_data3['hostjira']
    API_token_jira = config_data3['api_token_jira']
    jira = JIRA(hostJira , token_auth=(API_token_jira))
    issueja = config_data3['issue_key']
    issue = jira.issue(issueja)
    jira.add_comment(issue, data['result'])
    print(f"Jira comment - CREATED - issue->{issueja}")
    return "OK"




if __name__ == '__main__':
    config_data4 = config["HOST"]
    host = config_data4['host']
    port = config_data4['port']
    app.run(host= host, port= port)