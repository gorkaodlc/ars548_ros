from setuptools import setup

package_name = 'ars548_driver_py'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='maintainer',
    maintainer_email='example@example.com',
    description='Python driver for the ARS548 radar.',
    license='BSD-3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ars548_driver_py = ars548_driver_py.driver_node:main'
        ],
    },
)
