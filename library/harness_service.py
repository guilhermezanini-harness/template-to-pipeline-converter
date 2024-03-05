import requests

class HarnessService:
    def __init__(self, api_key, account_identifier):
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': api_key,
            'Harness-Account': account_identifier,
            'Content-Type': 'application/json'
        })
        self.base_url = "https://app.harness.io"

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        if response.status_code == 200:
            return response.json()
        print(response.text)
        response.raise_for_status()
    
    def fetch_pipeline_yaml(self, org_identifier, project_identifier, pipeline_identifier):
        endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/pipelines/{pipeline_identifier}"
        return self._make_request("GET", endpoint)
    
    def fetch_template_yaml(self, template_identifier, version, org_identifier=None, project_identifier=None):
        if template_identifier.startswith("org"):
            endpoint = f"/v1/orgs/{org_identifier}/templates/{template_identifier}/versions"
        elif template_identifier.startswith("account"):
            endpoint = f"/v1/templates/{template_identifier}/versions"
        else:
            endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/templates/{template_identifier}/versions/{version}"
        return self._make_request("GET", endpoint)
    
    def create_pipeline(self, org_identifier, project_identifier, pipeline_data):
        endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/pipelines"
        return self._make_request("POST", endpoint, json=pipeline_data)
    
    def update_pipeline(self, org_identifier, project_identifier, pipeline_data, pipeline_identifier):
        endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/pipelines/{pipeline_identifier}"
        return self._make_request("PUT", endpoint, json=pipeline_data)
    
    def delete_pipeline(self, org_identifier, project_identifier, pipeline_identifier):
        endpoint = f"/v1/orgs/{org_identifier}/projects/{project_identifier}/pipelines/{pipeline_identifier}"
        return self._make_request("DELETE", endpoint)