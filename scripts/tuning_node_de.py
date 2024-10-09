#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from pid_tuning.evolutive_algorithms.dif_evolution import DifferentialEvolution
from pid_tuning.settings.control_gazebo import ControlGazebo

class TuningDE(Node):
    def __init__(self):
        super().__init__("tuning_de_node")
        
        self.A = 3
        self.m = 9
        self.N = 10
        self.Gm = 10000
        self.F = 0.65
        self.C = 0.85
        self.hz = 25
        self.reset_control = ControlGazebo()

        self.de = DifferentialEvolution(self.N, self.m, self.Gm, self.F, self.C, self.A, '/home/arne/jazzy_ws/src/scara_robot_description/config/paths.json', epsilon_1=1, tm=28800)
        self.X = self.de.gen_population()

        self.timer = self.create_timer(1.0/self.hz, self.timer_callback)

    def timer_callback(self):
        try:
            self.get_logger().warn("Läuft!")
            file = open("best_pid_values_DE.txt", 'w')
            self.de.evaluate(self.X, self.reset_control, self.hz)
            X_best = self.de.dif_evolution(self.X, self.reset_control, self.hz)
            file.write(str(X_best))
            file.close()
        except Exception as e:
            self.get_logger().warn(f"Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = TuningDE()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()