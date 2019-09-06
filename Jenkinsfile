pipeline {
  agent any
  stages {
    stage('') {
      steps {
        sh '''python -m virtaulenv venv
source venv/bin/activate
pip install -r requirements.txt
pytest'''
      }
    }
  }
}