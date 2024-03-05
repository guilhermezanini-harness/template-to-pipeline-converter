# Harness Template Conversion Toolkit

## Overview
The Harness Template Conversion Toolkit provides a seamless solution for converting template-based pipelines into regular (non-template) pipelines in Harness platform. This toolkit is developed in response to the [feature request](https://ideas.harness.io/continuous-delivery/p/feature-request-option-to-convert-the-template-into-a-non-template) for an option to convert the template into a non-template, preserving all existing inputs. It offers developers the flexibility to utilize an existing template as-is or to copy the template into their pipeline for further customization.

## Features
- **Preserve Existing Inputs**: Converts pipeline templates into regular pipelines while maintaining all existing inputs and configurations.
- **Easy to Use**: Simplifies the process of detaching pipelines from their templates, enabling further customization without losing the initial setup.
- **Flexible Customization**: After conversion, developers can modify the pipeline without the constraints of the original template, allowing for bespoke customization.

## Prerequisites
- Python 3.6 or higher.
- Access to the Harness API and a valid API key.
- The `yaml` Python library for YAML file operations.
- The `request` Python library for API Operations.

## Installation
1. Ensure Python 3.6+ is installed on your system.
2. Clone this repository or download the toolkit scripts.
3. Install required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your Harness API key as an environment variable (`HARNESS_PLATFORM_API_KEY`) or be prepared to input it when prompted.
5. Set your pipeline URL(`HARNESS_PIPELINE_URL`) to convert into a non-template or be prepared to input it when prompted.

## Usage
1. **Start the Script**:
   Execute the main script from your terminal:
   ```bash
   python main.py
   ```
2. **Enter API Key** (if not set as an environment variable):
   You will be prompted to enter your Harness Platform API Key.
3. **Enter the Pipeline URL**:
   Input the URL of the pipeline you wish to convert. This URL should contain all necessary parameters for identifying the pipeline within Harness.
4. **Follow On-Screen Instructions**:
   The script will guide you through the conversion process, including fetching the current pipeline configuration, converting the template, and creating a new, updated pipeline.

## How It Works
- The toolkit first fetches the YAML configuration of the specified pipeline.
- It then parses this configuration to identify the template it's based on.
- The script fetches the template's YAML, combines it with the original pipeline's configurations (preserving inputs), and then creates a new pipeline instance with these combined configurations.
- The original template-based pipeline is safely deleted, and the new pipeline (now detached from the template) takes its place, ready for further customization.

## Limitations
- This toolkit requires manual execution for each pipeline conversion.
- It assumes that the user has the necessary permissions within the Harness platform to create, delete, and update pipelines.