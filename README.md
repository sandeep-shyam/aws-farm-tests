# aws-devicefarm-tests

This script needs the path of app-release.apk and appium_tests.zip files and also need Test Name with -n --name option

Also the build agent should be configured to have latest AWS CLI and proper credentials to initiate tests on AWS Device Farm

# How to initiate the script
python aws-devicefarm.py -n <Testname>
  
  Test Name can be any alphanumeric string without any spaces or special characters
