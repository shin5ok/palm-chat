.PHONY: deploy
deploy:
	bash ./scripts/deploy.sh

.PHONY: sa
sa:
	gcloud iam service-accounts create palm2-api
	gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=$LOGSA --role=roles/aiplatform.user

