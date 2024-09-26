#! /usr/bin/env python3

import rclpy

from pid_tuning.settings.control_gazebo import ControlGazebo
from pid_tuning.evolutive_algorithms.evolutive_algorithms import HarmonySearch

# objeto para reiniciar la simulacion
reset_control = ControlGazebo()

A = 3
m = 9
N = 10
Gm = 10000
r_accept = 0.7
r_pa = 0.45
hz = 25

hs = HarmonySearch(N, m, Gm, A, r_accept, r_pa, '/docker_humble_ws/src/scara_robot_description/config/paths.json', epsilon_1=1, tm = 28800)
X = hs.gen_population()

def evol_loop():
    rospy.init_node("tuning_node")
    file = open("best_pid_values_HS.txt", 'w')

    reset_control.init_values()
    rate = rospy.Rate(hz)
    while not rospy.is_shutdown():
        hs.evaluate(X, reset_control, rate)
        X_best = hs.harmony_search(X, reset_control, rate)  
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