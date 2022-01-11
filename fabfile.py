# from fabric import task
import datetime
import json

import boto3
from fabric.api import local

REPOSITORIES = {
    "prod": {
        "django": "site-recsys/django",
        "nginx": "site-recsys/nginx",
    },
}

ECS_DEPLOY_TARGETS = {
    "prod": [
        {"cluster": "prod-cluster", "service": "server-django"},
        # {"cluster": "prod-cluster", "service": "service-nginx"},
    ],
}

def deploy(profile='default', phase='prod'):

    profileArg = ""
    if profile == "ym":
        profileArg = f"--profile site_recsys"

    account_id = local(
        f"aws sts get-caller-identity --output text --query 'Account' {profileArg}",
        capture=True,
    )
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 로그인
    local(
        f"aws ecr get-login-password {profileArg} | "
        f"docker login --username AWS "
        f"--password-stdin {account_id}.dkr.ecr.ap-northeast-2.amazonaws.com/"
    )

    repo_url = f"{account_id}.dkr.ecr.ap-northeast-2.amazonaws.com/"

    # 레포지트리 URL를 구함
    repo_name = REPOSITORIES[phase]
    django_repo_url = f"{repo_url}{repo_name['django']}"
    nginx_repo_url = f"{repo_url}{repo_name['nginx']}"

    # # 이미지 빌드
    # local(f"docker-compose up -d")
    local(
        f"docker build . "
        f"-f docker/django/Dockerfile "
        f"--tag {django_repo_url}"
    )
    local(f"docker tag {django_repo_url}:latest {django_repo_url}:{timestamp}")
    local(f"docker tag backend_django:latest {django_repo_url}:{timestamp}")

    local(
        f"docker build . "
        f"-f docker/nginx/Dockerfile "
        f"--tag {nginx_repo_url}"
    )
    local(f"docker tag {nginx_repo_url}:latest {nginx_repo_url}:{timestamp}")
    local(f"docker tag nginx:latest {nginx_repo_url}:{timestamp}")

    # 이미지를 ECR으로 푸쉬
    local(f"docker push {django_repo_url}:{timestamp}")
    local(f"docker push {nginx_repo_url}:{timestamp}")

    local(f"docker tag {django_repo_url}:{timestamp} {django_repo_url}:latest")
    local(f"docker tag {nginx_repo_url}:{timestamp} {nginx_repo_url}:latest")

    local(f"docker push {django_repo_url}:latest")
    local(f"docker push {nginx_repo_url}:latest")

    update_service_command = (
        "aws ecs update-service --cluster {cluster} "
        "--service {service} --region ap-northeast-2 --force-new-deployment {profileArg}"
    )

    # 서비스를 업데이트
    ecs_deploy_target = ECS_DEPLOY_TARGETS[phase]
    for target in ecs_deploy_target:
        cluster = target["cluster"]
        service = target["service"]
        local(update_service_command.format(cluster=cluster, service=service, profileArg=profileArg))

def load_secrets(profile='default',phase='prod'):

    if profile == 'ym':
        profile = 'site_recsys'

    secret_name = f"site-recsys/prod"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="ap-northeast-2",
    )
    secrets = client.get_secret_value(SecretId=secret_name)
    secrets = json.loads(secrets['SecretString'])

    with open(".env", "w") as f:
        f.write("\n".join(f'{key}="{value}"' for key, value in sorted(secrets.items())))

