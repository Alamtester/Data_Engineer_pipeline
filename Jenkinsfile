
pipeline {

    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(
            numToKeepStr: '20'
        ))
    }

    triggers {
        cron('H * * * *')
    }

    stages {

        stage('Checkout GitHub Code') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python Environment') {
            steps {
                powershell '''
                    Write-Host "Checking Python installation..."

                    python --version

                    if ($LASTEXITCODE -ne 0) {
                        throw "Python is not available in PATH"
                    }
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    $python = Join-Path $env:WORKSPACE "venv\\Scripts\\python.exe"

                    if (!(Test-Path $python)) {
                        Write-Host "Creating virtual environment..."

                        python -m venv venv

                        if ($LASTEXITCODE -ne 0) {
                            throw "Virtual environment creation failed"
                        }
                    }

                    Write-Host "Installing dependencies..."

                    & $python -m pip install -r requirements.txt

                    if ($LASTEXITCODE -ne 0) {
                        throw "Dependency installation failed"
                    }
                '''
            }
        }

        stage('Execute Data Pipeline') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    $python = Join-Path $env:WORKSPACE "venv\\Scripts\\python.exe"

                    Write-Host "Starting SQL Server to PostgreSQL pipeline..."

                    & $python main.py

                    if ($LASTEXITCODE -ne 0) {
                        throw "Data pipeline execution failed"
                    }

                    Write-Host "Data pipeline completed successfully."
                '''
            }
        }
    }

    post {

        success {
            echo 'SUCCESS: Data pipeline completed.'
        }

        failure {
            echo 'FAILED: Data pipeline execution failed.'
        }

        always {
            echo 'Jenkins execution completed.'
        }
    }
}
