# LiteLLM-Exposure-PoC-to-find-vulnerable-versions

This script is used to find vulnerable versions from a list of domains. 
It checks LiteLLM responses and collects version information from the traffic. 
Then, it creates a file named evraka.txt with this list. 
The script is based on the LiteLLM exposure incident from March 2026.

# Usage
Create the Virtual Environment:

Bash
python3 -m venv venv
Activate the Environment:

Bash
source venv/bin/activate
(You should now see (venv) at the start of your terminal line.)

Install the Required Library:

Bash
pip install requests
Run Your Script:

Bash
python3 script.py
