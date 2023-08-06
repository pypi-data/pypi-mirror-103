import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
from walpy import suppress

def r_importer(modules, install_only=None, log=False):
  """
  Import and install R packages. If the desired packages are not installed it will
  automatically install them. Note that this function will act as a one time
  delay in running time, if modules need to be installed. Import R packages
  manually as e.g. <stargazer =  rpy2.robjects.packages.importr('stargazer')>.
  So, the same name used for installing, should be used to import the functions.
  Important to note, this function imports the following modules from rpy2:
  "rpy2.robjects.packages" and "rpy2.robjects.vectors".
 
  Args:
      modules: list of the desired packages. The packages to be included should
      be as a string. E.g. modules = ['stargazer', 'tidyverse'].
 
      install_only: default=None. list or string of packages to be installed 
      only. Note, combinations are possible.
 
      log: default=False. Prints a log message if true, of the packages that are
      (succesfully) installed.
 
  Returns:
      None
  """
  # import R's utility package:
  utils = rpackages.importr('utils')
 
  # R package names:
  packnames = tuple(modules)
 
  # Selectively install what needs to be install. Use CRAN cloud server:
  names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
  if len(names_to_install) > 0 and log == True:
    utils.install_packages(StrVector(names_to_install),
                            repos='https://cloud.r-project.org/')
    print('Successfully installed:', names_to_install)
  
  elif len(names_to_install) > 0:
    with suppress():
      utils.install_packages(StrVector(names_to_install),
                             repos='https://cloud.r-project.org/')
  
  # Make modules non-overlapping with install_only:
  modules = set(modules) - set(install_only)
 
  # Import modules to be automatically imported
  for module in modules:
    rpackages.importr(module)
  
  # Print log message if true:
  if log == True:
    print('Successfully imported:', [i for i in modules])
 
  return