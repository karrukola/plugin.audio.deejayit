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
        sh '''
        source venv/bin/activate
        pip -V
        pytest --junitxml=pytest_jout.xml -v
        '''
        junit(testResults: 'pytest_jout.xml', healthScaleFactor: 1)
      }
    }
  }
  post {
    always {
      emailext body: '$DEFAULT_CONTENT',
        subject: '$DEFAULT_SUBJECT',
        to: '$DEFAULT_RECIPIENTS'
    }
  }
}
