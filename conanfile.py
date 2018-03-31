from conans import ConanFile, CMake, tools


class SfmlConan(ConanFile):
    name = "SFML"
    version = "2.4.2"
    license = "zlib/png"
    url = "https://www.sfml-dev.org/"
    description = "Simple and Fast Multimedia Library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/SFML/SFML.git")
        # self.run("cd SFML && git checkout static_shared")
        self.run("cd SFML")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("SFML/CMakeLists.txt", "project(SFML)",
                              '''PROJECT(SFML)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="SFML")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["sfml-graphics", "sfml-audio", "sfml-system", "sfml-network", "sfml-window"]

