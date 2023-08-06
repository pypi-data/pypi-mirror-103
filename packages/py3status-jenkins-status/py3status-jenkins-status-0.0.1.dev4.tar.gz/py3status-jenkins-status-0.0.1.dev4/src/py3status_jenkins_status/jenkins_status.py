# -*- coding: utf-8 -*-
"""
Displays status of jenkins jobs.

This py3status module displays the status of desired jenkins jobs.
The desired jenkins jobs are defined by configuration. The current
status of each job is represented by the i3status colors. In default
configuration of the colors is as following:

color_good     = job status "SUCCESS"
color_degraded = job status "UNSTABIL"
color_bad      = job status "FAILURE"

@authors Andreas Schmidt
@license MIT

Exsample:
```
jenkins_status {
  jenkins_url = "https://myjenkins:1234"
  jenkins_pass_path = "Jenkins"
  jobs = [
    {
      "name": "job1",
      "text": {
        "status": "J1"
      }
    },
    {
      "name": "job2",
      "text": {
        "status": "J2"
      }
    }
  ]
}
```
"""

import logging
import pypass
import jenkins
from time import time
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

log = logging.getLogger("py3status-jenkins_status")

class Py3status:

    jenkins_url = ""
    cache_timeout = 60
    jenkins_pass_path = None
    jenkins_username = None
    jenkins_password = None
    jobs = []
    default_text = {
        "status":"S",
        "not_connected":"-",
        "error":"E",
        "prefix":"JS"
    }
    jenkins_server = None


    def jenkins_status(self):
        response = {
            'cached_until': self.py3.time_in(self.cache_timeout),
        }
        if not self._set_jenkins_server():
            return self._error_response('error', set_prefix=True)
        if not self._is_jenkins_available():
            return self._error_response('not_connected', set_prefix=True)

        composite=[{'full_text': self.default_text['prefix'] + ": "}]
        if not isinstance(self.jobs, list):
          return self._error_response('error', set_prefix=True)

        for job in self.jobs:
            job_response = {}
            if not isinstance(job, dict):
                return self._error_response('error', set_prefix=True)
            # merge default_text with overriden by configuration for this job
            if 'text' in job.keys():
              text = {**self.default_text, **job['text']}
            else:
              text = self.default_text
            (result, color) = self._get_job_color(job)
            if not result:
              job_response = self._error_response('error', text=text)
            else:
              job_response['full_text'] = text['status']
              job_response['color'] = color
            composite.append(job_response)
        response['composite'] = composite
        return response


    def _error_response(self, error_text_key : str, text : dict = None, set_prefix : bool = False) -> dict:
        error_text = ""
        if not text:
            text = self.default_text
        if set_prefix:
            error_text += text['prefix'] + ": "
        error_text += text[error_text_key];
        return {
            'full_text': error_text,
            'color': self.py3.COLOR_BAD
        }


    def _set_jenkins_server(self) -> bool:
        if self.jenkins_server:
            return True
        user, pw = self._get_crendentials()
        if user is None or pw is None:
            return False
        try:
            self.jenkins_server = jenkins.Jenkins(self.jenkins_url, username=user, password=pw)
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            self.jenkins_server._session.verify = False
        except Exception as e:
            log.error("Jenkins init error: {}".format(e))
            return False
        return True


    def _is_jenkins_available(self) -> bool:
        try:
            self.jenkins_server.get_whoami()
        except Exception as e:
            log.error("Jenkins communication error: {}".format(e))
            return False
        return True


    def _get_job_color(self, job : dict):
        #TODO make colors configurable in depends of jenkins status
        try:
            job_info = self.jenkins_server.get_job_info(job['name'])
            last_build_number = job_info['lastCompletedBuild']['number']
            build_info = self.jenkins_server.get_build_info(job['name'], last_build_number)

            if build_info['result'] == "SUCCESS":
                return True, self.py3.COLOR_GOOD
            elif build_info['result'] == "UNSTABLE":
                return True, self.py3.COLOR_DEGRADED
            else:
                return True, self.py3.COLOR_BAD

        except Exception as e:
            log.error("Get jenkins job info failed: {}".format(e))
            return False, self.py3.COLOR_BAD


    def _get_crendentials(self):
        if self.jenkins_pass_path:
            return self._get_pass_crendentials()
        elif self.jenkins_username and self.jenkins_password:
            return self.jenkins_username, self.jenkins_password
        else:
            log.error("No credentials information found")
            return None, None


    def _get_pass_crendentials(self):
        try:
            ps = pypass.PasswordStore()
        except Exception as e:
            log.error("Initialization of pypass failed: {}".format(e))
            return None, None
        credentials_list = ps.get_passwords_list()
        if self.jenkins_pass_path not in credentials_list:
            log.error("No credentials under path \"{}\" found".format(self.jenkins_pass_path))
            return None, None
        user = ps.get_decrypted_password(self.jenkins_pass_path, pypass.EntryType.username)
        pw = ps.get_decrypted_password(self.jenkins_pass_path, pypass.EntryType.password)
        return user, pw


if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from py3status.module_test import module_test

    logging.basicConfig()
    log.setLevel(logging.DEBUG)

    config = {
    #    'jenkins_pass_path': "",
    #    'jenkins_url': "",
    #    'jobs': [
    #      {
    #      'job_url': ""
    #      }
    #    ]
    }

    module_test(Py3status, config)
