from distutils.core import setup

files = ["util/*","pipelines/*","config","usage"]

setup(name = "vertex_pipeline",
      version = "1.0",
      description = "commands to use and manipulate vertex pipelines",
      author = "kand",
      author_email = "akos123@gmail.com",
      url = "https://github.com/kand/aws_pipeline.git",
      packages = ["pipeline"],
      package_data = {"pipeline":files},
      scripts = ["vertex_pipeline"],
      long_description = '''commands to use and manipulate vertex pipelines''',
      #classifiers = []
      )