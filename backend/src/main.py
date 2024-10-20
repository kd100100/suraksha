import json
import argparse
import time
from typing import Dict, Any, List
from validators.impl.sql_injection_validator import SQLInjectionValidator
from validators.impl.dom_injection_validator import DOMInjectionValidator
from validators.impl.string_length_validator import StringLengthValidator
from models.validation_result import ValidationResult, ValidationSummary


def load_api_specs(file_path: str) -> List[Dict[str, Any]]:
    """Load API specifications from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def run_validation(api_specs: List[Dict[str, Any]]) -> List[ValidationSummary]:
    """Run SQL injection, DOM injection, and string length validations for each API specification."""
    sql_validator = SQLInjectionValidator()
    dom_validator = DOMInjectionValidator()
    string_length_validator = StringLengthValidator()
    all_summaries = []

    for spec in api_specs:
        method = spec.get('method', 'GET')
        url = spec['url']
        url_params = spec.get('url_params', {})
        headers = spec.get('headers', {})
        req_body = spec.get('body', {})

        sql_results = sql_validator.validate(
            method, url, url_params, req_body, headers)
        dom_results = dom_validator.validate(
            method, url, url_params, req_body, headers)
        string_length_results = string_length_validator.validate(
            method, url, url_params, req_body, headers)

        all_summaries.extend([
            ValidationSummary.create("SQL_INJECTION", url, sql_results),
            ValidationSummary.create("DOM_INJECTION", url, dom_results),
            ValidationSummary.create(
                "STRING_LENGTH", url, string_length_results)
        ])

    return all_summaries


def save_results(summaries: List[ValidationSummary], output_file: str = 'results.json') -> None:
    """Save validation summaries to a JSON file."""
    with open(output_file, "w") as f:
        json.dump([summary.to_dict() for summary in summaries], f, indent=2)

    with open("../frontend/public/results.json", "w") as f:
        json.dump([summary.to_dict() for summary in summaries], f, indent=2)
    print(f"Validation complete. Results saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Run SQL injection, DOM injection, and string length validations on API specifications.")
    parser.add_argument(
        'spec_file', help="Path to the API specification JSON file")
    args = parser.parse_args()

    api_specs = load_api_specs(args.spec_file)
    validation_summaries = run_validation(api_specs)
    save_results(validation_summaries)


if __name__ == "__main__":
    main()
