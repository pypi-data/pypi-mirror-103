# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contribution_complexity']

package_data = \
{'': ['*']}

install_requires = \
['PyDriller>=1.15.5,<2.0.0', 'docopt>=0.6.2,<0.7.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['contribcompl = contribution_complexity.compute:run']}

setup_kwargs = {
    'name': 'contribution-complexity',
    'version': '0.1.1',
    'description': ' Tool to compute the complexity of a Git contributions ',
    'long_description': '![](artwork/logo.png)\n\n\n# Contribution Complexity\n\n## What is this?\n\nThis tool computes the complexity of a specified contribution to a git repository.\nA contribution is one or more commits specified by their commit hashes.\nAlternatively, if commit messages contain references to issue numbers, a contribution can be specified by a regular expression matching a certain set of commits.\n\nThe tool reports a contribution complexity on the scale `low`, `moderate`, `medium`, `elevated`, `high`.\nThat value identifies weather a contribution was simple to make (value `low`) or if it consists of multiple intricate changes (value `high`) that were difficult to integrate into the system.\n\nFor example, the storage engine of [Apache Cassandra](https://cassandra.apache.org/) (DBMS) was refactored for version 3 to better support certain concepts of the query language and to allow for future performance optimizations, see [ticket `CASSANDRA-8099`](https://issues.apache.org/jira/browse/CASSANDRA-8099)\nThe [corresponding commit](https://github.com/apache/cassandra/commit/a991b64811f4d6adb6c7b31c0df52288eb06cf19) modifies almost 50k lines in 645 files and contains many non-trivial changes.\nOn the other hand a [bug](https://issues.apache.org/jira/browse/CASSANDRA-12886) that prevented under certain circumstances streaming between cluster nodes was fixed with a [quite tiny patch](https://github.com/apache/cassandra/commit/06feaefba50301734c490521d720c8a482f638e4) modifying 15 lines in two files.\n\nFor humans inspecting the two contributions it is quickly clear that the former contribution is way more complex to implement than the latter.\n\nThis tool is meant to automate the process of identification of contributions of various complexities either for inclusion in a CI setup or for research. \n<!-- \n\n\n## Why does it exist?\n -->\n\n<!-- ## How does it work?\n\nTo determine complexity of a contribution it is not enough to solely check the size of it, e.g., via the number of modified files or the number of modified lines.\n\nFor example, the [highly complex refactoring of Apache Cassandra\'s storage engine](https://github.com/apache/cassandra/commit/a991b64811f4d6adb6c7b31c0df52288eb06cf19) modifies 645 files.\nThe work on [issue #2228](https://github.com/gchq/Gaffer/issues/2228) of the Gaffer graph DB [modifies with 1975 more than three times as many files](https://github.com/gchq/Gaffer/commit/3de5b326c3edd22730000d6585c2fe8b039dabba).\nHowever, that contribution is -even though quite large- really simple.\nIt just updates a year number in all copyright headers. -->\n\n\n## Installation\n\n```bash\n$ pip install contribution-complexity\n```\n\n## Running \n\nYou can run the tool either by specifying a list of commits or by providing a regular expression that matches commit messages containing \n\n```bash\n$ contribcompl commits <path_to_repo> <commit_shas>...\n$ contribcompl issue <path_to_repo> <issue_regex>...\n```\n\nFor example, \n\n```bash\n$ git clone git@github.com:apache/Cassandra.git /tmp/cassandra\n$ contribcompl commits /tmp/cassandra 021df085074b761f2b3539355ecfc4c237a54a76 2f1d6c7254342af98c2919bd74d37b9944c41a6b\nContributionComplexity.LOW\n$ contribcompl issue /tmp/cassandra \'CASSANDRA-8099( |$)\'\nContributionComplexity.HIGH\n```\n\n## Calling from Code\n\n```python\nfrom contribution_complexity.compute import find_commits_for_issue\nfrom contribution_complexity.metrics import compute_contrib_compl\n\n\nissue_re = "CASSANDRA-8099( |$)"\npath_to_repo = "/tmp/cassandra"\ncommit_shas = find_commits_for_issue(path_to_repo, issue_re)\ncontribcompl = compute_contrib_compl(path_to_repo, commit_shas)\nprint(contribcompl)\n```\n\n\n\n----------------\n# Recreating the Experiment\n\n## Requirements\n\n  * [Vagrant](https://www.vagrantup.com) with [DigitalOcean plugin](https://github.com/devopsgroup-io/vagrant-digitalocean)\n  * A [DigitalOcean account](https://www.digitalocean.com/)\n  * [SSH keys registered with DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-1804)\n  * The SSH key name on an environment variable `SSH_KEY_NAME`\n  * A [DigitalOcean API token](https://docs.digitalocean.com/reference/api/create-personal-access-token/) on an environment variable `DIGITAL_OCEAN_TOKEN`\n\n## Run!\n\n  * Set your Github API key in the `Vagrantfile`, i.e., replace `<PUT_YOUR_KEY_HERE>` on line 33 with your key.\n  * Run `vagrant up` in this directory, which will bring up and configure a VM accordingly. It will automatically start the experiment recreation, which will take some hours to run.\n  * Once done you have all results on the VM (log onto the machine with `vagrant ssh`) in the directory `/vagrant/data/`\n\nThe experiment is described in `experiment/run_experiment.sh`.\n\n\n\n\n### Attribution\n\nThe logo is adapted from a [flaticon icon](on https://www.flaticon.com/free-icon/puzzle_808497?term=contribution&page=1&position=16&page=1&position=16&related_id=808497&origin=search). Proper attribution to the original:\n<div>Icons made by <a href="https://www.flaticon.com/authors/mynamepong" title="mynamepong">mynamepong</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>',
    'author': 'HelgeCPH',
    'author_email': 'ropf@itu.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HelgeCPH/contribution-complexity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
