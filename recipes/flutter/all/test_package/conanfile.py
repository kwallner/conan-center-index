import os
from conans import ConanFile, tools


class TestPackageConan(ConanFile):

    def test(self):
        self.output.info("Dart version:")
        self.run("dart --version", run_environment=True)
        self.output.info("Flutter version:")
        self.run("flutter --version", run_environment=True)
