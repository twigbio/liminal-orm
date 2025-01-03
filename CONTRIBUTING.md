# Contributing to Liminal ORM

Thank you in advance for your contribution to Liminal! A contribution of any kind has an impact on the community. Remember to star the repo on GitHub and share Liminal with your colleagues to grow our community!

## Ways to Contribute

Everyone in the community has the ability to influence the roadmap of Liminal, no matter how big or small the contribution. Below are some ways you can contribute:

- **Code Contribution**: Help us improve the codebase by fixing bugs, adding new features, or improving documentation.
- **Documentation**: Help us improve the documentation by adding missing information, improving existing documentation, or raising an issue to update the documentation where needed.
- **Raising an Issue**: Report bugs, suggest features, or provide feedback to help us improve.
- **Spread the Word**: Leave a star on the repo in GitHub or spread the word with coworkers to help grow and cultivate the community.
- **Add yourself as a User**: If your project or organization uses Liminal, add yourself to [USERS.md](https://github.com/dynotx/liminal-orm/blob/main/USERS.md). This is a great way to help us prioritize Liminal's roadmap, and get first dibs on new features ;).

## Setup

If you are interested in contributing to Liminal, please follow the steps below to setup the Liminal repository locally.

1. Fork the Liminal repository and sync to upstream. Instructions here: [Fork a repo](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

2. Install Poetry

   Use the [Poetry Installation guide](https://python-poetry.org/docs/#installing-with-pipx)

3. Install Liminal dependencies

    `poetry install --all-extras`

4. Ensure python version matches Liminal's supported version

    Supported python versions of Liminal can be found in pyproject.toml. We recommend using [pyenv](https://github.com/pyenv/pyenv) to manage python versions.

5. Start developing :)

## Development cycle

Liminal uses [`pre-commit`](https://pre-commit.com/) hooks for enforcing formatting, linting, and mypy. Formatting and linting is done using [`ruff`](https://docs.astral.sh/ruff/) Every commit requires these to pass and you can run them manually using `pre-commit run` (use `-a` flag to run on all files). Commit with the `--no-verify` flag to avoid running the pre-commit hooks.

Please include tests when adding new functionality. Liminal uses [`pytest`](https://docs.pytest.org/en/stable/) for testing. Run this using `pytest liminal/` to run all tests. All tests must pass in order to merge in a Pull Request.

If making changes to the documentation (which is created using [`MKDocs-material`](https://squidfunk.github.io/mkdocs-material/)). Host and get a live preview of website using `mkdocs serve`.

## Making a Pull Request

Contributions to the codebase must be made by submitting a [Pull Request](https://github.com/dynotx/liminal-orm/pulls)
