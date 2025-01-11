argocd app create guestbook \
      --repo git@github.com:felipecadar/TP2-CIDC.git \
      --path guestbook \
      --project $USER-project \
      --dest-namespace $USER \
      --dest-server https://kubernetes.default.svc \
      --sync-policy auto
