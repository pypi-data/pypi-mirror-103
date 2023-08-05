from distutils.core import setup
setup(
  name = 'risk_manage',         # How you named your package folder (MyLib)
  packages = ['risk_manage'],   # Chose the same as "name"
  version = '1.0.10',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'test version ',   # Give a short description about your library
  author = 'Hao-Chen, Chiu',                   # Type in your name
  author_email = 'pro.imoney@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/william1209/Risk_Manage.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/william1209/Risk_Manage/archive/refs/tags/1.0.10.tar.gz',    # I explain this later o
  keywords = ['Quants', 'ML', 'DL'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'datetime',
          'numpy',
          'pandas_datareader',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)