{ inputs = None ./../types/com.github.tektoncd.pipeline.v1.Inputs.dhall
, outputs = None ./../types/com.github.tektoncd.pipeline.v1.Outputs.dhall
, steps = None (List ./../types/com.github.tektoncd.pipeline.v1.Step.dhall)
, volumes = None (List (./../Kubernetes.dhall).Volume.Type)
, stepTemplate = None (./../Kubernetes.dhall).Container.Type
, sidecars = None (List (./../Kubernetes.dhall).Container.Type)
, workspaces =
    None
      ( List
          ./../types/com.github.tektoncd.pipeline.v1.WorkspaceDeclaration.dhall
      )
, results =
    None (List ./../types/com.github.tektoncd.pipeline.v1.TaskResult.dhall)
}
