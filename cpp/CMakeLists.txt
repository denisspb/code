cmake_minimum_required(VERSION 2.8)
project(testproj)

add_definitions(-std=c++11)

add_executable(${PROJECT_NAME}
    main.cpp
)

set(LINKLIBS
    pthread
)

target_link_libraries(${PROJECT_NAME} ${LINKLIBS})