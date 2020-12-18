import os
from conans import ConanFile, CMake, tools


class MosquittoConan(ConanFile):
    name = "mosquitto"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://mosquitto.org"
    description = "Eclipse Mosquitto - An open source MQTT broker"
    topics = ("conan", "eclipse", "mqtt", "broker", "protocol")
    license = "Eclipse Public License 2.0"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    no_copy_source = True

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def requirements(self):
        self.requires("cjson/1.7.14")
        self.requires("openssl/1.1.1i")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["WITH_BUNDLED_DEPS"] = False
        self._cmake.definitions["WITH_TLS"] = True # SSL Support
        self._cmake.definitions["WITH_TLS_PSK"] = False # SSL Support
        self._cmake.definitions["WITH_EC"] = False
        self._cmake.definitions["WITH_UNIX_SOCKETS"] = False
        self._cmake.definitions["WITH_SOCKS"] = False
        self._cmake.definitions["WITH_SRV"] = False

        self._cmake.definitions["WITH_STATIC_LIBRARIES"] = not self.options.shared
        self._cmake.definitions["WITH_PIC"] = "fPIC" in self.options and self.options.fPIC
        self._cmake.definitions["WITH_THREADING"] = False
        self._cmake.definitions["WITH_DLT"] = False

        self._cmake.definitions["WITH_CLIENTS"] = True
        self._cmake.definitions["WITH_BROKER"] = True
        self._cmake.definitions["WITH_APPS"] = True
        self._cmake.definitions["WITH_PLUGINS"] = True
        self._cmake.definitions["DOCUMENTATION"] = True
       
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        zstd_cmake = "libzstd_shared" if self.options.shared else "libzstd_static"
        self.cpp_info.components["zstdlib"].names["pkg_config"] = "libzstd"
        self.cpp_info.components["zstdlib"].names["cmake_find_package"] = zstd_cmake
        self.cpp_info.components["zstdlib"].names["cmake_find_package_multi"] = zstd_cmake
        self.cpp_info.components["zstdlib"].libs = tools.collect_libs(self)
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["zstdlib"].system_libs.append("pthread")
