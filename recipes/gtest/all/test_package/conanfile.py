#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"
    options = {"shared": [True, False], "build_gmock": [True, False], "fPIC": [True, False], "no_main": [True, False], "hide_symbols": [True, False]}
    default_options = {"shared": False, "build_gmock": True, "fPIC": True, "no_main": False, "hide_symbols": False}
    _test_package_variants = [
        "conan_libs",
        ## "conan_targets", # Not working, not sure why
        "conan_find_package",
        "conan_find_include",
        "cmake_find_package",
    ]

    def build(self):
        cmake = CMake(self)
        cmake.definitions['WITH_GMOCK'] = self.options['gtest'].build_gmock
        cmake.definitions['WITH_MAIN'] = not self.options['gtest'].no_main
        for test_package_variant in self._test_package_variants:
            cmake.definitions['TEST_PACKAGE_VARIANT'] = test_package_variant
            cmake.configure()
            cmake.build()

    def test(self):
        assert os.path.isfile(os.path.join(self.deps_cpp_info["gtest"].rootpath, "licenses", "LICENSE"))
        if not tools.cross_building(self.settings):
            for test_package_variant in self._test_package_variants:
                test_package = os.path.join("bin", "test_package-%s" % test_package_variant)
                self.run(test_package, run_environment=True)
