#
#   This file is part of do-mpc
#
#   do-mpc: An environment for the easy, modular and efficient implementation of
#        robust nonlinear model predictive control
#
#   Copyright (c) 2014-2019 Sergio Lucia, Alexandru Tatulea-Codrean
#                        TU Dortmund. All rights reserved
#
#   do-mpc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as
#   published by the Free Software Foundation, either version 3
#   of the License, or (at your option) any later version.
#
#   do-mpc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with do-mpc.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from casadi import *
from casadi.tools import *
import pdb
import sys
import os
rel_do_mpc_path = os.path.join('..','..')
sys.path.append(rel_do_mpc_path)
import do_mpc


def template_mpc(model, silence_solver = False):
    """
    --------------------------------------------------------------------------
    template_mpc: tuning parameters
    --------------------------------------------------------------------------
    """
    mpc = do_mpc.controller.MPC(model)

    mpc.settings.n_horizon =  20
    mpc.settings.n_robust =  0
    mpc.settings.open_loop =  0
    mpc.settings.t_step =  1.0
    mpc.settings.state_discretization =  'collocation'
    mpc.settings.collocation_type =  'radau'
    mpc.settings.collocation_deg =  2
    mpc.settings.collocation_ni =  2
    mpc.settings.store_full_solution =  True

    if silence_solver:
        mpc.settings.supress_ipopt_output()


    mterm = model.x['tau']
    lterm = -model.x['x4']

    mpc.set_objective(mterm=mterm, lterm=lterm)
    mpc.set_rterm(tau=1.0)


    mpc.bounds['lower', '_x', 'x1'] = -1.5
    mpc.bounds['lower', '_x', 'x2'] = 1.5
    #mpc.bounds['lower', '_x', 'x3'] = 0.0
    #mpc.bounds['lower', '_x', 'x4'] = 0.0

    mpc.bounds['upper', '_x','x1'] = 1.5
    mpc.bounds['upper', '_x','x2'] = 1.5

    mpc.bounds['lower','_u','tau'] = -5
    mpc.bounds['upper','_u','tau'] = 5

    a_var = np.array([0.5, 0.2, 1])
    b_var= np.array([0.5, 0.2, 1])

    mpc.set_uncertainty_values(a = a_var, b = b_var)
 

    mpc.setup()

    return mpc
