# mljboard-client (HOS)

A client for my [mljboard](https://github.com/duckfromdiscord/mljboard) project. Put a `config.json` alongside your `main.py` before running it.

## config

| key | value |
|---|---|
| local_server | The url (minus http:// or https://) to your Maloja client |
| local_port | The port Maloja is running on |
| local_https | True/false whether you're using https |
| remote_server | The HOS server |
| remote_path | Keep as `/ws` for now. This is the path on the remote server that the websocket is on |
| remote_port | The port of the HOS server |
| remote_https | True/false whether to use `wss` for the remote HOS server |
| remote_pairing_code | The code your Maloja client will be identified with to the HOS server |
