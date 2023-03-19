# prophet_model
prophet model as http service

## test deployed model



1. pull latest docker image [rkrikbaev/prophet-model:latest]
2. run dockerfile Dockerfile.yaml in the root `docker-compose up -d`
3. check container with name [prophet-model] has been started on port 8007 `docker ps -a`            
4. run test script `sh ./test/model_test.sh`
5. as result JSON message with data

<!-- sample of response:

{"model_status": "200 OK", "result": [[1676034000, 21.706878756813186], [1676037600, 27.428275384143706]...], "model_uri": null, "anomalies": null}
-->



