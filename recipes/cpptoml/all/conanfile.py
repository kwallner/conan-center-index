from conans import ConanFile, tools, AutoToolsBuildEnvironment
from contextlib import contextmanager
import os

from conans import ConanFile, CMake

class CpptomlConan(ConanFile):
    name = "cpptoml"
    description = "A header-only library for parsing TOML configuration files."
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/skystrife/cpptoml"
    topics = ("cpptoml", "toml", "date", "time")
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    no_copy_source = True
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        archive_name = "{0}-{1}".format(self.name, self.version)
        os.rename(archive_name, self._source_subfolder)

    def _cmake_configure(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure(source_folder=self._source_subfolder)
        return self._cmake

    def build(self):
        cmake = self._cmake_configure()
        cmake.build()

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()

    def package_id(self):
        self.info.header_only()
