{ TaskResource = ./schemas/com.github.tektoncd.pipeline.v1.TaskResource.dhall
, Inputs = ./schemas/com.github.tektoncd.pipeline.v1.Inputs.dhall
, EnvVarSource =
    ./schemas/io.k8s.apimachinery.pkg.apis.meta.v1.EnvVarSource.dhall
, PipelineResource =
    ./schemas/com.github.tektoncd.pipeline.v1.PipelineResource.dhall
, TestResult = ./schemas/com.github.tektoncd.pipeline.v1.TestResult.dhall
, ResourceParam = ./schemas/com.github.tektoncd.pipeline.v1.ResourceParam.dhall
, TaskSpec = ./schemas/com.github.tektoncd.pipeline.v1.TaskSpec.dhall
, Outputs = ./schemas/com.github.tektoncd.pipeline.v1.Outputs.dhall
, SecretParam = ./schemas/com.github.tektoncd.pipeline.v1.SecretParam.dhall
, ParamSpec = ./schemas/com.github.tektoncd.pipeline.v1.ParamSpec.dhall
, ResourceDeclaration =
    ./schemas/com.github.tektoncd.pipeline.v1.ResourceDeclaration.dhall
, Task = ./schemas/com.github.tektoncd.pipeline.v1.Task.dhall
, EnvVar = ./schemas/io.k8s.apimachinery.pkg.apis.meta.v1.EnvVar.dhall
, PipelineResourceSpec =
    ./schemas/com.github.tektoncd.pipeline.v1.PipelineResourceSpec.dhall
, Param = ./schemas/com.github.tektoncd.pipeline.v1.Param.dhall
, WorkspaceBinding =
    ./schemas/com.github.tektoncd.pipeline.v1.WorkspaceBinding.dhall
, WorkspaceDeclaration =
    ./schemas/com.github.tektoncd.pipeline.v1.WorkspaceDeclaration.dhall
, ObjectMeta = ./schemas/io.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta.dhall
, WorkspacePipelineDeclaration =
    ./schemas/com.github.tektoncd.pipeline.v1.WorkspacePipelineDeclaration.dhall
, WorkspacePipelineTaskBinding =
    ./schemas/com.github.tektoncd.pipeline.v1.WorkspacePipelineTaskBinding.dhall
, Step = ./schemas/com.github.tektoncd.pipeline.v1.Step.dhall
}
