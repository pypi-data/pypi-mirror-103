import os
import distutils.command.build_scripts
from setuptools import setup

class build_scripts(distutils.command.build_scripts.build_scripts):
    def copy_scripts(self):
        (outfiles, updated_files) = super().copy_scripts()

        # ensure scripts are installed without *.py extension
        # (looks prettier on POSIX operating systems ... although this is
        # not a good idea on Windows)
        replace = []
        for old_fn in updated_files:
            new_fn = old_fn.replace('.py', '')
            os.rename(old_fn, new_fn)
            replace.append(new_fn)
        return (outfiles, replace)


setup(
    data_files=[
        ('share/man/man1', ['shrep.1']),
    ],
    cmdclass={'build_scripts': build_scripts},
)
