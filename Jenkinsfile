pipeline {
  agent any
  stages {
    stage('error') {
      steps {
        sh '''python2 -m virtaulenv venv
source venv/bin/activate
pip install -r requirements.txt
'''
      }
    }
  }
}