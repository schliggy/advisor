#!/usr/bin/env python

import json

from advisor_client.model import Study
from advisor_client.model import Trial
from advisor_client.model import TrialMetric
from advisor_client.client import AdvisorClient

client = AdvisorClient()

# Create Study
name = "new_Study2"
maxTrials = 20
study_configuration = {
    #"goal":
    # "MAXIMIZE",
    "goal":
    "MINIMIZE",
    "maxTrials":
    maxTrials,
    "maxParallelTrials":
    1,
    "randomInitTrials":
    10,
    "params": [{
        "parameterName": "x",
        "type": "DOUBLE",
        "minValue": -10,
        "maxValue": 10,
        "scallingType": "LINEAR"
    }]
}

algorithm = "RandomSearch"
#algorithm = "BayesianOptimization"
#algorithm = "TPE"
#algorithm = "SimulateAnneal"
#algorithm = "QuasiRandomSearch"
#algorithm = "ChocolateRandomSearch"
#algorithm = "ChocolateBayes"
#algorithm = "CMAES"
#algorithm = "MOCMAES"


# falls die study bereits exisitert, wird die ID zurückgegeben?
study = client.get_or_create_study(name, study_configuration, algorithm=algorithm)
print(study)



for i in range(20):
  # erstelle trial aus der oben angegebenen study
  trial = client.get_suggestions(study.name, 1)[0]

  # die parameter Werte der zurückgegebene trial werde in ein dict geladen
  parameter_value_dict = json.loads(trial.parameter_values)
  
  # hier werden dann die parameter für die Funktion gesetzt
  x = parameter_value_dict['x']
  
  # Evaluation der Funktion bzw. Berechnung der Metriken..
  metric = x * x - 3 * x + 2
  #metric = -(x * x - 3 * x + 2)
  
  # die Ergebnisse der Trial werden wieder zurück an den Server geschickt
  trial = client.complete_trial_with_one_metric(trial, metric)
  print(trial)

# hier wird die Study von Pending auf completed gesetzt
is_done = client.is_study_done(study.name)

# Rückgabe der besten Trial
best_trial = client.get_best_trial(study.name)

print("Best trial: {}".format(best_trial))
