from conans import ConanFile, CMake
from conans.tools import download, untargz, check_sha1
import os
import shutil

class AmqpcppConan(ConanFile):
    name = "amqpcpp"
    version = "2.7.4"
    url = "https://github.com/theirix/conan-amqpcpp"
    license = "https://github.com/CopernicaMarketingSoftware/AMQP-CPP/blob/master/LICENSE"
    description = "C++ library for asynchronous non-blocking communication with RabbitMQ"
    FOLDER_NAME = 'AMQP-CPP-%s' % version
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "CMakeLists.txt"
    generators = "cmake", "txt"

    def source(self):
        tarball_name = "v%s.tar.gz" % self.version
        download("https://github.com/CopernicaMarketingSoftware/AMQP-CPP/archive/%s" % tarball_name, tarball_name)
        check_sha1(tarball_name, "76ba6f00d2ac96ef171da85bcfadd985e7d0b567")
        untargz(tarball_name)
        os.unlink(tarball_name)
        shutil.move("%s/CMakeLists.txt" % self.FOLDER_NAME, "%s/CMakeListsOriginal.cmake" % self.FOLDER_NAME)
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.FOLDER_NAME)

    def configure(self):
        if self.settings.os == "Windows":
            raise Exception("Windows is not supported by upstream")

    def build(self):
        cmake = CMake(self.settings)

        # compose cmake options
        extra_command_line = ''
        if self.options.shared:
            extra_command_line += " -DBUILD_SHARED=ON"
        # avoid rpath
        if self.settings.os == "Macos":
            extra_command_line += " -DCMAKE_SKIP_RPATH=ON"

        cmd = 'cmake %s/%s %s %s' % (self.conanfile_directory, self.FOLDER_NAME, cmake.command_line, extra_command_line)
        self.output.warn('Running CMake: ' + cmd)
        self.run(cmd)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("license*", src="%s" % (self.FOLDER_NAME), dst="licenses", ignore_case=True, keep_path=False)
        self.copy("*.h", dst="include/amqpcpp", src="%s/include" % (self.FOLDER_NAME))
        self.copy("amqpcpp.h", dst="include", src="%s" % (self.FOLDER_NAME))
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['amqp-cpp']
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread"])
