{ name : Text
, subPath : Optional Text
, persistentVolumeClaim :
    Optional (../Kubernetes.dhall).PersistentVolumeClaimVolumeSource.Type
, emptyDir : Optional (../Kubernetes.dhall).EmptyDirVolumeSource.Type
, configMap : Optional (../Kubernetes.dhall).ConfigMapVolumeSource.Type
, secret : Optional (../Kubernetes.dhall).SecretVolumeSource.Type
}
