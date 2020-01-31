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
tekton_type_files = (
    "apis/resource/v1alpha1/pipeline_resource_types.go",
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
            continue
        if l == '}' and in_type:
            if in_type['typedef']:
                types[in_type['name']] = in_type
            in_type = None
        if in_type:
            in_type['typedef'].append(l.strip())
    return types


def show_type_file(type_name):
    return tekton_ns + '.v1.' + type_name + '.dhall'


def show_type(type):
    """A quick golang type def to dhall"""
    type_def = []
    for typedef in type['typedef']:
        if typedef.startswith('metav1.TypeMeta '):
            type_def.append(('apiVersion', 'Text')),
            type_def.append(('kind', 'Text'))
        elif typedef.startswith('metav1.ObjectMeta'):
            type_def.append(('metadata', './io.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta.dhall'))
        else:
            name, tdef, json_def = typedef.split()
            name = name[0].lower() + name[1:]

            # First look for list
            if tdef.startswith('[]'):
                tdef = tdef[2:]
                tval = 'List '
            else:
                tval = ''

            # Skip for now
            if tdef[0] == '*':
                continue

            if tdef == 'string':
                tval += 'Text'
            elif tdef == 'bool':
                tval += 'Bool'
            elif tdef == 'PipelineResourceType':
                tval += 'Text'
            else:
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
        v = v.replace('./', './../types/')
        if v.startswith('Optional'):
            defaults.append((n, 'None ' + v[len('Optional'):]))
        elif v.startswith('List'):
            defaults.append((n, '[] : List ' + v[len('List'):]))
        elif n == 'apiVersion':
            defaults.append((n, '"tekton.dev/v1alpha1"'))
        elif n == 'kind':
            defaults.append((n, '"' + type['name'] + '"'))
    defaults_str = " , ".join(map(lambda td: " = ".join(td), defaults)) if defaults else '='
    write_file(default_file, "{" + defaults_str + "}")
    schema_file = Path('schemas') / show_type_file(type['name'])
    write_file(schema_file, "{ Type = ./../%s , default = ./../%s }" % (str(type_file), str(default_file)))



for tekton_type in tekton_type_files:
    for t in read_type(tekton_type).values():
        if t['name'].endswith('List'):
            continue
        type_def = show_type(t)
        write_type(t, type_def)

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
