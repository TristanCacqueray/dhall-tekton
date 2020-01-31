# dhall-tekton

`dhall-tekton` contains [Dhall][dhall-lang] bindings to [Tekton Pipeline][tektoncd].

## Example

```dhall
let Tekton = https://raw.githubusercontent.com/TristanCacqueray/dhall-tekton/master/package.dhall sha256:95d9a132a6eff02b5a3bccdc4b4ae91bff60dca4f080a1983849689b89fbe3e3

let step-env =
      [ Tekton.EnvVar::{
        , name = "UPLOADER_USERNAME"
        , valueFrom = Tekton.EnvVarSource::{
          , secretKeyRef = Some
              { name = Some "openshift-install"
              , key = "uploader-username"
              , optional = None Bool
              }
          }
        }
      , Tekton.EnvVar::{
        , name = "UPLOADER_PASSWORD"
        , valueFrom = Tekton.EnvVarSource::{
          , secretKeyRef = Some
              { name = Some "openshift-install"
              , key = "uploader-password"
              , optional = None Bool
              }
          }
        }
      ]

in  Tekton.Task::{
    , metadata = Tekton.ObjectMeta::{
      , name = "build-tektoncd-pipeline-and-push"
      }
    , spec = Tekton.TaskSpec::{
      , inputs = Some Tekton.Inputs::{
        , params = Some
            [ Tekton.ParamSpec::{
              , name = "UPLOADER_HOST"
              , type = "text"
              , description = Some "GO Simple Uploader hostname"
              }
            , Tekton.ParamSpec::{ name = "CLUSTER_NAME", type = "text" }
            ]
        }
      , steps = Some
          [ Tekton.Step::{
            , name = "container-buildpush"
            , env = step-env
            , image = Some "quay.io/buildah/stable:v1.11.0"
            , workingDir = Some "\$(inputs.resources.plumbing-git.path)"
            , command =
              [ ''
                #!/usr/bin/env bash
                set -eu
                sudo dnf -y install make
                ...
                ''
              ]
            }
          , Tekton.Step::{
            , name = "generate-release-yaml"
            , env = step-env
            , image = Some "registry.access.redhat.com/ubi8/ubi:latest"
            , workingDir = Some "\$(inputs.resources.plumbing-git.path)"
            , command =
              [ ''
                #!/usr/bin/env bash
                set -e
                function upload() {...}
                ...
                ''
              ]
            }
          , Tekton.Step::{
            , name = "install-release-yaml"
            , env = step-env
            , image = Some "quay.io/openshift/origin-cli:latest"
            , workingDir = Some "\$(inputs.resources.plumbing-git.path)"
            , command =
              [ ''
                #!/usr/bin/env bash
                set -e
                function upload() {...}
                ...
                ''
              ]
            }
          ]
      }
    }
```

```yaml
# dhall-to-yaml --omit-empty --file ./examples/task.dhall
apiVersion: tekton.dev/v1alpha1
kind: Task
metadata:
  name: build-tektoncd-pipeline-and-push
spec:
  inputs:
    params:
      - description: "GO Simple Uploader hostname"
        name: UPLOADER_HOST
        type: text
      - name: CLUSTER_NAME
        type: text
  steps:
    - command:
        - |
          #!/usr/bin/env bash
          set -eu
          sudo dnf -y install make
          ...
      env:
        - name: UPLOADER_USERNAME
          valueFrom:
            secretKeyRef:
              key: uploader-username
              name: openshift-install
        - name: UPLOADER_PASSWORD
          valueFrom:
            secretKeyRef:
              key: uploader-password
              name: openshift-install
      image: quay.io/buildah/stable:v1.11.0
      name: container-buildpush
      workingDir: "$(inputs.resources.plumbing-git.path)"
    - command:
        - |
          #!/usr/bin/env bash
          set -e
          function upload() {...}
          ...
      env:
        - name: UPLOADER_USERNAME
          valueFrom:
            secretKeyRef:
              key: uploader-username
              name: openshift-install
        - name: UPLOADER_PASSWORD
          valueFrom:
            secretKeyRef:
              key: uploader-password
              name: openshift-install
      image: registry.access.redhat.com/ubi8/ubi:latest
      name: generate-release-yaml
      workingDir: "$(inputs.resources.plumbing-git.path)"
    - command:
        - |
          #!/usr/bin/env bash
          set -e
          function upload() {...}
          ...
      env:
        - name: UPLOADER_USERNAME
          valueFrom:
            secretKeyRef:
              key: uploader-username
              name: openshift-install
        - name: UPLOADER_PASSWORD
          valueFrom:
            secretKeyRef:
              key: uploader-password
              name: openshift-install
      image: quay.io/openshift/origin-cli:latest
      name: install-release-yaml
      workingDir: "$(inputs.resources.plumbing-git.path)"

```

[dhall-lang]: https://dhall-lang.org
[tektoncd]: https://tekton.dev/
