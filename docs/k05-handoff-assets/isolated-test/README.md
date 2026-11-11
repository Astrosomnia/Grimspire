# Local K05 comparison

This local-only playable comparison uses a game snapshot with the merged 2× renderer patch. It is not the exact hosted game revision. It uses fixed seed 151133, forces K05 instead of the other K05 variants, and biases generation toward bridge runs. Lighting and effects remain animated. Match viewport and camera when comparing.

After cloning or downloading this branch, from this directory run:

```sh
python3 build.py ../K05-hand-texture-study-v2.forge.json
python3 -m http.server 8765 --bind 127.0.0.1
```

Open [draft](http://127.0.0.1:8765/k05-isolated.html?bridge=draft#grounds&drowned) or [original](http://127.0.0.1:8765/k05-isolated.html?bridge=original#grounds&drowned) in your browser. These links require the server above; GitHub does not host the playable test. If you omit the build argument it uses the earlier `K05-relief-draft.forge.json`. The builder writes only a generated local test HTML and never changes Forge or the shared game.
