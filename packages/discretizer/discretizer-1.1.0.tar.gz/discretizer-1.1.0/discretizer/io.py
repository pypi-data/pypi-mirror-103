# This file is part of Discretizer.
#
# Copyright (c) 2017 Jan Plhak
# https://github.com/loschmidt/discretizer
#
# Discretizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Discretizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Discretizer.  If not, see <https://www.gnu.org/licenses/>.

import logging
import numpy as np

from discretizer.tunnel import Sphere, Tunnel


def load_tunnel_from_pdb(path: str) -> Tunnel:
    spheres = []
    with open(path) as file:
        for line in file:
            words = line.split()
            if words and words[0] == "ATOM":
                center = np.array([float(w) for w in words[6:9]])
                radius = float(words[9])
                spheres.append(Sphere(center, radius))

        logging.info("Tunnel loaded (%d spheres).", len(spheres))
    return Tunnel(spheres)