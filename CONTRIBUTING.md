# Contributing

Contributions to `lvsfunc` are always appreciated.
However, before opening an issue or submitting a pull request,
please read and follow the guidelines
outlined in this document.

Contributors are responsible
for the content they submit.
Repeated misuse of the issue tracker,
failure to follow contribution guidelines,
or consistently low-quality submissions
may result in contributions being rejected
or the contributor being blocked from the repository.

## General Guidelines

Before submitting a pull request,
contributors **MUST** consider the following:

- **Necessity:** Consider whether the proposed change is actually necessary and beneficial to the project.
- **Scope:** Keep changes minimal and focused. Avoid unrelated refactoring or unnecessary additions.
- **Consistency:** Follow existing coding conventions, formatting rules, and architectural patterns.
- **Testing:** Where applicable, write or update tests that exercise the proposed changes.
- **Compatibility:** Consider the impact of changes on existing functionality and users.
- **Documentation:** Update relevant documentation when introducing or changing user-facing behaviour.

Contributors should be prepared to explain
the purpose and implementation of their changes
and address any concerns raised during review.

The maintainers reserve the right
to reject contributions that do not meet these expectations.

## Development Installation

**[uv](https://github.com/astral-sh/uv)** is the default tool
used for development in this repository.

Clone the repository and sync all dependencies:

```bash
git clone https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc.git
cd lvsfunc
uv sync --all-extras
```

Install and enable the local Git hooks:

```bash
uv run prek install
```

Before submitting a pull request,
contributors are encouraged to run the available checks:

```bash
uv run poe lint-ci
uv run pytest
```

Ensure that any errors introduced by the proposed changes
are resolved before requesting review.

## Semantic Line Breaks

When submitting pull requests
that modify Markdown files,
contributors **MUST** follow
the conventions described in [Semantic Line Breaks][sembr].

In general, each sentence or meaningful clause
should be placed on a separate line.
This makes documentation changes easier to review
and reduces unnecessary differences in pull request diffs.

## Trivial Changes

We consider typo corrections,
minor wording or grammatical adjustments,
comment-only changes,
and simple find-and-replace operations
to be *trivial changes* when they provide little substantive improvement.

For these types of changes,
we prefer contributors to open an issue
or contact the maintainers directly,
such as through the [JET Discord server][discord],
rather than submitting a pull request.

Pull requests consisting entirely of trivial changes
may be closed without review at the maintainers' discretion.

This does not necessarily apply to corrections
that meaningfully improve accuracy, functionality,
or the clarity of technical documentation.

## AI-Assisted Contributions

Unverified AI-generated contributions
create an unnecessary maintenance burden
and can slow down meaningful development.
Issues and pull requests that demonstrate
insufficient understanding, verification, or testing
may be closed without further review.

**`lvsfunc` DOES NOT accept fully AI-generated pull requests**
**that have not been meaningfully reviewed and verified by their authors.**

AI tools may be used to assist with research,
problem-solving, debugging, documentation,
and understanding existing code.
However, contributors **MUST NOT** submit AI-generated changes
that they do not understand,
have not reviewed,
or cannot adequately explain and verify.

Contributors remain fully responsible
for the correctness, quality, and maintainability
of their submissions,
regardless of whether AI tools were involved.

### Transparency and Accountability

Contributors using AI tools **MUST** comply
with the following requirements:

- **Disclose AI involvement.** Clearly indicate when AI tools were used in preparing an issue or pull request.
- **Identify the tools used.** Provide the name and version of the AI tools, where available, and describe how they were used.
- **Demonstrate understanding.** Explain the problem, proposed changes, and implementation in your own words.
- **Verify generated content.** Review and validate any AI-generated code, tests, documentation, or technical claims before submitting them.
- **Assist reviewers.** Clearly disclose any limitations, uncertainties, or aspects of the contribution that could not be independently verified.

Contributors are also encouraged
to document AI involvement in their commit messages
for additional transparency
using the `Assisted-by:` trailer
or at the bottom of the commit message.

### Use of AI Agents

AI agents assisting with contributions to `lvsfunc`
**MUST** follow the instructions provided
in [AGENTS.md][agents].

These instructions establish additional requirements
for agent-assisted development,
including disclosure, authorisation,
and restrictions on the use of repository contents
for AI training and dataset collection.

Contributors are responsible
for ensuring that any agents they use
comply with these requirements.

[sembr]: https://sembr.org/
[discord]: https://discord.gg/D2FkZ8DDxj
[agents]: AGENTS.md
