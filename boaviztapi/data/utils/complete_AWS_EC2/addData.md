# addData.go

This script add aws instances to aws.csv that are not already included based on a export of data from Vantage.

## Usage

```sh
# Inside PROJECT/hack/complete_AWS_EC2/
go run complete_AWS_EC2.go
```

## Getting Vantage export
1. Go to https://instances.vantage.sh.
2. Add all columns
3. Click export in upper right corner, left to the search bar.
4. Override PROJECT/hack/addData/vantage-export.csv
