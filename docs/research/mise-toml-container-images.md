# `mise.toml` in container images

**Date:** 2026-08-12

## Conclusion

Yes: `mise.toml` is a good source of intent for selecting an application's runtime version. For a reproducible production image, however, use `mise.lock` as the effective source when it is present. `mise.toml` accepts broad selectors (`"22"`, `lts`, `latest`); the lockfile fixes the version, URL, and, when supported by the backend, checksum per platform. [Lockfile documentation](https://mise.jdx.dev/dev-tools/mise-lock.html)

Do not keep mise in the final stage merely to run the application. Use it in a *builder* to resolve or install tools when necessary, but keep only the runtime and required artifacts in the final image. The project provides `mise install-into <TOOL@VERSION> <PATH>` to install outside mise-managed directories, explicitly for cases where the tool should not be managed at runtime. [`install-into` reference](https://mise.jdx.dev/cli/install-into.html)

## Recommended policy for `create-image`

1. Read `[tools]` in `mise.toml` and identify the runtime the application actually uses (for example, `node`, `python`, `ruby`, or `go`); do not install every declared development tool.
2. If a versioned `mise.lock` has an entry for the target platform (`linux-x64` or `linux-arm64`), use its exact version. With only `mise.toml`, treat the version as a compatibility constraint, not a pin: prefer an official runtime image with an exact compatible version, or generate and commit a lockfile before deployment.
3. Prefer a minimal official runtime image with an exact tag for the final stage. Use mise in the *builder* only when the official distribution cannot satisfy the runtime, backend, or compilation process. `mise install-into` is the official route for copying an isolated installation into the final stage; validate dynamic libraries, CA certificates, and architecture.
4. Make resolution repeatable by generating a lock for published architectures (`mise lock --platform linux-x64,linux-arm64`) and installing in strict mode (`MISE_LOCKED=1 mise install`). In this mode, installation fails without a previously resolved URL for the platform. [Strict mode and platforms](https://mise.jdx.dev/dev-tools/mise-lock.html#strict-lockfile-mode)
5. When inspecting configuration from an untrusted branch or author, do not run tasks, hooks, or `mise install` normally. Use `MISE_SAFE=1 mise lock --bump --dry-run --json` for safe resolution through HTTP backends; this mode blocks code execution, asdf plugin scripts, and plugin installation. [Safe mode](https://mise.jdx.dev/security.html#safe-mode)

## Important limitations

- Configuration is hierarchical: files closest to the current directory override parents, and `mise.local.toml` takes precedence over `mise.toml`. For an image, explicitly use the service's file and directory, without accidentally inheriting build-context configuration. [Configuration precedence](https://mise.jdx.dev/configuration.html#mise-toml)
- Backends are not equivalent. Mise supports `core`, `aqua`, `asdf`, `vfox`, `npm`, `pipx`, `github`, `http`, and others; plugins can define how to list, install, and activate tools. A `[tools]` declaration therefore does not guarantee a portable, verifiable binary that is suitable for the final image. [Backends](https://mise.jdx.dev/dev-tools/backends/) · [Plugin architecture](https://mise.jdx.dev/backend-plugin-development.html)
- Lockfiles are platform-specific and can depend on extra options (for example, the Swift distribution). Generate and test the lock against the same Linux family and architecture as the image. [Platform format](https://mise.jdx.dev/dev-tools/mise-lock.html#platform-information)
- In minimal images, mise might not detect `musl` versus `glibc`; the documentation calls for `MISE_LIBC=musl` or `glibc` when needed. This further supports using official runtime images for the final stage. [Docker cookbook](https://mise.jdx.dev/mise-cookbook/docker.html#overriding-libc-detection)
- `mise.toml` can contain `[env]`, hooks, and tasks that execute code; explicit trust exists for this reason. Reading `[tools]` differs from executing the configuration. [Trust model](https://mise.jdx.dev/getting-started#trusting-config-files)

## Example resolution flow

```sh
# Run by a maintainer before the production build
mise lock --platform linux-x64,linux-arm64

# In the builder, only with a committed lockfile and for the target platform
MISE_LOCKED=1 mise install node
# Or, when the installation must live outside mise:
mise install-into node@<exact-version-from-lock> /opt/node
```

`mise install` installs the declared tools without activating them; `mise install node` uses the configuration version and updates an existing lockfile. [Tool commands](https://mise.jdx.dev/dev-tools/#mise-install)
