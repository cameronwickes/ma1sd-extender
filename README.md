<h1 align="center">
  <img alt="matrix logo" src="https://www.cameronwickes.co.uk/ma1sd-extender.png" width="250px"/><br/>
  Matrix-Automation
</h1>

<p align="center">
  <img alt="Supported Platforms" src="https://img.shields.io/badge/Platform-Linux-blueviolet?color=blue&style=for-the-badge">
  <img alt="Language" src="https://img.shields.io/badge/Language-Python-blue?color=blueviolet&style=for-the-badge">
  <img alt="License" src="https://img.shields.io/github/license/cameronwickes/ma1sd-extender?color=brightgreen&style=for-the-badge">
</p>

<p align="center">
  An API, built with <b>Docker</b> and <b>FastAPI</b>, that allows <b>Matrix</b> user directory searches to be recursively federated for corporate use.
</p>

</br>

<p>
  <b>MA1SD-Extender performs the following sequence of actions in order to recursively federate directory lookups:</b>
  <ul>
    <li>Checks the validity of API supplied credentials</li>
    <li>Checks the validity of a user specified authorisation token against all federation domains</li>
    <li>Returns previously cached responses for faster lookups</li>
    <li>Searches within local directory for users</li>
    <li>Recursively searches other federation domains for users</li>
    <li>Returns pooled responses masquerading as the local MA1SD server</li>
  </ul>
  
  </br>
  
  MA1SD-Extender is available from this repository, and can also be found on the <a target="_blank" href="https://hub.docker.com/repository/docker/cameronwickes/ma1sd-extender">Docker Hub</a>.
</p>

## ⚙️ Configuration Variables

The following environment variables are required by MA1SD-Extender:

- `MA1SD_EXTENDER_USERNAME`: The username for MA1SD-Extender access.
- `MA1SD_EXTENDER_PASSWORD`: The password for MA1SD-Extender access.
- `MA1SD_EXTENDER_MATRIX_DOMAIN`: The domain that Synapse and MA1SD are running on.
- `MA1SD_EXTENDER_FEDERATED_DOMAINS`: Any domains to be recursively federated.

MA1SD-Extender needs a valid account on the local Synapse homeserver, specified by the `MA1SD_EXTENDER_USERNAME` and `MA1SD_EXTENDER_PASSWORD` variables.

## 🐍 Running With Python

MA1SD-Extender can be run with Python, Poetry and FastAPI.

```bash
export MA1SD_EXTENDER_USERNAME="X" MA1SD_EXTENDER_PASSWORD="X" MA1SD_EXTENDER_MATRIX_DOMAIN="X" MA1SD_EXTENDER_FEDERATED_DOMAINS="['X']"
poetry install
uvicorn --reload --host='0.0.0.0' --port=PORT_NUMBER ma1sd-extender.main:app
```

## 📦 Running With Docker/Podman

MA1SD-Extender can also be run with Docker/Podman using the following commands:

```bash
docker pull cameronwickes/ma1sd-extender:latest
docker run --name ma1sd \
-e MA1SD_EXTENDER_USERNAME="X" \
-e MA1SD_EXTENDER_PASSWORD="X" \
-e MA1SD_EXTENDER_MATRIX_DOMAIN="X" \
-e MA1SD_EXTENDER_FEDERATED_DOMAINS="['X']" \
ma1sd-extender:latest
```

## ⚖️ License

`MA1SD-Extender` is free and open-source software licensed under the [Apache 2.0 License](https://github.com/cameronwickes/ma1sd-extender/blob/main/LICENSE).
