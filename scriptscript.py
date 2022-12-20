from flask import Flask, request, abort
from flask import Flask, request
from api4jenkins import Jenkins
from configparser import ConfigParser
from jira import JIRA
import json
import gitlab
import jenkins
import requests
import time



config = ConfigParser()
config.read("paramjenkinsadmin.ini")

app = Flask(__name__)

@app.route('/gitlab',methods=['POST'])
def foo():
   data = json.loads(request.data)
   print("GITLAB Project")
   print (f"Project: {data['project']}\n"
          f"Event: {data['object_kind']}\n\n")
    #push
   if data['object_kind'] == 'push':
      config_data = config["JENKINS"]
      hostJenkins = config_data['hostjenkins']
      usernameJenkins = config_data['usernamejenkins']
      passwordJenkins = config_data['passwordjenkins']
      server = Jenkins(hostJenkins, auth=(usernameJenkins,passwordJenkins))
      
      job_name = config_data['job']
      job = server.get_job(job_name) 
      item = job.build()
      while not item.get_build():
         time.sleep(1)
      global build
      build = item.get_build()
      while build.building:
         time.sleep(1)
      while build.result == None:
         time.sleep(1)
      print (build.result)
      resultt = build.result

      config_data3 = config["JIRA"]
      hostJira = config_data3['hostjira']
      API_token_jira = config_data3['api_token_jira']
      jira = JIRA(hostJira , token_auth=(API_token_jira))

      issueja = config_data3['issue_key']
      issue = jira.issue(issueja)
      jira.add_comment(issue, f"Pipeline result: {resultt}. GitLab-Merge request can be accepted.")

   
   return "OK"





if __name__ == '__main__':
    config_data4 = config["HOST"]
    host = config_data4['host']
    port = config_data4['port']
    app.run(host= host, port= port)
