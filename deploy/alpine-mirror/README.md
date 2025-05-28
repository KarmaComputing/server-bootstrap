# How to Use

- Adjust `synchroniser/crontab` for desired schedule of synchronising
- Adjust `synchroniser/mirror.sh` for which repos to exclude, etc.
- The container image must be re-built when `crontab` or `mirror.sh` are changed
- Run by `<podman|docker> compose up`

# Notes

- [Alpine Wiki - How to setup a Mirror](https://wiki.alpinelinux.org/wiki/How_to_setup_a_Alpine_Linux_mirror)
- You can trigger the syncs manually via
  - `<podman|docker> exec -it alpine-mirror-sync /app/mirror.sh`

# How I've Tested It

1. `git clone git@github.com:KarmaComputing/server-bootstrap-ncl.git`
2. `cd server-bootstrap-ncl/deploy/alpine-mirror`
3. `sudo docker compose up`
4. `sudo docker run --rm -it --network host alpine:3.21 sh`
  - `echo -e "http://localhost/v3.21/main\nhttp://localhost/v3.21/community" > /etc/apk/repositories`
  - `apk update`
  - Feel free to install anything to test, with `apk add`
    - e.g. `apk add fastfetch` and `fastfetch`