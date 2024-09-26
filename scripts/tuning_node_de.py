#!/usr/bin/env python3

import rclpy

from pid_tuning.evolutive_algorithms.dif_evolution import DifferentialEvolution
from pid_tuning.settings.control_gazebo import ControlGazebo

reset_control = ControlGazebo()

A = 3
m = 9
N = 10
Gm = 10000
F = 0.65
C = 0.85
hz = 25

de = DifferentialEvolution(N, m, Gm, F, C, A, '/docker_humble_ws/src/scara_robot_description/config/paths.json', epsilon_1=1, tm=28800)
X = de.gen_population()

def evol_loop():
    rospy.init_node("tuning_node")
    file = open("best_pid_values_DE.txt", 'w')

    reset_control.init_values()
    rate = rospy.Rate(hz)
    while not rospy.is_shutdown():
        de.evaluate(X, reset_control, rate)
        X_best = de.dif_evolution(X, reset_control, rate)
        file.write(str(X_best))
        file.close()
        break


def main(args=None):
    rclpy.init(args=args)
    node =
    while rclpy.ok():
        try:
            evol_loop()
        except KeyboardInterrupt:
            pass
    rclpy.shutdown()

if __name__ == "__main__":
    main()