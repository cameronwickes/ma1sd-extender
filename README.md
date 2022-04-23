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
