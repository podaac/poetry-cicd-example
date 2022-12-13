# poetry-cicd-example
Bare bones repository demonstrating a python [poetry](https://python-poetry.org/) project using GitHub actions

Assumptions:

* Project is hosted on github.com 
* Project uses an organization-scoped GitHub App for CICD operations
* Project built using [poetry](https://python-poetry.org/)
* Docker images will be published to ghcr.io
* Credentials stored in GitHub Secrets
  * CICD_APP_ID
  * CICD_APP_PRIVATE_KEY
  * SONAR_TOKEN
  * GITHUB_TOKEN
* Branch names: `main`, `develop`, `issues/*`
* Project is using [semantic versioning](https://semver.org/)

## Important Notes

* After merging to `master`, a new change request should be opened to merge `master`
back in to `develop` so that the version in `develop` is at least one minor version 
ahead of `master`. This can't be automated because development likely will have continued while
the release was being evaluated and will cause merge conflicts since both branches will have
modified the version number. 
* Changes made in release branches should also be pushed back to `develop` if they are critical. Otherwise, the
merge from `master` to `develop` after release will incorporate the changes.
* It is recommended that only one change request targeting `master` should be open at any given time. 

## Stages Overview

The main unit of work for Jenkins pipelines are Stages. Stages can contain sub-stages and can be conditionally run. At a high-level, this template defines the following
stages listed below. In general, the stages are executed in order from top to bottom. However, some stages can be skipped for any particular run of the pipeline. 

* **Checkout**  
  This stage checks out the code as triggered by the server event.  

## Git Branching Strategy

The template is built with the assumption that the project follows the [git-workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) branching
strategy. A lot of the functionality is conditional on matching against branch naming conventions. Therefore, it is important that the project conform to this workflow.

## Software Versioning

This template assumes the use of [semantic versioning](https://semver.org/) for the project being built. The strategy can be summarized as:

* The `develop` branch always contains a [prerelease](https://semver.org/#spec-item-9) version of the project
* The `develop` branch will always be at least 1 minor version ahead of `master`
* Feature branches (prefixed with `issues/`) are branched from `develop`. When a feature branch is built, [build metadata](https://semver.org/#spec-item-10) is appended to the prerelease version 
* Every merge to develop increments the prerelease version number by one
* Release branches are branched from `develop` and are named as `release/<semver>` where `<semver>` is a valid 'major.minor.patch' semantic version string.
* The `<semver>` part of the branch name is used as the version for the release. See [Releasing](#Releasing) for details
* As soon as a release branch is created, the minor version in the `develop` branch is bumped automatically by the `release-created.yml` workflow
* Release candidates are created once a change request is created from a `release/*` branch that targets `master`
* When a release candidate is created, the prerelease identifier is set to `rc` and the prerelease version is reset to 1
* Any change (commit) to a release candidate change request results in a bump to the prerelease version
* Merges to master remove the prerelease version and identifier but leave the remaining 'major.minor.patch' version
* Tags using the version as the tag name are created for every new prerelease, release candidate, and release

## Releasing

When it is time to cut a release from the develop branch, a decision must be made. Is the release a major, minor, or patch release?
There are rules that should be followed when determining if the release is [minor](https://semver.org/#spec-item-7) or [major](https://semver.org/#spec-item-8).

If it is minor, create a branch prefixed with `release/` and followed by the development version without prerelease version or identifier. 
For example, if `0.2.0-alpha.4` is the current develop version, then create a branch called `release/0.2.0`

If it is major, create a branch prefixed with `release/` and followed by the development major version incremented by 1 and using 0 for minor and patch number. 
For example, if `0.2.0-alpha.4` is the current develop version, then create a branch called `release/1.0.0`

## Reviews

There are two points of review in this workflow:

1. When a change request is initiated from a feature branch to develop. This is a chance for developers to review the code that was developed as part of the feature request
and suggest changes. The assumption is that code that makes it to develop is eligible for release and it will be deployed to a system integration testing (SIT) environment.
2. When a change request is initiated from a release branch to `master`. This is a chance for other stakeholders to review the proposed changed that will be released 
to operations (OPS). As soon as a change request is initiated, the software will be deployed to a user acceptance testing (UAT) environment so that functionality can be tested.
It is recommended that only one change request targeting `master` should be open at any given time. 
