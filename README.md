# Jupyterlab Rucio Extension OIDC Authentication Setup

Instructions for configuring the Rucio extension and Rucio Command Line Interface (CLI) in a JupyterHub environment, such as Z2JH, with a focus on the OpenID Connect (OIDC) authentication method and process. Reference issue: https://github.com/rucio/jupyterlab-extension/issues/20

This repo contains the helm chart config for Z2JH and a custom docker file with the Rucio extension, which is build by GH Actions on push to main.

The script [token_test_script](tests/token_test_script.py) gets a access token with a password grant flow, exchanges it for a refresh token and performs some basic rucio operations for testing the valididty of the token.

## Local Setup with kind

Install `kind` and `helm`, then from the base dir run:

1. `kind create cluster`
2. ```bash
   helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
   helm repo update
   ```
3. ```bash
   helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
   helm repo update
   helm upgrade --cleanup-on-fail \
     --install jhub jupyterhub/jupyterhub \
     --namespace jhub \
     --create-namespace \
     --version=2.0.0 \
     --values helm/config.yaml
   ```
4. `kubectl --namespace=jhub port-forward service/proxy-public 8080:http`
   
Then goto localhost:8080 and login.

## Some notes on the process

- eos fuse through the [daemonset](eos-daemonset.yml) in every node - the image is still in the GitLab repo and needs to be moved and rebuild - how to treat the keytab secret?
- full functionality of the Rucio extension verified in replica mode (see helm config for most up to date config)
- the entire setup now needs to be moved to the openstack cluster to verif full functionality there
- https://github.com/rucio/jupyterlab-extension/blob/13a32b9e9b50a99fb365b50e93e85bf40b3350ca/rucio_jupyterlab/mode_handlers/replica.py#L28 - created replica rule, otherwise files that are in the mounted eos rse are available by default - this seems to be there only to speed up things, but is not necessary for the extension to work, see this test:
  ```bash
  rucio --config rucio.cfg list-rules --file test:auto_uploaded_1DuHtRWxtfXlmmH6UaXrzr7dJK4LDiES
  ID                                ACCOUNT    SCOPE:NAME                                           STATE[OK/REPL/STUCK]    RSE_EXPRESSION    COPIES    EXPIRES (UTC)    CREATED (UTC)
  --------------------------------  ---------  ---------------------------------------------------  ----------------------  ----------------  --------  ---------------  -------------------
  aac036ef00cb411abe17523be0514b13  dogosein   test:auto_uploaded_1DuHtRWxtfXlmmH6UaXrzr7dJK4LDiES  OK[1/0/0]               CERN-EOS          1                          2023-05-19 15:21:27
  ```
  