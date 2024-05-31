pipeline {
    agent any
    environment {
        OCI_CREDENTIALS = credentials('oci-user-authtoken')
        BOT_CREDENTIALS = credentials('d04f8052-8f74-4c4e-9617-c24969d413c7')
        PATH = "/home/jenkins/bin:${env.PATH}"
    }
    stages{
        stage('Build docker image'){
            steps{
                script{
                    sh "docker build -t open-ai-flask-app:${BUILD_NUMBER}-${GIT_COMMIT} ."
                }
            }
        }
        stage('Push image to OCI Container Registry'){
            steps{
                script{
                    sh 'echo ${OCI_CREDENTIALS_PSW} | docker login --username ${OCI_CREDENTIALS_USR} --password-stdin qro.ocir.io'
                    sh "docker tag open-ai-flask-app:${BUILD_NUMBER}-${GIT_COMMIT} qro.ocir.io/ax6svbbnc2oh/open-ai-flask-app:${BUILD_NUMBER}-${GIT_COMMIT}"
                    sh "docker push qro.ocir.io/ax6svbbnc2oh/open-ai-flask-app:${BUILD_NUMBER}-${GIT_COMMIT}"
                }
            }
        }
        stage('Push to cluster'){
            steps{
                script{
                    sh 'kubectl apply -f deploymentOpenAi.yaml'
                    sh 'kubectl apply -f ingress-nginx.yaml'
                    sh 'kubectl rollout restart deployment openai-flask-deployment'
                }
            }
        }
        stage('Cleanup'){
            steps{
                script{
                    sh 'rm /home/jenkins/.docker/config.json'
                    sh 'docker logout'
                }
                cleanWs()
            }
        }
    }
}