if(CMAKE_HOST_WIN32)
  cmake_minimum_required(VERSION 3.19)
else()
  cmake_minimum_required(VERSION 3.5)
endif()

project(ConvertPointCloudWithNormalsToPcl)

set(CMAKE_CXX_STANDARD 14)

set(Files ${PROJECT_SOURCE_DIR}/ConvertPointCloudWithNormalsToPcl.cpp)

if(CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "aarch64")
  add_compile_options(-mno-outline-atomics)
endif()

if(CMAKE_HOST_WIN32)
  find_package(MechEyeApi REQUIRED CONFIG PATHS "$ENV{MECHEYE_DIR}/API")
  if(NOT MechEyeApi_FOUND)
    message(
      FATAL_ERROR "MechEyeApi not found. Please install MechEyeApi first.")
  endif()
elseif(CMAKE_HOST_UNIX)
  find_package(PkgConfig)
  if(NOT PkgConfig_FOUND)
    message(FATAL_ERROR "PkgConfig not found.")
  else()
    pkg_check_modules(MECHEYEAPI REQUIRED MechEyeApi)
    if(NOT MECHEYEAPI_FOUND)
      message(
        FATAL_ERROR "MechEyeApi not found. Please install MechEyeApi first.")
    endif()
  endif()
endif()

if(CMAKE_HOST_WIN32)
  if(MSVC_VERSION LESS 1910)
    message(FATAL_ERROR "Please use Visual Studio 2017 or higher.")
  elseif(MSVC_VERSION LESS 1920)
    find_package(PCL 1.8.1...1.9.1 REQUIRED)
  elseif(MSVC_VERSION LESS 1930)
    find_package(PCL 1.8.1...1.12.1 REQUIRED)
  else()
    find_package(PCL 1.8.1 REQUIRED)
  endif()
elseif(CMAKE_HOST_UNIX)
  find_package(PCL REQUIRED)
endif()
if(NOT PCL_FOUND)
  message(
    FATAL_ERROR
      "Point Cloud Library (PCL) not found. Please point PCL_DIR to the directory of your PCL installation (containing the file PCLConfig.cmake)."
  )
endif()

include_directories(${MECHEYEAPI_INCLUDE_DIRS} ${PCL_INCLUDE_DIRS})
link_directories(${MECHEYEAPI_LIBRARY_DIRS} ${PCL_LIBRARY_DIRS})

add_executable(${PROJECT_NAME} ${Files})

target_link_libraries(${PROJECT_NAME} ${MECHEYEAPI_LIBRARIES} ${PCL_LIBRARIES})
