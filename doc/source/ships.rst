:mod:`sidereal.ships` --- Ship classes
======================================

.. module:: sidereal.ships
   :synopsis: Ship classes.

.. versionadded:: 0.0.0

The :mod:`ships` module contains classes that define ingame ship object,
from the perspective of both server and client.

This includes a ship's unique ID (from the :mod:`sidereal.universe`) module,
and its own logger for debugging.

Ships statistics including engine, weapon placement, weight, and other
such statistics, should be imported from ship data files, possibly in JSON.

.. _sidereal.ships.Ship:

:class:`Ship` Objects
---------------------

.. class:: Ship([universe])

  *universe*, if provided, must be a Universe instance.

  If not provided, the Ship will use the default instance provided by
  the :mod:`sidereal.universe` module.
