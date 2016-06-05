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
import unittest

from . import util


class TestSyntax(unittest.TestCase):
    @unittest.skipIf(
        not os.path.exists(util.CONFIG_PATH),
        'cannot test configuration JSON with a missing {}'
        .format(util.CONFIG_PATH))
    def test_syntax(self):
        """All configuration JSON MUST be encoded in UTF-8.

        The spec wording in the docstring summary is from [1,2].

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/glossary.md#json
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/glossary.md#json
        """
        self.assertTrue(
            util.CONFIG_BYTES,
            'unable to read any content from {}'.format(util.CONFIG_PATH))
        try:
            config_string = util.CONFIG_BYTES.decode('UTF-8')
        except ValueError as error:
            raise self.failureException(
                'all configuration JSON MUST be encoded in UTF-8') from error
        try:
            json.loads(config_string)
        except ValueError as error:
            raise self.failureException(
                'invalid JSON encoding: {}'.format(error)) from error
