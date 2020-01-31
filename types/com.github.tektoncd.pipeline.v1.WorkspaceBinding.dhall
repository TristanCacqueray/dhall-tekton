{ name : Text
, subPath : Optional Text
, persistentVolumeClaim :
    Optional
      ./com.github.tektoncd.pipeline.v1.corev1.PersistentVolumeClaimVolumeSource.dhall
, emptyDir :
    Optional ./com.github.tektoncd.pipeline.v1.corev1.EmptyDirVolumeSource.dhall
, configMap :
    Optional
      ./com.github.tektoncd.pipeline.v1.corev1.ConfigMapVolumeSource.dhall
, secret :
    Optional ./com.github.tektoncd.pipeline.v1.corev1.SecretVolumeSource.dhall
}
