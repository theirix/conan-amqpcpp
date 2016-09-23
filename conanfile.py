from conans import ConanFile, CMake
from conans.tools import download, untargz, check_sha1, replace_in_file
import os
import shutil

class AmqpcppConan(ConanFile):
    name = "amqpcpp"
    version = "2.6.2"
    url = "https://github.com/theirix/conan-amqpcpp"
    license = "https://github.com/CopernicaMarketingSoftware/AMQP-CPP/blob/master/LICENSE"
    FOLDER_NAME = 'AMQP-CPP-%s' % version
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "CMakeLists.txt"
    generators = "cmake", "txt"

    def config(self):
        pass

    def source(self):
        tarball_name = "v%s.tar.gz" % self.version
        download("https://github.com/CopernicaMarketingSoftware/AMQP-CPP/archive/%s" % tarball_name, tarball_name)
        check_sha1(tarball_name, "952dd2d455c9c45ffea292e15ea58bab1622b5b3")
        untargz(tarball_name)
        os.unlink(tarball_name)
        shutil.move("%s/CMakeLists.txt" % self.FOLDER_NAME, "%s/CMakeListsOriginal.cmake" % self.FOLDER_NAME)
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.FOLDER_NAME)

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
