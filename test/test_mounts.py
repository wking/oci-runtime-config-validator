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

from . import util


class TestMounts(unittest.TestCase):
    @util.skip_if_unrecognized_version
    def test_destination(self):
        """destination (string, required).

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#mounts
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#mounts
        """
        for i, mount in enumerate(util.CONFIG_JSON.get('mounts', [])):
            with self.subTest(i=i):
                self.assertIn(
                    'destination', sorted(mount.keys()),
                    'destination is not set')
                destination = mount['destination']
                self.assertTrue(
                    isinstance(destination, str),
                    'destination is not a string')

    @util.skip_if_unrecognized_version
    @unittest.skipUnless(
        util.PLATFORM_OS == 'windows' and
        util.VERSION == '1.0.0-rc1',
        'the destination-nesting restriction only applies to Windows for '
        'specification version 1.0.0-rc1.')
    @util.skip_unless_path_separator_matches
    def test_destination_nesting(self):
        """Mount destinations MUST not be nested within another mount.

        1.0.0-rc1 has a restriction [1] (beyond 0.5.0 [2]):

          For the Windows operating system, one mount destination MUST
          NOT be nested within another mount. (Ex: c:\foo and
          c:\foo\bar).

        The status of c:\foo followed by c:\foo and c:\foo\bar
        followed by c:\foo are unclear [3].

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#mounts
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#mounts
        [3]: https://github.com/opencontainers/runtime-spec/pull/437#issuecomment-223793968
        """
        destinations = []
        for i, mount in enumerate(util.CONFIG_JSON.get('mounts', [])):
            destination = mount.get('destination')
            if not isinstance(destination, str):
                continue  # already covered by test_destination
            with self.subTest(i=i, destination=destination):
                for previous in destinations:
                    relative_path = os.path.relpath(destination, previous)
                    print(destination, previous, relative_path)
                    if destination == previous:
                        pass
                    elif relative_path == os.path.pardir:  # parent directory
                        pass
                    elif os.path.sep not in relative_path: # child directory
                        raise self.failureException(
                            'for the Windows operating system, one mount '
                            'destination MUST not be nested within another '
                            'mount, but {} is nested within {}.'
                            .format(destination, previous))
                    elif (relative_path.split(os.path.sep, 1)[0] ==
                          os.path.pardir):  # ancestor directory
                        pass
                    else:  # descendant directory
                        raise self.failureException(
                            'for the Windows operating system, one mount '
                            'destination MUST not be nested within another '
                            'mount, but {} is nested within {}.'
                            .format(destination, previous))
                destinations.append(destination)

    @util.skip_if_unrecognized_version
    def test_type(self):
        """type (string, required).

        The spec wording is [1,2]:

          Linux, filesystemtype argument supported by the kernel are
          listed in /proc/filesystems (e.g., "minix", "ext2", "ext3",
          "jfs", "xfs", "reiserfs", "msdos", "proc", "nfs",
          "iso9660").  Windows: ntfs

        But this is underspecified [3], so we only check the type
        here.

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#mounts
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#mounts
        [3]: https://github.com/opencontainers/runtime-spec/issues/470
        """
        for i, mount in enumerate(util.CONFIG_JSON.get('mounts', [])):
            with self.subTest(i=i):
                self.assertIn(
                    'type', sorted(mount.keys()), 'type is not set')
                type = mount['type']
                self.assertTrue(isinstance(type, str), 'type is not a string')

    @util.skip_if_unrecognized_version
    def test_source(self):
        """source (string, required).

        The spec wording is [1,2]:

          a device name, but can also be a directory name or a
          dummy. Windows, the volume name that is the target of the
          mount point. \?\Volume{GUID}\ (on Windows source is called
          target)

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#mounts
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#mounts
        """
        for i, mount in enumerate(util.CONFIG_JSON.get('mounts', [])):
            with self.subTest(i=i):
                self.assertIn(
                    'source', sorted(mount.keys()), 'source is not set')
                source = mount['source']
                self.assertTrue(
                    isinstance(source, str), 'source is not a string')

    @util.skip_if_unrecognized_version
    def test_options(self):
        """options (list of strings, optional).

        The spec wording is [1,2]:

          in the fstab format https://wiki.archlinux.org/index.php/Fstab.

        But this is underspecified [3], so we only check the type
        here.

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#mounts
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#mounts
        [3]: https://github.com/opencontainers/runtime-spec/pull/439
        """
        for i, mount in enumerate(util.CONFIG_JSON.get('mounts', [])):
            with self.subTest(i=i):
                options = mount.get('options', [])
                self.assertTrue(
                    isinstance(options, list), 'options is not an array')
                for j, option in enumerate(options):
                    with self.subTest(j=j):
                        self.assertTrue(
                            isinstance(option, str), 'option is not a string')
