{ inputs : Optional ./com.github.tektoncd.pipeline.v1.Inputs.dhall
, outputs : Optional ./com.github.tektoncd.pipeline.v1.Outputs.dhall
, steps : Optional (List ./com.github.tektoncd.pipeline.v1.Step.dhall)
, volumes :
    Optional (List ./com.github.tektoncd.pipeline.v1.corev1.Volume.dhall)
, stepTemplate :
    Optional ./com.github.tektoncd.pipeline.v1.corev1.Container.dhall
, sidecars :
    Optional (List ./com.github.tektoncd.pipeline.v1.corev1.Container.dhall)
, workspaces :
    Optional (List ./com.github.tektoncd.pipeline.v1.WorkspaceDeclaration.dhall)
, results : Optional (List ./com.github.tektoncd.pipeline.v1.TaskResult.dhall)
}
