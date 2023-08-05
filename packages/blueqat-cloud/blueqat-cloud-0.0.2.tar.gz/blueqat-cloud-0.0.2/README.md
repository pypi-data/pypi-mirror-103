# Blueqat cloud SDK (bqcloud)
Client SDK for Blueqat cloud.

# Handling API key
## Register API
```py
import bqcloud
api = bqcloud.register_api("Your API key here")
```

Your API key is stored to `$HOME/.bqcloud/api_key`.
If you don't want to save API key, use insteads following codes.

```py
import bqcloud
api = bqcloud.api.Api("Your API key here")
```

## Load API
Once API key is saved, the key can be loaded from file.

```py
import bqcloud
api = bqcloud.load_api()
```

# Annealing
```py
import bqcloud
api = bqcloud.load_api()
api.annealing([[-1, 0], [0, 0.5]], 5, 10)
```
