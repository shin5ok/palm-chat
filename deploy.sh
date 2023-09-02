NAME=${1:-palm2-chat}
PROJECT_ID=$(gcloud config get project)
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")

gcloud run deploy \
    ${NAME} \
    --region=asia-northeast1 \
    --source=. \
    --max-instances=1 \
    --memory=1Gi \
    --allow-unauthenticated \
    --set-env-vars=PROJECT_NUMBER=${PROJECT_NUMBER},PROJECT_ID=${PROJECT_ID}

