from conans import ConanFile, tools, AutoToolsBuildEnvironment
from contextlib import contextmanager
import os

from conans import ConanFile, CMake

class CpptomlConan(ConanFile):
    name = "iceoryx"
    license = "Apache License Version 2.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    description = ""
    url = "https://github.com/eclipse-iceoryx/iceoryx"
    author = ""
    scm = { "type": "git", "url": "auto", "revision": "auto" }
    exports_sources = ["CMakeLists.txt", "iceoryxConfig.cmake", "patches/*"]
    options = {"shared": [True, False], "fPIC": [True, False], "build_test": [True, False], "build_doc": [True, False], "build_examples": [True, False]}
    default_options = {"shared": False, "fPIC": True, "build_test" : True, "build_doc" : False, "build_examples" : True } 
    no_copy_source = True
    _cmake = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build_requirements(self):
        self.build_requires("cmake/3.19.2")
        if self.options.build_test:
            self.build_requires("gtest/1.10.0")
        if self.options.build_doc:
            self.build_requires("doxygen/1.8.20")
        self.build_requires("cpptoml/0.1.1")

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
        self._cmake.definitions['BUILD_ALL'] = "OFF" # Do not enable as this will add subsequent
        self._cmake.definitions['TOML_CONFIG'] = "ON" 
        self._cmake.definitions['ONE_TO_MANY_ONLY'] = "OFF" 
        self._cmake.definitions['BUILD_STRICT'] = "OFF" 
        self._cmake.definitions['BUILD_SHARED_LIBS'] = "ON" if self.options.shared else "OFF" 
        self._cmake.definitions['BUILD_TEST'] = "ON" if self.options.build_test else "OFF" 
        self._cmake.definitions['BUILD_DOC'] = "ON" if self.options.build_doc else "OFF" 
        self._cmake.definitions['COVERAGE'] = "OFF" 
        self._cmake.definitions['EXAMPLES'] = "ON" if self.options.build_examples else "OFF" 
        self._cmake.definitions['INTROSPECTION'] = "OFF" 
        self._cmake.definitions['DDS_GATEWAY'] = "OFF" 
        self._cmake.definitions['BINDING_C'] = "ON"  
        self._cmake.definitions['SANITIZE'] = "OFF"  
        self._cmake.definitions['CLANG_TIDY'] = "OFF"  
        self._cmake.definitions['ROUDI_ENVIRONMENT'] = "ON"  
        self._cmake.definitions['CMAKE_BUILD_TYPE'] = self.settings.build_type
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._cmake_configure()
        cmake.build()

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()
        self.copy(pattern="iceoryxConfig.cmake", dst="lib/cmake/iceoryx")

    def package_id(self):
        del self.info.options.build_test
        del self.info.options.build_doc
        del self.info.options.build_examples
