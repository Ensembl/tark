We need to display matches from GRCh37 showing equivalence in 5' UTR, 3' UTR and CDS in relation to MANE Select and 
MANE Plus Clinical transcripts on GRCh38. Refer dev page: http://dev-tark.ensembl.org/web/mane_GRCh37_list/.
The script `utr_cds_to_json.py` will query the Tark DB for this information and dump it in a static file that we then 
load into the website.

Run these commands to populate the static file:

```
cd /homes/ens_tarkdev01/workspace/
source src/tark_env_376/bin/activate

cd src/tark/tark
PYTHONPATH='.' python scripts/utr_cds_to_json.py
```

By default, this will load MySQL connection config from the `settings.py` file and put the results in the location 
`<project root>/tark/tark/static/apache/txt/mane_grch37.txt`.  You can override either the MySQL config or the output 
location with CLI arguments, run `PYTHONPATH='.' python scripts/utr_cds_to_json.py --help` for details.

The Apache server should automatically pick up the change.  If it does not then restart the server.