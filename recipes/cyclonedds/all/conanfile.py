from conans import ConanFile, tools, AutoToolsBuildEnvironment
from contextlib import contextmanager
import os

from conans import ConanFile, CMake

class CycloneddsConan(ConanFile):
    name = "cyclonedds"
    license = "Apache License Version 2.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    description = ""
    url = "https://github.com/eclipse-cyclonedds/cyclonedds"
    author = ""
    exports_sources = ["CMakeLists.txt", "patches/*"]
    options = {"shared": [True, False], "fPIC": [True, False], "build_testing": [True, False], "build_docs": [True, False], "build_schema": [True, False], "build_idlc": [True, False]}
    default_options = {"shared": False, "fPIC": True, "build_testing" : True, "build_docs" : False, "build_schema" : False, "build_idlc" : False } 
    no_copy_source = True
    _cmake = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build_requirements(self):
        self.build_requires("cmake/3.19.2")
        if self.options.build_testing:
            self.build_requires("cunit/2.1-3")
            self.build_requires("gtest/1.10.0")
        if self.options.build_docs:
            self.build_requires("doxygen/1.8.20")

    def requirements(self):
        self.requires("openssl/1.1.1i")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        archive_name = "{0}-{1}".format(self.name, self.version)
        os.rename(archive_name, self._source_subfolder)
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def _cmake_configure(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions['BUILD_TESTING'] = "ON" if self.options.build_testing else "OFF" 
        self._cmake.definitions['BUILD_DOCS'] = "ON" if self.options.build_docs else "OFF" 
        self._cmake.definitions['BUILD_SCHEMA'] = "ON" if self.options.build_schema else "OFF" 
        self._cmake.definitions['BUILD_IDLC'] = "ON" if self.options.build_idlc else "OFF"
        self._cmake.definitions['CMAKE_CONFIGURATION_TYPES'] = self.settings.build_type
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._cmake_configure()     
        cmake.build()

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()
        
    def package_id(self):
        del self.info.options.build_testing
        del self.info.options.build_docs
        del self.info.options.build_schema
