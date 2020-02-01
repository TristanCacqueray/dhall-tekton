let Tekton =
        env:DHALL_TEKTON
      ? https://raw.githubusercontent.com/TristanCacqueray/dhall-tekton/master/package.dhall sha256:6e1beb1306b092073106c992df768951b4bfd62fc1299af06d6220312f2eeafe

let Kubernetes =
        env:DHALL_KUBERNETES
      ? https://raw.githubusercontent.com/dhall-lang/dhall-kubernetes/3c6d09a9409977cdde58a091d76a6d20509ca4b0/package.dhall sha256:e9c55c7ff71f901314129e7ef100c3af5ec7a918dce25e06d83fa8c5472cb680

let step-env =
      [ Kubernetes.EnvVar::{
        , name = "UPLOADER_USERNAME"
        , valueFrom = Kubernetes.EnvVarSource::{
          , secretKeyRef = Some
              { name = Some "openshift-install"
              , key = "uploader-username"
              , optional = None Bool
              }
          }
        }
      , Kubernetes.EnvVar::{
        , name = "UPLOADER_PASSWORD"
        , valueFrom = Kubernetes.EnvVarSource::{
          , secretKeyRef = Some
              { name = Some "openshift-install"
              , key = "uploader-password"
              , optional = None Bool
              }
          }
        }
      ]

in  Tekton.Task::{
    , metadata = Kubernetes.ObjectMeta::{
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
            , script = Some
                ''
                #!/usr/bin/env bash
                set -eu
                sudo dnf -y install make
                ...
                ''
            }
          , Tekton.Step::{
            , name = "generate-release-yaml"
            , env = step-env
            , image = Some "registry.access.redhat.com/ubi8/ubi:latest"
            , workingDir = Some "\$(inputs.resources.plumbing-git.path)"
            , script = Some
                ''
                #!/usr/bin/env bash
                set -e
                function upload() {...}
                ...
                ''
            }
          , Tekton.Step::{
            , name = "install-release-yaml"
            , env = step-env
            , image = Some "quay.io/openshift/origin-cli:latest"
            , workingDir = Some "\$(inputs.resources.plumbing-git.path)"
            , script = Some
                ''
                #!/usr/bin/env bash
                set -e
                function upload() {...}
                ...
                ''
            }
          ]
      }
    }
