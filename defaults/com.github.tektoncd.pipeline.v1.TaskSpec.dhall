{ inputs = None ./../types/com.github.tektoncd.pipeline.v1.Inputs.dhall
, outputs = None ./../types/com.github.tektoncd.pipeline.v1.Outputs.dhall
, steps = None (List ./../types/com.github.tektoncd.pipeline.v1.Step.dhall)
, volumes =
    None (List ./../types/com.github.tektoncd.pipeline.v1.corev1.Volume.dhall)
, stepTemplate =
    None ./../types/com.github.tektoncd.pipeline.v1.corev1.Container.dhall
, sidecars =
    None
      (List ./../types/com.github.tektoncd.pipeline.v1.corev1.Container.dhall)
, workspaces =
    None
      ( List
          ./../types/com.github.tektoncd.pipeline.v1.WorkspaceDeclaration.dhall
      )
, results =
    None (List ./../types/com.github.tektoncd.pipeline.v1.TaskResult.dhall)
}
