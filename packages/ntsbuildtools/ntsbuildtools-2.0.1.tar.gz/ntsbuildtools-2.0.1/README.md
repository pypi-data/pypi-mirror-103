# BuildTools Project Description

[![PyPI version](https://badge.fury.io/py/ntsbuildtools.svg)](https://badge.fury.io/py/ntsbuildtools)

This is a collection of scripts that supports UO's Network and Telecom Services team (NTS) continuous integration and deployment solutions. 

> At this time, BuildTools provides integrations with BitBucket Server, GitHub, and Microsoft Teams.

## Install BuildTools

BuildTools is packaged as `ntsbuildtools` and provided in the Python Package Index (PyPI).
So, simply use pip to install BuildTools.

    pip install ntsbuildtools

## BuildTools Usage

With BuildTools installed, the `buildtools` CLI utility should now be available in your shell.

    $ buildtools --version
    BuildTools Version: 1.3.5

Below is an example of posting a comment onto an existing BitBucket Pull Request.

    $ buildtools post bitbucket pr-comment \
        --bitbucket-url https://git.uoregon.edu \
        --user rleonar7 \ 
        --password SuperSecretPassword \ 
        --project ISN \
        --repo buildtools \
        --pull-request-id 2 \ 
        --message "Hello, world! I am BuildTools!"

![Screenshot of the created pull request comment.](https://uoregon-my.sharepoint.com/:i:/r/personal/rleonar7_uoregon_edu/Documents/share/post-bb-pr-comment.png)

## BuildTools Capabilities

BuildTools has many capabilities. These capabilities are provided as subcommands. 
To discover the subcommands available in your version of BuildTools, use the `--help` argument anywhere in the CLI. 

> BuildTools capabilities can discovered much more easily when using tab completion -- **how to enable tab completion via `argcomplete` is discussed below.**

In the example below, we see how the `--help` flag informs us that the `buildtools post bitbucket pr-comment` command is available and how to run it!

    $ buildtools --help
    usage: buildtools [-h] [--version] [--bitbucket-url BITBUCKET_URL] {post,parse} ...
     
    positional arguments:
      {post,parse}
        post                Make an HTTP POST to a target.
        parse               Parse some input (typically from a file).

    $ buildtools post --help
    usage: buildtools post [-h] {bitbucket,teams,github} ...
    
    positional arguments:
      {bitbucket,teams,github}
        bitbucket           Target Bitbucket.
        teams               Target Microsoft Teams.
        github              Target GitHub.

    $ buildtools post bitbucket --help
    usage: buildtools post bitbucket [-h] {build-status,pr-comment} ...
    
    positional arguments:
      {build-status,pr-comment}
        build-status        Set the "Build Status" in Bitbucket for a particular git commit.
        pr-comment          Posts a comment to a Bitbucket pull request, with optional arguments for 'Jenkins build 
                            annotations', indicating build status, encasing content in 'diff markdown', and more!

    $ buildtools post bitbucket pr-comment --help
    usage: buildtools post bitbucket pr-comment [-h] [--version] [--bitbucket-url BITBUCKET_URL]
                                                (--message COMMENT_MESSAGE | --file COMMENT_FILE | --json JSON_OUTPUT | --json-file JSON_FILE)
                                                --user USER --password PASSWORD --project PROJECT
                                                --repo REPO --pull-request-id PULL_REQUEST_ID
                                                [--diff-markdown] [--clean-ansi-colors]
                                                [--code-markdown]
                                                [--max-comment-size MAX_COMMENT_SIZE] [--tail TAIL]
                                                [--build-annotation]
                                                [--playbook-limit PLAYBOOK_LIMIT]
                                                [--build-id BUILD_ID] [--build-url BUILD_URL]
                                                [--build-status {SUCCESS,UNSTABLE,FAILURE,NOT_BUILD,ABORTED}]
    
    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --bitbucket-url BITBUCKET_URL
                            URL for Bitbucket. [env var: BITBUCKET_URL]
      --message COMMENT_MESSAGE, -m COMMENT_MESSAGE
                            Provide the comment as a message on the command line.
      --file COMMENT_FILE, -f COMMENT_FILE
                            Provide the comment in a file.
      --json JSON_OUTPUT, -j JSON_OUTPUT
                            Provide ansible JSON output as a message on the command line (which will
                            be parsed to extract build-status info). NOTE: Additional 'formatting'
                            arguments, such as '--code-markdown', are ignored when using json input.
      --json-file JSON_FILE
                            Provide ansible JSON output as a file (which will be parsed to extract
                            build-status info). NOTE: Additional 'formatting' arguments, such as '--
                            code-markdown', are ignored when using json input.
      --user USER           Bitbucket user that will be used to authenticate to Bitbucket. [env var:
                            BITBUCKET_USER]
      --password PASSWORD   Bitbucket password (or Personal Access Token) for the Bitbucket user.
                            [env var: BITBUCKET_PASSWORD]
      --project PROJECT     The Bitbucket project key for the project where the pull request exists.
                            [env var: BITBUCKET_PROJECT]
      --repo REPO           The Bitbucket repository slug for the repository where the pull request
                            exists. [env var: BITBUCKET_REPO]
      --pull-request-id PULL_REQUEST_ID
                            The ID of the Bitbucket pull request to be commented on. [env var: PR_ID]
    
    formatting:
      --diff-markdown       Wrap the provided comment in diff markdown. E.g. ```diff \{comment\}) ```
      --clean-ansi-colors   Clean/remove any ANSI Color codes that are in the provided message/file.
      --code-markdown       Wrap the provided comment in code markdown. E.g. ``` \{comment\}) ```
      --max-comment-size MAX_COMMENT_SIZE
                            Fragment the comment into based on the maximum comment size.
      --tail TAIL           Only print the last `TAIL` lines of the provided message/file.

### Tab Completion? Yes, please!

BuildTools works as a CLI by default, and can support tab completion via the [`argcomplete` module](https://kislyuk.github.io/argcomplete/).

    $ buildtools (double press 'tab' to see possible commands) 
    --bitbucket-url  --help           --version        -h               parse            post             
    $ buildtools post (double press 'tab')
    --help     -h         bitbucket  github     teams      
    $ buildtools post bitbucket (double press 'tab')
    --help        -h            build-status  pr-comment    
    $ buildtools post bitbucket pr-comment

Unfortunately, this does not work 'out of the box' without doing some 'bash configuration' -- run the following commands:
        
    eval "$(register-python-argcomplete buildtools)"

Or, install argcomplete to your user site-package and add it to your `~/.bashrc`:

    # dactivate (if currently in a `venv`)
    pip3 install --user argcomplete

Add the following to your `~/.bashrc`:

    if [ -x "register-python-argcomplete" ] ; then
        eval "$(register-python-argcomplete buildtools)"
    fi


# For Developers

## Running BuildTools from source code

This is simple to do using the `--editable` flag to a pip  -- any changes you make in your local development environment will be reflected in the `buildtools` CLI tool installed with '--editable' specified.

    # run this from the directory where setup.py lives
    pip install --editable .

> NOTE: If dependency updates are part of your changes, now it is a good idea to ignore the 'buildtools' package, e.g. via grep --invert-match: `pip freeze | grep -v "buildtools" > requirements.txt`

## Deploying a new version of BuildTools to PyPI

There is a [Jenkins pipeline (authorization required)](https://is-jenkins01.uoregon.edu/job/NTS/job/BuildTools-CICD/) that defines the Continuous Integration and Deployment (CICD) solution for this project (see [Jenkinsfile](Jenkinsfile) and the [Jenkinsfile Readme](README-Jenkinsfile.md)).
For this project, 'deployment' is essentially 'deploying a new version to PyPI.'

The deployment process is directly-tied to the BitBucket Pull Request process for the [BuildTools Project (authorization required)](https://git.uoregon.edu/projects/ISN/repos/buildtools/browse).
When a Pull Request for BuildTools merges, Jenkins will queue a 'deployment build' and will attempt to automatically deploy that latest version to the [ntsbuildtools PyPI project](https://pypi.org/project/ntsbuildtools/).

1. Create a git feature branch with your new feature/changes.
1. Update the `buildtools/__init__.py` `__version__` variable per [semantic versioning](https://semver.org/)
    - (MAJOR) If you add any 'required arguments' to an **existing CLI**, you must increment the MAJOR version. 
    - (MINOR) If you add only 'optional arguments' to an existing CLI, increment the MINOR version.
        - e.g. adding a new `--optional-argument`
        - e.g. adding a new positional argument option, `{get}` -> `{get, post}`
    - (PATCH) If you don't change the CLI in any way, increment the PATCH version.
1. Create a pull request in the [BuildTools Project (authorization required)](https://git.uoregon.edu/projects/ISN/repos/buildtools/browse).
1. Get `approval` and then `merge` the pull request.
1. Patiently watch the [ntsbuildtools PyPI project](https://pypi.org/project/ntsbuildtools/) until your new release appears!

## Automated Testing

Pytest is used for unit testing and integration testing of this solution.

There is a bit of setup before running pytest locally, discussed below.

First, you must have your local 'buildtools' source-code installed in editable-mode.

    pip install --editable .

Then, run the `pytest` CLI tool from the local directory.

    $ pytest 
    ======================================= test session starts =======================================
    platform linux -- Python 3.8.5, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
    rootdir: /home/rleonar7/dev/jenkins_py_scripts
    plugins: vcr-1.0.2, resource-path-1.2.1
    collected 82 items                                                                                
      
    tests/e2e/test_e2e_bitbucket_build_status.py ...                                            [  3%]
    tests/e2e/test_e2e_bitbucket_pr_comment.py ..............                                   [ 20%]
    tests/e2e/test_e2e_github_pr_comment.py .....                                               [ 26%]
    tests/e2e/test_e2e_parse_ansible_json.py ....                                               [ 31%]
    tests/e2e/test_e2e_teams_integration.py .........                                           [ 42%]
    tests/util/test_fragment_markdown_comment.py ..................................             [ 84%]
    tests/util/test_parse_ansible_json.py .....                                                 [ 90%]
    tests/util/test_teams_cards.py ........                                                     [100%]
    
    ======================================= 82 passed in 0.92s ========================================
