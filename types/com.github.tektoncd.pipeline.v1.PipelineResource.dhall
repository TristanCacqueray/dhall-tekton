{ apiVersion : Text
, kind : Text
, metadata : (../Kubernetes.dhall).ObjectMeta.Type
, spec : Optional ./com.github.tektoncd.pipeline.v1.PipelineResourceSpec.dhall
}
