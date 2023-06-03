import nest

def create_model(amplitude=-180):
  nest.ResetKernel()

  # Set simulation kernel
  nest.SetKernelStatus({
    "local_num_threads": 1,
    "resolution": 0.1,
    "rng_seed": 1
  })

  # Create nodes 

  # excitatory
  n1 = nest.Create("iaf_psc_alpha", 300, params={
    "C_m": 30,
    "E_L": -70,
    "V_reset": -70,
    "V_th": -60,
    "t_ref": 2,
    "tau_m": 20,
    "tau_syn_ex": 1,
    "tau_syn_in": 10,
  })

  # inhibitory
  n2 = nest.Create("iaf_psc_alpha", 500, params={
    "C_m": 30,
    "E_L": -70,
    "V_reset": -70,
    "V_th": -60,
    "t_ref": 2,
    "tau_m": 20,
    "tau_syn_ex": 1,
    "tau_syn_in": 10,
  })
  pg1 = nest.Create("poisson_generator", 1, params={
    "rate": 800,
    "start": 0,
    "stop": 2100,
  })
  vm1 = nest.Create("voltmeter", 1, params={
    "interval": 1,
    "start": 0,
    "stop": 2100,
  })

  # excitatory
  sr1 = nest.Create("spike_recorder", 1, params={
      "start": 0,
      "stop": 2100,
  }) 

  # inhibitory
  sr2 = nest.Create("spike_recorder", 1, params={
    "start": 0,
    "stop": 2100,
  })
  pg2 = nest.Create("poisson_generator", 1, params={
    "rate": 800,
    "start": 700,
    "stop": 2100,
  })

  dc1 = nest.Create("dc_generator", 1, params={
    "amplitude": amplitude,
    "start": 1400,
    "stop": 2100,
  })

  # Connect nodes
  nest.Connect(n1, n2, conn_spec={
    "rule": "fixed_indegree",
    "indegree": 50,
  }, syn_spec={ 
    "weight": 30,
    "delay": 5,
  })
  nest.Connect(n2, n1, conn_spec={
    "rule": "fixed_indegree",
    "indegree": 30,
  }, syn_spec={ 
    "weight": -15,
    "delay": 5,
  })
  nest.Connect(n1, n1, conn_spec={
    "rule": "fixed_indegree",
    "indegree": 50,
  }, syn_spec={ 
    "weight": 50,
    "delay": 2,
  })
  nest.Connect(n2, n2, conn_spec={
    "rule": "fixed_indegree",
    "indegree": 30,
  }, syn_spec={ 
    "weight": -5,
    "delay": 2,
  })
  nest.Connect(vm1, n1)
  nest.Connect(n1, sr1)
  nest.Connect(n2, sr2)
  nest.Connect(vm1, n2)
  nest.Connect(pg1, n1, syn_spec={ 
    "weight": 65,
  })
  nest.Connect(pg1, n2, syn_spec={ 
    "weight": 40,
  })
  nest.Connect(pg2, n2, syn_spec={ 
    "weight": -5,
  })
  nest.Connect(dc1, n1)

  # Run simulation
  nest.Simulate(2100)

  response = {
    "events": [vm1.events, sr1.events, sr2.events]
  }

  return response