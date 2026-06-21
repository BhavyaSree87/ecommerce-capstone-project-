# Capstone_Project



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab1.rpsconsulting.in/26SUB0723_U04/capstone_project.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab1.rpsconsulting.in/26SUB0723_U04/capstone_project/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

## DevOps / CI-CD

This project includes a production-ready CI/CD pipeline and Docker compose orchestration.

### Files added/updated
- `Jenkinsfile` — Declarative Jenkins pipeline implementing the full build and deploy stages.
- `docker-compose.yml` — Enhanced compose file with `env_file` support, `healthcheck`, restart policy and custom network.
- `backend/.dockerignore` — Excludes virtualenvs, logs, and python build artifacts.
- `frontend/.dockerignore` — Excludes `node_modules`, `dist` and `.env`.
- `.env.example` — Example environment file with Oracle DB and JWT variables.

### Docker commands
- Build images and services:

```bash
docker compose build
```

- Run services in background:

```bash
docker compose up -d
```

- Stop and remove services:

```bash
docker compose down
```

### Jenkins setup
1. Install Jenkins (with Docker and Node + Python tool available on the agent) and configure a node/agent with Docker privileges.
2. Place the repository in Jenkins and create a pipeline job using the repository's `Jenkinsfile`.
3. Ensure the agent has `docker`, `docker-compose`, `node` and `python3` installed.
4. Configure credentials and notification hooks (email/Slack) in your Jenkins instance and update the `post` sections in the `Jenkinsfile` to call them.

### Pipeline overview
Stages implemented (in `Jenkinsfile`):
1. Checkout Source Code
2. Install Backend Dependencies (Python venv + pip)
3. Install Frontend Dependencies (npm ci)
4. Run Backend Tests (if present)
5. Build Frontend (`npm run build`)
6. Build Backend Docker Image
7. Build Frontend Docker Image
8. Run `docker compose up -d --build`
9. Verify Backend Health (curl /docs)
10. Verify Frontend Health (curl /)
11. Deployment Success

The pipeline will always run `docker compose down` in the `post` step to ensure clean state.

### Troubleshooting
- If `docker compose up` fails, run the compose with `--verbose` to see detailed logs.
- If health checks fail, try `docker compose logs backend` and `docker compose logs frontend` to inspect logs.
- Ensure the `.env` file exists and contains the real secrets (copy from `.env.example`).
- For Jenkins agent issues, ensure the agent user has permission to run Docker commands (often requires adding user to `docker` group on Linux).

### Notes & recommendations
- The current `backend/Dockerfile` starts `uvicorn` on port `8000` and is suitable for production behind a reverse proxy. Consider using Gunicorn with Uvicorn workers for heavy loads.
- The current `frontend/Dockerfile` runs the Vite dev server. For a true production image, build static assets (`npm run build`) and serve them with `nginx` or use `vite preview` on a controlled port.
- Never commit real secrets. Use `.env` and secret stores (Vault, Jenkins credentials, or cloud secrets manager) for production.

***

