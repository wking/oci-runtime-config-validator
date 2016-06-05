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

import os
import unittest

from . import util


class TestBundle(unittest.TestCase):
    def test_configuration(self):
        """config.json MUST reside in the root of the bundle directory.

        The spec wording is [1,2]:

          config.json: contains configuration data. This REQUIRED file
          MUST reside in the root of the bundle directory and MUST be
          named config.json.

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/bundle.md#container-format
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/bundle.md#container-format
        """
        self.assertTrue(
            os.path.exists(util.CONFIG_PATH),
            'no file found at {}'.format(util.CONFIG_PATH))
        self.assertIsNotNone(
            util.CONFIG_BYTES, 'unable to read configuration JSON')

    @util.skip_if_unrecognized_version
    @util.skip_unless_path_separator_matches
    def test_root(self):
        """The bundle directory MUST contain the root filesystem.

        The 1.0.0-rc1 spec wording is [1]:

          A Standard Container bundle ... MUST include the following artifacts:

          ...

          2. A directory representing the root filesystem of the container...

          ... these artifacts MUST all be present in a single
          directory on the local filesystem...

        And the 0.5.0 spec wording is [2]:

          A Standard Container bundle ... includes the following
          artifacts which MUST all reside in the same directory on the
          local filesystem:

          ...

          2. A directory representing the root filesystem of the container...

          ... these artifacts MUST all be present in a single
          directory on the local filesystem...

        The path to the root filesystem comes from the configuration
        JSON.  In 1.0.0-rc1 [3]:

          Each container has exactly one root filesystem, specified in
          the root object:

          * path (string, required) Specifies the path to the root
            filesystem for the container. A directory MUST exist at
            the path declared by the field.

        And in 0.5.0 [4]:

          Each container has exactly one root filesystem, specified in
          the root object:

          * path (string, required) Specifies the path to the root
            filesystem for the container, relative to the path where
            the manifest is. A directory MUST exist at the relative
            path declared by the field.

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/bundle.md#container-format
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/bundle.md#container-format
        [3]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#root-configuration
        [4]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#root-configuration
        """
        self.assertIn(
            'root', sorted(util.CONFIG_JSON.keys()), 'root is not set')
        root = util.CONFIG_JSON['root']
        self.assertTrue(isinstance(root, dict), 'root is not an object')
        self.assertIn('path', sorted(root.keys()), 'root.path is not set')
        path = root['path']
        self.assertTrue(isinstance(path, str), 'root.path is not a string')
        bundle = os.environ.get('BUNDLE', '.')
        root_path = os.path.join(bundle, path)
        self.assertTrue(
            os.path.isdir(root_path),
            'the configured root.path ({}) does not point to a directory'
            .format(path)
        )
        relative_root_path = os.path.relpath(root_path, bundle)
        self.assertFalse(
            os.path.sep in relative_root_path,
            'root filesystem MUST be present in the same directory as '
            'config.json, but its relative path is {}'
            .format(relative_root_path))
