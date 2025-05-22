# How to Use

- Adjust ./synchroniser/crontab for desired schedule of synchronising
- Adjust ./synchroniser/mirror.sh for which repos to exclude, etc.
- Image has to be re-built whenever crontab or mirror.sh are changed
- Run by `podman compose up` or `docker compose up`