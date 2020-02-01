{ script : Optional Text
, args : List Text
, command : List Text
, env : List (../Kubernetes.dhall).EnvVar.Type
, envFrom : List (../Kubernetes.dhall).EnvFromSource.Type
, livenessProbe : (../Kubernetes.dhall).Probe.Type
, name : Text
, ports : List (../Kubernetes.dhall).ContainerPort.Type
, readinessProbe : (../Kubernetes.dhall).Probe.Type
, startupProbe : (../Kubernetes.dhall).Probe.Type
, volumeDevices : List (../Kubernetes.dhall).VolumeDevice.Type
, volumeMounts : List (../Kubernetes.dhall).VolumeMount.Type
, image : Optional Text
, imagePullPolicy : Optional Text
, lifecycle : Optional (../Kubernetes.dhall).Lifecycle.Type
, resources : Optional (../Kubernetes.dhall).ResourceRequirements.Type
, securityContext : Optional (../Kubernetes.dhall).SecurityContext.Type
, stdin : Optional Bool
, stdinOnce : Optional Bool
, terminationMessagePath : Optional Text
, terminationMessagePolicy : Optional Text
, tty : Optional Bool
, workingDir : Optional Text
}
