import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class BazelInstallerConan(ConanFile):
    name = "bazel"
    description = "bazel build system"
    topics = ("conan", "bazel", "tensorflow")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.bazel.build"
    license = "Apache-2.0"
    settings = {"os_build", "arch_build"}
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return os.path.join(self.source_folder, "source_subfolder")

    def _extract_from_data(self):
        data = self.conan_data["sources"][self.version][str(self.settings.os_build)][str(self.settings.arch_build)]
        url, sha256 =data['url'], data['sha256']
        filename = os.path.basename(url)
        return url, filename, sha256

    def source(self):
        data = self.conan_data["sources"][self.version][str(self.settings.os_build)][str(self.settings.arch_build)]
        url, filename, sha256 = self._extract_from_data()
        tools.download(url, filename, sha256=sha256)
    
    def build(self):
        _, filename, _ = self._extract_from_data()
        tools.unzip(os.path.join(self.source_folder, filename), destination=os.path.splitext(filename)[0])

    def package(self):
        _, filename, _ = self._extract_from_data()
        self.copy(pattern="*", src=os.path.splitext(filename)[0])

    def package_info(self):
        self.env_info.PATH.append(self.package_folder)
