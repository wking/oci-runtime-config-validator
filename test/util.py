# Copyright 2016 W. Trevor King <wking@tremily.us>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os


VERSIONS = [  # supported specification versions
    '1.0.0-rc1',
    '0.5.0',
]

CONFIG_PATH = os.path.join(os.environ.get('BUNDLE', '.'), 'config.json')
CONFIG_BYTES = CONFIG_JSON = VERSION = None
try:
    with open(CONFIG_PATH, 'rb') as f:
        CONFIG_BYTES = f.read()
except FileNotFoundError:
    pass
else:
    try:
        # All configuration JSON MUST be encoded in UTF-8.
        # https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/glossary.md#json
        # https://github.com/opencontainers/runtime-spec/blob/v0.5.0/glossary.md#json
        _config_string = CONFIG_BYTES.decode('UTF-8')
    except UnicodeDecodeError:
        pass
    else:
        try:
            CONFIG_JSON = json.loads(_config_string)
        except ValueError:
            pass
        else:
            # ociVersion (string, required)
            # https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#specification-version
            # https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#specification-version
            VERSION = CONFIG_JSON.get('ociVersion')
