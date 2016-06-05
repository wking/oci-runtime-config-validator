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

import unittest

import semver

from . import util


class TestVersion(unittest.TestCase):
    @unittest.skipIf(
        not util.VERSION,
        'cannot check for recognized version without a version string')
    def test_recognized_version(self):
        """Check for a recognized configuration version.

        The test suite may not understand all current runtime-spec
        releases.  Die if the user is giving us a version we don't
        recognize, so we don't give the user the impression that we
        can validate
        """
        self.assertIn(
            util.VERSION, util.VERSIONS,
            'Unrecognized configuration version.  Either your configuration '
            'does not match an OCI specification or the test suite has not '
            'been taught to process the version you are using.'
            .format(util.VERSION))

    @unittest.skipIf(
        not util.CONFIG_JSON,
        'cannot test version without configuration JSON')
    def test_semantic_version(self):
        """ociVersion (string, required) MUST be in SemVer v2.0.0 format.

        The spec wording in the docstring summary is from [1,2].
        v0.5.0 used 'must' instead of 'MUST', but that was accidental
        [3].

        This test is not restricted to known versions, because we
        expect a semantic-versioned field to extend to all spec
        releases (otherwise what's the point of SemVer?).

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#specification-version
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#specification-version
        [3]: https://github.com/opencontainers/runtime-spec/pull/409
        """
        self.assertTrue(isinstance(util.VERSION, str), 'ociVersion is not a string')
        try:
            version = semver.parse(version=util.VERSION)
        except ValueError as error:
            raise self.failureException(str(error)) from error
