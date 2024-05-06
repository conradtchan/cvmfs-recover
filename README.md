# cvmfs-recover

Example usage:

Generate a list of missing/corrupted chunks and catalogs:
```
cvmfs_server check cms.cern.ch > cms.cern.ch.out 2> cms.cern.ch.err
```

Place the `.err` file in the same directory as the script and run
```
./cvmfs-recover.py --repo_name cms.cern.ch --server_name oasis-replica.opensciencegrid.org:8002
```

The script will look for the `.err` file matching the repo name and download the missing files from the specified server.
