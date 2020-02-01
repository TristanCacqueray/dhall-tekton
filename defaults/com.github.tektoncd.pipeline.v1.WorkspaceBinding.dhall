{ subPath = None Text
, persistentVolumeClaim =
    None (./../Kubernetes.dhall).PersistentVolumeClaimVolumeSource.Type
, emptyDir = None (./../Kubernetes.dhall).EmptyDirVolumeSource.Type
, configMap = None (./../Kubernetes.dhall).ConfigMapVolumeSource.Type
, secret = None (./../Kubernetes.dhall).SecretVolumeSource.Type
}
