# DNS ping
for i in $dns1 $dns2; do
        ebegin "Awaiting accessible DNS at $i"
        while ! ping -c 1 -w 1 -q "$i" > /dev/null 2>&1; do
                sleep 1
        done
        eend $?

        echo "nameserver $i" >> /etc/resolv.conf
done

# Alpine mirror ping
if [[ -n "$ALPINE_REPO" ]] && [[ "$ALPINE_REPO" != "auto" ]]; then
    local alpine_repo_domain=$(echo "$ALPINE_REPO" | sed -E 's#https?://([^/]+).*#\1#')
    ebegin "Awaiting accessible Alpine repo at $alpine_repo_domain"
    while ! ping -c 1 -w 1 -q "$alpine_repo_domain" > /dev/null 2>&1; do
        sleep 1
    done
    eend $?
fi
