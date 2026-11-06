---
name: Release
about: Checklist and communication channel for PyPI and GitHub release
title: "Ready for <version-number> PyPI/GitHub release"
labels: "release"
assignees: ""
---

Releases are made from the release branch (e.g. `1.0.9-release`) through a GitHub workflow when a version tag is pushed. Only the GitHub user set as `maintainer_github_username` in that workflow can start a release. Tags must have the form `X.Y.Z` (e.g. `1.0.9`) or `X.Y.Z-rc.N` (e.g. `1.0.9-rc.0`), and the `X.Y.Z` must match the release branch name.

### PyPI/GitHub rc-release preparation checklist:

- [ ] All PRs/issues attached to the release are merged into the release branch.
- [ ] The news items in `news/` cover major features, bug fixes, language additions, breaking changes, and contributors.
- [ ] License information is verified as correct. If you are unsure, please comment below.
- [ ] The README and the guides in `docs/` are up-to-date with any changes in the code.
- [ ] Installation instructions in the README are updated.
- [ ] All new features have corresponding examples and README updates.
- [ ] Wx Inspection tool is removed from the runner, and all debug prints are removed.
- [ ] All warnings are resolved (run tests with `PYTHONWARNINGS=default`).
- [ ] Successfully run all Gooey Examples with the latest Python version.
- [ ] Grammar and writing quality are checked (no typos).
- [ ] Install `pip install build twine`, run `python -m build` and `twine check dist/*` to ensure that the package can be built and is correctly formatted for PyPI release.
- [ ] Dispatch matrix testing to test the release on all Python versions and systems. If you do not have permission to run this workflow, tag the maintainer and say `@maintainer, please dispatch matrix testing workflow`.

Please tag the maintainer (e.g., `@username`) in the comment here when you are ready for the PyPI/GitHub release. Include any additional comments necessary, such as version information and details about the pre-release here:

The maintainer releases the rc by tagging the latest commit on the release branch:

```
git checkout <version>-release
git pull upstream <version>-release
git tag <version>-rc.0
git push upstream <version>-rc.0
```

This publishes a pre-release on GitHub and PyPI. `CHANGELOG.rst` is not updated for an rc.

### PyPI/GitHub full-release preparation checklist:

- [ ] Create a new conda environment and install the rc from PyPI (`pip install Gooey==<version>rc0`).
- [ ] License information on PyPI is correct.
- [ ] Successfully run all tests and Gooey Examples with the rc.

Please let the maintainer know that all checks are done and the package is ready for full release.

The maintainer releases the full version by tagging the latest commit on the release branch:

```
git checkout <version>-release
git pull upstream <version>-release
git tag <version>
git push upstream <version>
```

This merges the files in `news/` into `CHANGELOG.rst` with a commit on the release branch, moves the tag to that commit, creates the GitHub release, and uploads to PyPI.

### conda-forge release preparation checklist:

<!-- After the maintainer releases the PyPI package, please check the following when creating a PR for conda-forge release.-->

- [ ] Ensure that the full release has appeared on PyPI successfully.
- [ ] New package dependencies listed in `requirements/conda.txt` and `requirements/tests.txt` are added to `meta.yaml` in the feedstock.
- [ ] Close any open issues on the feedstock. Reach out to the maintainer if you have questions.
- [ ] Tag the maintainer for conda-forge release.

### Post-release checklist

<!-- Before closing this issue, please complete the following: -->

- [ ] `CHANGELOG.rst` on the release branch has the new release section, and `news/` only contains `TEMPLATE.rst`.
- [ ] Run Gooey Examples and conduct functional testing using the installation guide in the README. Attach screenshots/results as comments.
- [ ] The README and the guides in `docs/` have no broken links or missing figures.
- [ ] Merge the release branch into `master` with a pull request.
- [ ] Tag the maintainer to create the next release branch from `master` (e.g. `git checkout -b 1.0.10-release upstream/master` and `git push upstream 1.0.10-release`).
- [ ] Update CONTRIBUTING.md to point at the next release branch.
