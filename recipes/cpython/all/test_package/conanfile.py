#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools

class TestPackageConan(ConanFile):
    generators = "cmake", "cmake_find_package"
    settings = "os", "compiler", "build_type", "arch"
    options = { "shared": [True, False] }
    default_options = { "shared": True }
    _test_package_variants = [
        "conan_libs",
        "conan_targets",
        "conan_find_package",
        "cmake_find_package",
    ]

    def build(self):
        # Ugly hack to make debug test_package work on windows
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            python_vers = "".join(self.deps_cpp_info["cpython"].version.split(".")[0:2])
            tools.replace_in_file("conanbuildinfo.cmake", "python%s" % python_vers, "python%s_d" % python_vers, strict=False)
            tools.replace_in_file("Findcpython.cmake", "python%s" % python_vers, "python%s_d" % python_vers, strict=False)
        cmake = CMake(self)
        cmake.definitions['CMAKE_VERBOSE_MAKEFILE'] = True
        for test_package_variant in self._test_package_variants:
            cmake.definitions['TEST_PACKAGE_VARIANT'] = test_package_variant
            cmake.configure()
            cmake.build()

    def test(self):
        assert os.path.isfile(os.path.join(self.deps_cpp_info["cpython"].rootpath, "LICENSE"))
        if not tools.cross_building(self.settings):
            for test_package_variant in self._test_package_variants:
                test_package = os.path.join("bin", "test_package-%s" % test_package_variant)
                self.run(test_package, run_environment=True)