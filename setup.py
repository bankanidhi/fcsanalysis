from setuptools import setup

setup(name="fcsanalysis",
      version="0.0.1",
      description="FCS automatic batch analysis.",
      url="https://github.com/bankanidhi/fcsanalysis",
      entry_points={
          "console_scripts": [
              "fcsanalysis=fcsanalysis.run:run"
          ]
      },
      install_requires=["numpy==1.14.5",
                        "scipy==1.1.0",
                        "matplotlib==2.2.2",
                        "lmfit==0.9.11"],
      license="MIT",
      zip_safe=False)
