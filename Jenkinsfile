pipeline {
    agent {
        docker {
	    alwaysPull true
            image "lordmyshepherd/jenkins-build"
            args "-e SECRET_KEY=ssssss -u root:root"
        }
    }

    stages {
        stage("1. Environment Setup") {
            steps {
                echo "The build number is ${env.BUILD_NUMBER}"
		
		sh """
		    pip install -r requirements/requirements.txt

		    sudo service mysql start
		    sudo mysql -uroot -ppassowrd -e "CREATE DATABASE jenkinsdb";
                """
                }
        }
        stage("2. Build & Test") {
            steps {
                sh "python3.8 manage.py test ."
            }
        }
    }
}
