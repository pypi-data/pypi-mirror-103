from IPython.core.magic import register_cell_magic
from IPython import get_ipython
@register_cell_magic
def write_run(line, cell):
    """
    Write and run the cell. Use as follows: 
    
    %%write_and_run script.py to overwrite existing scripts.
    
    %%write_and_run -a script.py to append to the existing script.
    
    For both cases, if the script does not exist, then a new one is 
    created automatically.
 
    Args:
        line: ignore. See above.
 
        cell: ignore. See above.
 
    Returns:
        None
    """
    argz = line.split()
    file = argz[-1]
    mode = 'w'
    if len(argz) == 2 and argz[0] == '-a':
        mode = 'a'
    with open(file, mode) as f:
        f.write(cell)
    get_ipython().run_cell(cell)
 
    return