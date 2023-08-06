[![coverage report](https://gitlab.com/Guenole.cherot/admm/badges/master/coverage.svg)](https://gitlab.com/Guenole.cherot/admm/commits/master)

# A Real-Time Congestion Control Strategy in Distribution Network

## Abstract
This paper proposes an algorithm for real-time congestion management in a distribution network. It sets up a peer-to-peer market allowing the distribution system operator to inject network charges. This enables him to obtain flexibility from distributed agents with heterogeneous preferences.
These network charges vary in real time and are related to the network's congestion. Prosumers minimize their cost function, and find a consensus through ADMM decomposition. 
This formulation allows the management of the large number of agents present in the distribution networks only using one price broadcast by the DSO to prosumers.
We demonstrate with the CIGRE low voltage test case that this strategy is efficient to manage congestion and presents limited sub-optimality compared to the OPF.

## Warning
Data presented in the paper ([Pecan Street dataport](https://www.pecanstreet.org/dataport/)) is not sharable.
Examples and figures are therefore based on a different data set. This does not change our conclusions.

## Paper
Paper submited to ISGT 2021. Not yet available online.

## Instal

Instal using :
`pip install RT-Congestion-Control`

## Contact
- Corresponding author : Guénolé CHEROT
- e-mail : guenole.cherot@ens-rennes.fr

## Futur improvements
- [ ] New test case
- [ ] New grid cost trategies
- [ ] New types of grid cost
  - [ ] Voltage limits
  - [ ] Unbalanced network
  - [ ] Encourage producers and consumers in a different way
- [ ] Fair redistribution of profit