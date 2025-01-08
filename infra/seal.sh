#!/bin/bash

# Check if the input file ends with -secret.yaml
if [[ $1 != *-secret.yaml ]]; then
  echo "Error: The input file must end with '-secret.yaml'."
  exit 1
fi

# Generate the output file name by replacing -secret.yaml with -sealedsecret.yaml
output_file="${1/-secret.yaml/-sealedsecret.yaml}"

# Run kubeseal with the generated output file name
kubeseal --cert cert.pub -f "$1" -w "$output_file"
