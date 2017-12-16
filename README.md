[ ![Download](https://api.bintray.com/packages/theirix/conan-repo/amqpcpp%3Atheirix/images/download.svg) ](https://bintray.com/theirix/conan-repo/amqpcpp%3Atheirix/_latestVersion)
[![Build Status](https://travis-ci.org/theirix/conan-amqpcpp.svg)](https://travis-ci.org/theirix/conan-amqpcpp)

# conan-amqpcpp

[Conan.io](https://conan.io) package for [amqpcpp](https://github.com/CopernicaMarketingSoftware/AMQP-CPP) library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/amqpcpp/2.7.4/theirix/stable).

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Upload packages to server

    $ conan upload amqpcpp/2.7.4@theirix/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install amqpcpp/2.7.4@theirix/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    amqpcpp/2.7.4@theirix/stable

    [options]
    amqpcpp:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
