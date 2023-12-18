#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>

# include "Aria/Aria.h"

class ariaNode : public rclcpp::Node {
    public:
        ariaNode(int argc, char** argv) : Node("Aria_node") {
            Aria::init();
            ArArgumentParser parser(&argc, argv);
            parser.loadDefaultArguments();
            robot = new ArRobot();
            cmdVelSub = create_subscription<geometry_msgs::msg::Twist> (
                "cmd_vel", 10, std::bind(&ariaNode::cmdVelCallback, this, std::placeholders::_1)
            );

            ArRobotConnector robotConnector(&parser, robot);
            if(!robotConnector.connectRobot()) {
                ArLog::log(ArLog::Terse, "simpleConnect: Could not connect to the robot.");
                if(parser.checkHelpAndWarnUnparsed()) {
                    // -help not given
                    Aria::logOptions();
                    Aria::exit(1);
                }
            }

            robot->enableMotors();

            
        }

        ~ariaNode() {
            Aria::exit();
            if (robot != nullptr) {
                delete robot;
            }
        }

        void run() {
            robot->runAsync(true);
            rclcpp::spin(shared_from_this());
            robot->stopRunning();
        }

    private:
        void cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg) {
            double linearSpeed = msg->linear.x;
            double angularSpeed = msg->angular.z;

            double forwardSpeed = linearSpeed;
            double rotationSpeed = angularSpeed;

            robot->lock();
            robot->setVel(forwardSpeed);
            robot->setRotVel(rotationSpeed);
            robot->unlock();
        }

        ArRobot* robot;
        rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmdVelSub;
    
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto aNode = std::make_shared<ariaNode>(argc, argv);
    aNode->run();
    rclcpp::shutdown();
    return 0;
}