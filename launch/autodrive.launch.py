import launch
import launch.actions
import launch.substitutions
import launch_ros.actions


def generate_launch_description():
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'node_prefix',
            default_value=[launch.substitutions.EnvironmentVariable('USER'), '_'],
            description='Prefix for node names'),
        launch_ros.actions.Node(
            package='robot_car1', executable='distance', output='screen',
            name=[launch.substitutions.LaunchConfiguration('node_prefix'), 'distance']),
        launch_ros.actions.Node(
            package='robot_car1', executable='car', output='screen',
            name=[launch.substitutions.LaunchConfiguration('node_prefix'), 'car']),
    ])
