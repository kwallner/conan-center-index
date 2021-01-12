import os
from conans import ConanFile, tools


class TestPackageConan(ConanFile):

    def test(self):
        self.output.info("Bazel version:")
        self.run("bazel --version", run_environment=True)
