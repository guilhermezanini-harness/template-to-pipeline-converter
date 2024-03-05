import yaml
import os

from library import helpers, harness_service

def main():
    api_key = os.environ.get('HARNESS_PLATFORM_API_KEY')
    if not api_key:
        api_key = input("Enter your API key: ")

    pipeline_url = os.environ.get('HARNESS_PIPELINE_URL')
    if not pipeline_url:
        pipeline_url = input("Enter the pipeline URL: ")

    # Extract necessary parameters from the pipeline URL for API requests.
    pipeline_parameters = helpers.extract_parameters_from_url(pipeline_url)

    # Initialize the HarnessService with the API key and account identifier.
    harness_api = harness_service.HarnessService(api_key, pipeline_parameters['account_identifier'])

    print("Loading the pipeline YAML for pipeline: " + pipeline_parameters["pipeline_identifier"])

    pipeline_yaml = harness_api.fetch_pipeline_yaml(
        pipeline_parameters["org_identifier"],
        pipeline_parameters["project_identifier"],
        pipeline_parameters["pipeline_identifier"]
    )['pipeline_yaml']

    pipeline_json = yaml.safe_load(pipeline_yaml).copy()

    if pipeline_json:
        template_ref = pipeline_json['pipeline']['template']['templateRef']
        template_version = pipeline_json['pipeline']['template']['versionLabel']

        print("Loading the template YAML for template: " + template_ref + " with the version label: " + template_version)

        # Fetch the YAML for the template used in the pipeline.
        template_response = harness_api.fetch_template_yaml(
            template_ref,
            template_version,
            pipeline_parameters["org_identifier"],
            pipeline_parameters["project_identifier"]
        )

        if template_response:
            template_yaml = template_response['template']['yaml']
            template_json = yaml.safe_load(template_yaml)

            replaced_pipeline = helpers.find_and_update_json_values(template_json, pipeline_json)

            # Prepare the updated pipeline payload for creation.
            pipeline_payload_conversion = {
                "pipeline": {
                    **replaced_pipeline['template']['spec'],
                    "identifier": pipeline_json['pipeline']['identifier'] + "_temporary",
                    "name": pipeline_json['pipeline']['identifier'] + "_temporary"
                }
            }
            
            pipeline_data = {
                "pipeline_yaml": yaml.dump(pipeline_payload_conversion),
                "identifier": pipeline_payload_conversion['pipeline']['identifier'],
                "name": pipeline_payload_conversion['pipeline']['name']
            }

            print("Creating a new pipeline...")
            response = harness_api.create_pipeline(
                pipeline_parameters["org_identifier"], 
                pipeline_parameters["project_identifier"], 
                pipeline_data
            )

            print("Deleting the old pipeline...")
            harness_api.delete_pipeline(pipeline_parameters['org_identifier'], pipeline_parameters['project_identifier'], pipeline_json['pipeline']['identifier'])
            print("Pipeline deleted successfully.")
            
            print("Renaming new pipeline...")
            pipeline_payload_conversion['pipeline']['name'] = pipeline_json['pipeline']['name']
            pipeline_data = {
                "pipeline_yaml": yaml.dump(pipeline_payload_conversion),
                "identifier": pipeline_payload_conversion['pipeline']['identifier'],
                "name": pipeline_json['pipeline']['name']
            }
            harness_api.update_pipeline(pipeline_parameters['org_identifier'], pipeline_parameters['project_identifier'], pipeline_data, pipeline_payload_conversion['pipeline']['identifier'])

        else:
            print("Failed to fetch template YAML. Response:", template_response)
    else:
        print("Failed to fetch pipeline YAML. Response:", pipeline_yaml)

if __name__ == "__main__":
    main()