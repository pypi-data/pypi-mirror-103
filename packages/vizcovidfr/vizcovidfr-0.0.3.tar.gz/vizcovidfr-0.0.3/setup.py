
from setuptools import setup, find_packages

setup(
  name='vizcovidfr',
  version='0.0.3',
  description='A python package to visualize spatial evolution of Covid19 cases in France',
  url='https://github.com/AmelieVernay/vizcovidfr',
  author='Foux Quentin ; Llinares Laurent ; Nicolas Alexandre ; Vernay Amelie',
  author_email='quentin.foux@etu.umontpellier.fr, laurent.llinares@etu.umontpellier.fr, alexandre.nicolas@etu.umontpellier.fr, amelie.vernay@etu.umontpellier.fr',
  license='MIT',
  zip_safe=False,
  packages=find_packages(include=['vizcovidfr',
                                  'vizcovidfr.loads',
                                  'vizcovidfr.preprocesses',
                                  'vizcovidfr.tests',
                                  'vizcovidfr.barplots',
                                  'vizcovidfr.regression',
                                  'vizcovidfr.prediction',
                                  'vizcovidfr.heatmaps',
                                  'vizcovidfr.line_charts',
                                  'vizcovidfr.pie_charts',
                                  'vizcovidfr.maps',
                                  'vizcovidfr.sparse'])
)
