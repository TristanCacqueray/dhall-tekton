{ inputs : Optional ./com.github.tektoncd.pipeline.v1.Inputs.dhall
, outputs : Optional ./com.github.tektoncd.pipeline.v1.Outputs.dhall
, steps : Optional (List ./com.github.tektoncd.pipeline.v1.Step.dhall)
, volumes : Optional (List (../Kubernetes.dhall).Volume.Type)
, stepTemplate : Optional (../Kubernetes.dhall).Container.Type
, sidecars : Optional (List (../Kubernetes.dhall).Container.Type)
, workspaces :
    Optional (List ./com.github.tektoncd.pipeline.v1.WorkspaceDeclaration.dhall)
, results : Optional (List ./com.github.tektoncd.pipeline.v1.TaskResult.dhall)
}
