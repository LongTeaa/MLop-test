pipeline {
    agent any
    
    environment {
        // Biến môi trường
        APP_NAME = 'ml-service-v3'
        IMAGE_NAME = "ml-model:${BUILD_NUMBER}"
        PREVIOUS_STABLE = "ml-model:stable"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Prepare Model') {
            steps {
                script {
                    echo "Preparing model before build..."
                    // Có thể tải model từ Artifact của GitHub Actions nếu cần
                    // Ở đây chạy script train cho mục đích lab
                    dir('lab3') {
                        sh 'python3 train.py'
                    }
                }
            }
        }

        stage('Build Image') {
            steps {
                dir('lab3') {
                    sh "docker build -t ${IMAGE_NAME} ."
                    sh "docker tag ${IMAGE_NAME} ml-model:latest"
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                script {
                    echo "Deploying ${IMAGE_NAME} to production server..."
                    // Lưu image mới nhất vào file tạm để rollback nếu cần
                    sh "docker stop ${APP_NAME} || true"
                    sh "docker rm ${APP_NAME} || true"
                    sh "docker run -d --name ${APP_NAME} -p 5000:5000 ml-model:latest"
                    
                    // Kiểm tra sức khỏe (Health Check)
                    sh "sleep 5"
                    sh "curl -f http://localhost:5000/health || exit 1"
                    
                    // Nếu thành công, đánh dấu là stable
                    sh "docker tag ${IMAGE_NAME} ${PREVIOUS_STABLE}"
                }
            }
            post {
                failure {
                    echo "Deploy thất bại, thực hiện Rollback về version ổn định trước đó..."
                    sh './lab3/rollback.sh'
                }
            }
        }
    }
}