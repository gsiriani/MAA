# -*- coding: UTF-8 -*-

from learn import Learner, Representacion

learner = Learner(Representacion(),0.1)
learner.run(200)