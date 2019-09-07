pipeline {
  agent any
  stages {
    stage('Set up Python env') {
      steps {
        sh '''python2 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
'''
      }
    }
    stage('Run tests') {
      steps {
        sh 'pytest --junitxml=pytest_jout.xml -v'
        junit(testResults: 'pytest_jout.xml', healthScaleFactor: 1)
      }
    }
  }
}