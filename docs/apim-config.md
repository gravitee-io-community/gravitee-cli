# gio apim config

Configuration values are stored in file with structure of INI file. The config file is located `~/graviteeio`.

Each section contains the configuration by environment for each module. Environment can mean staging, production...

Default environment: `demo`. The configuration of demo environment point to `https://demo.gravitee.io/`

Environment Variable:

* `GRAVITEEIO_CONF_FILE`: The file of CLI conf. Default `~/graviteeio`.

## Commands

	$ gio apim config get
    $ gio apim config load
    $ gio apim config set


* get: This command prints current configuration values loaded
* load: This command load current environment
* set: This command writes configuration values according to environment


<!-- <table>
    <thead>
        <tr>
            <th colspan="2">
                <h3><a href="#option-global" id="option-global">--help</a></h3>
            </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Description</th>
            <td>
                <div><p>Use global CLI config</p>
                </div>
            </td>
        </tr>
    </tbody>
</table> -->
