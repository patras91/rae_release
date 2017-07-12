RAE is working with multiple stacks. Each stack is implemented a Python thread.
Some issues to be resolved:
    1. Sharing the state variables globally instead of always passing them as a parameter to the tasks and commands
    2. Review in the code which portions are critical sections and which are not. Match this with the pseudocode
    3. Handle incoming sequence of tasks as another thread instead of assuming a predefined list of tasks

We have the following domains

1. domain_simpleFetch: Robot collecting objects in a harbour
   --- developed and integrated with RAE
2. domain_simpleOpenDoor: Robot opening a door
   --- developed: fine tuning needed, not integrated with RAE
3. domain_ste: Robot travelling from one location to another by foot or taxi
   --- developed and integrated with RAE
4. domain_chargeableRobot: A chargeable robot collecting different objects
   --- developed and integrated with RAE: with some bugs
5. domain_springDoor: Robot needs to collect objects in an environment with spring doors
   --- developed but not integrated with RAE

