# PGAcloud_Fitness_Agent
Bachelor's Thesis on deploying Parallel Genetic Algorithms (PGAs) in the cloud.
This specific repository contains the **cloud fitness container**,
the agent which invokes the genetic operator *cloud fitness evaluation*.

The genetic operator *Fitness* evaluates individuals fitness value,
and usually passes them on to the *Runner* container for survival selection at the end of a generation.

This genetic operator - contrary to other repositories belonging to the PGAcloud project - is implemented in Java.
Having selected a different programming language helps demonstrating the possibility of including *external code*
(after the concept of "bring-your-own-code").

## License
*PGAcloud_Fitness_Agent* is licensed under the terms of the [MIT License](https://opensource.org/licenses/MIT).
Please see the [LICENSE](LICENSE.md) file for full details.
