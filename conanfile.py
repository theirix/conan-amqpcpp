from conans import ConanFile, CMake, tools
import os
import shutil

class AmqpcppConan(ConanFile):
    name = "amqpcpp"
    version = "2.8.0"
    url = "https://github.com/theirix/conan-amqpcpp"
    license = "Apache-2.0"
    description = "C++ library for asynchronous non-blocking communication with RabbitMQ"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "CMakeLists.txt"
    generators = "cmake"

    @property
    def majorver(self):
        return int(self.version.split('.')[0])

    def source(self):
        tools.get("https://github.com/CopernicaMarketingSoftware/AMQP-CPP/archive/v%s.tar.gz" % self.version)
        os.rename("AMQP-CPP-%s" % (self.version), self.name)

    def configure(self):
        if self.settings.os == "Windows":
            raise Exception("Windows is not supported by upstream")

    def requirements(self):
        if int(self.majorver) >= 3:
            self.requires.add("OpenSSL/1.0.2n@conan/stable")

    def build(self):
        shutil.move("%s/CMakeLists.txt" % self.name, "%s/CMakeListsOriginal.cmake" % self.name)
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.name)
        cmake = CMake(self)

        if self.majorver == 2:
            cmake.definitions['BUILD_SHARED'] = self.options.shared

        if self.majorver >= 3:
            cmake.definitions['AMQP-CPP_BUILD_SHARED'] = self.options.shared
            cmake.definitions['AMQP-CPP_BUILD_EXAMPLES'] = False
            cmake.definitions['AMQP-CPP_LINUX_TCP'] = True

        # avoid rpath
        if self.settings.os == "Macos":
            cmake.definitions['CMAKE_SKIP_RPATH'] = True

        cmake.configure(source_dir=self.name, build_dir="./")
        cmake.build()

    def package(self):
        self.copy("license*", src="%s" % (self.name), dst="licenses", ignore_case=True, keep_path=False)
        if self.majorver >= 3:
            self.copy("*.h", dst="include", src="%s/include" % (self.name))
        else:
            self.copy("*.h", dst="include/amqpcpp", src="%s/include" % (self.name))
        self.copy("amqpcpp.h", dst="include", src="%s" % (self.name))
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread"])
