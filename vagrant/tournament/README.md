# P2: Tournament Results

This is a submission for the project P2 - Tournament Results as part of the Udacity fullstack-web-developer ND.

Running the solution
--------------------

Assumption: The solution (tournament.sql, tournament.py, tournament_test.py) are all available in a Vagrant VM instance at '/vagrant/tournament'.

1. Run the psql command in a terminal on the Vagrant VM instance to bring up the PostgreSQL command prompt.
```shell
$ psql
```

2. (Re-)create the DB schema using the updated solution file - tournament.sql
```shell
vagrant=> \i tournament.sql
```

3. Exit the psql prompt
```shell
vagrant=> \q
```

4. Run the unit test python file tournament_test.py 
```shell
$ ./tournament_test.py
```

All tests should pass.

