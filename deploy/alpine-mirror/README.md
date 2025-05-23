# How to Use

- Adjust `synchroniser/crontab` for desired schedule of synchronising
- Adjust `synchroniser/mirror.sh` for which repos to exclude, etc.
- The container image must be re-built when `crontab` or `mirror.sh` are changed
- Run by `<podman|docker> compose up`

# Notes

- [Alpine Wiki - How to setup a Mirror](https://wiki.alpinelinux.org/wiki/How_to_setup_a_Alpine_Linux_mirror)
- You can trigger the syncs manually via
  - `<podman|docker> exec -it alpine-mirror-sync /app/mirror.sh`
