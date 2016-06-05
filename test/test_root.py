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

import os.path
import unittest

import semver

from . import util


class TestRoot(unittest.TestCase):
    @util.skip_if_unrecognized_version
    @util.skip_unless_path_separator_matches
    def test_path(self):
        """path (string, required).

        1.0.0-rc1 just requires a path [1], but 0.5.0 requires the
        path to be relative [2]:

          A directory MUST exist at the relative path declared by the
          field.

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#root-configuration
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#root-configuration
        """
        self.assertIn(
            'root', sorted(util.CONFIG_JSON.keys()), 'root is not set')
        root = util.CONFIG_JSON['root']
        self.assertTrue(isinstance(root, dict), 'root is not an object')
        self.assertIn('path', sorted(root.keys()), 'root.path is not set')
        path = root['path']
        self.assertTrue(isinstance(path, str), 'root.path is not a string')
        if util.VERSION == '0.5.0':
            self.assertFalse(os.path.isabs(path), 'root.path MUST be relative')

    @util.skip_if_unrecognized_version
    def test_readonly(self):
        """readonly (bool, optional).

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#root-configuration
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#root-configuration
        """
        root = util.CONFIG_JSON.get('root', {})
        if 'readonly' in root:
            readonly = root['readonly']
            self.assertIn(
                readonly, [True, False],
                'root.readonly is not a boolean')
