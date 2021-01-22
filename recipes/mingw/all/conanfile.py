import os
import subprocess
from conans import ConanFile, tools, errors


class MinGWInstallerConan(ConanFile):
    name = "mingw"
    description = "Minimalist GNU compiler collection for windows"
    topics = ("conan", "compiler", "gcc")
    license = "http://www.mingw.org/license"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://mingw.org"
    license = "GPL-3.0"
    settings = {"os_build", "arch_build" }
    options = {"threads": ["posix", "win32"], "exception": ["sjlj", "seh", "dwarf2"]}
    default_options = {"threads": "posix", "exception": "seh"}
    no_copy_source = True

    def build_requirements(self):
        self.build_requires("7zip/19.00")

    def _extract_from_data(self):
        try:
            data = self.conan_data["sources"][self.version][str(self.settings.os_build)][str(self.settings.arch_build)][str(self.options.threads)][str(self.options.exception)]
            url, sha256 =data['url'], data['sha256']
            filename = os.path.basename(url)
            return url, filename, sha256
        except:
            raise errors.ConanInvalidConfiguration("Failed to retrieve sources for: version=%s os_build=%s arch_build=%s threads=%s exception=%s" % 
                (self.version, self.settings.os_build, self.settings.arch_build, self.options.threads, self.options.exception))

    def source(self):
        url, filename, sha256 = self._extract_from_data()
        tools.download(url, filename, sha256=sha256)

    def build(self):
        url, filename, sha256 = self._extract_from_data()
        subprocess.run(["7z", "x", os.path.join(self.source_folder, filename)], check=True)

    def package(self):
        self.copy("*", dst="", src="mingw32")
        self.copy("*", dst="", src="mingw64")

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.env_info.MINGW_HOME = str(self.package_folder)
        self.env_info.CONAN_CMAKE_GENERATOR = "MinGW Makefiles"
        self.env_info.CXX = os.path.join(self.package_folder, "bin", "g++.exe").replace("\\", "/")
        self.env_info.CC = os.path.join(self.package_folder, "bin", "gcc.exe").replace("\\", "/")
