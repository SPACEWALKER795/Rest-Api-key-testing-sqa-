@echo off
echo Cleaning old results...
rmdir /s /q allure-results

echo Running tests - pass 1...
py -m pytest tests/ --alluredir=allure-results -v

echo Running tests - pass 2 for trend...
py -m pytest tests/ --alluredir=allure-results -v

echo Copying categories...
copy categories.json allure-results\categories.json

echo Writing environment info...
echo Base.URL=https://jsonplaceholder.typicode.com > allure-results\environment.properties
echo Project.Name=SQA REST API Test Suite >> allure-results\environment.properties
echo Environment=Test >> allure-results\environment.properties
echo Developer=Rehan >> allure-results\environment.properties
echo Python.Version=3.11 >> allure-results\environment.properties

echo Generating JSON report...
py -m pytest tests/ --json-report --json-report-file=results.json -v

echo Generating custom dashboard...
py generate_dashboard.py

echo Opening Allure report...
allure serve allure-results