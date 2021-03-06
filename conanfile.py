from conans import ConanFile, CMake, tools
import platform

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
        cmake.configure(source_folder="SFML", defs={"CMAKE_BUILD_TYPE":"Release","BUILD_SHARED_LIBS":True, "SFML_USE_STATIC_STD_LIBS": False,   })
        
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "", "bin")
        self.copy("*.dylib", "", "lib")

    def package(self):
        # self.copy("*.h", dst="include", src="include")
        # self.copy("*.hpp", dst="include/SFML", src="include/SFML")
        # self.copy("*.hpp", dst="include/SFML/Audio", src="include/SFML/Audio")
        # self.copy("*.hpp", dst="include/SFML/Graphics", src="include/SFML/Graphics")
        # self.copy("*.hpp", dst="include/SFML/Network", src="include/SFML/Network")
        # self.copy("*.hpp", dst="include/SFML/System", src="include/SFML/System")
        # self.copy("*.hpp", dst="include/SFML/Window", src="include/SFML/Window")
        self.copy("*", src="SFML/include", dst="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        #self.cpp_info.includedirs = ['include']
        self.cpp_info.libs = ["sfml-system",
                              "sfml-window","sfml-network",
                              "sfml-graphics","sfml-audio",
                              "flac", "freetype", "ogg", "openal32",
                              "vorbis", "vorbisenc", "vorbisfile"  ]
        
        if platform.system() == "Windows":
            self.cpp_info.libs.insert(0, "sfml-main") 
        
        
        '''
flac.lib
freetype.lib
ogg.lib
openal32.lib
sfml-audio-s.lib
sfml-graphics-s.lib
sfml-main.lib
sfml-network-s.lib
sfml-system-s.lib
sfml-window-s.lib
vorbis.lib
vorbisenc.lib
vorbisfile.lib
        '''
        

