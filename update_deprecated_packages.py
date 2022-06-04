import re
import csv
from generate_pull_request import generate_pull_requests
from get_package_object import get_package_object
from write_output_csv_file import write_output_csv_file

def create_output_csv_file(input_file_name, package_name, package_version, bear_token):
    with open(input_file_name, mode ='r') as file:
        input_csv_file = csv.reader(file)
        new_csv_file = []

        # Our final output.csv file should contain these headers
        table_header_names = ["name", "repo", "version", "version_satisfied", "update_pr"]

        for values in input_csv_file:

            # package.json dependencies value is stored in dependencies object
            # values is nothing but rows in the given csv file. In this case values[0] give us repo name and
            # values[1] will give us repo link
            package_json, package_lock_json, dependencies = get_package_object(values[1], bear_token)

            if package_name in dependencies:
                each_row = []
                each_row.append(values[0])
                each_row.append(values[1])

                # The below code is used to retrieve the version of the repo package
                existing_version = dependencies[package_name]
                # The below line is used to remove symbols like "^" and "@"
                existing_version = re.sub(r"[^0-9\.]", "", existing_version)

                each_row.append(existing_version)
                if (package_version > existing_version):
                    each_row.append("false")
                    pull_request_url = generate_pull_requests(package_json, package_lock_json, package_name, package_version, existing_version, values[1], bear_token)
                    each_row.append(pull_request_url)
                    new_csv_file.append(each_row)
                else:
                    each_row.append("true")
                    new_csv_file.append(each_row)

        return table_header_names, new_csv_file, package_name

def update_deprecated_packages(input_file_name, package_name_with_version, bear_token):
    package_name = package_name_with_version.split("@")[0];
    package_version = package_name_with_version.split("@")[1];

    table_header_names, new_csv_file, package_name = create_output_csv_file(input_file_name, package_name, package_version, bear_token)
    write_output_csv_file(table_header_names, new_csv_file, package_name)