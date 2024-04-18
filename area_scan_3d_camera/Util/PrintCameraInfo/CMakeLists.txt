cmake_minimum_required(VERSION 3.5)

project(PrintCameraInfo)

set(CMAKE_CXX_STANDARD 14)

set(Files ${PROJECT_SOURCE_DIR}/PrintCameraInfo.cpp)

set(MIN_EYE_VERSION 2.1.0)
if(CMAKE_HOST_WIN32)
  find_package(MechEyeApi ${MIN_EYE_VERSION} REQUIRED CONFIG PATHS
               "$ENV{MECHEYE_DIR}/API")
  if(NOT MechEyeApi_FOUND)
    message(
      FATAL_ERROR
        "MechEyeApi not found. Please install MechEyeApi with version ${MIN_EYE_VERSION} or higher."
    )
  endif()
elseif(CMAKE_HOST_UNIX)
  find_package(PkgConfig)
  if(NOT PkgConfig_FOUND)
    message(FATAL_ERROR "PkgConfig not found.")
  else()
    pkg_check_modules(MECHEYEAPI REQUIRED MechEyeApi>=${MIN_EYE_VERSION})
    if(NOT MECHEYEAPI_FOUND)
      message(
        FATAL_ERROR
          "MechEyeApi not found. Please install MechEyeApi with version ${MIN_EYE_VERSION} or higher."
      )
    endif()
  endif()
endif()

include_directories(${MECHEYEAPI_INCLUDE_DIRS})
link_directories(${MECHEYEAPI_LIBRARY_DIRS})

add_executable(${PROJECT_NAME} ${Files})
target_link_libraries(${PROJECT_NAME} ${MECHEYEAPI_LIBRARIES})
