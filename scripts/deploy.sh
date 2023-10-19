NAME=${1:-palm2-chat}
PROJECT_ID=$(gcloud config get project)
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
SA=palm2-api@${PROJECT_ID}.iam.gserviceaccount.com

CMD="gcloud run deploy \
    ${NAME} \
    --region=asia-northeast1 \
    --source=. \
    --memory=1Gi \
    --set-env-vars=PROJECT_NUMBER=${PROJECT_NUMBER},PROJECT_ID=${PROJECT_ID},SLACK_TOKEN=${SLACK_TOKEN} \
    --service-account=${SA} \
    --allow-unauthenticated $@"

eval $CMD
