# Cache catalog

Read this before classifying a path. A sample shows the usual shape. The disposition is what this skill's scanner will do. A sample is not deletion approval, and a category total is not a list of targets.

Manual directories are named and then not measured, so an unknown size is not zero. Packaged apps found inside those directories are separate rows with their own sizes. Approving a parent is a different decision from noticing a file inside it.

## Dispositions

| Disposition | Meaning |
|---|---|
| eligible | Recognized generated directory. It can enter a cleanup plan only as an exact path the user approves after a fresh scan. |
| manual | Reported, never script-deleted. The name can be source, a release, or a dependency checkout. |
| audit | On the closed `--audit-home` list below. Measured read-only. Planning rejects the path. |
| leave | Not a cleanup target. SDK, emulator, toolchain, signing material, archive, or container state. |

Do not run a package-manager cache command, `./gradlew clean`, `flutter clean`, or a container prune as a substitute for the plan. Those are separate requests.

## Node.js

```text
app/
  package.json
  node_modules/          eligible
  .turbo/                eligible    Turborepo
  .yarn/                 manual      may hold the Yarn binary and a committed cache
  dist/                  manual
  out/                   manual
```

| Path | Disposition | Notes |
|---|---|---|
| `node_modules/` | eligible | One target for the whole tree. Do not also plan a nested cache inside it. |
| `.turbo/` | eligible | Turborepo cache. |
| `.yarn/` | manual | Zero-install repos commit `.yarn/cache`. The reported unit is `.yarn`, not only the cache subdirectory. |
| `dist/`, `out/` | manual | Build output. Confirm it is generated and untracked before any hand deletion. |

Home audit: `.npm`, `.cache/yarn`, `.cache/pnpm`, `Library/pnpm/store`, `.local/share/pnpm/store`, `.bun/install/cache`.

Leave `~/.nvm`, `~/.fnm`, and other Node installs.

## Web

```text
web/
  package.json
  next.config.js
  .next/                 eligible    approving this removes the whole Next build
  .nuxt/                 eligible
  .output/               eligible    Nitro / Nuxt server build
  .svelte-kit/           eligible
  .parcel-cache/         eligible
  .vite/                 eligible
  .swc/                  eligible
  angular.json
  .angular/              eligible    only when angular.json sits beside it
  .cache/                manual
  storybook-static/      manual
  playwright-report/     manual
  test-results/          manual
  coverage/              manual
```

`.next`, `.nuxt`, and `.output` are the build, not a small inner cache folder. Say that before asking for approval.

## Mobile

### Android, APK, and AAB

```text
android/
  build.gradle.kts
  .gradle/                               manual    project Gradle cache
  app/
    build.gradle.kts
    .cxx/                                eligible  NDK / CMake cache, only beside a Gradle file
    build/                               manual    the walk stops here; size stays unknown
      outputs/apk/release/app-release.apk          manual packaged app, size is recorded
      outputs/bundle/release/app-release.aab       manual packaged app, size is recorded
```

A loose `.apk`, `.aab`, or `.apks` outside `build/` is also a manual packaged-app row. It may be the release binary someone meant to keep. Keystores (`.jks`, `.keystore`) are leave-alone.

Home audit: `.gradle/caches`, `.android/cache`, `.android/build-cache`.

Leave `~/Library/Android/sdk` and `~/.android/avd`. Those are the SDK and emulators.

### iOS

```text
ios/
  Podfile
  Pods/                    manual
  build/                   manual
  Carthage/                manual    Build/ is generated; Checkouts may matter
Runner.xcarchive           manual    release archive, wherever it sits
```

Home audit: `Library/Developer/Xcode/DerivedData`. A project-local `DerivedData/` directory is manual, not eligible.

Leave `~/Library/Developer/Xcode/Archives`, device-support files, simulator runtimes, and provisioning profiles.

A loose `.ipa` is a manual packaged-app row, same as an APK.

### Flutter, Expo, and React Native

```text
app/
  pubspec.yaml
  .dart_tool/              eligible  only when pubspec.yaml sits beside it
  build/                   manual
  .expo/                   manual
  node_modules/            eligible  React Native / Expo JavaScript dependencies
  android/                 use the Android sample
  ios/                     use the iOS sample
```

Home audit: `.pub-cache`.

Leave `.fvm` SDK checkouts. A path component named `.fvm` makes the directory protected.

## Backend

### Java and Kotlin

```text
service/
  pom.xml
  target/                  eligible  Maven, only when pom.xml sits beside it
  build.gradle.kts
  build/                   manual    Gradle
  .gradle/                 manual
```

`target/` next to `Cargo.toml` is Rust. `target/` next to `pom.xml` is Maven. When both markers sit on one directory, the row stays eligible only as that exact path and is reported as a marked build output.

Home audit: `.gradle/caches`, `.m2/repository`. The Maven repository can hold locally installed snapshots. It stays audit-only.

### .NET

`bin/` and `obj/` next to a `.csproj` are usually regenerable and still manual, because those names are also used for source and tools. Confirm they are untracked before any hand deletion.

Home audit: `.nuget/packages`.

### Python

`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.tox/`, `.nox/`, and `.hypothesis/` are eligible.

Home audit: `.cache/pip`.

Leave `.venv` and `venv`. They are environments. A `__pycache__` directory inside one can still be an eligible nested target; do not treat that as permission to delete the environment.

### Go

```text
service/
  go.mod
  go.sum
  vendor/                  manual      may be committed for reproducible builds
  bin/                     manual      go install / local build output
  cmd/api/main.go
```

```text
# Typical module cache (home, audit-only — not a project cleanup root)
~/go/
  pkg/mod/                 audit       downloaded modules; use go clean -modcache separately
  bin/                     leave       installed tools
```

Project scans treat a directory literally named `go` as protected, so do not point `--root` at `~/go` or `$GOPATH`. Use `--audit-home` only when the user explicitly asks to measure the module cache under that home.

Home audit: `.cache/go-build` (build cache). Optional audit row when present under the chosen home: `go/pkg/mod`.

Leave `GOROOT`, the toolchain install, and anything under `~/go/bin` that is an installed CLI.

### Ruby

```text
app/
  Gemfile
  Gemfile.lock
  vendor/bundle/           manual      Bundler path vendor; whole vendor/ is manual
  .bundle/                 manual      Bundler config and may hold local paths
  tmp/cache/               manual      not scanned by name; delete by hand if regenerable
  log/                     leave       not a cache
```

Home audit: `.gem` (user gem directory). Bundler's global cache path varies by install; it is not on the closed home-audit list unless the user names a bounded directory for a manual inventory.

Leave rbenv, rvm, and chruby install roots.

### Elixir / Phoenix

```text
my_app/
  mix.exs
  mix.lock
  deps/                    manual      fetched dependencies; often large but not auto-deleted
  _build/                  eligible    only when mix.exs sits beside it
  cover/                   manual      local coverage output
  priv/static/             leave       compiled assets may be committed or deployed
```

```text
# BEAM / OTP release output (still manual — release artifact, not a cache folder name)
my_app/
  _build/prod/rel/my_app/  manual      treat like build output, not eligible
```

Home audit: `.mix`, `.hex` (Mix and Hex download caches).

Leave `.asdf` installs (protected path component). `.elixir_ls/` in a project is editor state: manual, not eligible.

### Rust

```text
crate/
  Cargo.toml
  Cargo.lock
  target/                  eligible    only when Cargo.toml sits beside it
```

Home audit: `.cargo/registry`. Leave `~/.cargo/bin` and `~/.rustup`.

### PHP

| Path | Disposition | Notes |
|---|---|---|
| `vendor/` | manual | Composer checkout; often committed in legacy apps. |
| `.phpunit.cache/` | eligible | PHPUnit cache. |

Home audit: `.composer/cache`, `.cache/composer`.

## Containers, Docker, and local Kubernetes

This skill does not prune images, volumes, or container filesystems. That is a separate operational request (`docker system df`, `docker builder prune`, Colima/OrbStack disk settings, and so on).

```text
repo/
  Dockerfile
  compose.yaml
  .docker/                 protected   path component blocks unsafe roots, not a delete target
```

| Area | Disposition | Notes |
|---|---|---|
| Docker Desktop / Colima / OrbStack / Minikube data | leave | Lives outside normal project roots; can hold databases and volumes. |
| Path components `.docker`, `.colima`, `.orbstack`, `.minikube` | protected | Cleanup roots that include these names are refused. |
| Project `build/` from `docker build` context | manual | Image layers live in the engine store, not in the context folder. |
| `.docker/buildx` or CI layer export dirs | manual | Inspect before hand deletion. |

If the user asks to reclaim Docker disk space, stay in audit/advice mode or route to the engine's supported prune workflow. Do not widen `--root` into engine data directories.

## Home audit closed list

`scan --audit-home` inspects only these subpaths. A missing path is skipped. Every row is `scope: global-audit` and cannot become a plan target. Do not add a home path that is not in this list.

- `.npm`
- `.cache/pip`
- `.cache/yarn`
- `.cache/pnpm`
- `.cache/go-build`
- `.cache/composer`
- `.cargo/registry`
- `.bun/install/cache`
- `.gradle/caches`
- `.m2/repository`
- `.nuget/packages`
- `.pub-cache`
- `.composer/cache`
- `.mix`
- `.hex`
- `.gem`
- `go/pkg/mod`
- `.android/cache`
- `.android/build-cache`
- `Library/Caches`
- `Library/pnpm/store`
- `Library/Developer/Xcode/DerivedData`
- `.local/share/pnpm/store`

## Not cleanup targets

- Language SDKs, version-manager installs, Android emulators, iOS simulators, and device-support files
- Xcode archives, keystores, and signing material
- Container disks, VM images, and Docker / Colima / OrbStack / Minikube engine data
- A `build`, `dist`, `bin`, `obj`, or `out` directory selected by name alone
- Anything git tracks
