from setuptools import setup, find_packages
setup(
    name="lum_bam_foo",
    version="1.0",
    py_modules=['lum_bam_foo'],
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['click', 'parsimonious', 'pytest'],
    entry_points='''
        [console_scripts]
        lum_bam_foo=lum_bam_foo:cli
    ''',
)
