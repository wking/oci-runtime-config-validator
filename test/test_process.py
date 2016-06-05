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
import re
import unittest

from . import util


class TestProcess(unittest.TestCase):
    ENVIRONMENT_VARIABLE_KEY_INVALID_REGEX = re.compile('[^a-zA-Z0-9_]')

    @util.skip_if_unrecognized_version
    def test_process(self):
        """process (object, required).

        This is currently underspecified [1,2], but I expect it to be
        required [3].

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#process-configuration
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#process-configuration
        [3]: https://github.com/opencontainers/runtime-spec/pull/489
        """
        self.assertIn(
            'process', sorted(util.CONFIG_JSON.keys()),
            'process is not set')
        process = util.CONFIG_JSON['process']
        self.assertTrue(isinstance(process, dict), 'process is not an object')

    @util.skip_if_unrecognized_version
    @unittest.skipUnless(
        isinstance(util.CONFIG_JSON.get('process'), dict),
        'cannot validate process.terminal without a process object')
    def test_terminal(self):
        """terminal (bool, optional).

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#process-configuration
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#process-configuration
        """
        process = util.CONFIG_JSON['process']
        if 'terminal' in process:
            terminal = process['terminal']
            self.assertIn(
                terminal, [True, False], 'process.terminal is not a boolean')

    @util.skip_if_unrecognized_version
    @unittest.skipUnless(
        isinstance(util.CONFIG_JSON.get('process'), dict),
        'cannot validate process.cwd without a process object')
    @util.skip_unless_path_separator_matches
    def test_cwd(self):
        """cwd (string, required).

        From the spec [1,2]:

          This value MUST be an absolute path.

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#process-configuration
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#process-configuration
        """
        process = util.CONFIG_JSON['process']
        self.assertIn('cwd', sorted(process.keys()), 'process.cwd is not set')
        cwd = process['cwd']
        self.assertTrue(
            os.path.isabs(cwd), 'process.cwd MUST be an absolute path')

    @util.skip_if_unrecognized_version
    @unittest.skipUnless(
        isinstance(util.CONFIG_JSON.get('process'), dict),
        'cannot validate process.env without a process object')
    def test_env(self):
        """env (array of strings, optional).

        From the spec [1,2]:

          Elements in the array are specified as Strings in the form
          "KEY=value". The left hand side must consist solely of
          letters, digits, and underscores _ as outlined in IEEE Std
          1003.1-2001.

        I'd rather punt to POSIX [3] (which is less strict), but the
        pull request for that is still in flight.

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#process-configuration
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#process-configuration
        [3]: https://github.com/opencontainers/runtime-spec/pull/427#issuecomment-220530504
        """
        process = util.CONFIG_JSON['process']
        if 'env' in process:
            env = process['env']
            self.assertTrue(
                isinstance(env, list), 'process.env is not an array')
            for i, env_var in enumerate(env):
                with self.subTest(i=i, environment_variable=env_var):
                    self.assertTrue(
                        isinstance(env_var, str),
                        'process.env[{}] ({}) is not a string'
                        .format(i, env_var))
                    # the only POSIX requirement is an equals sign
                    self.assertTrue(
                        '=' in env_var,
                        'process.env[{}] ({}) does not contain an equals sign'
                        .format(i, env_var))
                    # additional restrictions from the OCI spec
                    key = env_var.split('=', 1)[0]
                    match = self.ENVIRONMENT_VARIABLE_KEY_INVALID_REGEX.search(
                        key)
                    if match:
                        invalid_character = match.group(0)
                        raise self.failureException(
                            "process.env[{}]'s key ({}) contains an invalid "
                            'character: {!r}'
                            .format(i, key, invalid_character))

    @util.skip_if_unrecognized_version
    @unittest.skipUnless(
        isinstance(util.CONFIG_JSON.get('process'), dict),
        'cannot validate process.args without a process object')
    def test_args(self):
        """args (array of strings, required).

        From the spec [1,2]:

          The executable is the first element and MUST be available at
          the given path inside of the rootfs. If the executable path
          is not an absolute path then the search $PATH is interpreted
          to find the executable.

        v0.5.0 used 'must' instead of 'MUST', but that was accidental
        [3].

        I don't see how "MUST be available at the given path" squares
        with "If the executable path is not an absolute path then
        search $PATH".  And that's not how execvp works anyway (it
        walks PATH only if there *no* separators in the the file [4]).
        I expect we want to punt all of this to POSIX [5], so for now
        I only check that args is an array of strings with at least
        one element.

        [1]: https://github.com/opencontainers/runtime-spec/blob/v1.0.0-rc1/config.md#process-configuration
        [2]: https://github.com/opencontainers/runtime-spec/blob/v0.5.0/config.md#process-configuration
        [3]: https://github.com/opencontainers/runtime-spec/pull/438
        [4]: http://pubs.opengroup.org/onlinepubs/9699919799/functions/execvp.html
        [5]: https://github.com/opencontainers/runtime-spec/pull/427#issuecomment-220530504
        """
        process = util.CONFIG_JSON['process']
        self.assertIn(
            'args', sorted(process.keys()), 'process.args is not set')
        args = process['args']
        self.assertTrue(isinstance(args, list), 'process.args is not an array')
        self.assertTrue(
            len(args) > 0, 'process.args must have at least one element')
        for i, arg in enumerate(args):
            with self.subTest(i=i, argument=arg):
                self.assertTrue(
                    isinstance(arg, str),
                    'process.args[{}] ({}) is not a string'.format(i, arg))
