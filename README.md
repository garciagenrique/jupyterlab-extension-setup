# jupyterlab-extension-setup

 Instructions for configuring the Rucio extension and Rucio Command Line Interface (CLI) in a JupyterHub environment, such as Z2JH, with a focus on the OpenID Connect (OIDC) authentication method and process

## Local Setup with kind

Install `kind` and `helm`, then run:

* `kind create cluster`
* ```bash
  helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
  helm repo update
  helm upgrade --cleanup-on-fail \
    --install jhub jupyterhub/jupyterhub \
    --namespace jhub \
    --create-namespace \
    --version=2.0.0 \
    --values config.yaml
  ```
  