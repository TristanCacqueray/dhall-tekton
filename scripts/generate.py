#!/bin/env python3
# Copyright 2020 Red Hat
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import subprocess
import sys
from pathlib import Path

tekton_pipeline_git = Path(sys.argv[1])
tekton_ns = 'com.github.tektoncd.pipeline'
tekton_type_files = [
    "apis/resource/v1alpha1/pipeline_resource_types.go",
    "apis/pipeline/v1alpha2/task_types.go", # To import TaskResult
    "apis/pipeline/v1alpha1/task_types.go",
    "apis/pipeline/v1alpha2/workspace_types.go",
]

ignored_types = ['TaskResource']
renamed_types = dict(
    ResourceDeclaration="TaskResource"
)

def read_type(type_path):
    """A quick golang type definition parser"""
    type_file = tekton_pipeline_git / "pkg" / type_path
    types = {}
    in_type = None

    for l in filter(lambda s: not s.strip().startswith('//') and s.strip(),
                    type_file.read_text().split('\n')):
        if l.startswith('type '):
            in_type = dict(name=l.split()[1], path=type_path, typedef=[])
            if in_type['name'] in ignored_types:
                in_type = None
            elif in_type['name'] == renamed_types:
                in_type['name'] = renamed_types[in_type['name']]
            continue
        if l == '}' and in_type:
            types[in_type['name']] = in_type
            in_type = None
        if in_type:
            # read_type simply extract the attributes go definition for each type struct
            in_type['typedef'].append(l.strip())
    return types


def show_type_file(type_name: str) -> str:
    return tekton_ns + '.v1.' + type_name + '.dhall'


def show_type(type, all_types):
    """A quick golang type def to dhall"""
    type_def = []
    if type['name'] == 'ResourceDeclaration':
        type['name'] = 'TaskResource'
    for typedef in type['typedef']:
        if typedef.startswith('metav1.TypeMeta '):
            type_def.append(('apiVersion', 'Text')),
            type_def.append(('kind', 'Text'))
        elif typedef.startswith('Kind '):
            type_def.append(('kind', 'Text'))
        elif typedef.startswith('metav1.ObjectMeta'):
            type_def.append(('metadata', '(../Kubernetes.dhall).ObjectMeta.Type'))
        elif typedef.startswith('corev1.Container'):
            continue
        elif 'inline' in typedef:
            # skip for now
            continue
        else:
            try:
                typedef = typedef.split()
                name, tdef = typedef[0], typedef[1]
            except:
                print("Decode error", typedef)
                raise
            json_def = typedef[-1]
            name = name[0].lower() + name[1:]

            # First look for list
            if tdef.startswith('[]'):
                tdef = tdef[2:]
                tval = 'List '
            else:
                tval = ''

            if tdef[0] == '*':
                tdef = tdef[1:]

            if tdef == 'string':
                tval += 'Text'
            elif tdef == 'bool':
                tval += 'Bool'
            elif tdef == 'PipelineResourceType':
                tval += 'Text'
            elif tdef.startswith('corev1'):
                tval += '(../Kubernetes.dhall).%s.Type' % tdef.split('.')[1]
            else:
                if all_types.get(tdef) and all_types[tdef]["typedef"] == []:
                    # Skip empty type such as Status
                    continue

                tval += './' + show_type_file(tdef)

            if 'omitempty' in json_def:
                tval = 'Optional (' + tval + ')'
            type_def.append((name, tval))

    return type_def


def write_file(file, content):
    file.write_text(content)
    subprocess.Popen(["dhall", "format", "--inplace", str(file)]).wait()


def write_type(type, type_def):
    type_file = Path('types') / show_type_file(type['name'])
    write_file(type_file, "{" + " , ".join(map(lambda td: " : ".join(td), type_def)) + "}")
    default_file = Path('defaults') / show_type_file(type['name'])
    defaults = []
    for n, v in type_def:
        v = v.replace('./', './../types/').replace('../../types/Kubernetes', './../Kubernetes')
        if v.startswith('Optional'):
            defaults.append((n, 'None ' + v[len('Optional'):]))
        elif v.startswith('List'):
            defaults.append((n, '[] : List ' + v[len('List'):]))
        elif n == 'apiVersion':
            defaults.append((n, '"tekton.dev/v1alpha1"'))
        elif n == 'kind':
            defaults.append((n, '"' + type['name'] + '"'))
        elif n.endswith('Probe'):
            defaults.append((n, '(./../Kubernetes.dhall).Probe.default'))
    defaults_str = " , ".join(map(lambda td: " = ".join(td), defaults)) if defaults else '='
    write_file(default_file, "{" + defaults_str + "}")
    schema_file = Path('schemas') / show_type_file(type['name'])
    write_file(schema_file, "{ Type = ./../%s , default = ./../%s }" % (str(type_file), str(default_file)))
    print(f"Wrote {type_file}")


all_types = {}
for tekton_type_file in tekton_type_files:
    tekton_types = read_type(tekton_type_file)
    all_types.update(tekton_types)
    for tekton_type in tekton_types.values():
        # Skip List type for now
        if tekton_type['name'].endswith('List'):
            continue
        try:
            type_def = show_type(tekton_type, all_types)
        except:
            print("Couldn't show", tekton_type)
            raise
        # Skip empty type def
        if not type_def:
            continue
        write_type(tekton_type, type_def)


write_type(dict(name="Step"), [("script", "Optional Text"),
  # Converted from kubernetes container type definition
  #  \([a-zA-Z]+\) : \(.*\)  -> ("\1", "\2")
  #  ..io.k8s.api.core.v1.\([a-zA-Z]+\).dhall -> (../Kubernetes.dhall).\1.Type
  ("args", "List Text")
, ("command", "List Text")
, ("env", "List (../Kubernetes.dhall).EnvVar.Type")
, ("envFrom", "List (../Kubernetes.dhall).EnvFromSource.Type")
, ("livenessProbe", "(../Kubernetes.dhall).Probe.Type")
, ("name", "Text")
, ("ports", "List (../Kubernetes.dhall).ContainerPort.Type")
, ("readinessProbe", "(../Kubernetes.dhall).Probe.Type")
, ("startupProbe", "(../Kubernetes.dhall).Probe.Type")
, ("volumeDevices", "List (../Kubernetes.dhall).VolumeDevice.Type")
, ("volumeMounts", "List (../Kubernetes.dhall).VolumeMount.Type")
, ("image", "Optional Text")
, ("imagePullPolicy", "Optional Text")
, ("lifecycle", "Optional (../Kubernetes.dhall).Lifecycle.Type")
, ("resources", "Optional (../Kubernetes.dhall).ResourceRequirements.Type")
, ("securityContext", "Optional (../Kubernetes.dhall).SecurityContext.Type")
, ("stdin", "Optional Bool")
, ("stdinOnce", "Optional Bool")
, ("terminationMessagePath", "Optional Text")
, ("terminationMessagePolicy", "Optional Text")
, ("tty", "Optional Bool")
, ("workingDir", "Optional Text")])


schemas = []
for schema in os.listdir('schemas'):
    schemas.append(schema.split('.')[-2] + " = ./schemas/" + schema)
write_file(Path('schemas.dhall'), "{ " + " , ".join(schemas) + " }")
types, typesUnion = [], []
for type in os.listdir('types'):
    types.append(type.split('.')[-2] + " = ./types/" + type)
    typesUnion.append(type.split('.')[-2] + " : ./types/" + type)
write_file(Path('types.dhall'), "{ " + " , ".join(types) + " }")
write_file(Path('typesUnion.dhall'), "< " + " | ".join(typesUnion) + " >")
exit(subprocess.Popen(["dhall", "freeze", "--all", "--inplace", "package.dhall"]).wait())
