# JUnit XML action

A [Github Action](https://github.com/features/actions) that reads test results in JUnit's XML format and posts them in the [job summary](https://github.blog/2022-05-09-supercharging-github-actions-with-job-summaries/) of the job it is included in.

## Usage

To use this action in a job, include a step like this one:

```
- uses: ljpengelen/junit-xml-action@main
  if: always()
  with:
    files: "**/build/test-results/test/TEST-*.xml"
```

The input parameter `files` is a [glob pattern](https://en.wikipedia.org/wiki/Glob_(programming)) matching the file names containing the test results that you want to read and post in the job's summary.
Their location depends on the tools you use to execute tests.
For tests executed via Gradle, the files are matched by the pattern `**/build/test-results/test/TEST-*.xml`.
For tests executed via Maven's Surefire plugin, the files are matched by the pattern `**/target/surefire-reports/TEST-*.xml`.

## Development
### Getting Started

1. Install [pyenv](https://github.com/pyenv/pyenv), a tool for managing [Python](https://www.python.org/) versions.
1. The file `.python-version` in the root folder specifies the Python version required by the main Python script for this action.
  Navigate to the root folder and execute `pyenv install` to install this Python version.
1. Install [pipenv](https://pypi.python.org/pypi/pipenv) by executing `pip install pipenv`.
  There's an [issue related to language and region settings](https://github.com/pypa/pipenv/issues/538) that you might run into on Macs, but it's easy to resolve.
1. Create a new virtual environment with all dependencies by executing `pipenv install --dev --ignore-pipfile`.
  The flag `ignore-pipfile` is used to indicate that the exact versions of the dependencies as specified in `Pipfile.lock` should be installed.
  The flag `dev` is used to also install development dependencies.

### Activating the virtual environment

Before executing any of the commands below, you need to activate the virtual environment.
You can do so by executing `pipenv shell`.
Your command prompt should now indicate that you've activated the virtual environment.
It can be deactivated by executing `exit`.
