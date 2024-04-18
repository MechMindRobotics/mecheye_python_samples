cmake_minimum_required(VERSION 3.5)

project(ConvertPointCloudToObjectModel3D)

set(CMAKE_CXX_STANDARD 14)

if(CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "aarch64")
  message(FATAL_ERROR "This sample is not valid in ARM platform.")
endif()

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/../cmake;${CMAKE_MODULE_PATH}")

set(Files ${PROJECT_SOURCE_DIR}/ConvertPointCloudToObjectModel3D.cpp)

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

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/Halcon/cmake;${CMAKE_MODULE_PATH}")
find_package(Halcon REQUIRED)
find_package(HDevEngine REQUIRED)
if(NOT HALCON_FOUND)
  message(FATAL_ERROR "Halcon not found.")
endif()

include_directories(${MECHEYEAPI_INCLUDE_DIRS} ${HALCON_INC_DIRS})

link_directories(${MECHEYEAPI_LIBRARY_DIRS} ${HALCON_EXT_LIB_DIR})

add_executable(${PROJECT_NAME} ${Files} "HalconUtil.cpp")

target_link_libraries(${PROJECT_NAME} ${MECHEYEAPI_LIBRARIES} ${HALCON_LIBS}
                      ${HALCON_LIBS_XL})
