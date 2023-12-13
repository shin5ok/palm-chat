SA:=parm2-api@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com

.PHONY: deploy
deploy:
	bash ./scripts/deploy.sh

.PHONY: sa
sa:
	gcloud iam service-accounts create palm2-api
	gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} --member=$(SA) --role=roles/aiplatform.user

.PHONY: test-local
test-local:
	echo 'token=test_token&team_id=TCAP5P4EQ&team_domain=shin5ok&service_id=5838650690709&channel_id=C05QNK1JK45&channel_name=palm2-chat&timestamp=1697634721.315859&user_id=UCB0LHTUJ&user_name=shingo.slack&text=hey' | curl localhost:8080/chat/slack -X POST -d @-

.PHONY: run-local
run-local:
	SLACK_TOKEN=test_token poetry run python main.py

