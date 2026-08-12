---
name: create-image
description: Create or improve a secure, lean production container image for an application. Use when a project needs a Dockerfile, a smaller or safer image, a multi-stage build, or container-image validation.
---

# Create Image

Make the production image **lean**: it contains only the runtime, application,
and production dependencies needed to run the workload.

## 1. Read the application

Inspect the repository before proposing files. Identify:

- runtime, package manager, lockfile, and required system libraries;
- build command, production start command, listening port, and health endpoint;
- generated runtime assets, native modules, migrations, workers, and persistent
  data needs;
- existing Docker-related files and deployment conventions.

If `mise.toml` exists, read its `[tools]` entry for the runtime the application
actually uses; do not install every development tool it declares. Treat that
version as a compatibility constraint, since selectors such as `latest`, `lts`,
or a major version are not pins. If a versioned `mise.lock` includes the target
Linux platform, use its exact locked version as the source of truth. Otherwise
select an exact compatible runtime version, state the decision, and recommend
committing a lockfile for every published platform.

Ask only for facts that cannot be discovered and materially change the image.
Do not guess a start command, port, build output, or persistence requirement.

**Completion:** the runtime contract is recorded: build inputs, runtime command,
port, required artifacts, environment variables by name, and persistence needs.

## 2. Build a lean image

Create or revise these files as applicable:

- `Dockerfile` with explicit build and runtime stages when the application
  compiles or needs build-only tooling;
- `.dockerignore` that excludes VCS metadata, local dependencies, tests,
  coverage, editor files, logs, secrets, and build artifacts regenerated inside
  the image.

Apply the runtime's production pattern:

1. Use an official runtime image with the exact version selected from `mise.lock`
   or the compatibility decision, and the smallest compatible base-image variant.
2. Copy dependency manifests before source code so dependency installation is
   cacheable.
3. Install deterministic dependencies from the lockfile; install development
   dependencies only in a build stage when they are needed to build.
4. Build in the builder stage, then copy only the runtime artifacts and
   production dependencies into the final stage.
5. Run as a non-root user whenever the runtime allows it, and make copied files
   owned by that user.
6. Set the production environment, expose the documented application port, and
   use an exec-form `CMD` for the documented start command.

Prefer build arguments only for values required at build time and safe to embed.
Keep credentials, API keys, and other secrets as runtime environment variables.
Never copy `.env` files, credentials, package-manager tokens, or private keys
into an image.

Do not add an OS package, process manager, reverse proxy, shell, or healthcheck
unless the application contract proves it is needed. Run one primary process per
image.

Use mise in a builder only when the official runtime image cannot satisfy the
required runtime or build process. Keep mise out of the final stage; copy only
the installed runtime and verified runtime artifacts. Resolve untrusted mise
configuration in safe mode, and ensure the lock's Linux architecture and libc
match the selected image.

**Completion:** the final stage has no source/build tooling unless it is itself
runtime-required, and every copied path is required by the runtime contract.

## 3. Validate the artifact

Build the image from its documented Dockerfile path and context. Run it with
non-secret placeholder values for required environment-variable names, then
verify the documented port and a real health or readiness behavior.

Inspect the final image size and image history. If a surprising layer or large
file remains, trace it to its source and remove it when safe; do not chase small
size wins that make the runtime less reliable.

Report:

- files created or changed;
- runtime version and its source (`mise.lock` or compatibility decision);
- Dockerfile and build-context paths;
- runtime environment-variable names and persistent-data requirements;
- commands run, image size, and any validation not possible locally.

**Completion:** a local build and run (or a clearly stated blocker) verifies the
runtime contract, and the image build paths are unambiguous.
