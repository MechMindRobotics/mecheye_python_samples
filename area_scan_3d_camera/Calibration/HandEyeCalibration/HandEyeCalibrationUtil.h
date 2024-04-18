#pragma once
#include <iostream>
#include <math.h>
#include <fstream>
#include <time.h>
#include <sstream>
#include <vector>
#include <limits>
#include "area_scan_3d_camera/HandEyeCalibration.h"

#define PI 3.14159265
namespace {
enum class CommandType { AddPose, Calibrate, GetPatternImg, GetOriginImg, Unknown };
// Obtain keyboard input.
std::string getInputCommand()
{
    std::string command;
    std::cin.clear();
    std::getline(std::cin, command);
    if (std::cin.rdbuf()->in_avail() != 0) {
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    return command;
}

template <typename T>
T getInputNumber()
{
    if (std::cin.rdbuf()->in_avail() != 0) {
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    T input;
    std::string inputStr;
    while (true) {
        std::cin.clear();
        std::getline(std::cin, inputStr);
        std::istringstream iss(inputStr);
        if (iss >> input && iss.eof()) {
            break;
        } else {
            std::cout << "Invalid input. Please enter a valid number." << std::endl;
        }
    }
    return input;
}

// Convert Euler angles to quaternions. The unit of Euler angles is degree.
mmind::eye::HandEyeCalibration::Transformation eulerToquad(int eulerType, double x, double y,
                                                           double z, double R1, double R2,
                                                           double R3)
{
    auto a1 = (R1 * PI / 180) / 2;
    auto a2 = (R2 * PI / 180) / 2;
    auto a3 = (R3 * PI / 180) / 2;
    double quadW = 0.0;
    double quadX = 0.0;
    double quadY = 0.0;
    double quadZ = 0.0;
    switch (eulerType) {
    case 1: // Z-Y'-X''
        quadW = sin(a1) * sin(a2) * sin(a3) + cos(a1) * cos(a2) * cos(a3);
        quadX = -sin(a1) * sin(a2) * cos(a3) + sin(a3) * cos(a1) * cos(a2);
        quadY = sin(a1) * sin(a3) * cos(a2) + sin(a2) * cos(a1) * cos(a3);
        quadZ = sin(a1) * cos(a2) * cos(a3) - sin(a2) * sin(a3) * cos(a1);
        break;

    case 2: // Z-Y'-Z''
        quadW = cos(a2) * cos(a1 + a3);
        quadX = -sin(a2) * sin(a1 - a3);
        quadY = sin(a2) * cos(a1 - a3);
        quadZ = cos(a2) * sin(a1 + a3);
        break;

    case 3: // X-Y'-Z''
        quadW = -sin(a1) * sin(a2) * sin(a3) + cos(a1) * cos(a2) * cos(a3);
        quadX = sin(a1) * cos(a2) * cos(a3) + sin(a2) * sin(a3) * cos(a1);
        quadY = -sin(a1) * sin(a3) * cos(a2) + sin(a2) * cos(a1) * cos(a3);
        quadZ = sin(a1) * sin(a2) * cos(a3) + sin(a3) * cos(a1) * cos(a2);
        break;

    case 4: // Z-X'-Z''
        quadW = cos(a2) * cos(a1 + a3);
        quadX = sin(a2) * cos(a1 - a3);
        quadY = sin(a2) * sin(a1 - a3);
        quadZ = cos(a2) * sin(a1 + a3);
        break;

    case 5: // X-Y-Z
        a1 = (R3 * PI / 180) / 2;
        a2 = (R2 * PI / 180) / 2;
        a3 = (R1 * PI / 180) / 2;
        quadW = sin(a1) * sin(a2) * sin(a3) + cos(a1) * cos(a2) * cos(a3);
        quadX = -sin(a1) * sin(a2) * cos(a3) + sin(a3) * cos(a1) * cos(a2);
        quadY = sin(a1) * sin(a3) * cos(a2) + sin(a2) * cos(a1) * cos(a3);
        quadZ = sin(a1) * cos(a2) * cos(a3) - sin(a2) * sin(a3) * cos(a1);
        break;

    default:

        break;
    }
    std::string split = ",";
    std::string quadresult = std::to_string(x) + split + std::to_string(y) + split +
                             std::to_string(z) + split + std::to_string(quadW) + split +
                             std::to_string(quadX) + split + std::to_string(quadY) + split +
                             std::to_string(quadZ);
    std::string eulerresult = std::to_string(x) + split + std::to_string(y) + split +
                              std::to_string(z) + split + std::to_string(R1) + split +
                              std::to_string(R2) + split + std::to_string(R3);
    std::cout << "\nThe entered pose is: \n" << eulerresult << std::endl;
    std::cout << "The converted pose (Euler angles --> quaternions) is: \n"
              << quadresult << std::endl;
    return mmind::eye::HandEyeCalibration::Transformation(x, y, z, quadW, quadX, quadY, quadZ);
}

// Convert the obtained keyboard input to the corresponding operation.
CommandType enterCommand()
{
    std::cout << "\nEnter the letter that represents the action you want to perform." << std::endl;
    std::cout << "P: obtain the original 2D image" << std::endl;
    std::cout << "T: obtain the 2D image with feature recognition result" << std::endl;
    std::cout << "A: enter the current robot pose" << std::endl;
    std::cout << "C: calculate extrinsic parameters" << std::endl;
    const auto command = getInputCommand();
    if (command == "P" || command == "p") {
        return CommandType::GetOriginImg;
    }
    if (command == "T" || command == "t") {
        return CommandType::GetPatternImg;
    }
    if (command == "A" || command == "a") {
        return CommandType::AddPose;
    }
    if (command == "C" || command == "c") {
        return CommandType::Calibrate;
    }
    return CommandType::Unknown;
}

// Set the Euler angle convention of the robot.
int getEulerType()
{
    std::cout << "\nEnter the number that represents the Euler angle convention of your robot."
              << std::endl;
    std::cout << "1: Z-Y'-X'' (intrinsic rotations) : the intrinsic rotations are known as: yaw, "
                 "pitch and roll"
              << std::endl;
    std::cout << "2: Z-Y'-Z''/OAT (intrinsic rotations) " << std::endl;
    std::cout << "3: X-Y'-Z''(intrinsic rotations) " << std::endl;
    std::cout << "4: Z-X'-Z'' (intrinsic rotations) " << std::endl;
    std::cout << "5: X-Y-Z/WPR (extrinsic rotations) " << std::endl;

    int eulerTypeCode = getInputNumber<int>();
    switch (eulerTypeCode) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        return eulerTypeCode;
    default:
        return 0;
    }
    return eulerTypeCode;
}

// Set the camera mounting method.
bool inputCalibType(mmind::eye::HandEyeCalibration::CameraMountingMode& mountingMode)
{
    std::cout << "\nEnter the number that represents the camera mounting method." << std::endl;
    std::cout << "1: eye-in-hand" << std::endl;
    std::cout << "2: eye-to-hand" << std::endl;
    switch (getInputNumber<int>()) {
    case 1:
        mountingMode = mmind::eye::HandEyeCalibration::CameraMountingMode::EyeInHand;
        break;
    case 2:
        mountingMode = mmind::eye::HandEyeCalibration::CameraMountingMode::EyeToHand;
        break;
    default:
        std::cout << "Unknown calibrateType, please enter correct calibrateType number."
                  << std::endl;
        return false;
    }
    return true;
}

// Set the model of the calibration board.
bool inputBoardType(mmind::eye::HandEyeCalibration::CalibrationBoardModel& boardModel)
{
    std::cout << "\nEnter the number that represent the model of your calibration board (the model "
                 "is labeled on the calibration board)."
              << std::endl;
    std::cout << "1: BDB-5\n2: BDB-6\n3: BDB-7" << std::endl;
    std::cout << "4: CGB-020\n5: CGB-035\n6: CGB-050" << std::endl;
    std::cout << "7: OCB-005\n8: OCB-010\n9: OCB-015\n10: OCB-020" << std::endl;
    switch (getInputNumber<int>()) {
    case 1:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::BDB_5;
        break;
    case 2:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::BDB_6;
        break;
    case 3:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::BDB_7;
        break;
    case 4:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::CGB_20;
        break;
    case 5:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::CGB_35;
        break;
    case 6:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::CGB_50;
        break;
    case 7:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::OCB_5;
        break;
    case 8:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::OCB_10;
        break;
    case 9:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::OCB_15;
        break;
    case 10:
        boardModel = mmind::eye::HandEyeCalibration::CalibrationBoardModel::OCB_20;
        break;
    default:
        std::cout << "Unknown boardType, please enter correct boardType number." << std::endl;
        return false;
    }
    return true;
}

// Input the current robot pose. The unit of the translational components is mm, and the
// unit of the Euler angles is degrees.
mmind::eye::HandEyeCalibration::Transformation enterRobotPose(int eulerType)
{
    std::cout << "\nEnter the X translational component of the robot pose (in mm): " << std::endl;
    double poseX = getInputNumber<double>();
    std::cout << "\nEnter the Y translational component of the robot pose (in mm): " << std::endl;
    double poseY = getInputNumber<double>();
    std::cout << "\nEnter the Z translational component of the robot pose (in mm): " << std::endl;
    double poseZ = getInputNumber<double>();
    double poseR1 = 0;
    double poseR2 = 0;
    double poseR3 = 0;
    switch (eulerType) {
    case 1: // Prompt for Z-Y'-X'' Euler angles
        std::cout << "\nEnter the Z rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR1 = getInputNumber<double>();
        std::cout << "\nEnter the Y' rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR2 = getInputNumber<double>();
        std::cout << "\nEnter the X'' rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR3 = getInputNumber<double>();
        break;
    case 2: // Prompts for Z-Y'-Z'' (OAT) Euler angles
        std::cout << "\nEnter the Z(O) rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR1 = getInputNumber<double>();
        std::cout << "\nEnter the Y'(A) rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR2 = getInputNumber<double>();
        std::cout << "\nEnter the Z''(T) rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR3 = getInputNumber<double>();
        break;
    case 3: // Prompts for X-Y'-Z'' Euler angles
        std::cout << "\nEnter the X rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR1 = getInputNumber<double>();
        std::cout << "\nEnter the Y' rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR2 = getInputNumber<double>();
        std::cout << "\nEnter the Z'' rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR3 = getInputNumber<double>();
        break;
    case 4: // Prompts for Z-X'-Z'' Euler angles
        std::cout << "\nEnter the Z rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR1 = getInputNumber<double>();
        std::cout << "\nEnter the X' rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR2 = getInputNumber<double>();
        std::cout << "\nEnter the Z'' rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR3 = getInputNumber<double>();
        break;
    case 5: // Prompts for X-Y-Z (WPR) Euler angles
        std::cout << "\nEnter the X rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR1 = getInputNumber<double>();
        std::cout << "\nEnter the Y rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR2 = getInputNumber<double>();
        std::cout << "\nEnter the Z rotational component of the robot pose (in degrees): "
                  << std::endl;
        poseR3 = getInputNumber<double>();
        break;
    }
    if (std::cin.rdbuf()->in_avail() != 0) {
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    return eulerToquad(eulerType, poseX, poseY, poseZ, poseR1, poseR2, poseR3);
}

// Save extrinsic parameters to a TXT file named "ExtrinsicParameters (+time stamp)".
void saveExtrinsicParameters(std::string ExtrinsicParameters)
{
    char pStrPath1[1024];
    time_t currTime;
    struct tm* mt;
    currTime = time(NULL);
    mt = localtime(&currTime);
    sprintf(pStrPath1, "ExtrinsicParameters%d%02d%02d%02d%02d%02d.txt", mt->tm_year + 1900,
            mt->tm_mon + 1, mt->tm_mday, mt->tm_hour, mt->tm_min, mt->tm_sec);
    std::ofstream out(pStrPath1);
    out << "ExtrinsicParameters:" << std::endl;
    out << ExtrinsicParameters;
    out.close();
    std::cout << "Save result in file " << pStrPath1 << std::endl;
}
} // namespace
