Results schemas are used to capture experimental and assay data in lab notebooks ([reference](https://help.benchling.com/hc/en-us/articles/9684211058957-Creating-Result-schemas-and-tables)). One of the main properties of results schemas is that once there is data stored within a results schema, the schema fields cannot be modified. This makes it much less frequent to need to update results schemas over time. Because of this, it is possible to just create a "one way street" from Benchling to your codebase, as supposed to the "two way street" in the case of entity schemas and its migration pattern.

Liminal's current pattern for results schema synchronization is described below.

1. Create and edit results schemas in Benchling.

2. Now to synchronize with your codebase, run the following CLI command to "regenerate" the results schema files in your codebase.

    ```bash
    liminal generate-files <benchling_tenant_name> -p [<write_path>] -rs
    ```

    The `-rs` flag will write only the results schema files to the given write path.

    Running the same command with the `-o` flag will overwrite the existing files in the given write path.

3. Now you can use the results schema classes in your codebase!

!!! note
    As of v4.0.0 release, Liminal does not support the ability to detect changes to results schemas and run migrations to synchronize what is defined in code to what is defined in Benchling. Reach out if this would be a valuable feature for you in order to upgrade its priority in a future release!
