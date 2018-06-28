import subprocess
import commands
import json
import time 
import argparse


app_arn = ''
app_url = ''
test_app_arn = ''
test_app_url = ''
testname = ''
status = ''

parser = argparse.ArgumentParser()

parser.add_argument(
    "-n",
    "--name",
    help="The name of the test to be schduled",
    required=True)
args = parser.parse_args()
testname = args.name

app_upload = commands.getstatusoutput("aws devicefarm create-upload --project-arn arn:aws:devicefarm:us-west-2:028957328603:project:4de09718-8dad-467f-80af-b30f60bdeacd --name app-release.apk --type ANDROID_APP")
j = json.loads(app_upload[1])['upload']

if(j['status'] == "INITIALIZED"):
    app_arn = j['arn']
    app_url =  j['url']

app_upload_finish = commands.getstatusoutput("curl -T app-release.apk "  + '"' + app_url + '"')

app_upload_check = commands.getstatusoutput("aws devicefarm get-upload --arn " + app_arn)

j = json.loads(app_upload_check[1])['upload']
if(j['status'] == "SUCCEEDED"):
	print "App upload SUCCEEDED"


test_app_upload = app_upload = commands.getstatusoutput("aws devicefarm create-upload --project-arn arn:aws:devicefarm:us-west-2:028957328603:project:4de09718-8dad-467f-80af-b30f60bdeacd --name appium_tests.zip --type APPIUM_JAVA_TESTNG_TEST_PACKAGE")
j = json.loads(test_app_upload[1])['upload']

if(j['status'] == "INITIALIZED"):
    test_app_arn = j['arn']
    test_app_url =  j['url']

test_app_upload_finish = commands.getstatusoutput("curl -T appium_tests.zip "  + '"' + test_app_url + '"')

test_app_upload_check = commands.getstatusoutput("aws devicefarm get-upload --arn " + test_app_arn)

j = json.loads(test_app_upload_check[1])['upload']
if(j['status'] == "SUCCEEDED"):
	print "Test app upload SUCCEEDED"

print "Now scheduling a test run \n"

schedule_run_con = "aws devicefarm schedule-run --project-arn arn:aws:devicefarm:us-west-2:028957328603:project:4de09718-8dad-467f-80af-b30f60bdeacd --app-arn " + app_arn + " --device-pool-arn arn:aws:devicefarm:us-west-2:028957328603:devicepool:4de09718-8dad-467f-80af-b30f60bdeacd/fb5fe3bf-93f9-4a43-8734-e9c04fceebba --name " + testname + " --test \'{\"type\":\"APPIUM_JAVA_TESTNG\",\"testPackageArn\":\"" + test_app_arn + "\"}\' --configuration \'{\"location\":{\"latitude\":40.7247,\"longitude\":-73.9478},\"radios\":{\"wifi\": true,\"bluetooth\": true,\"nfc\": true,\"gps\": true},\"billingMethod\":\"UNMETERED\"}\'"

schedule_run = commands.getstatusoutput(schedule_run_con)
j = json.loads(schedule_run[1])['run']
status = j['status']
run_arn = j['arn']
print ("{} is {}".format(testname, status))

while (status == "SCHEDULING" or status== "RUNNING" or status== "PENDING"):
	print "sleeping for 10 minutes for results"
	time.sleep(120)
	run_status = commands.getstatusoutput('aws devicefarm get-run --arn ' + run_arn)
	j = json.loads(run_status[1])['run']
	status = j['status']
	print status
	if (status == "COMPLETED"):
		break

print ("Total Tests: {}".format(j['counters']['total']))
print ("passed Tests: {}".format(j['counters']['passed']))
print ("failed Tests: {}".format(j['counters']['failed']))
print ("skipped Tests: {}".format(j['counters']['skipped']))
print ("warned Tests: {}".format(j['counters']['warned']))
print ("stopped Tests: {}".format(j['counters']['stopped']))
print ("errored Tests: {}".format(j['counters']['errored']))