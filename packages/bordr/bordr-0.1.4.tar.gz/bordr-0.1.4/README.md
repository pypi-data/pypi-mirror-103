## bordr ##

A pip installable version of RDRPOSTagger with Tibetan-specific changes.

 - See the original [RDRPOSTagger](https://github.com/datquocnguyen/RDRPOSTagger) for documentation.
 - Check the [modifications](https://github.com/Esukhia/bordr/blob/master/CHANGELOG.md) implemented in this repo.
 - See [rdr-data](https://github.com/Esukhia/rdr-data) for RDR models for Tibetan.
 - See [usage.py](https://github.com/Esukhia/bordr/blob/master/usage.py) for the programmatic interface available in bordr

### Maintenance

Build the source dist:

```bash
rm -rf dist/
python3 setup.py clean sdist
```

and upload on twine (version >= `1.11.0`) with:

```bash
twine upload dist/*
```

### Latest change
The SDICT content passed to generate INIT file is changed.
The words in SDICT are given U(Unique tag from bilou tagging system) tag as those words are segmented as Unique token by botok.
With that changed SDICT content, we will get INIT file based on botok segmentation. Hence rules generated will be able to resolve botok segmentation ambiguity.