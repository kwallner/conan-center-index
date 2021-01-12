import os
import stat
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
        return url, sha256
    
    def _executable_filename(self):
        if self.settings.os_build == "Windows":
            return self.name + ".exe" 
        else:
            return self.name

    def source(self):
        data = self.conan_data["sources"][self.version][str(self.settings.os_build)][str(self.settings.arch_build)]
        url, sha256 = self._extract_from_data()
        filename = self._executable_filename()
        tools.download(url, filename, sha256=sha256)
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)
    
    def build(self):
        pass

    def package(self):
        filename = self._executable_filename()
        self.copy(pattern=filename)

    def package_info(self):
        self.env_info.PATH.append(self.package_folder)
