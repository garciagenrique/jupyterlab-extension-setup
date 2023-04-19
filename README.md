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
