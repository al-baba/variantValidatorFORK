pipeline {
    agent {
        docker {
            image "docker:latest"
        }
    environment {
        CODECOV_TOKEN = "50dd5c2e-4259-4cfa-97a7-b4429e0d179e"
    }

    stages {
        stage("Check Environment") {
            steps {
                echo "Checking PATH"
                sh "echo $PATH"
            }
        }

        stage("Install Docker") {
            steps {
                sh "apt update"
                sh "apt install -y git"
            }
        }

        stage("Clone Repository") {
            steps {
                checkout scm
            }
        }

        stage("Test Syntax") {
            agent {
                docker {
                    image "docker/whalesay:latest"
                }
            }
            steps {
                echo "Running Whale Say"
                sh "cowsay 'Testing syntax check'"
            }
        }

        stage("Build VVTA") {
            agent {
                docker {
                    image "postgres:14.7"
                }
            }
            environment {
                POSTGRES_DB = "vvta"
                POSTGRES_USER = "uta_admin"
                POSTGRES_PASSWORD = "uta_admin"
            }
            steps {
                sh "echo 'shared_buffers = 2GB' > postgres_config.conf"
                sh "wget https://www528.lamp.le.ac.uk/vvdata/vvta/vvta_2023_05_no_seq.sql.gz -O input_file.sql.gz"
                sh "gzip -dq input_file.sql.gz"
                sh "sed 's/anyarray/anycompatiblearray/g' input_file.sql > modified_file.sql"
                sh "gzip modified_file.sql"
                sh "docker cp postgres_config.conf postgres-vvta:/docker-entrypoint-initdb.d/postgresql.conf"
                sh "docker cp modified_file.sql.gz postgres-vvta:/docker-entrypoint-initdb.d/vvta_2023_05_noseq.sql.gz"
            }
        }

        stage("Mount VVTA") {
            steps {
                sh "docker run -d --name postgres-vvta -p 5432:5432 postgres:14.7"
                sh "docker network connect bridge postgres-vvta"
            }
        }

        stage("Build Validator") {
            agent {
                docker {
                    image "ubuntu/mysql:8.0-22.04_beta"
                }
            }
            environment {
                MYSQL_RANDOM_ROOT_PASSWORD = "yes"
                MYSQL_DATABASE = "validator"
                MYSQL_USER = "vvadmin"
                MYSQL_PASSWORD = "var1ant"
            }
            steps {
                sh "apt-get update && apt-get install -y wget"
                sh "wget https://www528.lamp.le.ac.uk/vvdata/validator/validator_2023_08.sql.gz -O /docker-entrypoint-initdb.d/validator_2023_08.sql.gz"
            }
        }

        stage("Mount Validator") {
            steps {
                sh "docker run -d --name mysql-validator -p 3306:33306 ubuntu/mysql:8.0-22.04_beta"
                sh "docker network connect bridge mysql-validator"
            }
        }

        stage("Build SeqRepo") {
            agent {
                docker {
                    image "ubuntu:22.04"
                    args '-v $WORKSPACE:/workspace'
                }
            }
            steps {
                sh "apt-get update"
                sh "apt-get install -y wget"
                sh "mkdir -p /workspace/seqrepo"
                sh "wget --output-document=/workspace/seqrepo/VV_SR_2023_05.tar https://www528.lamp.le.ac.uk/vvdata/vv_seqrepo/VV_SR_2023_05.tar"
                sh "tar -xvf /workspace/seqrepo/VV_SR_2023_05.tar --directory /workspace/seqrepo"
                sh "rm /workspace/seqrepo/VV_SR_2023_05.tar"
            }
        }

        stage("Build and Test VariantValidator") {
            agent {
                docker {
                    image "python:3.10"
                }
            }
            steps {
                sh "apt-get update"
                sh "apt-get install -y wget"
                sh "mkdir -p /usr/local/share/seqrepo"
                sh "wget --output-document='/usr/local/share/seqrepo/VV_SR_2023_05.tar' https://www528.lamp.le.ac.uk/vvdata/vv_seqrepo/VV_SR_2023_05.tar"
                sh "tar -xvf /usr/local/share/seqrepo/VV_SR_2023_05.tar -C /usr/local/share/seqrepo/"
                sh "pip install --upgrade pip"
                sh "pip install ."
                sh "cp configuration/continuous_integration.ini \"$HOME\"/.variantvalidator"
                sh "pytest --cov-report=term --cov=VariantValidator/"
                sh "codecov"
            }
        }

        stage("Cleanup Docker") {
            steps {
                sh "docker stop postgres-vvta"
                sh "docker rm postgres-vvta"
                sh "docker stop mysql-validator"
                sh "docker rm mysql-validator"
                sh "docker rmi postgres:14.7"
                sh "docker rmi ubuntu/mysql:8.0-22.04_beta"
            }
        }
    }
}
